# Branch statistics: feat_structured_planning_agent_outputs

## Summary

- `success_rate`: **`95.7%`** — headline metric.
- `story_points_total`: `230` — denominator (sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`).
- `issue_cost_total`: `10` — subtraction (sum of each user-review observation's severity weight, in story-point units).
- `story_plan_tasks`: `15` — retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `2` — retained raw count of observations across all `feat_structured_planning_agent_outputs_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((230 - 10) / 230, 0, 1) * 100, 1)` = `round(95.6521…, 1)` = `95.7%`.

Edge cases (the rate is always computed via the formula, then adjusted by these rules):

- **No issues** — when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`.
- **Clamped at zero** — when `issue_cost_total > story_points_total` (weighted defect load exceeds the planned story points), the raw value goes negative; the rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`.
- **No points** — when `story_points_total` is `0` the rate is recorded as `n/a` (cannot divide by zero). This is only reachable when the story index has **zero** task entries; a story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)** — when the story index has task entries but **none** carry a `_(points: …)_` tag (an older branch predating story points), `story_points_total` falls back to `story_plan_tasks` (the legacy task-count denominator) and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are retained so the metric can be refined later without re-deriving them.

- **Story-index source** — `story_points_total`: `230`, `story_plan_tasks`: `15`
  - counted from `harness-runs/story_plans/feat_structured_planning_agent_outputs_story_plan.md` (the `N. [ ] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike; all 15 are `[x]`).
  - per-task points (`_(points: <N>)_` tag on each entry), summed:
    - Task 1: `15`
    - Task 2: `15`
    - Task 3: `15`
    - Task 4: `15`
    - Task 5: `20`
    - Task 6: `15`
    - Task 7: `10`
    - Task 8: `15`
    - Task 9: `15`
    - Task 10: `20`
    - Task 11: `20`
    - Task 12: `10`
    - Task 13: `20`
    - Task 14: `15`
    - Task 15: `10`
    - **sum (`story_points_total`)**: `230`
  - `dispositioned_points`: `0` — one commit in `dev..HEAD` (read as `origin/dev..HEAD`; no local `dev` ref exists in this checkout) carries the `record disposition of ` record: `Finding 1` at `c281609a` (a user-review fix-round unit, not a `**Task K**` entry of this story index) — listed as unpointed and summed nowhere. No story-index task was closed without a fix.
  - Back-compat fallback did not fire: every entry carries a `_(points: …)_` tag.
- **User-review source** — `user_review_issues`: `2`, `issue_cost_total`: `10` (per user-review file, then summed)
  - `harness-runs/user_reviews/feat_structured_planning_agent_outputs_review.md`: `2` observations → cost `10`. Counted by **arm 2, top-level list items** — `grep -cE '^[0-9]+\.|^[-*][[:space:]]' <file>` → `2`, arm 1 (`grep -cE '^#{2,4} +[0-9]+[.):]' <file>`) having returned `0`; the indented sub-items under each observation are not counted. Each observation's assigned weight beside it:
    1. move each planning agent's return JSON schema out of its definition into a separate plugin file, keeping a trimmed `### Return fields` list in the agent → **Minor** `5`
    2. optimise the tokens agents spend reading prose (thin the orchestrator's runtime module, move authoring rules to a maintainer document, make touched files more instruction-like) → **Minor** `5`
  - **total**: `2` observations → `issue_cost_total` `10`
  - Each file's observation count is the count of whatever top-level enumeration that file uses, taken from the first of four arms to return non-zero and never summed across arms: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'` — here `0`; (2) top-level numbered/bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'` — here `2`, so arm 2 is this file's count; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, reserved for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted, including any a later fix plan verifies as OK — the count measures what the user found, not what survived triage.
  - Each observation is weighted in story-point units: **Major** `15` (explicit `[major]` marker, or the observation describes a broken/incorrect user-facing flow, a missing/client-only authorization gate, data loss/corruption/unprotected data, or an absent whole ported behaviour — the deciding phrase is quoted beside the observation), **Trivial** `2` (explicit `[trivial]` marker), **Minor** `5` (the default for every observation without a Major/Trivial classification).

**Why both observations took the Minor default.** Neither carries an explicit `[major]` or `[trivial]` marker, and neither, read from the review text alone, describes a Major condition — both are refactor and token-budget requests (relocating a schema, trimming prose), not a broken flow, an authorization gap, data loss or an absent behaviour.

## Status

- status: `post-user-review` — `pre-user-review` means this file was written right after the branch (code) review with no user review yet (`issue_cost_total` `0` → `100%`); `post-user-review` means it was re-written after user-review fixes, with the issues from the `feat_structured_planning_agent_outputs_review*.md` files counted and weighted.
- last_updated: `2026-11-16`

## Notes

This is a deliberately basic but points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`: the denominator is the sum of the story-plan tasks' story-point complexity estimates (the scope the agent committed to, weighted by effort rather than raw task count), and the subtraction is the severity-weighted cost of user-review observations (defects found after the workflow finished, each costing Minor `5` by default, Major `15` on an explicit marker or a documented broken-flow / security / data-integrity / missing-behaviour classification — with the deciding phrase quoted in the breakdown — and Trivial `2` only on an explicit marker). The retained raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` let the metric be refined later without losing the raw data. A unit closed via the unit loop's dispositioned outcome keeps its points in the denominator, so the rate counts them as delivered.

`0` story points closed without a fix (`Finding 1`, unpointed, `c281609a`) — the rate counts them as delivered.
