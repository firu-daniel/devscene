### 1. Record the three stale conventions sentences the cutover falsified, which no channel carries

**Site:** `cli/templates/scripts/autonomous-watcher.sh` → `planning_driver_run`, the hunk `hr_flow_host_exec "$SCRIPT_DIR" "$HR_FLOW_HOST_DRIVER" "${driver_args[@]}"`. The deviation's claimed authorisation is at `harness-runs/story_plans/feat_planning_driver_python_cutover_story_plan.md` → `## Scope register`, rows 1–3 (*"recorded as a `stale-rule` entry in `corpus_staleness`"*).

**Class:** Broken contract
**Failure:** If the watcher launches the planning driver as `planning_driver_run` now does (`hr_flow_host_exec "$SCRIPT_DIR" "$HR_FLOW_HOST_DRIVER" …`), the flow host is launched by a caller other than `flow-walker.sh`. That contradicts `.claude/context/conventions.md` → `## The layers` and `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not`, and the branch leaves no `stale-rule` record anywhere that would bring either rule, or the now-dangling `prl_artifact_commit` citation, to a maintainer.

**The problem.**

The launch rule is stated twice:

- `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host/` bullet: *"**Every caller launches it through `flow-walker.sh`**, whose hand-off runs `devscene-flow-walker` …; there is no bash fallback"*.
- `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not`: *"every caller launches it through `flow-walker.sh`'s hand-off"*.

This branch adds a second caller. The watcher's `planning_driver_run` runs `devscene-planning-driver` through the new library function `hr_flow_host_exec` (`cli/templates/scripts/lib/harness-run-lib.sh`), and never goes through `flow-walker.sh`. The branch also deletes `cli/templates/scripts/lib/planning-record-lib.sh`. That leaves `.claude/context/conventions.md` → `## Commit-message policy`'s citation *"the planning driver reads the same table (`cli/templates/scripts/lib/planning-record-lib.sh` → `prl_artifact_commit`)"* pointing at a file that no longer exists.

The substance of the launch rule survives. There is one launch route, now `hr_flow_host_exec`, which both `flow-walker.sh` and the watcher use. The provisioning refusal is kept (`hr_flow_host_missing`), and there is still no bash fallback. An implementing run may not edit a conventions document, so the plan correctly does not edit either one. Instead it justifies the deviation by citing a record: scope register rows 1–3 say each falsified sentence *"is recorded as a `stale-rule` entry in `corpus_staleness`"*.

That record does not exist:

- **The task prompt drops it.** `harness-runs/task_prompts/feat_planning_driver_python_cutover_task_prompt.md`, the bullet *"The corpus-staleness record is not this branch's."*, says *"This branch keeps the bash pilot's behaviour, which drops `corpus_staleness`."*
- **This branch's own planning ran on that pilot.** `harness-runs/improvement_observations/feat_planning_driver_python_cutover.md` carries *"Script-driven planning node sessions (pd_drive returned 0)"*. So the writer's `corpus_staleness` was dropped and never reached the observations file or a Done summary.
- **The decision of record does not mention it either.** `docs/flow-graph-walker.md` → `### Corpus staleness is still dropped` records the drop. Its **Cost.** paragraph says *"a planning agent's `corpus_staleness` entry on the script-driven path reaches no record"*.
- **No artifact names it.** Searching the branch's run artifacts for `stale-rule` finds only the story plan and the plan-time architecture reviews. The improvement-observations file has no staleness entry.

The cited authorisation therefore does not exist. Under the *Verify justifications* rule a non-existent authorisation does not waive the rule. The branch ships two conventions documents stating a launch rule its own code no longer follows, plus one citation that no longer resolves, and nothing routes any of them to the supervised `/devscene:analyze` re-run or hand edit that `.claude/context/conventions.md` names as the only route for a stale rule.

**The fix.** Make the three `stale-rule` entries reach a maintainer through a durable channel. Do not edit either conventions document.

1. In `harness-runs/improvement_observations/feat_planning_driver_python_cutover.md`, append **one** `tooling-gap` block in the file's existing block shape. This is the channel `plugin/instructions/improvement_observations_instructions.md` prescribes for a plan's corpus staleness (*"The plan's corpus staleness is one of the observations"*). Insert it before the closing `# Task run (Phase D)` label if one is present, otherwise at the end:

   ```
   ## Corpus staleness the script-driven planning dropped: three stale-rule entries
   - **category:** tooling-gap
   - **evidence:** stale-rule `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host/` bullet ("Every caller launches it through `flow-walker.sh`") — the watcher now launches `devscene-planning-driver` through `hr_flow_host_exec`; owes a restatement naming `hr_flow_host_exec` as the one launch route for `flow-walker.sh` and the watcher alike. stale-rule `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not` ("every caller launches it through `flow-walker.sh`'s hand-off") — same cause, same restatement. stale-rule `.claude/context/conventions.md` → `## Commit-message policy` ("the planning driver reads the same table (`cli/templates/scripts/lib/planning-record-lib.sh` → `prl_artifact_commit`)") — that library is deleted; owes a restatement naming `devscene-flow-host/src/devscene_flow_host/host/commit_points.py` → `commit_artifact`, through `commit-on-branch.sh --artifact`.
   - **cost this run:** three conventions sentences left stale with no other record; each owes a supervised `/devscene:analyze` re-run or a hand edit
   ```

2. In `docs/flow-graph-walker.md` → `### Corpus staleness is still dropped`, add one sentence after **Cost.** stating that this branch's own three `stale-rule` entries are recorded in that observations file, and naming the three conventions-document sections above. The decision of record then points at where they went.

No test file is created or edited by this fix.
