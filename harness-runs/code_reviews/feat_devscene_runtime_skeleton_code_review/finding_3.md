### 3. The boundary test never exercises its allowed-set derivation against a planted manifest

**File:** `devscene-runtime/tests/test_boundary.py` (`allowed_names`, `_declared_dependencies`) — "def allowed_names(pyproject: Path) -> frozenset[str]:"

**Problem.** The real-tree case, `test_the_real_package_stays_inside_its_boundary`, gets its allowed set from `allowed_names(_PYPROJECT)`, which lower-cases each declared requirement, turns `-` into `_` and drops the specifier and extras. The only manifest that function is ever run on is the real one, whose one dependency is the bare name `graphscene`. So none of that normalisation is ever exercised. The counterpart this file mirrors does test it, against a planted manifest: `graphscene/tests/test_boundary.py` → `test_dependency_names_are_parsed_and_a_devscene_one_is_flagged` writes `dependencies = ["devscene-walker>=0.1", "PyYAML[extra]>=6"]` and asserts the parsed names and `allowed_names`. When this package gains its second dependency (#418), a parsing regression would show up as a false boundary violation, or as a dependency silently left out of the allowed set, and no case would point at the parser.

**Fix.** Add one planted case after `test_graphscene_is_a_declared_dependency`:

```python
def test_declared_dependencies_are_parsed_into_import_names(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "planted"\n'
        'dependencies = ["graphscene", "Some-Package[extra]>=6"]\n',
        encoding="utf-8",
    )
    assert _declared_dependencies(pyproject) == ["graphscene", "some_package"]
    assert {"graphscene", "some_package"} <= allowed_names(pyproject)
```

The expected values are written by hand from the planted manifest. `devscene-runtime/tests/test_boundary.py` is the one test file this fix edits, so it is the only test the fix runs, through `bash scripts/python-service.sh --package devscene-runtime test tests/test_boundary.py`.
