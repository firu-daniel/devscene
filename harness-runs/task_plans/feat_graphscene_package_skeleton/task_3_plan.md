### Task 3 — Add gate 13's GraphScene legs 13e–13g to `scripts/run-gates.sh` and retitle gate 13 as the Python packages

**Goal:** Wire the GraphScene library into the gates. Every Run gates round then lints, type-checks and tests it, grading each leg exactly as gate 13 already grades the docs-retrieval service's legs.

**Depends on:** Task 2, which makes `graphscene` a row of `scripts/python-service.sh`'s table. These are the calls this task makes, and the exit contract it relies on (unchanged by Task 2):
- `bash scripts/python-service.sh --package graphscene lint`
- `bash scripts/python-service.sh --package graphscene typecheck`
- `bash scripts/python-service.sh --package graphscene test`

The exit contract: `0` pass, `1` the tool failed, `2` usage, `3` not provisioned (`uv` missing or no `graphscene/.venv/pyvenv.cfg`). Task 1's package holds the files these legs grade, among them `tests/test_boundary.py`, which 13g runs.

**Where this task stops.** Task 5 owns `docs/development.md`'s account of these legs. This task changes the script and its own comments only.

### Targets

- `scripts/run-gates.sh`

**Work:**

- [ ] **Three new `run_unit` arms**, after `13d`, each calling the existing `python_gate` with `noskip`:
  - `13e)` → `python_gate "13e GraphScene lint" noskip bash scripts/python-service.sh --package graphscene lint`
  - `13f)` → `python_gate "13f GraphScene typecheck" noskip bash scripts/python-service.sh --package graphscene typecheck`
  - `13g)` → `python_gate "13g GraphScene tests" noskip bash scripts/python-service.sh --package graphscene test`

  `python_gate` already maps `3` to `BLOCKED`, adding the leg to `python_blocked`, and everything else non-zero to `FAIL`. Add no grading code.
- [ ] **The round and its prerequisites.** Append `13e 13f 13g` after `13d` in the `gr_run_round run_unit …` id list. Leave `GR_PREREQUISITES` unchanged: unlike 13c, none of the three runs `cli/dist`, so none depends on `2a`.
- [ ] **The title.** Every `gate_header 13 "Python docs-retrieval service"` call, in 13a–13d and in the three new arms, becomes `gate_header 13 "Python packages"`. In the closing `== gates this script cannot run` block, the `BLOCKED` line *"13 the Python docs-retrieval service, reported BLOCKED above"* becomes *"13 the Python packages, reported BLOCKED above"*, with its two continuation lines unchanged. The `13d` `SKIPPED` line stays as it is: 13d is still the only container leg.
- [ ] **The header comment.** In the paragraph that names the conditional gates, change *"Gate 13 (the Python docs-retrieval service) reports a leg BLOCKED where `uv` or its synced environment is missing"* so that it names both packages: the docs-retrieval service's legs 13a–13d and the GraphScene library's legs 13e–13g. Leave the count of gates the script runs as it is. No gate is added.

**Verification:**

- `grep -n 'Python docs-retrieval service' scripts/run-gates.sh` returns no hit.
- `grep -n '13e\|13f\|13g' scripts/run-gates.sh` shows each id in its arm, in the `gr_run_round` list, and in the header comment, and in no `GR_PREREQUISITES` value.
- The three new arms call `python_gate` with `noskip`, so an exit `4` from any of them grades `FAIL`. The wrapper never returns `4` for these sub-commands.
- Every added line uses only constructs the file already uses, so gate 16's `/bin/bash -n` parse still holds. Gate 16 grades it in the Run gates round.
