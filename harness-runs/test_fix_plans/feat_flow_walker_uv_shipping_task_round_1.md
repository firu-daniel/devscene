# Test Fix Plan: feat_flow_walker_uv_shipping — task round 1

## Context

**Branch:** `feat_flow_walker_uv_shipping`
**Test log:** `harness-runs/test_run_logs/feat_flow_walker_uv_shipping/task_round_1.log`
**Summary:** The typecheck gate exited 0. The test gate exited 1 on two `run-gates` checks: gate 4 (`npm test`: 20 failing tests: one `doctor` acceptance case, one `npm pack` case refused by the sandbox, and 18 cases of the stall-reset watcher suite) and gate 6a (no machine paths in three lines of tracked run artifacts).

The SKIPPED legs (13d, 14d) and the `gates this script cannot run` list are not failures and yield no finding. No earlier-round logs were named, so every failure is classed as first round.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the fix loop.** The loop walks the `[ ]` entries below from top to bottom. `[ ]` markers anywhere else, such as the sub-step bullets inside a per-finding file, are informational only and never drive the loop.

1. [x] **Finding 1** — Rewrite the home-directory npm-cache paths in two tracked run artifacts (gate 6a). _(layer: general)_
2. [x] **Finding 2** — Add the branch's `uv` and `flow-host` check ids to the doctor test's frozen pre-branch id list. _(layer: cli)_
3. [x] **Finding 3** — Make `createStallFixture`'s `watcher-test/bin` mkdir tolerate the directory the shared watcher fixture now creates. _(layer: cli)_
4. [x] **Finding 4** — Stall-reset (S1) reference-transaction case: EEXIST on `watcher-test/bin`. _(layer: cli)_
5. [x] **Finding 5** — Stall-reset (S2) committed settings.json case: EEXIST on `watcher-test/bin`. _(layer: cli)_
6. [x] **Finding 6** — Stall-reset (S3) nested core.fsmonitor case: EEXIST on `watcher-test/bin`. _(layer: cli)_
7. [x] **Finding 7** — Stall-reset (S5) symlinked PAUSE_PROGRESS.md case: EEXIST on `watcher-test/bin`. _(layer: cli)_
8. [x] **Finding 8** — Stall-reset (S6) forged base case: EEXIST on `watcher-test/bin`. _(layer: cli)_
9. [x] **Finding 9** — Stall-reset (S7) skip-worktree settings.json case: EEXIST on `watcher-test/bin`. _(layer: cli)_
10. [x] **Finding 10** — Stall-reset (S8) replace-ref case: EEXIST on `watcher-test/bin`. _(layer: cli)_
11. [x] **Finding 11** — Stall-reset (S9) info/grafts case: EEXIST on `watcher-test/bin`. _(layer: cli)_
12. [x] **Finding 12** — Stall-reset (S4) config.worktree case: EEXIST on `watcher-test/bin`. _(layer: cli)_
13. [x] **Finding 13** — Stall-reset (S4c) .git/config core.fsmonitor case: EEXIST on `watcher-test/bin`. _(layer: cli)_
14. [x] **Finding 14** — Stall-reset (S10) planted commondir case: EEXIST on `watcher-test/bin`. _(layer: cli)_
15. [x] **Finding 15** — Stall-reset (J1) unset default-branch job case: EEXIST on `watcher-test/bin`. _(layer: cli)_
16. [x] **Finding 16** — Stall-reset (J2) failing job-surfaces case: EEXIST on `watcher-test/bin`. _(layer: cli)_
17. [x] **Finding 17** — Stall-reset (J3) honest job branch case: EEXIST on `watcher-test/bin`. _(layer: cli)_
18. [ ] **Finding 18** — Stall-reset (J4) session-written .npmrc case: EEXIST on `watcher-test/bin`. _(layer: cli)_
19. [ ] **Finding 19** — Stall-reset (J5) session-written node_modules case: EEXIST on `watcher-test/bin`. _(layer: cli)_
20. [ ] **Finding 20** — Stall-reset (J6) forged base in job checkout case: EEXIST on `watcher-test/bin`. _(layer: cli)_

---

## Must Fix

### 1. Tracked run artifacts carry home-directory npm-cache paths (gate 6a)
→ [finding_1.md](feat_flow_walker_uv_shipping_task_round_1/finding_1.md)

### 2. Doctor Acceptance 1 fails: frozen check-id list lacks `uv` and `flow-host`
→ [finding_2.md](feat_flow_walker_uv_shipping_task_round_1/finding_2.md)

### 3. Stall fixture's `mkdir(bin)` collides with the shared fixture's uv-stub directory
→ [finding_3.md](feat_flow_walker_uv_shipping_task_round_1/finding_3.md)

### 4. (S1) reference-transaction case fails on EEXIST
→ [finding_4.md](feat_flow_walker_uv_shipping_task_round_1/finding_4.md)

### 5. (S2) committed settings.json case fails on EEXIST
→ [finding_5.md](feat_flow_walker_uv_shipping_task_round_1/finding_5.md)

### 6. (S3) nested core.fsmonitor case fails on EEXIST
→ [finding_6.md](feat_flow_walker_uv_shipping_task_round_1/finding_6.md)

### 7. (S5) symlinked PAUSE_PROGRESS.md case fails on EEXIST
→ [finding_7.md](feat_flow_walker_uv_shipping_task_round_1/finding_7.md)

### 8. (S6) forged base case fails on EEXIST
→ [finding_8.md](feat_flow_walker_uv_shipping_task_round_1/finding_8.md)

### 9. (S7) skip-worktree settings.json case fails on EEXIST
→ [finding_9.md](feat_flow_walker_uv_shipping_task_round_1/finding_9.md)

### 10. (S8) replace-ref case fails on EEXIST
→ [finding_10.md](feat_flow_walker_uv_shipping_task_round_1/finding_10.md)

### 11. (S9) info/grafts case fails on EEXIST
→ [finding_11.md](feat_flow_walker_uv_shipping_task_round_1/finding_11.md)

### 12. (S4) config.worktree case fails on EEXIST
→ [finding_12.md](feat_flow_walker_uv_shipping_task_round_1/finding_12.md)

### 13. (S4c) .git/config core.fsmonitor case fails on EEXIST
→ [finding_13.md](feat_flow_walker_uv_shipping_task_round_1/finding_13.md)

### 14. (S10) planted commondir case fails on EEXIST
→ [finding_14.md](feat_flow_walker_uv_shipping_task_round_1/finding_14.md)

### 15. (J1) unset default-branch job case fails on EEXIST
→ [finding_15.md](feat_flow_walker_uv_shipping_task_round_1/finding_15.md)

### 16. (J2) failing job-surfaces case fails on EEXIST
→ [finding_16.md](feat_flow_walker_uv_shipping_task_round_1/finding_16.md)

### 17. (J3) honest job branch case fails on EEXIST
→ [finding_17.md](feat_flow_walker_uv_shipping_task_round_1/finding_17.md)

### 18. (J4) session-written .npmrc case fails on EEXIST
→ [finding_18.md](feat_flow_walker_uv_shipping_task_round_1/finding_18.md)

### 19. (J5) session-written node_modules case fails on EEXIST
→ [finding_19.md](feat_flow_walker_uv_shipping_task_round_1/finding_19.md)

### 20. (J6) forged base in job checkout case fails on EEXIST
→ [finding_20.md](feat_flow_walker_uv_shipping_task_round_1/finding_20.md)

---

## Not fixable on this branch

### `npm pack lists the staged Python files` (`cli/test/python-packages-staged.test.mjs`): the sandbox refuses npm's cache write

```
        not ok 1244 - npm pack lists the staged Python files
          location: 'cli/test/python-packages-staged.test.mjs:110:1'
            Command failed: npm pack --dry-run --json
            npm error code EPERM
            npm error syscall open
            npm error path <home>/.npm/_cacache/tmp/3a65cb01
            npm error errno -1
            npm error Your cache folder contains root-owned files, due to a bug in
            npm error previous versions of npm which has since been addressed.
            npm error   sudo chown -R 501:20 "<home>/.npm"
```

**Reason:** This is a sandbox refusal, not a defect in the tree. `EPERM` on `open` means *Operation not permitted*. The refused path is `<home>/.npm/_cacache/tmp/…`, the operator's shared npm cache. The run's sandbox lets npm write only to `<home>/.npm/_logs`, so a write to `_cacache` falls outside the writable set. npm suggests that root-owned files cause the error, but that does not apply here. The same refusal is already on record from this branch's own units: the task 1 plan's deviation note and the code review's finding 2 both quote it under `_cacache/tmp/…` paths. The test leaves npm's default cache in place, and its assertions on the packed file list never got to run.

**Operator's remedy:** run gate 4's `npm pack` case where npm's cache is writable, outside this sandbox. Alternatively, lift the refusal through configuration: the named opt-out `sandbox.optOut` with its `reason` in `devscene.config.json`, followed by `init --upgrade`. Do not change the test or code to avoid the refused access, for example by giving the case a temporary `--cache`, unless an operator answer authorises that change for this failure. Only then can it become a finding.

---

## Source failures

- **Gate `typecheck`** (`commands.typecheck`): exited 0. No failure.
- **Gate `test`** (`commands.test`): exited 1. `run-gates: 2 failed, 34 passed`.
  - **Gate 4 `npm test`** (exit 1, `# fail 20`). Its failing tests:
    - `Acceptance 1: with docs.retrievalBackend absent, doctor reports what an explicit typescript does, plus three not-selected passes`, with its parent suite `doctor` (`1 subtest failed`), `cli/test/doctor.test.mjs` → **Finding 2**. First round (no earlier logs).
    - `npm pack lists the staged Python files`, `cli/test/python-packages-staged.test.mjs` → `## Not fixable on this branch`. First round (no earlier logs).
    - `an honest hung run resumes: the edit discarded, the branch unmoved, the note written`, `cli/test/watcher-stall-reset-payloads.test.mjs` → **Finding 3**. First round (no earlier logs).
    - `(S1) a githooks/reference-transaction committed on the branch is refused, and never runs` → **Finding 4**. First round.
    - `(S2) a .claude/settings.json committed with a hook is refused, and the working-tree file is not installed` → **Finding 5**. First round.
    - `(S3) a nested repository's own core.fsmonitor behind a gitlink is never run: the run resumes` → **Finding 6**. First round.
    - `(S5) a PAUSE_PROGRESS.md symlinked out of the clone is refused, and the outside file is unchanged` → **Finding 7**. First round.
    - `(S6) a forged base: the local default-branch refs pointed at a payload tip do not pass it` → **Finding 8**. First round.
    - `(S7) a session-written .claude/settings.json hidden by a skip-worktree bit in the clone's index is refused` → **Finding 9**. First round.
    - `(S8) a replace ref on the merge base does not pass a payload tip` → **Finding 10**. First round.
    - `(S9) an info/grafts line on the tip and the base does not pass a payload tip` → **Finding 11**. First round.
    - `(S4) a .git/config.worktree planted in the clone, carrying core.fsmonitor, is refused before the reset` → **Finding 12**. First round.
    - `(S4c) a core.fsmonitor in the clone's .git/config, off the allow-list, is refused before the reset` → **Finding 13**. First round.
    - `(S10) a .git/commondir planted in the clone, naming a repository whose config carries a payload, is refused before the reset` → **Finding 14**. First round.
    - `(J1) job mode with HARNESS_GITHUB_DEFAULT_BRANCH unset gives up without calling npx` → **Finding 15**. First round.
    - `(J2) job mode with the job-surfaces check failing gives up before the reset` → **Finding 16**. First round.
    - `(J3) job mode on an honest branch runs the pinned check from a scratch directory, then resumes` → **Finding 17**. First round.
    - `(J4) a session-written .npmrc never reaches the real npx: the offline fetch fails and the run is given up` → **Finding 18**. First round.
    - `(J5) a session-written node_modules never reaches the real npx: the run is given up` → **Finding 19**. First round.
    - `(J6) a forged base in the job checkout: the real doctor judges from the recorded commit and refuses` → **Finding 20**. First round.
  - **Gate 6a `no machine paths`** → **Finding 1**. First round (no earlier logs).
