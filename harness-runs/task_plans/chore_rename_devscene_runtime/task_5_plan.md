### Task 5 — Check that the maintainer's re-lock and workflow-edit commits are on the branch's remote, and park the run until they are

**Goal:** Carry out the task prompt's park-and-resume by a route on which the run parks rather than fails. The task prompt's `## Decided (2026-11-23)` workflow bullet reads: *"when the workflow change is committed and ready, the run parks and asks the maintainer to push it. It does not try to push it, and it does not work around the refusal. It resumes once the maintainer answers that the push is done"*. This task returns a `blocker` until all of the following hold:

- the maintainer's re-lock of `devscene-flow-host/uv.lock` is committed on the branch;
- the maintainer's edit of `.github/workflows/supply-chain.yml` is committed on the branch;
- the branch tip holding both is on the branch's remote.

**Depends on:** Task 1 and Task 4.

- Task 1 moved `uv.lock` byte for byte to `devscene-flow-host/uv.lock`. Its root `[[package]]` entry still reads `name = "devscene-runtime"`, because the run cannot re-lock (story index `## Context` → **The lock.**).
- Task 4 wrote `docs/development.md` → `## 8. The nightly supply-chain audit`, which says `uv-audit` runs *"once each from `docs-retrieval-service/`, `graphscene/` and `devscene-flow-host/"`*. The workflow edit this task checks for makes the workflow match that sentence.

**This task edits no file.** That includes `.github/workflows/supply-chain.yml`. It does none of the re-lock, the workflow edit, the commits, the push or the fetch. Those are the maintainer's manual steps 1 and 2 in the story index's `## Context`.

**Why the run must not commit the workflow edit.** Every commit the run lands is pushed in the same wrapper call (`plugin/instructions/plan_orchestration_instructions_autonomous.md` → `### <commit_call>`). When the commits to send change a path under `.github/workflows/`, `push-branch.sh` refuses and calls `hr_push_refusal_record` before its `exit 0` (`cli/templates/scripts/push-branch.sh` → `NO UNATTENDED PUSH CHANGES A WORKFLOW FILE`, and the `if [ -n "$send_refusal" ]` block). The watcher's tick pass then tears the session down and marks the run `failed` with `push refused: <reason>`, whatever the reason (`cli/templates/scripts/autonomous-watcher.sh` → `PUSH REFUSALS (check_push_refusals)`). A failed run is never resumed by an answer. So this unit parks while the workflow edit does not yet exist on the branch, and the maintainer commits it.

**The precondition, and why it parks the run.** This task's work is gated on one precondition: *"the maintainer's re-lock commit of `devscene-flow-host/uv.lock` and the maintainer's commit of the `.github/workflows/supply-chain.yml` edit are on the branch, and the branch tip holding them has landed on the branch's remote"*. This is an ordering precondition inside the dispatching phase. So when it does not hold, the implementer returns an `outcome` of `blocker` (`plugin/agents/layer-implementer.md` → **Unsatisfiable-gate disposition.**: *"return an `outcome` of `blocker` if the item it names has not landed"*). That return then takes this route:

1. `plugin/instructions/unit_loop_core.md` → `## The unit loop` step 3 turns the blocker into *"stop the whole loop and `<escalate>`"*.
2. The autonomous fork binds `<escalate>` to *"The clarification reroute — park and yield"* (`plan_orchestration_instructions_autonomous.md` → `### <escalate> — the clarification reroute`). A headless run writes the blocker to `harness-runs/clarifications/chore_rename_devscene_runtime/question_<n>.md`, logs `PARKED:`, and ends the session. The question file is machine-local, so the park lands no commit and makes no push. An interactive run asks the question live.
3. The watcher marks the run `parked` and resumes it once the question file is answered. Task 5 is then still the first `[ ]` readiness entry, so it is dispatched again and re-runs the checks below.
4. If the checks pass, the unit lands. If the maintainer answered without doing the steps, it parks again.

**Why this unit's own commit then pushes cleanly.** It is an index-only commit. `push-branch.sh` syncs the run copy's `refs/heads/chore_rename_devscene_runtime` into the main checkout (header → `A CLONE IS A TARGET TOO`). It then sends `rev-list refs/heads/<branch> --not refs/remotes/<remote>/<branch>`, computed in the main checkout (header → `NO COMMIT IT SENDS CARRIES A CREDENTIAL`). Manual step 2's fetch in the main checkout moves that ref past the maintainer's commits, so the send set holds only this unit's commit, and that commit touches no workflow path. **The fetch is the one step this unit cannot check.** The main checkout's refs are outside this checkout, so the check below reads only this checkout's `origin/chore_rename_devscene_runtime`, which the maintainer's push from here moves. The blocker line therefore names the fetch explicitly.

The ask-vs-assume policy that `<escalate>` consults first (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Ask-vs-assume policy`) has no assumption to proceed on:

- The re-lock reaches the network, which the run's sandbox refuses (`scripts/python-service.sh` header → `WHO RUNS lock, sync AND provision`).
- A workflow commit cannot pass through the run's push (above).
- A human performs all of these steps, and a CI change pushed to the remote cannot be undone from inside the run.

That makes this a park-and-ask, and the task prompt has already decided it.

### Targets

- None. This unit's commit carries no work file, only the readiness-index flip and run artifacts, so a `staged: index-only — …` line from the commit step is expected for this unit (`unit_loop_core.md` → `## The unit loop` step 6).

**Work:**

- [ ] **Lock check.** From the checkout root, run each of these as one plain command:
  - `grep -n -F 'name = "devscene-runtime"' devscene-flow-host/uv.lock` must print nothing.
  - `grep -n -F 'name = "devscene-flow-host"' devscene-flow-host/uv.lock` must print at least one line.
  - `git status --porcelain -- devscene-flow-host/uv.lock` must print nothing, so the re-lock is committed rather than left in the working tree.
- [ ] **Workflow check.** From the checkout root, run each of these as one plain command:
  - `git grep -n -i "devscene-runtime" -- .github/workflows/supply-chain.yml` must print nothing.
  - `git grep -n "working-directory: devscene-flow-host" -- .github/workflows/supply-chain.yml` must print exactly one line.
  - `git status --porcelain -- .github/workflows/supply-chain.yml` must print nothing, so the edit is committed.
- [ ] **Push check.** Run `git rev-parse HEAD`, then `git branch -r --contains <sha>` with the printed SHA written literally. The output must list `origin/chore_rename_devscene_runtime`. The two checks above prove that `HEAD` holds both of the maintainer's commits, so this check proves both are on the remote. Use no command substitution and no shell variable.
- [ ] **If any check above fails**, change no file and return an `outcome` of `blocker`. Its one line names the failed check and the owed steps, and must be usable unedited as the park's question:
  - `Maintainer steps owed before the run can continue (story index → Manual setup 1–2, which spell each step out): in this checkout (the run copy holding harness-runs/clarifications/chore_rename_devscene_runtime/), outside any sandbox, run bash scripts/python-service.sh --package devscene-flow-host lock; in .github/workflows/supply-chain.yml change devscene-runtime/uv.lock to devscene-flow-host/uv.lock in the header comment and working-directory: devscene-runtime to working-directory: devscene-flow-host in the uv-audit job; commit only those two files; push from this checkout with git push origin refs/heads/chore_rename_devscene_runtime:refs/heads/chore_rename_devscene_runtime (never --set-upstream); then in the main checkout run git fetch origin chore_rename_devscene_runtime, without which the run's next push is refused and the run fails; then answer this question — failed check: <which>`.
  - Do not edit the workflow file, push, re-lock, edit `uv.lock`, fetch, or retry anything yourself.
- [ ] **If every check passes**, return an `outcome` of `implemented` with no file changed.

**Verification:**

- Every check under **Work:** was executed, not reasoned about, and its output is quoted in the detail file. These checks are this unit's required work, so a check the sandbox refused counts as a failed check. It takes the `blocker` return above and is never a pass.
- On an `implemented` return, `git status --porcelain -- . ':!harness-runs'` prints nothing: this unit changed no file outside the run artifacts.
