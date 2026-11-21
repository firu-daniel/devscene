### 1. `test_a_planted_violation_breaks_its_contract` runs all eight planted clauses in one test, so the first failing clause hides the rest

**File:** `graphscene/tests/test_layers.py` (`test_a_planted_violation_breaks_its_contract`) — "for index, (module, line, expected) in enumerate(_VIOLATIONS):"

The layer contracts are checked against planted packages that each break one clause: model→engine, model→adapters, engine→adapters, adapters→engine, engine→facade, engine→root→facade, and `jsonschema` in `model` and in `engine`. All eight run inside one `for` loop in one test function. The first assertion that fails ends the test, so the clauses after it are never run in that session. `pytest` then reports one failure where several clauses may be broken, and the summary cannot tell you which clauses still hold.

`.claude/context/graphscene.md` → `## Tests` states the layer's shape for a scanner-enforced rule as *"a planted case per clause, each asserting the exact violation text"*, and `graphscene/tests/test_boundary.py` follows it with one test function per clause. This test already asserts the exact text for each clause. The only change needed is to make each clause its own collected case. No behaviour is wrong today, and every clause passes or fails together as written, so this is a Nice to Have.

**Fix:** turn the loop into a parametrized test over `_VIOLATIONS`. Each case then plants into its own `tmp_path`, and the `index` subdirectory is no longer needed:

```python
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
```

Add `import pytest` to the file's imports, in `ruff`'s `I` order: a third-party block after the standard-library block. Keep `_VIOLATIONS` and its comment unchanged. This fix edits one test file, `graphscene/tests/test_layers.py`, so that is the only test file it runs: `bash scripts/python-service.sh --package graphscene test tests/test_layers.py`, from the repository root.
