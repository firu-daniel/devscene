### Task 3 — Prove the driver re-dispatches a refused gate and correct the state-dir READMEs

**Goal:** Show end to end that script-driven planning handles a refused round file with no driver change, and make the adopter READMEs say why a round file can be replaced.

**Depends on:** Task 1, whose stub option `malformedMustFix: true` in `cli/test/helpers/planning-driver.mjs` writes a `verdict: FAIL` file whose entry lacks `**Class:**`. Task 2, whose walker prints `refused: <gate> attempt <n> of 3: <reason>`, re-dispatches a refused gate after its siblings finish, and on the third refusal prints `held: <gate> error` under `binding: <escalate>`.

### Targets

- `cli/test/planning-driver-control.test.mjs`
- `cli/templates/state-dir/task_plan_reviews/README.md`
- `cli/templates/state-dir/architecture_reviews/README.md`
- `cli/templates/state-dir/architecture_user_review_reviews/README.md`
- `cli/templates/state-dir/business_parity_reviews/README.md`
- `cli/templates/state-dir/business_parity_user_review_reviews/README.md`

**Work:**

- [ ] Add a driver case: `task-plan-reviewer` scripted `[{ outcome: 'FAIL', malformedMustFix: true }, { outcome: 'PASS' }]`. Assert `pd_drive` returns 0, `task-plan-reviewer` is called twice, `task-plan-writer` is called once, and the log carries `refused: plan_review attempt 1 of 3:`.
- [ ] Add a driver case: three scripted malformed `FAIL` returns from `task-plan-reviewer`. Assert status 3, three reviewer calls, one writer call, and a clarification carrying `held: plan_review error` and a `refused: plan_review attempt 3 of 3:` line. Extend the suite header's rule to cover a refused round file.
- [ ] In each of the five READMEs, replace "re-running a round that was interrupted" with "re-running a round that was interrupted, or whose file the round-file check refused". Change nothing else in those files.

**Verification:**

- `npm test --workspace cli -- test/planning-driver-control.test.mjs` passes with `cli/templates/scripts/lib/planning-driver-lib.sh` unchanged.
- `git grep -c 'whose file the round-file check refused' -- cli/templates/state-dir` lists exactly this task's five README targets.
