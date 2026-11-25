# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_7_plan.md` — concurrency case (1) is kept unchanged, but its lock assertion fails once Task 2 moves `walkerStatePath`**
   `cli/test/flow-walker-concurrency.test.mjs` defines `const lockPath = (dir) => \`${walkerStatePath(dir)}.lock\``. Case (1) ends each repetition with `assert.equal(existsSync(lockPath(dir)), false, 'a call left the lock directory behind')`. Task 2 makes `walkerStatePath(dir)` the per-branch file `<stateDir>/.flow_walker_state/feat_x.json`, so `lockPath` becomes `…/feat_x.json.lock`. That is exactly the file GraphScene's `FileStateStore.lock` creates (`graphscene/src/graphscene/adapters/state_file.py` → `lock`: `os.open(self._lock_path, os.O_RDWR | os.O_CREAT, 0o644)`, released with `flock(LOCK_UN)` and `os.close`, never unlinked). The module docstring says so: *"Deliberately not covered: … A lock file left behind: it is harmless, because a `flock` dies with its process."* Every `start`/`next` in (1) therefore leaves the file in place. `devscene-flow-host/README.md` → **The locks.** says (1) *"holds unchanged"*, but that was written before the helper's path moved. Task 7 repeats it.
   **Raised against:** "Keep (1) unchanged. Rewrite the header, citing that file and naming the three removed behaviours as deliberately not covered here, with the reason."
   **Must hold:** after Tasks 2 and 7, every case kept in `flow-walker-concurrency.test.mjs` asserts only what the Python walker actually leaves on disk. Its "no lock left behind" check is either removed or restated as the property `flock` gives (no lock *held*), and `lockPath` no longer stands for the bash lock directory.
   **Class:** Wrong build
   **Failure:** If the implementer applies Task 2's `walkerStatePath` and keeps case (1) unchanged as Task 7 says, then every repetition of (1) fails on `a call left the lock directory behind`, because `<stateDir>/.flow_walker_state/feat_x.json.lock` exists after the walk.
   **Fix:** In `task_7_plan.md`, add case (1)'s closing lock assertion and the `lockPath` helper to `### Targets` and `**Work:**`. Drop the `existsSync(lockPath(dir))` check, or replace it with a check the `flock` design supports, for example that a following `next`/`current` is not blocked. State in the rewritten header that a leftover `.lock` file is GraphScene's documented behaviour. Remove the stale "(1) holds unchanged" reasoning from the task's account.

2. **`task_16_plan.md` — the third verification grep can never print nothing**
   `git grep -n -e 'provision: SKIPPED' -e 'SKIPPED line' -- cli/test` matches `cli/test/python-service.test.mjs:388`: `test('provision with no uv on PATH prints one SKIPPED line, exits 0 and writes nothing in the fixture', …)`. That case tests `scripts/python-service.sh provision`, a different script whose `SKIPPED` outcome this branch does not change. No task targets that suite. After every edit Task 16 lists, the bullet still prints that line.
   **Raised against:** "`git grep -n -e 'provision: SKIPPED' -e 'SKIPPED line' -- cli/test` prints nothing."
   **Must hold:** every verification command in the task file gives its stated result on a tree where the task's work is done correctly, and none can be satisfied only by editing a file outside the task's targets.
   **Class:** Wrong action from operative text
   **Failure:** If the implementer runs Task 16's third verification bullet after completing its work, then it prints `cli/test/python-service.test.mjs:388: …prints one SKIPPED line…`. The task then fails its own check, or the implementer retitles a correct test it does not own.
   **Fix:** In `task_16_plan.md`, narrow the grep to the flow-host wording: for example `git grep -n -e 'flow-host: provision: SKIPPED' -- cli/test`, plus the four retitled case names. Alternatively, restrict the paths to this task's four target files.

## Should Fix
1. **`task_6_plan.md` — the graph is still claimed write-protected.** The Goal says *"the walker script, the environment it executes and the graph it reads are the ones `cli/src/generators/writeProtection.ts` write-protects"*. `protectedPaths` skips every `OUTER_LOOP_SCRIPTS` row with a `subdir` and adds only `libraryDir()` and `flowHostDir`, so `<main>/<scriptsDir>/flows/` is not covered. Drop the graph from the claim, so the header paragraph Task 6 writes does not repeat it.
2. **`task_7_plan.md` — smaller gaps.**
   - Its verification grep for `'the walk finished'` also hits the comment at `cli/test/flow-walker-resume.test.mjs` (`// core: "any other \`binding:\` — the walk finished".`), which the Work does not touch.
   - Case (11)'s regex `^…first$` has no `m` flag. Against stderr ending in `\n`, a JS `$` does not match.
   - `flow-walker-fan-out.test.mjs`'s `assert.doesNotMatch(readFileSync(walkerStatePath(dir), 'utf8'), /^round\.verdict\.plan_review=/m)` becomes vacuous against the JSON state.
3. **`task_10_plan.md` — a second citation in the same file.** `plugin/commands/branch-start-plan-semi-autonomous.md` step 3 also says *"over `<scripts_dir>/flows/task_plan_writing.graph.json`"*. The Work leaves it, so the first verification grep prints it. Editing it makes the second grep's baked-in *"exactly the three edited lines"* false. Add the line to the Work and drop the count.
4. **`task_15_plan.md` — its grep hits an untargeted paragraph.** `git grep -n … 'init --provision-python' -- docs/cli.md README.md` also matches `docs/cli.md`'s two-families paragraph (*"which `init --provision-python`, `setup-worktree.sh`'s bootstrap and a person run"*). That paragraph is not in `### Targets`.
5. **Scope register (story index) — anchors miss passages the branch makes false.** Each file is a row, but the owning task does not name these passages:
   - `docs/flow-graph-walker.md` → `### Format 4 — …`: *"`init` does not write the format-4 source"* and *"The walker … stay on format 3"*. Row 13 / Task 13.
   - `README.md`'s `uv` bullet, *"Nothing runs the walker yet, so without `uv` the `doctor` checks `uv` and `flow-host` only warn"*. Row 3 / Task 15.
   - `docs/cli.md` §7's `uv` and `flow-host` grading and the two-families paragraph. Row 9 / Task 15.
   - `cli/templates/scripts/README.md`'s *"`init` runs it when asked (`--provision-python`, or yes at its prompt)"*. Row 7 / Task 9, which does not depend on Task 4.

   Separately, `cli/templates/README.md` is a corpus target of Task 9 but has no row.
6. **`task_5_plan.md` — suites now need `uv` on the host.** With an absent `uv` graded `fail`, every `doctor` suite that asserts a clean exit on a fresh fixture, such as `cli/test/doctor.test.mjs` → `CLEAN_SUMMARY` (`0 fail — exit 0`), now passes only on a host with `uv` on `PATH`. State that, or give those fixtures a stub `uv`.
7. **`task_1_plan.md` — its verification `init` reaches the network.** Task 4 ships before Task 1, so the `init` run in a throwaway fixture now runs the networked `uv sync` by default. Pass `--no-provision-python` there.

## Nice to Have
1. `cli/templates/scripts/lib/harness-run-lib.sh` → `THE REMOTE STATE BUNDLE.` still says *"the walker's one graph is `task_plan_writing.graph.json`"*. `cli/src/generators/repoRoot.ts` → `RUN_CONTROL_ARTIFACTS`' doc comment calls the walker state a flat file. `cli/templates/scripts/remote-run.sh`'s REPRO comments describe `flow_walker_state` as one bundled file. Task 3 already edits that library header and could restate these.
2. `harness-runs/task_plans/feat_flow_walker_python_cutover/` holds a stray `task_plan_revision_1.md` beside the per-task files. The revision note's home is `harness-runs/plan_revisions/feat_flow_walker_python_cutover/`.
