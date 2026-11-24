# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **Scope register misses two `devscene-flow-host/README.md` sections the command entry reaches (story index, `fix_flow_walker_saved_render_story_plan.md` → `## Scope register`; owning task `task_5_plan.md`)** — disposition (i). The register's own closure invariant makes *"every section of a listed file that states … the host's records and entry points that Task 2 changes"* its own row. Re-running the command entry verbatim (`git grep -lE 'Differences from flow-walker|#475|current. re-renders' -- '*.md' ':!harness-runs/**'`) lists `devscene-flow-host/README.md`, and two of its sections that describe what Task 2 changes are not rows:
   - `## What it reads, answers and keeps` → **Recording a gate.** — *"The `HostStep` returned carries the step and the `refused:` lines it brings."* After Task 2, `HostStep` also carries `printed`, and `record_outcome` writes a second record under `RefusalStore`'s lock.
   - `## Errors` — *"A malformed refusal record raises `ValueError` naming the file"*. After Tasks 1–2, a malformed printed-reads record raises `ValueError` naming its file too, and `current_step` can now raise it on a `current`.

   Both are descriptions, and no command or step fails because of them, so this is a Should Fix and not a Must Fix. Add each one as a row with `change` → Task 5, or as `no-change` with a reason, and give Task 5 the matching `**Work:**` sub-bullet.

## Nice to Have

1. **`task_2_plan.md` — the `test_round_gates.py` case is built on a helper that returns nothing.** The bullet reads *"Reaching `ui_review` through `record_outcome`, using the suite's existing `_at_ui_review`, gives `printed == PrintedReads(...)`"*. `tests/test_round_gates.py` → `_at_ui_review` returns `None`, and the `HostStep` it gets is local to it. Say whether the case changes the helper to return the step or reads `PrintedReadsStore` after calling it.
2. **`task_4_plan.md` — planting the architecture files before `start` moves the round number.** The plan plants two `FAIL_BODY` files in `devscene/architecture_reviews/feat_x/` and then calls `start` with no entry. `start_walk` → `round_resume` treats the default entry `plan_writer` as the round's writer, so the walk resumes at the round after the highest planted file (`host/resume.py` → `if writer: return RoundResume(rn.id, r + 1)`). The listed cap literal does not depend on this, but the gates' `arg.iteration` lines during the drive do. The plan also leaves the closed round's `findings_file:` values and the summary's `{open_gates}` unnamed. Name the planted indices and state these literals, or plant the files after `start`, so the implementer does not have to work them out from the code's output.
