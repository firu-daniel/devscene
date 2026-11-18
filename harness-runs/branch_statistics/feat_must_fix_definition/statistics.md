# Branch statistics: feat_must_fix_definition

## Summary

- `success_rate`: **`90.7%`** — headline metric.
- `story_points_total`: `216` — denominator (sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`).
- `issue_cost_total`: `20` — subtraction (sum of each user-review observation's severity weight, in story-point units).
- `story_plan_tasks`: `15` — retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `4` — retained raw count of observations across all `feat_must_fix_definition_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((216 - 20) / 216, 0, 1) * 100, 1)` = `round(90.7407…, 1)` = `90.7%`.

Edge cases (the rate is always computed via the formula, then adjusted by these rules):

- **No issues** — when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`.
- **Clamped at zero** — when `issue_cost_total > story_points_total` (weighted defect load exceeds the planned story points), the raw value goes negative; the rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`.
- **No points** — when `story_points_total` is `0` the rate is recorded as `n/a` (cannot divide by zero). This is only reachable when the story index has **zero** task entries; a story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)** — when the story index has task entries but **none** carry a `_(points: …)_` tag (an older branch predating story points), `story_points_total` falls back to `story_plan_tasks` (the legacy task-count denominator) and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are retained so the metric can be refined later without re-deriving them.

- **Story-index source** — `story_points_total`: `216`, `story_plan_tasks`: `15`
  - counted from `harness-runs/story_plans/feat_must_fix_definition_story_plan.md` (the `N. [ ] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike; all `15` are `[x]` here).
  - per-task points (`_(points: <N>)_` tag on each entry), summed:
    - Task 1: `20`
    - Task 2: `20`
    - Task 3: `10`
    - Task 4: `15`
    - Task 5: `20`
    - Task 6: `15`
    - Task 7: `20`
    - Task 8: `20`
    - Task 9: `15`
    - Task 10: `15`
    - Task 11: `10`
    - Task 12: `15`
    - Task 13: `8`
    - Task 14: `5`
    - Task 15: `8`
    - **sum (`story_points_total`)**: `216`
  - `dispositioned_points`: `0` — no commit in `origin/dev..HEAD` carries the `record disposition of ` record, so no task here was closed without a fix and no unit token or short SHA is listed. The configured default branch `dev` has no local ref in this checkout, so the range was read from its remote-tracking ref `origin/dev`.
  - (Back-compat: the fallback did not fire; all `15` entries carry a `_(points: …)_` tag.)
- **User-review source** — `user_review_issues`: `4`, `issue_cost_total`: `20` (per user-review file, then summed)
  - The glob `harness-runs/user_reviews/feat_must_fix_definition_review*.md` matches one file. `feat_must_fix_definition_fix_plan.md` and the `feat_must_fix_definition_fix_plan` directory are not review files and are not counted.
  - `harness-runs/user_reviews/feat_must_fix_definition_review.md`: `4` observations → cost `20`. Counted by **arm 2, top-level list items** — `grep -cE '^[0-9]+\.|^[-*][[:space:]]' <file>` → `4`, arm 1 (`grep -cE '^#{2,4} +[0-9]+[.):]' <file>`) having returned `0`. Each observation's assigned weight beside it:
    1. a check an agent grades Must Fix is covered by no row of that agent's table → **Minor** `5`
    2. a table row names a class outside the four in `plugin/instructions/finding_grades.md` → **Minor** `5`
    3. a table row names a check group or section heading no longer in that agent's file → **Minor** `5`
    4. an agent citing `finding_grades.md` and grading checklist triggers Must Fix has no table → **Minor** `5`
  - **total**: `4` observations → `issue_cost_total` `20`
  - Each file's observation count is the count of whatever top-level enumeration that file uses, taken from the first of four arms to return non-zero and never summed across arms: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'` — here `0`; (2) top-level numbered/bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'` — here `4`, so arm 2 is this file's count; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, reserved for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted, including any a later fix plan verifies as OK — the count measures what the user found, not what survived triage.
  - Each observation is weighted in story-point units: **Major** `15` (explicit `[major]` marker, or the observation describes a broken/incorrect user-facing flow, a missing/client-only authorization gate, data loss/corruption/unprotected data, or an absent whole ported behaviour — the deciding phrase is quoted beside the observation), **Trivial** `2` (explicit `[trivial]` marker), **Minor** `5` (the default for every observation without a Major/Trivial classification).

**Why all four here took the Minor default.** The weight is assigned from the observation as the reviewer wrote it: none of the four carries an explicit `[major]` or `[trivial]` marker, and none describes a Major condition — no end-to-end broken user-facing flow, no missing or client-only authorization gate, no data loss, corruption or unprotected data, and no whole ported behaviour absent. Each states a condition a requested corpus test must detect.

## Status

- status: `post-user-review` — `pre-user-review` means this file was written right after the branch (code) review with no user review yet (`issue_cost_total` `0` → `100%`); `post-user-review` means it was re-written after user-review fixes, with the issues from the `feat_must_fix_definition_review*.md` files counted and weighted.
- last_updated: `2026-11-18`

## Notes

This is a deliberately basic but points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`: the denominator is the sum of the story-plan tasks' story-point complexity estimates (the scope the agent committed to, weighted by effort rather than raw task count), and the subtraction is the severity-weighted cost of user-review observations (defects found after the workflow finished, each costing Minor `5` by default, Major `15` on an explicit marker or a documented broken-flow / security / data-integrity / missing-behaviour classification — with the deciding phrase quoted in the breakdown — and Trivial `2` only on an explicit marker). The retained raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` let the metric be refined later (e.g., richer per-issue severity triage) without losing the raw data. A unit closed via the unit loop's dispositioned outcome keeps its points in the denominator, so the rate counts them as delivered; no unit on this branch was closed that way.

The review file is written as one request, for a corpus test, and its only top-level enumeration is the list of four conditions that test must fail on. The counting rule takes those four items as the file's observations, so `user_review_issues` is `4` and the cost is `20`; the items are requirements of that one request rather than four separately reported defects. Counted as a single Minor observation, the cost would be `5` and the rate `97.7%`.
