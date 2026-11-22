"""The rule this file exists to enforce: the package at `src/devscene_runtime/` imports only the
standard library, itself and its declared runtime dependencies; it reaches `graphscene` through
its public surface only (`import graphscene`, `from graphscene import <name>` with the name in
`graphscene.__all__`, never a submodule such as `graphscene.engine`); and GraphScene never
imports it, which `graphscene/tests/test_boundary.py` enforces from the other side.

`scan` parses every module under `src/devscene_runtime/` with `ast` and, for every `import`,
absolute `from ... import` and call to `importlib.import_module`, `import_module` or `__import__`
with an absolute string-constant module name (a relative one, with a leading `.` or a non-zero
constant `level`, is skipped), flags (a) a top-level name outside the allowed set; (b) a
`graphscene` module path deeper than the root; (c) `from graphscene import <name>` with the name
outside the public set (a `*` is not flagged).

Deliberately not covered:
- An import whose module name is computed at run time cannot be checked statically.
- A constant-name dynamic import the scanner does not recognise as one: an importer bound to
  another name (`from importlib import import_module as load`), a module name passed by keyword
  (`import_module(name=...)`), or `__import__` reached through a module (`builtins.__import__`).
- An attribute reached through the root (`graphscene.engine` after `import graphscene`).
- `tests/` is not scanned.
"""

import ast
import re
import sys
import tomllib
from pathlib import Path

import graphscene

_ROOT = Path(__file__).resolve().parents[1]
_PACKAGE_DIR = _ROOT / "src" / "devscene_runtime"
_PYPROJECT = _ROOT / "pyproject.toml"

_GRAPHSCENE = "graphscene"

_REQUIREMENT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")

# A dependency whose import name differs from its normalised PEP 508 name is added here when it
# arrives, keyed by that normalised name.
_IMPORT_NAMES: dict[str, str] = {}

_STDLIB_AND_SELF = frozenset(sys.stdlib_module_names) | {"devscene_runtime"}

_PLANTED_ALLOWED = _STDLIB_AND_SELF | {_GRAPHSCENE}
_PLANTED_PUBLIC = frozenset({"Walker"})


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
        if first.value.startswith(".") or _relative_level(call):
            return None
        return first.value
    return None


def _relative_level(call: ast.Call) -> bool:
    level: ast.expr | None = call.args[4] if len(call.args) > 4 else None
    for keyword in call.keywords:
        if keyword.arg == "level":
            level = keyword.value
    return isinstance(level, ast.Constant) and isinstance(level.value, int) and level.value != 0


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


def _names_from_root(node: ast.AST) -> list[tuple[int, str]]:
    if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module == _GRAPHSCENE:
        return [(node.lineno, alias.name) for alias in node.names if alias.name != "*"]
    return []


def scan(
    package_dir: Path, allowed: frozenset[str], public: frozenset[str]
) -> tuple[list[Path], list[str]]:
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
                if top == _GRAPHSCENE and module != _GRAPHSCENE:
                    violations.append(
                        f"{where}:{line}: imports {module}, below graphscene's public surface"
                    )
            for line, name in _names_from_root(node):
                if name not in public:
                    violations.append(
                        f"{where}:{line}: imports graphscene.{name}, not in graphscene.__all__"
                    )
    return visited, violations


def _plant(directory: Path, source: str) -> Path:
    directory.mkdir()
    (directory / "__init__.py").write_text(source, encoding="utf-8")
    return directory


def test_a_clean_module_produces_no_violation(tmp_path: Path) -> None:
    source = (
        "import json\n"
        "from . import sibling\n"
        "import graphscene\n"
        "from graphscene import Walker\n"
        "from graphscene import *\n"
    )
    package = _plant(tmp_path / "clean", source)
    visited, violations = scan(package, _PLANTED_ALLOWED, _PLANTED_PUBLIC)
    assert visited == [package / "__init__.py"]
    assert violations == []


def test_rule_a_flags_a_static_import_outside_the_allowed_set(tmp_path: Path) -> None:
    package = _plant(tmp_path / "rule_a", "import json\nfrom yaml import safe_load\n")
    _, violations = scan(package, _PLANTED_ALLOWED, _PLANTED_PUBLIC)
    assert violations == ["__init__.py:2: imports yaml, outside the allowed set"]


def test_rule_a_flags_a_constant_dynamic_import_outside_the_allowed_set(tmp_path: Path) -> None:
    sources = {
        "attribute": 'import importlib\n\nimportlib.import_module("yaml")\n',
        "bare": 'from importlib import import_module\n\nimport_module("yaml")\n',
        "dunder": '__import__("yaml")\n',
    }
    for name, source in sources.items():
        package = _plant(tmp_path / name, source)
        _, violations = scan(package, _PLANTED_ALLOWED, _PLANTED_PUBLIC)
        line = source.count("\n")
        assert violations == [f"__init__.py:{line}: imports yaml, outside the allowed set"], name


def test_a_relative_dynamic_import_is_not_flagged(tmp_path: Path) -> None:
    sources = {
        "dotted": 'import importlib\n\nimportlib.import_module(".engine", __package__)\n',
        "positional_level": '__import__("engine", globals(), None, [], 1)\n',
        "keyword_level": '__import__("engine", globals(), level=1)\n',
    }
    for name, source in sources.items():
        package = _plant(tmp_path / name, source)
        _, violations = scan(package, _PLANTED_ALLOWED, _PLANTED_PUBLIC)
        assert violations == [], name


def test_rule_b_flags_a_graphscene_submodule(tmp_path: Path) -> None:
    cases = {
        "static": (
            "import graphscene.engine\n",
            "__init__.py:1: imports graphscene.engine, below graphscene's public surface",
        ),
        "from_submodule": (
            "from graphscene.engine.walker import Walker\n",
            "__init__.py:1: imports graphscene.engine.walker, below graphscene's public surface",
        ),
        "dynamic": (
            'from importlib import import_module\n\nimport_module("graphscene.engine")\n',
            "__init__.py:3: imports graphscene.engine, below graphscene's public surface",
        ),
    }
    for name, (source, expected) in cases.items():
        package = _plant(tmp_path / name, source)
        _, violations = scan(package, _PLANTED_ALLOWED, _PLANTED_PUBLIC)
        assert violations == [expected], name


def test_rule_c_flags_a_name_outside_the_public_surface(tmp_path: Path) -> None:
    package = _plant(tmp_path / "rule_c", "from graphscene import Walker, engine\n")
    _, violations = scan(package, _PLANTED_ALLOWED, _PLANTED_PUBLIC)
    assert violations == ["__init__.py:1: imports graphscene.engine, not in graphscene.__all__"]


def test_the_real_package_stays_inside_its_boundary() -> None:
    public = frozenset(graphscene.__all__)
    visited, violations = scan(_PACKAGE_DIR, allowed_names(_PYPROJECT), public)
    assert _PACKAGE_DIR / "__init__.py" in visited, visited
    assert violations == [], "\n".join(violations)


def test_graphscene_is_a_declared_dependency() -> None:
    declared = _declared_dependencies(_PYPROJECT)
    assert _GRAPHSCENE in declared, declared
    assert _GRAPHSCENE in allowed_names(_PYPROJECT)
