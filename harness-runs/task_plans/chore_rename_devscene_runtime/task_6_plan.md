### Task 6 — Check that the maintainer's re-lock and workflow push have landed, and park the run until they have

**Goal:** Carry out the task prompt's park-and-resume through a route the flow really takes. The task prompt's `## Decided (2026-11-23)` workflow bullet says *"when the workflow change is committed and ready, the run parks and asks the maintainer to push it … It resumes once the maintainer answers that the push is done"*. This task returns a `blocker` until both of the following are on the branch's remote:

- the maintainer's re-lock commit of `devscene-flow-host/uv.lock`;
- Task 5's workflow commit.

**Depends on:** Task 1 and Task 5.

- Task 1 moved `uv.lock` byte for byte to `devscene-flow-host/uv.lock`. Its root `[[package]]` entry still reads `name = "devscene-runtime"`, because the run cannot re-lock (story index `## Context` → **The lock.**).
- Task 5 committed the `.github/workflows/supply-chain.yml` edit, and the run's push of that commit was refused. That refusal is `pushed: failed`, which is never escalated (`plugin/instructions/plan_orchestration_instructions_autonomous.md` → `### <commit_call>` → **The push is best-effort inside the wrapper.**).

**This task edits no file.** It does none of the re-lock, the lock commit or the push. Those are the maintainer's manual steps 1 and 2 in the story index's `## Context`.

**The precondition, and why it parks the run.** This task's work is gated on one precondition: *"the maintainer's re-lock commit of `devscene-flow-host/uv.lock` and Task 5's workflow commit have both landed on the branch's remote"*. This is an ordering precondition inside the dispatching phase. So when it does not hold, the implementer returns an `outcome` of `blocker` (`plugin/agents/layer-implementer.md` → **Unsatisfiable-gate disposition.**: *"return an `outcome` of `blocker` if the item it names has not landed"*). That return then takes this route:

1. `plugin/instructions/unit_loop_core.md` → `## The unit loop` step 3 turns the blocker into *"stop the whole loop and `<escalate>`"*.
2. The autonomous fork binds `<escalate>` to *"The clarification reroute — park and yield"* (`plan_orchestration_instructions_autonomous.md` → `### <escalate> — the clarification reroute`). A headless run writes the blocker to `harness-runs/clarifications/chore_rename_devscene_runtime/question_<n>.md`, logs `PARKED:`, and ends the session. An interactive run asks the question live.
3. The watcher resumes the run once the question file is answered. Task 6 is then still the first `[ ]` readiness entry, so it is dispatched again and re-runs the checks below.
4. If the checks pass, the unit lands. If the maintainer answered without doing the steps, it parks again.

The ask-vs-assume policy that `<escalate>` consults first (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Ask-vs-assume policy`) has no assumption to proceed on. The re-lock reaches the network the run's sandbox refuses (`scripts/python-service.sh` header → `WHO RUNS lock, sync AND provision`), and the push is refused by design (`cli/templates/scripts/push-branch.sh` → `NO UNATTENDED PUSH CHANGES A WORKFLOW FILE`). A human performs both, and pushing a CI change is not reversible from inside the run. That makes this a park-and-ask, and the task prompt has already decided it.

### Targets

- None. This unit's commit carries no work file, only the readiness-index flip and run artifacts, so a `staged: index-only — …` line from the commit step is expected for this unit (`unit_loop_core.md` → `## The unit loop` step 6).

**Work:**

- [ ] **Lock check.** From the checkout root, run `grep -n -F 'name = "devscene-runtime"' devscene-flow-host/uv.lock`, which must print nothing. Then run `grep -n -F 'name = "devscene-flow-host"' devscene-flow-host/uv.lock`, which must print at least one line. Then run `git status --porcelain -- devscene-flow-host/uv.lock`, which must print nothing, so the re-lock is committed rather than left in the working tree.
- [ ] **Push check.** Take the last commit touching each file, one plain call per file:
  - `git log -1 --format=%H -- devscene-flow-host/uv.lock`, the maintainer's re-lock commit once the lock check holds;
  - `git log -1 --format=%H -- .github/workflows/supply-chain.yml`, Task 5's commit.

  For each printed SHA, written literally, run `git branch -r --contains <sha>`. Each must list a remote-tracking branch ending in `/chore_rename_devscene_runtime`. Use no command substitution and no shell variable.
- [ ] **If any check above fails**, change no file and return an `outcome` of `blocker`. Its one line names the failed check and the owed steps, and must be usable unedited as the park's question:
  - `Maintainer step owed before the run can continue (story index Manual setup 1–2): in this checkout (the run copy holding harness-runs/clarifications/chore_rename_devscene_runtime/), outside any sandbox, run bash scripts/python-service.sh --package devscene-flow-host lock, commit only devscene-flow-host/uv.lock, push the branch with git push to the remote it tracks, then answer this question — failed check: <which>`.
  - Do not push, re-lock, edit `uv.lock`, or retry anything yourself.
- [ ] **If every check passes**, return an `outcome` of `implemented` with no file changed.

**Verification:**

- Every check under **Work:** was executed, not reasoned about, and its output is quoted in the detail file. These checks are this unit's required work, so a check the sandbox refused counts as a failed check. It takes the `blocker` return above and is never a pass.
- On an `implemented` return, `git status --porcelain -- . ':!harness-runs'` prints nothing: this unit changed no file outside the run artifacts.
