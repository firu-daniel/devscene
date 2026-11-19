### 3. The boundary test's dependency rule and its PEP 508 name parsing have no planted case

**File:** `graphscene/tests/test_boundary.py` (`test_no_declared_dependency_is_devscene_prefixed`, `_dependency_name`): "for name in _declared_dependencies(_PYPROJECT)"

The story index's decision 3 lists four things the boundary test flags. The fourth is "any declared dependency in `graphscene/pyproject.toml` whose name starts with `devscene`". It then says "Planted violations prove that each rule fires." Rules (a)–(d) on imports and literals each have a planted module. The dependency rule has none: `test_no_declared_dependency_is_devscene_prefixed` runs only against the real `pyproject.toml`, whose `dependencies` is `[]`.

So the check, and the `_dependency_name` / `allowed_names` path that rule (a)'s allowed set depends on, have only ever run over an empty list. That is the vacuous pass the story's third top risk names. A wrong parse goes unnoticed until the first real dependency lands. For example, if `_dependency_name` kept a version specifier or an extra, the `devscene` prefix test would still pass on the mangled name, but rule (a) would refuse the dependency's own import.

**Fix:** in `graphscene/tests/test_boundary.py`, pull the prefix check into a function and test it against a planted `pyproject.toml`. Keep the real-tree case.

```python
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
```

Keep every line within the package's 100-column `ruff` limit. This file is the one the fix edits. Its own run is gate 13's leg 13g in the Run gates phase, because no unit runs the Python toolchain outside `scripts/python-service.sh`, and the fix runs no other test.
