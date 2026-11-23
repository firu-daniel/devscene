"""The rule this file exists to enforce: this package's environment imports the checkout's own
GraphScene, the editable `graphscene/` sibling of this very checkout, and `uv.lock` resolves
GraphScene from the declared `../graphscene` path with exactly the runtime dependencies, and their
version specifiers, `graphscene/pyproject.toml` declares.

Deliberately not covered:
- Resolved dependency versions: the lock pins them, and only a re-lock moves them.
- Extras and environment markers on GraphScene's requirements.
- GraphScene's `dev` group: it never reaches this package's environment.
"""

import re
import tomllib
from pathlib import Path

import graphscene

from requirement_names import dependency_name

_REQUIREMENT = re.compile(r"([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*([^;]*)")


def _specifier_set(text: str) -> frozenset[str]:
    return frozenset(part.replace(" ", "") for part in text.split(",") if part.strip())


def _declared_requirement(requirement: str) -> tuple[str, frozenset[str]]:
    match = _REQUIREMENT.match(requirement.strip())
    if match is None:
        raise ValueError(f"unparseable dependency: {requirement!r}")
    return dependency_name(match.group(1)), _specifier_set(match.group(2))


_ROOT = Path(__file__).resolve().parents[1]
_CHECKOUT = Path(__file__).resolve().parents[2]
_PYPROJECT = _ROOT / "pyproject.toml"
_LOCK = _ROOT / "uv.lock"
_GRAPHSCENE_PYPROJECT = _CHECKOUT / "graphscene" / "pyproject.toml"

_RELOCK = "bash scripts/python-service.sh --package devscene-flow-host lock"


def test_graphscene_imports_from_this_checkouts_sibling() -> None:
    expected = _CHECKOUT / "graphscene" / "src" / "graphscene" / "__init__.py"
    assert Path(graphscene.__file__).resolve() == expected


def test_the_manifest_sources_graphscene_from_the_editable_sibling() -> None:
    sources = tomllib.loads(_PYPROJECT.read_text(encoding="utf-8"))["tool"]["uv"]["sources"]
    assert sources["graphscene"] == {"path": "../graphscene", "editable": True}


def test_the_lock_resolves_graphscene_from_the_path_with_its_declared_dependencies() -> None:
    lock = tomllib.loads(_LOCK.read_text(encoding="utf-8"))
    entries = [entry for entry in lock["package"] if entry["name"] == "graphscene"]
    assert len(entries) == 1, f"uv.lock has no single graphscene entry; re-lock: {_RELOCK}"
    entry = entries[0]
    assert entry["source"] == {"editable": "../graphscene"}, f"re-lock: {_RELOCK}"
    locked = {
        (dependency_name(item["name"]), _specifier_set(item.get("specifier", "")))
        for item in entry["metadata"]["requires-dist"]
    }
    project = tomllib.loads(_GRAPHSCENE_PYPROJECT.read_text(encoding="utf-8"))["project"]
    declared = {_declared_requirement(item) for item in project.get("dependencies", [])}
    assert locked == declared, f"uv.lock is stale against graphscene's manifest; re-lock: {_RELOCK}"
