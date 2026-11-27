# Branch statistics: feat_planning_driver_python_cutover

## Summary

- `success_rate`: **`88.6%`** — headline metric.
- `story_points_total`: `394` — denominator (sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`).
- `issue_cost_total`: `45` — subtraction (sum of each user-review observation's severity weight, in story-point units).
- `story_plan_tasks`: `25` — retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `5` — retained raw count of observations across all `feat_planning_driver_python_cutover_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((394 - 45) / 394, 0, 1) * 100, 1)` = `round(88.5786…, 1)` = `88.6%`.

Edge cases (the rate is always computed via the formula, then adjusted by these rules):

- **No issues** — when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`.
- **Clamped at zero** — when `issue_cost_total > story_points_total` (weighted defect load exceeds the planned story points), the raw value goes negative; the rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`.
- **No points** — when `story_points_total` is `0` the rate is recorded as `n/a` (cannot divide by zero). This is only reachable when the story index has **zero** task entries; a story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)** — when the story index has task entries but **none** carry a `_(points: …)_` tag (an older branch predating story points), `story_points_total` falls back to `story_plan_tasks` (the legacy task-count denominator) and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are retained so the metric can be refined later without re-deriving them.

- **Story-index source** — `story_points_total`: `394`, `story_plan_tasks`: `25`
  - counted from `harness-runs/story_plans/feat_planning_driver_python_cutover_story_plan.md` (the `N. [x] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike; all 25 are `[x]`). Section-scoped `awk` piped to `grep -cE '^[0-9]+\.\s*\[[ x]\]\s*\*\*Task'` → `25`; the points extraction summed → `394`.
  - per-task points (`_(points: <N>)_` tag on each entry), summed:
    - Task 1: `15`
    - Task 2: `20`
    - Task 3: `10`
    - Task 4: `15`
    - Task 5: `20`
    - Task 6: `8`
    - Task 7: `8`
    - Task 8: `5`
    - Task 9: `20`
    - Task 10: `20`
    - Task 11: `15`
    - Task 12: `10`
    - Task 13: `20`
    - Task 14: `20`
    - Task 15: `20`
    - Task 16: `20`
    - Task 17: `20`
    - Task 18: `20`
    - Task 19: `20`
    - Task 20: `20`
    - Task 21: `8`
    - Task 22: `10`
    - Task 23: `15`
    - Task 24: `20`
    - Task 25: `15`
    - **sum (`story_points_total`)**: `394`
  - `dispositioned_points`: `0` — no commit in `origin/dev..HEAD` (`git log --format='%h %s%n%b' origin/dev..HEAD`) carries the `record disposition of ` record (case-insensitive `grep -ci` → `0`), so no unit was closed without a fix and no tokens are listed.
  - (Back-compat: every entry carries a `_(points: …)_` tag, so the fallback did not fire; had it, `story_points_total` would have been `story_plan_tasks` = `25`.)
- **User-review source** — `user_review_issues`: `5`, `issue_cost_total`: `45` (per user-review file, then summed)
  - `harness-runs/user_reviews/feat_planning_driver_python_cutover_review.md` (the only file matched by `feat_planning_driver_python_cutover_review*.md`; no `_fix_plan` match to drop): `5` observations → cost `45`. Counted by **arm 2, top-level list items** — `grep -cE '^[0-9]+\.|^[-*][[:space:]]' <file>` → `5`, arm 1 (`grep -cE '^#{2,4} +[0-9]+[.):]' <file>`) having returned `0`. Each observation's assigned weight beside it:
    1. node output no longer reaches the run log while a session runs; the Python driver writes the stream and formatted log only at session end → **Major** `15` — a whole ported behaviour absent: "Node output no longer reaches the run log while a session runs. The bash pilot teed each node's stream … into the run log as it arrived"
    2. the pilot's `flow-efficiency` observation and `[plan-drive]` narration line for an undelivered re-dispatch are no longer produced → **Major** `15` — a whole ported behaviour absent: "The pilot's observation for an undelivered re-dispatch was dropped"
    3. drop the two `treeGuards` entries for `tests/test_driver_return_fields.py` from `devscene.config.json` → **Minor** `5`
    4. restore a test-only backoff override like the pilot's `PD_BACKOFF_SECS` so end-to-end suites stop sleeping → **Minor** `5`
    5. assert end to end that a refused or missing round file does not log the "no usage record" line → **Minor** `5`
  - **total**: `5` observations → `issue_cost_total` `45`
  - Each file's observation count is the count of whatever top-level enumeration that file uses, taken from the first of four arms to return non-zero and never summed across arms: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'` — here `0`; (2) top-level numbered/bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'` — here `5`, so arm 2 is this file's count; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, reserved for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted, including any a later fix plan verifies as OK — the count measures what the user found, not what survived triage.
  - Each observation is weighted in story-point units: **Major** `15` (explicit `[major]` marker, or the observation describes a broken/incorrect user-facing flow, a missing/client-only authorization gate, data loss/corruption/unprotected data, or an absent whole ported behaviour — the deciding phrase is quoted beside the observation), **Trivial** `2` (explicit `[trivial]` marker), **Minor** `5` (the default for every observation without a Major/Trivial classification).

**Why two took Major and three the Minor default.** No observation carries an explicit `[major]` or `[trivial]` marker. Observations 1 and 2 each describe, in the review text itself, a behaviour the bash pilot had and the Python port does not: live per-node output in the run log, and the undelivered re-dispatch observation with its narration line. That is the "whole ported behaviour absent" condition. Observation 4 also restores a pilot knob, but it is a test-only override that affects suite run time and not the driver's behaviour, so it stays Minor. Observations 3 and 5 are configuration hygiene and a missing test assertion.

## Status

- status: `post-user-review` — `pre-user-review` means this file was written right after the branch (code) review with no user review yet (`issue_cost_total` `0` → `100%`); `post-user-review` means it was re-written after user-review fixes, with the issues from the `feat_planning_driver_python_cutover_review*.md` files counted and weighted.
- last_updated: `2026-11-27`

## Notes

This is a deliberately basic but points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`: the denominator is the sum of the story-plan tasks' story-point complexity estimates (the scope the agent committed to, weighted by effort rather than raw task count), and the subtraction is the severity-weighted cost of user-review observations (defects found after the workflow finished, each costing Minor `5` by default, Major `15` on an explicit marker or a documented broken-flow / security / data-integrity / missing-behaviour classification — with the deciding phrase quoted in the breakdown — and Trivial `2` only on an explicit marker). The retained raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` let the metric be refined later (e.g., richer per-issue severity triage) without losing the raw data. A unit closed via the unit loop's dispositioned outcome keeps its points in the denominator; on this branch no commit records a disposition, so `dispositioned_points` is `0`.
