### 1. The lock-staleness test compares dependency names only, so a GraphScene specifier change that was never re-locked passes 13j

**File:** `devscene-runtime/tests/test_graphscene_dependency.py` (`test_the_lock_resolves_graphscene_from_the_path_with_its_declared_dependencies`) — "locked = {_dependency_name(item[\"name\"])"

**Problem.** The test exists so that `devscene-runtime/uv.lock` cannot go stale against `graphscene/pyproject.toml` → `[project] dependencies` without someone noticing. Story decision 4 states it that way: 13j "fails on the first GraphScene dependency change that did not re-lock this package". Two documents this branch adds promise the same thing:

- `devscene-runtime/README.md` → `## The lock follows GraphScene`: "A change to `graphscene/pyproject.toml` → `[project] dependencies` re-locks this package too … `tests/test_graphscene_dependency.py` fails until it is done."
- `docs/development.md` → **Gate 13**, closing paragraph: "a change to `graphscene/pyproject.toml` → `[project] dependencies` re-locks `devscene-runtime` too … `13j` fails until it is done."

The test only compares the *set of names*. The lock's `graphscene` entry records each requirement's specifier as well (`devscene-runtime/uv.lock` → `[package.metadata]` under `name = "graphscene"`: `requires-dist = [{ name = "jsonschema", specifier = ">=4.26" }]`), but the test throws it away. Suppose a contributor raises GraphScene's floor from `jsonschema>=4.26` to `jsonschema>=5` and does not re-lock `devscene-runtime`. The name set is still `{"jsonschema"}` on both sides, so the test passes. The lock keeps `specifier = ">=4.26"` and its old pinned `jsonschema`. `provision`'s `uv sync --frozen` does not check whether the lock is fresh, so it installs that stale set into `devscene-runtime/.venv`. The module docstring lists "Dependency versions and specifiers" as deliberately not covered, but a specifier is exactly what `[project] dependencies` carries, and the lock already holds it to compare against.

Confirmed by reading only: no probe was run. `devscene-runtime/.venv` would have to be provisioned to run the suite, and this review runs no suite.

**Fix.** Compare each requirement's specifier set as well as its name, and narrow the docstring's non-coverage to the resolved versions.

1. Under the existing `_REQUIREMENT_NAME` / `_dependency_name`, add the code below. If Finding 2 has already landed, add it under `from requirement_names import dependency_name` instead, and write `dependency_name` wherever the snippets in steps 1 and 2 write `_dependency_name`.

```python
_REQUIREMENT = re.compile(r"([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*([^;]*)")


def _specifier_set(text: str) -> frozenset[str]:
    return frozenset(part.replace(" ", "") for part in text.split(",") if part.strip())


def _declared_requirement(requirement: str) -> tuple[str, frozenset[str]]:
    match = _REQUIREMENT.match(requirement.strip())
    if match is None:
        raise ValueError(f"unparseable dependency: {requirement!r}")
    return _dependency_name(match.group(1)), _specifier_set(match.group(2))
```

2. In `test_the_lock_resolves_graphscene_from_the_path_with_its_declared_dependencies`, replace the two set comprehensions (`locked = …` and `declared = …`) with:

```python
    locked = {
        (_dependency_name(item["name"]), _specifier_set(item.get("specifier", "")))
        for item in entry["metadata"]["requires-dist"]
    }
    project = tomllib.loads(_GRAPHSCENE_PYPROJECT.read_text(encoding="utf-8"))["project"]
    declared = {_declared_requirement(item) for item in project.get("dependencies", [])}
```

   Keep the final `assert locked == declared, …` line and its re-lock message unchanged. Today both sides give `{("jsonschema", frozenset({">=4.26"}))}`.

3. In the module docstring:
   - Change the rule sentence's "with exactly the runtime dependencies `graphscene/pyproject.toml` declares" to "with exactly the runtime dependencies, and their version specifiers, `graphscene/pyproject.toml` declares".
   - Replace the bullet "Dependency versions and specifiers: the lock pins them, and only a re-lock moves them." with two bullets: "Resolved dependency versions: the lock pins them, and only a re-lock moves them." and "Extras and environment markers on GraphScene's requirements."

The README and `docs/development.md` sentences then hold as written and need no edit. `devscene-runtime/tests/test_graphscene_dependency.py` is the one test file this fix edits, so it is the only test the fix runs, through `bash scripts/python-service.sh --package devscene-runtime test tests/test_graphscene_dependency.py`.
