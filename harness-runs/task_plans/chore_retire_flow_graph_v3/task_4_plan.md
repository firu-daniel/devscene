### Task 4 — Stop GraphScene's static checker and its suite citing the retired bash checker

**Goal:** `graphscene/` stops citing `scripts/check-flow-graph.sh`, which Task 7 deletes. The static checker's ids keep their names and are stated on their own. Its suite's *"Deliberately not covered"* list stops scheduling a comparison with a checker that no longer exists.

**Where this layer stops.** This is docstring text only: no check, id, reason text or test case changes. The checks that read harness documents, ids 4–7, are the harness's, not GraphScene's. **Task 6** ports them into `devscene-flow-host/tests/core_agreement.py`. Nothing under `graphscene/` names that file or any other harness path: `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` requires the library to stay harness-free. Name no `devscene`-prefixed module or path in either file.

### Targets

- `graphscene/src/graphscene/engine/static_check.py` — the module docstring's *"The rule:"* paragraph.
- `graphscene/tests/engine/test_static_check.py` — the module docstring's *"Deliberately not covered:"* list.

**Work:**

- [ ] `static_check.py`: in *"… 8 (`gate-in-round`) and 9 (`round-fan-out`), the ids `scripts/check-flow-graph.sh` gives them."*, drop the clause *"the ids `scripts/check-flow-graph.sh` gives them"*. The check numbers and their ids stay as written, and so does every other sentence of the docstring.
- [ ] `test_static_check.py`: in *"Deliberately not covered:"*, the bullet *"Checks 4–7 of `scripts/check-flow-graph.sh`: they read plugin documents and are not ported."* becomes a bullet saying that checks 4–7 read a host's own documents and belong to the host, not to this package. Remove the bullet *"Agreement with the bash checker on the harness's own graph: it needs the harness side, and belongs to the cutover."*. The bash checker is retired on this branch, and there is nothing left to compare. Every test case stays as it is.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_static_check.py` passes, unchanged in what it asserts. It is the one test file this task edits.
- `git grep -n -e 'check-flow-graph' -e 'bash checker' -- graphscene` prints nothing.
- `git grep -n -i devscene -- graphscene/src/graphscene/engine/static_check.py` prints nothing: the docstring names no harness module or path.
