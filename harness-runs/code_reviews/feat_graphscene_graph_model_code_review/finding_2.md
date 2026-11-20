### 2. Two new test files fail the package's `ruff` lint: an unsorted import in `test_model.py` and two unformatted assertions in `test_loader.py`

**File:** `graphscene/tests/test_model.py` (the `from graphscene.model import (` block) — "    RouteEdge,\n    RoundNode,"; and `graphscene/tests/test_loader.py` (`test_a_missing_required_field_names_the_node`, `test_a_schema_failure_never_reaches_the_vocabulary_stage`) — "assert raised.value.violations == (\n        Violation(\"nodes.draft\", \"'agent' is a required property\"),\n    )"
**Class:** Wrong behaviour
**Failure:** If gate 13's lint leg runs `bash scripts/python-service.sh --package graphscene lint` on this branch, then it exits 1, reporting `I001 [*] Import block is un-sorted or un-formatted --> tests/test_model.py:12:1` and `1 file would be reformatted` for `tests/test_loader.py`.

The reviewer ran the package lint on this branch and it exited 1. `graphscene/pyproject.toml` selects `I` (isort) under `[tool.ruff.lint]`, and the lint command also checks formatting. Both files are new on this branch.

1. **`tests/test_model.py`.** The import list from `graphscene.model` has `RouteEdge` before `RoundNode`. Isort's case-sensitive ordering puts `RoundNode` first, because `o` sorts before `u`.
2. **`tests/test_loader.py`.** Two assertions spread a one-element tuple over three lines that fits on one line of 99 characters. Ruff's formatter collapses it.

**Fix:**

1. In `graphscene/tests/test_model.py`, swap the two lines in the `from graphscene.model import (` block, so the block reads:

   ```python
   from graphscene.model import (
       BindingEdge,
       DispatchNode,
       FlowGraph,
       InterruptBinding,
       OnCapEdge,
       OutcomeDeclaration,
       PredicateDeclaration,
       RoundNode,
       RouteEdge,
       SkipEntry,
       StopBinding,
       TerminalNode,
       build_flow_graph,
   )
   ```

2. In `graphscene/tests/test_loader.py`, there are two occurrences of this three-line assertion, one in `test_a_missing_required_field_names_the_node` and one in `test_a_schema_failure_never_reaches_the_vocabulary_stage`:

   ```python
       assert raised.value.violations == (
           Violation("nodes.draft", "'agent' is a required property"),
       )
   ```

   Replace each with the one-line form:

   ```python
       assert raised.value.violations == (Violation("nodes.draft", "'agent' is a required property"),)
   ```

   Leave the two-element tuple in `test_schema_violations_come_back_sorted_by_path` as it is. It does not fit on one line, and the formatter keeps it multi-line.

Both files are ones this fix edits, so they are the only test files the fix runs, through `bash scripts/python-service.sh --package graphscene test tests/test_model.py` and `bash scripts/python-service.sh --package graphscene test tests/test_loader.py`.
