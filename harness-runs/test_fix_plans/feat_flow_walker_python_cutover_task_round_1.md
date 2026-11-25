# Test Fix Plan: feat_flow_walker_python_cutover — task round 1

## Context

**Branch:** `feat_flow_walker_python_cutover`
**Test log:** `harness-runs/test_run_logs/feat_flow_walker_python_cutover/task_round_1.log`
**Summary:** The typecheck gate passed; the test gate failed on two of its sub-gates — gate 4 (`npm test`: two `create-worktree.test.mjs` cases whose fixture has no flow host and no `uv` stub, now that this branch's Task 3 made `setup-worktree.sh` step 6 fail on a missing project, and one `doctor.test.mjs` case whose hand-built `PATH` has no `uv`, now that this branch's Task 5 grades a missing `uv` as a failure) and gate 6a (a committed architecture review quoting an absolute plugin path under the home directory).

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the fix loop.** The loop walks the `[ ]` entries below top-to-bottom; the commit step flips each one to `[x]` as that fix's commit lands. `[ ]` markers anywhere else (sub-step bullets inside the per-finding files) are informational only — never the iteration source.

Each entry resolves to a self-contained `finding_<K>.md` in `feat_flow_walker_python_cutover_task_round_1/` via its `**Finding K**` reference. Sorted lowest blast-radius first; Finding 1 is the suspected root cause of Finding 2 and precedes it.

1. [x] **Finding 4** — Replace the absolute plugin path in the round-0 architecture review with its `${CLAUDE_PLUGIN_ROOT}` form (gate 6a). _(layer: general)_
2. [x] **Finding 3** — Give `pathWithNpxButNoNpm` in `cli/test/doctor.test.mjs` a `uv` stub so the new `uv` failure grade does not fail the `--check-registry` no-client case. _(layer: cli)_
3. [ ] **Finding 1** — Seed the `create-worktree.test.mjs` fixture with a flow-host `pyproject.toml` and run `create` with a stub `uv` first on `PATH`, so default-mode bootstrap step 6 passes. _(layer: cli)_
4. [ ] **Finding 2** — The `(E5)` honest `--existing` case fails on the same step-6 provision failure. _(layer: cli)_

---

## Must Fix

### 1. Default-mode `create-worktree.sh` case fails at bootstrap step 6: the fixture has no flow host
→ [finding_1.md](feat_flow_walker_python_cutover_task_round_1/finding_1.md)

### 2. `(E5)` `--existing` case fails at bootstrap step 6: the fixture has no flow host
→ [finding_2.md](feat_flow_walker_python_cutover_task_round_1/finding_2.md)

### 3. `--check-registry` no-client doctor case exits 1: its `PATH` has no `uv`
→ [finding_3.md](feat_flow_walker_python_cutover_task_round_1/finding_3.md)

### 4. Gate 6a: the round-0 architecture review names a machine path
→ [finding_4.md](feat_flow_walker_python_cutover_task_round_1/finding_4.md)

---

## Not fixable on this branch

None.

---

## Source failures

Earlier logs: none — this is round 1, so every failure below is classed **first round (no earlier log to classify against)**.

- **Gate `typecheck`** — exited 0; no failure.
- **Gate `test`** — exited 1 (`run-gates: 2 failed, 34 passed`):
  - **Sub-gate 4 `npm test`** (`FAIL  4 npm test (exit 1, 2660 s)`; `# fail 3`):
    - `not ok 278 - the default mode bootstraps the clone, then pushes from the main checkout and mirrors the tip` (`cli/test/create-worktree.test.mjs`) → **Finding 1** — first round.
    - `not ok 290 - (E5) an honest --existing branch is cloned at its tip and bootstrapped from the main configuration` (`cli/test/create-worktree.test.mjs`) → **Finding 2** — first round.
    - `not ok 59 - --check-registry claims no registry read when npm does not resolve on PATH` (`cli/test/doctor.test.mjs`) → **Finding 3** — first round.
    - `not ok 382 - doctor` (`cli/test/doctor.test.mjs`, suite, `'1 subtest failed'`) — the parent suite of test 59 → **Finding 3** — first round.
  - **Sub-gate 6a `no machine paths`** (`FAIL  6a no machine paths`) → **Finding 4** — first round.
  - Sub-gates `13d` and `14d` are `SKIPPED` and gates 5, 7–10, 12 and 15 are listed as not runnable by the script; none is a failure and none yields a finding.
