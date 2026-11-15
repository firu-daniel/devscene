# Review plan meta-review — iteration 0

## Must Fix
1. **The new outer-loop scripts' required accompanying set is never checked** — refers to "Structure" (missed check). Offending file: the index, `harness-runs/code_reviews/feat_script_driven_planning_pilot_code_review.md` (`## Context`).
   The diff adds three shipped outer-loop scripts: `cli/src/generators/outerLoopScripts.ts` (`OUTER_LOOP_SCRIPTS`) — "Object.freeze({ file: 'planning-node-lib.sh', subdir: 'lib'", plus `planning-record-lib.sh` and `planning-driver-lib.sh`. `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, row *An outer-loop script*, sets out what has to land with each one: (a) its row in the shipped table with `agentInvocable` set deliberately, (b) the permission-profile entries that flag implies, and (c) a deny-list entry in `plugin/hooks/autonomous-script-allowlist-guard.sh` → `DENY_SCRIPT_BASENAMES` where the script must not be agent-runnable. The index's Context only says the diff "covers" Task 4's `OUTER_LOOP_SCRIPTS` rows. It never says that any of the three members was checked, and no finding covers them. The rows' own comment says no `DENY_SCRIPT_BASENAMES` entry is owed. Nothing in the review shows that this claim was checked, or that the permission profile needs no entry for `agentInvocable: false` library rows.
   **Fix:** In the index's `## Context`, add a clean-pass sentence for each of the three members (a), (b) and (c), for all three libraries. Each sentence must name what was checked: the row and its `agentInvocable: false`, the permission-profile generator's treatment of `agentInvocable: false` rows, and why `DENY_SCRIPT_BASENAMES` owes no entry. If a member does not hold, add a new `finding_<N>.md` for it, with its index pointer and its readiness entry.

2. **The bounded-retry lesson is exhibited by the diff but neither covered nor cleared** — refers to "Structure" (missed check). Offending file: the index, `harness-runs/code_reviews/feat_script_driven_planning_pilot_code_review.md` (`## Context`).
   `harness-runs/lessons.md` → `## Unattended control loops` carries this rule: *"Every automatic retry in an unattended path is bounded by a count or a deadline. When the bound is reached, send exactly one notification naming the error and the manual way on, then stop retrying."* The diff adds exactly such a retry: `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_undelivered`) — "PD_STRIKES=$((PD_STRIKES + 1))". It re-dispatches undelivered node sessions, backs off on the second strike and self-pauses through `prl_pause` on the third. The review's Context lists "undelivered sessions" only as a test case that has a suite. No finding and no clean-pass rationale grades the retry against the lesson, so nothing shows that the bound holds. Nothing shows either that reaching it produces exactly one notification naming the error and the manual way on: `prl_pause` (`cli/templates/scripts/lib/planning-record-lib.sh`) writes `PAUSE_PROGRESS.md` and `PAUSE_ACK` and sends no notification itself.
   **Fix:** In the index's `## Context`, add a clean-pass rationale for the lesson. It must state the bound (three consecutive undelivered sets, with a backoff capped at 60s) and name the path by which the pause reaches the operator as one notification. If no such notification fires, add a new `finding_<N>.md` anchored at `pd_undelivered`, with its index pointer and its readiness entry.

## Should Fix

_None._

## Nice to Have

_None._
