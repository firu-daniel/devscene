# Branch statistics: feat_script_driven_planning_pilot

## Summary

- `success_rate`: **`76.5%`** — headline metric.
- `story_points_total`: `170` — denominator (sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`).
- `issue_cost_total`: `40` — subtraction (sum of each user-review observation's severity weight, in story-point units).
- `story_plan_tasks`: `10` — retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `4` — retained raw count of observations across all `feat_script_driven_planning_pilot_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((170 - 40) / 170, 0, 1) * 100, 1)` = `round(76.4705…, 1)` = `76.5%`.

Edge cases (the rate is always computed via the formula, then adjusted by these rules):

- **No issues** — when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`.
- **Clamped at zero** — when `issue_cost_total > story_points_total` (weighted defect load exceeds the planned story points), the raw value goes negative; the rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`.
- **No points** — when `story_points_total` is `0` the rate is recorded as `n/a` (cannot divide by zero). This is only reachable when the story index has **zero** task entries; a story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)** — when the story index has task entries but **none** carry a `_(points: …)_` tag (an older branch predating story points), `story_points_total` falls back to `story_plan_tasks` (the legacy task-count denominator) and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are retained so the metric can be refined later without re-deriving them.

- **Story-index source** — `story_points_total`: `170`, `story_plan_tasks`: `10`
  - counted from `harness-runs/story_plans/feat_script_driven_planning_pilot_story_plan.md` (the `N. [x] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike; all ten are `[x]`).
  - per-task points (`_(points: <N>)_` tag on each entry), summed:
    - Task 10: `15`
    - Task 1: `20`
    - Task 2: `20`
    - Task 3: `20`
    - Task 4: `15`
    - Task 5: `20`
    - Task 6: `20`
    - Task 7: `15`
    - Task 8: `15`
    - Task 9: `10`
    - **sum (`story_points_total`)**: `170`
  - `dispositioned_points`: `0` — no commit in `dev..HEAD` (evaluated as `origin/dev..HEAD`, the only `dev` ref present in this checkout) carries the `record disposition of ` record, so no task here was closed without a fix, and no unpointed token was matched.
  - (Back-compat: every entry carries a `_(points: …)_` tag, so the task-count fallback did not fire.)
- **User-review source** — `user_review_issues`: `4`, `issue_cost_total`: `40` (per user-review file, then summed)
  - `harness-runs/user_reviews/feat_script_driven_planning_pilot_review.md`: `4` observations → cost `40`. Counted by **arm 2, top-level list items** — `grep -cE '^[0-9]+\.|^[-*][[:space:]]' <file>` → `4`, arm 1 (`grep -cE '^#{2,4} +[0-9]+[.):]' <file>`) having returned `0`. The indented `   -` sub-bullets under observations 2 and 3 are not counted. Each observation's assigned weight beside it:
    1. script-driven planning must also run on remote (GitHub Actions) jobs; replace the watcher tunable with a config key → **Minor** `5`
    2. run analytics double-counts time when node sessions overlap → **Major** `15` — deciding phrase: "Run analytics double-counts time when node sessions overlap … so three 10-minute gates add 30 minutes of \"wall\" time" (a user-facing report that works incorrectly end-to-end)
    3. a node that fails for an infrastructure reason must be retried, not parked at once → **Major** `15` — deciding phrase: "parks planning on the first occurrence, where the orchestrated path's `Agent` tool would often have recovered" (a whole behaviour of the orchestrated path, infrastructure-failure recovery, absent from the scripted port)
    4. verify, and cover with a test, what a resume after an escalation park re-runs → **Minor** `5`
  - **total**: `4` observations → `issue_cost_total` `40`
  - Each file's observation count is the count of whatever top-level enumeration that file uses, taken from the first of four arms to return non-zero and never summed across arms: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'` — here `0`; (2) top-level numbered/bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'` — here `4`, so arm 2 is this file's count; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, reserved for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted, including any a later fix plan verifies as OK — the count measures what the user found, not what survived triage.
  - Each observation is weighted in story-point units: **Major** `15` (explicit `[major]` marker, or the observation describes a broken/incorrect user-facing flow, a missing/client-only authorization gate, data loss/corruption/unprotected data, or an absent whole ported behaviour — the deciding phrase is quoted beside the observation), **Trivial** `2` (explicit `[trivial]` marker), **Minor** `5` (the default for every observation without a Major/Trivial classification).

**Why observations 1 and 4 took the Minor default.** No observation carries an explicit `[major]` or `[trivial]` marker. Observation 1 asks to extend the pilot to a further execution mode (remote jobs). It is a scope and configuration choice, not a flow that breaks. Observation 4 asks to establish and test existing resume behaviour, and describes no defect. Neither describes a Major condition as written.

## Status

- status: `post-user-review` — `pre-user-review` means this file was written right after the branch (code) review with no user review yet (`issue_cost_total` `0` → `100%`); `post-user-review` means it was re-written after user-review fixes, with the issues from the `feat_script_driven_planning_pilot_review*.md` files counted and weighted.
- last_updated: `2026-11-15`

## Notes

This is a deliberately basic but points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`. The denominator is the sum of the story-plan tasks' story-point complexity estimates: the scope the agent committed to, weighted by effort rather than raw task count. The subtraction is the severity-weighted cost of user-review observations, meaning defects found after the workflow finished. Each costs Minor `5` by default. Major `15` applies on an explicit marker or a documented broken-flow / security / data-integrity / missing-behaviour classification, with the deciding phrase quoted in the breakdown. Trivial `2` applies only on an explicit marker. The retained raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` let the metric be refined later (e.g., richer per-issue severity triage) without losing the raw data. No unit on this branch was closed via the dispositioned outcome (`dispositioned_points` `0`, no matched tokens).
