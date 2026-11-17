# Branch statistics: feat_review_sweep_in_conventions

## Summary

- `success_rate`: **`100%`**, the headline metric.
- `story_points_total`: `170`, the denominator: the sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`.
- `issue_cost_total`: `0`, the subtraction: the sum of each user-review observation's severity weight, in story-point units.
- `story_plan_tasks`: `10`, the retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `0`, the retained raw count of observations across all `feat_review_sweep_in_conventions_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((170 - 0) / 170, 0, 1) * 100, 1)` = `100%`.

Edge cases (the rate is always computed with the formula, then adjusted by these rules):

- **No issues**: when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`. This rule applies here.
- **Clamped at zero**: when `issue_cost_total > story_points_total` (the weighted defect load exceeds the planned story points), the raw value goes negative. The rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`.
- **No points**: when `story_points_total` is `0` the rate is recorded as `n/a` (it cannot divide by zero). Only a story index with **zero** task entries reaches this rule. A story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)**: when the story index has task entries but **none** carry a `_(points: …)_` tag, `story_points_total` falls back to `story_plan_tasks` and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are kept so the metric can be refined later without re-deriving them.

- **Story-index source**: `story_points_total`: `170`, `story_plan_tasks`: `10`
  - Counted from `harness-runs/story_plans/feat_review_sweep_in_conventions_story_plan.md`. These are the `N. [x] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike, scoped to that section with `awk '/## Phase 2 Readiness — Ordered Fix List/{f=1;next} /^## /{f=0} f'` and matched with `grep -cE '^[0-9]+\.\s*\[[ x]\]\s*\*\*Task'`, which returns `10`.
  - Per-task points (the `_(points: <N>)_` tag on each entry), summed:
    - Task 1: `20`
    - Task 2: `20`
    - Task 3: `15`
    - Task 4: `15`
    - Task 5: `15`
    - Task 6: `15`
    - Task 7: `20`
    - Task 8: `20`
    - Task 9: `10`
    - Task 10: `20`
    - **sum (`story_points_total`)**: `170`
  - `dispositioned_points`: `0`. No commit in `dev..HEAD` carries the `record disposition of ` record, so no unit was closed without a fix. The range was read as `git log --format='%h %s%n%b' origin/dev..HEAD` because no local `dev` ref exists in this checkout and `dev..HEAD` did not resolve.
  - Every entry carries a `_(points: …)_` tag, so the back-compat fallback did not fire.
- **User-review source**: `user_review_issues`: `0`, `issue_cost_total`: `0`
  - The glob `harness-runs/user_reviews/feat_review_sweep_in_conventions_review*.md` matches no file, which is expected for a pre-user-review write. No files means no observations to count or weight.
  - **total**: `0` observations, so `issue_cost_total` is `0`.
  - Each file's observation count comes from whatever top-level enumeration that file uses. The count is taken from the first of four arms to return non-zero, and arms are never summed: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'`; (2) top-level numbered or bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'`; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, kept for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted.
  - Each observation is weighted in story-point units:
    - **Major** `15`: an explicit `[major]` marker, or an observation that describes a broken or incorrect user-facing flow, a missing or client-only authorization gate, data loss, corruption or unprotected data, or a whole ported behaviour that is absent. The deciding phrase is quoted beside the observation.
    - **Trivial** `2`: an explicit `[trivial]` marker.
    - **Minor** `5`: the default for every observation without a Major or Trivial classification.

## Status

- status: `pre-user-review`. This file was written right after the branch (code) review, before any user review, so `issue_cost_total` is `0` and the rate is `100%`. `post-user-review` would mean the file was rewritten after user-review fixes, with the issues from the `feat_review_sweep_in_conventions_review*.md` files counted and weighted.
- last_updated: `2026-11-18`

## Notes

This is a deliberately basic, points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`.

- The denominator is the sum of the story-plan tasks' story-point estimates. It measures the scope the agent committed to, weighted by effort rather than raw task count.
- The subtraction is the severity-weighted cost of user-review observations, meaning defects found after the workflow finished. Each one costs Minor `5` by default. It costs Major `15` on an explicit marker or a documented broken-flow, security, data-integrity or missing-behaviour classification, with the deciding phrase quoted in the breakdown. It costs Trivial `2` only on an explicit marker.

The raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` are kept so the metric can be refined later without losing the raw data. No unit on this branch was closed via the dispositioned outcome (`dispositioned_points` is `0`, with no matched tokens).
