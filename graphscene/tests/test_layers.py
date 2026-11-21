"""The rule this file exists to enforce: the package is four layers, `graphscene.facade` over
`graphscene.adapters` and `graphscene.engine` over `graphscene.model`, and an import only ever
points downward. `adapters` and `engine` are independent siblings: neither imports the other.
`jsonschema` is confined to `adapters`: neither `model` nor `engine` imports it.

The rule is two `import-linter` contracts in `graphscene/pyproject.toml`, so it travels with the
library. Every case here runs those committed contracts, against the real package and against
planted packages that break one clause each. The expected report lines were read from
`import-linter` 2.17.

Deliberately not covered:
- An import whose module name is computed at run time, or passed to `importlib.import_module`,
  is invisible to `import-linter`, as `tests/test_boundary.py`'s docstring lists for its own scan.
  A reviewer checks those by reading.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

_PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"

_PROGRAM = (
    "import sys\n"
    "from importlinter.cli import lint_imports\n"
    "sys.exit(lint_imports(config_filename=sys.argv[1], no_cache=True, no_logo=True))\n"
)

# Each layer module imports only what its layer may; `adapters` is where `jsonschema` belongs.
_CLEAN_PLANT: dict[str, str] = {
    "__init__.py": "import graphscene.facade\n",
    "facade/__init__.py": "",
    "facade/api.py": (
        "import graphscene.adapters.io\n"
        "import graphscene.engine.rules\n"
        "import graphscene.model.core\n"
    ),
    "adapters/__init__.py": "",
    "adapters/io.py": "import jsonschema\nimport graphscene.model.core\n",
    "engine/__init__.py": "",
    "engine/rules.py": "import graphscene.model.core\n",
    "model/__init__.py": "",
    "model/core.py": "import json\n",
}


def _lint(cwd: Path, pythonpath: Path | None) -> subprocess.CompletedProcess[str]:
    env = None
    if pythonpath is not None:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(pythonpath)
    return subprocess.run(
        [sys.executable, "-c", _PROGRAM, str(_PYPROJECT)],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def _plant(root: Path, extra: dict[str, str]) -> Path:
    package = root / "graphscene"
    for relative, source in _CLEAN_PLANT.items():
        path = package / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    for relative, line in extra.items():
        path = package / relative
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        path.write_text(existing + line + "\n", encoding="utf-8")
    return root


def test_the_real_package_keeps_every_layer_contract(tmp_path: Path) -> None:
    result = _lint(tmp_path, None)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (tmp_path / ".import_linter_cache").exists()


def test_a_clean_planted_package_keeps_every_contract(tmp_path: Path) -> None:
    root = _plant(tmp_path, {})
    result = _lint(root, root)
    assert result.returncode == 0, result.stdout + result.stderr


# (planted module, added import, the report's header and chain lines naming importer and
# imported), hand-read from a first run of each case under import-linter 2.17.
_VIOLATIONS: list[tuple[str, str, str]] = [
    (
        "model/core.py",
        "import graphscene.engine.rules",
        "graphscene.model is not allowed to import graphscene.engine:\n\n"
        "- graphscene.model.core -> graphscene.engine.rules (l.2)\n",
    ),
    (
        "model/core.py",
        "import graphscene.adapters.io",
        "graphscene.model is not allowed to import graphscene.adapters:\n\n"
        "- graphscene.model.core -> graphscene.adapters.io (l.2)\n",
    ),
    (
        "engine/rules.py",
        "import graphscene.adapters.io",
        "graphscene.engine is not allowed to import graphscene.adapters:\n\n"
        "- graphscene.engine.rules -> graphscene.adapters.io (l.2)\n",
    ),
    (
        "adapters/io.py",
        "import graphscene.engine.rules",
        "graphscene.adapters is not allowed to import graphscene.engine:\n\n"
        "- graphscene.adapters.io -> graphscene.engine.rules (l.3)\n",
    ),
    (
        "engine/rules.py",
        "import graphscene.facade.api",
        "graphscene.engine is not allowed to import graphscene.facade:\n\n"
        "- graphscene.engine.rules -> graphscene.facade.api (l.2)\n",
    ),
    (
        "engine/rules.py",
        "import graphscene",
        "graphscene.engine is not allowed to import graphscene.facade:\n\n"
        "- graphscene.engine.rules -> graphscene (l.2)\n"
        "  graphscene -> graphscene.facade (l.1)\n",
    ),
    (
        "model/core.py",
        "import jsonschema",
        "graphscene.model is not allowed to import jsonschema:\n\n"
        "-   graphscene.model.core -> jsonschema (l.2)\n",
    ),
    (
        "engine/rules.py",
        "import jsonschema",
        "graphscene.engine is not allowed to import jsonschema:\n\n"
        "-   graphscene.engine.rules -> jsonschema (l.2)\n",
    ),
]


@pytest.mark.parametrize(("module", "line", "expected"), _VIOLATIONS)
def test_a_planted_violation_breaks_its_contract(
    tmp_path: Path, module: str, line: str, expected: str
) -> None:
    root = _plant(tmp_path, {module: line})
    result = _lint(root, root)
    output = result.stdout + result.stderr
    assert result.returncode != 0, (module, line, output)
    assert expected in output, (module, line, output)
    assert "does not exist" not in output, (module, line, output)
    assert "include_external_packages" not in output, (module, line, output)


def test_jsonschema_in_adapters_is_allowed(tmp_path: Path) -> None:
    root = _plant(tmp_path, {"adapters/check.py": "import jsonschema"})
    result = _lint(root, root)
    assert result.returncode == 0, result.stdout + result.stderr
