"""The rule this file exists to enforce: the package is three layers, `devscene_flow_host.commands`
over `devscene_flow_host.host` over `devscene_flow_host.records`, and an import only ever points
downward. `graphscene` is kept out of `records`: only `host` and `commands` import it.

The rule is two `import-linter` contracts in `devscene-flow-host/pyproject.toml`. Every case here
runs those committed contracts, against the real package and against planted packages that break
one clause each. The expected report lines were read from `import-linter` 2.17.

Deliberately not covered:
- An import whose module name is computed at run time, or passed to `importlib.import_module`,
  is invisible to `import-linter`. A reviewer checks those by reading.
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

# Each layer module imports only what its layer may; `graphscene` stays out of `records`.
_CLEAN_PLANT: dict[str, str] = {
    "__init__.py": "",
    "records/__init__.py": "",
    "records/core.py": "import json\n",
    "host/__init__.py": "",
    "host/glue.py": "import graphscene\nimport devscene_flow_host.records.core\n",
    "commands/__init__.py": "",
    "commands/cli.py": (
        "import devscene_flow_host.host.glue\nimport devscene_flow_host.records.core\n"
    ),
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
    package = root / "devscene_flow_host"
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
        "records/core.py",
        "import devscene_flow_host.host.glue",
        "devscene_flow_host.records is not allowed to import devscene_flow_host.host:\n\n"
        "- devscene_flow_host.records.core -> devscene_flow_host.host.glue (l.2)\n",
    ),
    (
        "records/core.py",
        "import devscene_flow_host.commands.cli",
        "devscene_flow_host.records is not allowed to import devscene_flow_host.commands:\n\n"
        "- devscene_flow_host.records.core -> devscene_flow_host.commands.cli (l.2)\n",
    ),
    (
        "host/glue.py",
        "import devscene_flow_host.commands.cli",
        "devscene_flow_host.host is not allowed to import devscene_flow_host.commands:\n\n"
        "- devscene_flow_host.host.glue -> devscene_flow_host.commands.cli (l.3)\n",
    ),
    (
        "records/core.py",
        "import graphscene",
        "devscene_flow_host.records is not allowed to import graphscene:\n\n"
        "-   devscene_flow_host.records.core -> graphscene (l.2)\n",
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


def test_graphscene_in_host_and_commands_is_allowed(tmp_path: Path) -> None:
    root = _plant(tmp_path, {"commands/cli.py": "import graphscene"})
    result = _lint(root, root)
    assert result.returncode == 0, result.stdout + result.stderr
