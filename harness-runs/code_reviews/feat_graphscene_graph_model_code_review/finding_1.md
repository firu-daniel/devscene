### 1. `_strings` in `vocabulary.py` was re-annotated `list[Violation]`, so the package's strict `mypy` fails

**File:** `graphscene/src/graphscene/vocabulary.py` (`_strings`) — "def _strings(value: object) -> list[Violation]:"
**Class:** Wrong behaviour
**Failure:** If gate 13's leg `13f` runs `bash scripts/python-service.sh --package graphscene typecheck` on this branch, then it exits 1 with `src/graphscene/vocabulary.py:37: error: List comprehension has incompatible type List[str]; expected List[Violation]  [misc]` and `src/graphscene/vocabulary.py:52: error: Argument 2 to "_Binding" has incompatible type "list[Violation]"; expected "list[str]"  [arg-type]`.

Task 1 changed every `list[str]` return in `vocabulary.py` to `list[Violation]`, and one of them was the wrong function. `_strings` does not return violations. It filters a binding's declared `reasons` array down to its string members, and its result goes to `_Binding(..., reasons: list[str])` in `_bindings`. Its body still builds `[item for item in value if isinstance(item, str)]`, a `list[str]`. Nothing breaks at run time, which is why all 102 `pytest` cases pass. But `graphscene/pyproject.toml` sets `[tool.mypy] strict = true` over `src` and `tests`, and the package's typecheck reports the two errors quoted above. The reviewer ran it on this branch and it exited 1.

**Fix:** put back the annotation `_strings` had before this branch. Change only the signature line:

```python
def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
```

Do not touch any other function in the file. Every other `list[Violation]` annotation the branch introduced is correct.
