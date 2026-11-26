# Branch statistics: feat_flow_host_claude_executor

## Summary

- `success_rate`: **`70.6%`** — headline metric.
- `story_points_total`: `85` — denominator (sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`).
- `issue_cost_total`: `25` — subtraction (sum of each user-review observation's severity weight, in story-point units).
- `story_plan_tasks`: `5` — retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `3` — retained raw count of observations across all `feat_flow_host_claude_executor_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((85 - 25) / 85, 0, 1) * 100, 1)` = `round(70.5882…, 1)` = `70.6%`.

Edge cases (the rate is always computed via the formula, then adjusted by these rules):

- **No issues** — when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`.
- **Clamped at zero** — when `issue_cost_total > story_points_total` (weighted defect load exceeds the planned story points), the raw value goes negative; the rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`.
- **No points** — when `story_points_total` is `0` the rate is recorded as `n/a` (cannot divide by zero). This is only reachable when the story index has **zero** task entries; a story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)** — when the story index has task entries but **none** carry a `_(points: …)_` tag (an older branch predating story points), `story_points_total` falls back to `story_plan_tasks` (the legacy task-count denominator) and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are retained so the metric can be refined later without re-deriving them.

- **Story-index source** — `story_points_total`: `85`, `story_plan_tasks`: `5`
  - counted from `harness-runs/story_plans/feat_flow_host_claude_executor_story_plan.md` (the `N. [x] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike; all five are `[x]`). Task count by the section-scoped `awk … | grep -cE '^[0-9]+\.\s*\[[ x]\]\s*\*\*Task'` → `5`; points by the section-scoped `awk … | grep -oE '_\(points: *[0-9]+\)_' | grep -oE '[0-9]+' | awk '{s+=$1} END{print s+0}'` → `85`.
  - per-task points (`_(points: <N>)_` tag on each entry), summed:
    - Task 1: `15`
    - Task 2: `20`
    - Task 3: `20`
    - Task 4: `20`
    - Task 5: `10`
    - **sum (`story_points_total`)**: `85`
  - `dispositioned_points`: `0` — no commit in `origin/dev..HEAD` (`git log --format='%h %s%n%b' origin/dev..HEAD`, 45 commits) carries the `record disposition of ` record, so no unit here was closed without a fix; no unit tokens matched.
  - The back-compat fallback did not fire: every entry carries a `_(points: …)_` tag.
- **User-review source** — `user_review_issues`: `3`, `issue_cost_total`: `25` (per user-review file, then summed)
  - The glob `harness-runs/user_reviews/feat_flow_host_claude_executor_review*.md` matches one file; no match contains `_fix_plan`, so none was dropped.
  - `harness-runs/user_reviews/feat_flow_host_claude_executor_review.md`: `3` observations → cost `25`. Counted by **arm 2, top-level list items** — `grep -cE '^[0-9]+\.|^[-*][[:space:]]' <file>` → `3`, arm 1 (`grep -cE '^#{2,4} +[0-9]+[.):]' <file>`) having returned `0`. The indented continuation paragraphs and the two indented `-` sub-items under observation 3 are not counted. Each observation's assigned weight beside it:
    1. `ClaudeExecutor.run` passes `dispatch.prompt` (the prompt variant) to `claude -p` as prompt text → **Major** `15` — deciding phrase: *"`run` would raise `ValueError("… carries no prompt")` for every reviewer, and the writers would be launched with `-p initial`"*. This is the executor's core flow working incorrectly end-to-end for every node of the planning graph.
    2. docstrings and README defer work to issue numbers instead of describing it → **Minor** `5`
    3. two unapplied Should Fix items from the round-0 task-plan review (timeout `Launch` row without a usage record; `--add-dir <plugin_dir>` not named) → **Minor** `5`
  - **total**: `3` observations → `issue_cost_total` `25`
  - Each file's observation count is the count of whatever top-level enumeration that file uses, taken from the first of four arms to return non-zero and never summed across arms: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'` — here `0`; (2) top-level numbered/bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'` — here `3`, so arm 2 is this file's count; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, reserved for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted, including any a later fix plan verifies as OK — the count measures what the user found, not what survived triage.
  - Each observation is weighted in story-point units: **Major** `15` (explicit `[major]` marker, or the observation describes a broken/incorrect user-facing flow, a missing/client-only authorization gate, data loss/corruption/unprotected data, or an absent whole ported behaviour — the deciding phrase is quoted beside the observation), **Trivial** `2` (explicit `[trivial]` marker), **Minor** `5` (the default for every observation without a Major/Trivial classification).

## Status

- status: `post-user-review` — `pre-user-review` means this file was written right after the branch (code) review with no user review yet (`issue_cost_total` `0` → `100%`); `post-user-review` means it was re-written after user-review fixes, with the issues from the `feat_flow_host_claude_executor_review*.md` files counted and weighted.
- last_updated: `2026-11-26`

## Notes

This is a deliberately basic but points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`: the denominator is the sum of the story-plan tasks' story-point complexity estimates (the scope the agent committed to, weighted by effort rather than raw task count), and the subtraction is the severity-weighted cost of user-review observations (defects found after the workflow finished, each costing Minor `5` by default, Major `15` on an explicit marker or a documented broken-flow / security / data-integrity / missing-behaviour classification — with the deciding phrase quoted in the breakdown — and Trivial `2` only on an explicit marker). The retained raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` let the metric be refined later (e.g., richer per-issue severity triage) without losing the raw data. No unit on this branch was closed via the dispositioned outcome, so no story points are counted as delivered without a fix.

The base used for the commit range is `origin/dev` (`devscene.config.json` → `defaultBranch`).
