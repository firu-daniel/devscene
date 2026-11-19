"""The rule this file exists to enforce: the library at `src/graphscene/` reaches nothing outside
the standard library, itself and its declared runtime dependencies, never names
`devscene.config.json`, and declares no `devscene`-prefixed dependency.

`scan` parses every module under `src/graphscene/` with `ast` and flags (a) an `import` or an
absolute `from ... import` of a top-level name outside the allowed set; (b) a call to
`importlib.import_module`, `import_module` or `__import__` with a string-constant module name
outside it; (c) any top-level name from (a) or (b) starting with `devscene`, allowed or not; and
(d) any string constant containing `devscene.config.json`.

Deliberately not covered:
- `tests/` is not scanned, because this file has to carry the forbidden literal.
- An import whose module name is computed at run time cannot be checked statically.
- A constant-name dynamic import the scanner does not recognise as one: an importer bound to
  another name (`from importlib import import_module as load`), a module name passed by keyword
  (`import_module(name=...)`), or `__import__` reached through a module (`builtins.__import__`).
"""

import ast
import re
import sys
import tomllib
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_PACKAGE_DIR = _ROOT / "src" / "graphscene"
_PYPROJECT = _ROOT / "pyproject.toml"

_FORBIDDEN_PREFIX = "devscene"
_FORBIDDEN_LITERAL = "devscene.config.json"

_REQUIREMENT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")

# A dependency whose import name differs from its normalised PEP 508 name is added here when it
# arrives, keyed by that normalised name.
_IMPORT_NAMES: dict[str, str] = {}

_STDLIB_AND_SELF = frozenset(sys.stdlib_module_names) | {"graphscene"}


def _dependency_name(requirement: str) -> str:
    match = _REQUIREMENT_NAME.match(requirement.strip())
    if match is None:
        raise ValueError(f"unparseable dependency: {requirement!r}")
    return match.group(0).lower().replace("-", "_")


def _declared_dependencies(pyproject: Path) -> list[str]:
    project = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]
    return [_dependency_name(entry) for entry in project.get("dependencies", [])]


def allowed_names(pyproject: Path) -> frozenset[str]:
    declared = {_IMPORT_NAMES.get(name, name) for name in _declared_dependencies(pyproject)}
    return _STDLIB_AND_SELF | declared


def _dynamic_import_target(call: ast.Call) -> str | None:
    func = call.func
    if isinstance(func, ast.Attribute):
        is_importer = (
            func.attr == "import_module"
            and isinstance(func.value, ast.Name)
            and func.value.id == "importlib"
        )
    elif isinstance(func, ast.Name):
        is_importer = func.id in ("import_module", "__import__")
    else:
        is_importer = False
    if not is_importer or not call.args:
        return None
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value
    return None


def _imported_modules(node: ast.AST) -> list[tuple[int, str]]:
    if isinstance(node, ast.Import):
        return [(node.lineno, alias.name) for alias in node.names]
    if isinstance(node, ast.ImportFrom):
        if node.level == 0 and node.module is not None:
            return [(node.lineno, node.module)]
        return []
    if isinstance(node, ast.Call):
        target = _dynamic_import_target(node)
        if target is not None:
            return [(node.lineno, target)]
    return []


def scan(package_dir: Path, allowed: frozenset[str]) -> tuple[list[Path], list[str]]:
    """Return the `.py` files visited and one `<path>:<line>: <what>` line per violation."""
    visited: list[Path] = []
    violations: list[str] = []
    for path in sorted(package_dir.rglob("*.py")):
        visited.append(path)
        where = path.relative_to(package_dir).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            for line, module in _imported_modules(node):
                top = module.split(".")[0]
                if top not in allowed:
                    violations.append(f"{where}:{line}: imports {top}, outside the allowed set")
                if top.startswith(_FORBIDDEN_PREFIX):
                    violations.append(f"{where}:{line}: imports {top}, a devscene-prefixed module")
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and _FORBIDDEN_LITERAL in node.value
            ):
                violations.append(f"{where}:{node.lineno}: names {_FORBIDDEN_LITERAL}")
    return visited, violations


def _plant(directory: Path, source: str) -> Path:
    directory.mkdir()
    (directory / "__init__.py").write_text(source, encoding="utf-8")
    return directory


def test_a_clean_module_produces_no_violation(tmp_path: Path) -> None:
    source = "import json\nfrom . import sibling\nfrom .sibling import thing\n"
    package = _plant(tmp_path / "clean", source)
    visited, violations = scan(package, _STDLIB_AND_SELF)
    assert visited == [package / "__init__.py"]
    assert violations == []


def test_rule_a_flags_a_static_import_outside_the_allowed_set(tmp_path: Path) -> None:
    package = _plant(tmp_path / "rule_a", "import json\nfrom yaml import safe_load\n")
    _, violations = scan(package, _STDLIB_AND_SELF)
    assert violations == ["__init__.py:2: imports yaml, outside the allowed set"]


def test_rule_b_flags_a_constant_dynamic_import_outside_the_allowed_set(tmp_path: Path) -> None:
    sources = {
        "attribute": 'import importlib\n\nimportlib.import_module("yaml")\n',
        "bare": 'from importlib import import_module\n\nimport_module("yaml")\n',
        "dunder": '__import__("yaml")\n',
    }
    for name, source in sources.items():
        package = _plant(tmp_path / name, source)
        _, violations = scan(package, _STDLIB_AND_SELF)
        line = source.count("\n")
        assert violations == [f"__init__.py:{line}: imports yaml, outside the allowed set"], name


def test_rule_c_flags_a_devscene_prefixed_import_even_when_allowed(tmp_path: Path) -> None:
    package = _plant(tmp_path / "rule_c", "import devscene_walker\n")
    _, violations = scan(package, _STDLIB_AND_SELF | {"devscene_walker"})
    assert violations == ["__init__.py:1: imports devscene_walker, a devscene-prefixed module"]


def test_rule_d_flags_a_string_constant_naming_the_configuration_file(tmp_path: Path) -> None:
    package = _plant(tmp_path / "rule_d", 'CONFIG = "devscene.config.json"\n')
    _, violations = scan(package, _STDLIB_AND_SELF)
    assert violations == ["__init__.py:1: names devscene.config.json"]


def test_the_real_library_stays_inside_its_boundary() -> None:
    visited, violations = scan(_PACKAGE_DIR, allowed_names(_PYPROJECT))
    assert _PACKAGE_DIR / "__init__.py" in visited, visited
    assert violations == [], "\n".join(violations)


def prefixed_dependencies(pyproject: Path) -> list[str]:
    return [
        name for name in _declared_dependencies(pyproject) if name.startswith(_FORBIDDEN_PREFIX)
    ]


def test_dependency_names_are_parsed_and_a_devscene_one_is_flagged(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "planted"\n'
        'dependencies = ["devscene-walker>=0.1", "PyYAML[extra]>=6"]\n',
        encoding="utf-8",
    )
    assert _declared_dependencies(pyproject) == ["devscene_walker", "pyyaml"]
    assert prefixed_dependencies(pyproject) == ["devscene_walker"]
    assert {"devscene_walker", "pyyaml"} <= allowed_names(pyproject)


def test_no_declared_dependency_is_devscene_prefixed() -> None:
    prefixed = prefixed_dependencies(_PYPROJECT)
    assert prefixed == [], prefixed
