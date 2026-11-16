### 1. A resume entering at `convergence` never re-runs Override 3, so an uncommitted UI-test plan stays uncommitted

**File:** `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_handoff`. The change is the order of two blocks in that function: the decision `[ "$ui" != passed ] || ui_yes=yes`, followed by `prl_convergence_commits "$ui_yes" || return 2`, and the later block that opens `pd_ledger_read` / `if [ -z "$ui" ]; then`. The test goes in `cli/test/planning-driver-walk.test.mjs`.

**The problem.** `pd_handoff` decides whether to make Override 3's UI-test-plan commit (`chore: Add UI-test plan for <branch>`) from one input: the walker's `report: ui_test passed` line. The walker prints a `report:` line only for keys recorded on edges this walk passed through (`flow-walker.sh` → `record_reports`; OUTPUT: `<terminal_handoff>  report: <key> <value> per recorded key`). A walk started with `--entry convergence` passes no UI-test edge, so it prints no `report: ui_test` line. `ui` is then empty, `ui_yes` stays `no`, and `prl_convergence_commits no` skips the UI-test commit.

Only after both commits and the `P3` flip does `pd_handoff` work out the missing fact from the ledger and disk. With `P2` `[x]` and the UI-test index present it sets `ui=passed`. That value is used only for the summary log line (`ui_test: <index>, per-test files …`), so the code knows a plan was written and still does not commit it.

**Why it is reachable.** `pd_entry` picks `entry=convergence` exactly when `P1` is `[x]`, `P2` is resolved and no answered pair is pending (the branch `elif [ "$PD_P1" = x ]; then if pd_resolved "$PD_P2"; then entry=convergence`). On a UI-test PASS, `pd_act` flips and commits `P2` (`prl_ledger_flip P2`, its own commit and push) before `pd_handoff` runs Override 3. Any interruption between those two commits creates exactly this case: a stall kill or watchdog kill of the launch subshell, a host crash, or a push that hangs and is killed. Another way in is an earlier orchestrated session that crashed in the same window, followed by a launch with the pilot on. The next drive then finds `P1` `[x]`, `P2` `[x]` and `P3` `[ ]`, finds the saved walk finished (`<terminal_handoff>`, never continued), enters at `convergence`, flips `P3` and hands off. The UI-test index and the `<state_dir>/ui_test_plans/<branch>/` detail directory stay untracked.

**Runtime symptom.** The branch reaches "ready for review" with the UI-test plan not committed. Override 3 exists to prevent exactly this (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 3 — commit the UI-test plan after it converges` → **Why a commit is needed here.**: *"the index and/or the whole detail dir dangle uncommitted and are lost at PR time"*). Phase E's `ui_test_pass` committer stages only the index, and never stages the detail directory.

**Proof: the contract the driver claims to follow.** `plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 5 — pause/resume + flow-progress ledger (planning half)` → **Resume-from-ledger (planning).**: *"With `P1` and `P2` resolved and `P3` `[ ]`, the result is also `--entry convergence`: a finished `<terminal_handoff>` walk is never acted on again, Overrides 3 and 4 run again idempotently through exit 3, and `P3` is flipped."* The driver re-runs Override 4 on this path but not Override 3. Re-running Override 3 is safe where the plan is already tracked: the wrapper returns exit 3, which `prl_commit` treats as success.

**Fix.** In `pd_handoff`, work out the UI-test variant before the commit decision rather than after it. Move these lines up so that they sit directly after the `while … done <<EOF … EOF` loop that reads the `report: ui_test` line, and before `[ "$ui" != passed ] || ui_yes=yes`:

```bash
  pd_ledger_read
  if [ -z "$ui" ]; then
    case "$PD_P2" in
      -) if hr_phase_enabled "$PD_WORKTREE" qa >/dev/null 2>&1; then ui=run-mode-skipped; else ui=qa-phase-off; fi ;;
      x) if [ -e "$PD_STATE/ui_test_plans/${b}_ui_test_plan.md" ]; then ui=passed; else ui=no_ui; fi ;;
    esac
  fi
```

Remove them from their current position, between `if pd_ret_value plan_writer tasks_count; …` and `case "$ui" in`. The function then reads, in order:
1. the `report:` loop;
2. the moved block;
3. `[ "$ui" != passed ] || ui_yes=yes`;
4. `prl_convergence_commits "$ui_yes" || return 2`;
5. `prl_ledger_flip P3 || return 2`;
6. the `tasks_count` line;
7. `case "$ui" in` and everything after it, unchanged.

`pd_ledger_read` reads only the `P1`–`P3` boxes. `P2` is not changed by `prl_convergence_commits` or by the `P3` flip, so reading it earlier gives the same value.

**Test.** Add one case to `cli/test/planning-driver-walk.test.mjs`:

`test('a resume entering at convergence with P2 [x] and an uncommitted UI-test plan commits that plan before P3', { skip: SKIP }, async (t) => { … })`:

- Build the fixture: `const f = await driverFixture(t);`.
- Overwrite the ledger with `f.write(\`${f.sd}/flow_progress/${BRANCH}_progress.md\`, …)`, using the text `driverFixture` seeds (`cli/test/helpers/planning-driver.mjs` → the `seed` ledger lines) with `- [ ] P1.` changed to `- [x] P1.` and `- [ ] P2.` changed to `- [x] P2.`.
- Write the story index `` `${f.sd}/story_plans/${BRANCH}_story_plan.md` `` (any text).
- Write the UI-test index `` `${f.sd}/ui_test_plans/${BRANCH}_ui_test_plan.md` `` and one per-test file `` `${f.sd}/ui_test_plans/${BRANCH}/ui_test_1.md` `` (any text), all uncommitted.
- Run `const r = await drive(t, f);` and assert:
  - `r.status === 0`;
  - no stub call was made (`r.calls.length === 0`);
  - `assertInOrder(r.subjects, [\`chore: Add UI-test plan for ${BRANCH}\`, \`chore: Flow progress P3 for ${BRANCH}\`], show(r))`;
  - `git ls-files` in `f.dir` (through `runGit` from `./helpers/fixture.mjs`, imported for this case) lists both UI-test files.

Run only that file: `npm test --workspace cli -- test/planning-driver-walk.test.mjs`. Mutation check: with the moved block put back below the commits, the new case fails on the missing `chore: Add UI-test plan` subject.
