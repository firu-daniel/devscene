# Branch statistics: fix_injection_verdict_tools_used_prefix

## Summary

- `success_rate`: **`0%`** — headline metric.
- `story_points_total`: `35` — denominator (sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`).
- `issue_cost_total`: `50` — subtraction (sum of each user-review observation's severity weight, in story-point units).
- `story_plan_tasks`: `4` — retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `4` — retained raw count of observations across all `fix_injection_verdict_tools_used_prefix_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((35 - 50) / 35, 0, 1) * 100, 1)` = `round(clamp(-0.4285…, 0, 1) * 100, 1)` = `0%`.

Edge cases (the rate is always computed via the formula, then adjusted by these rules):

- **No issues** — when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`.
- **Clamped at zero** — when `issue_cost_total > story_points_total` (weighted defect load exceeds the planned story points), the raw value goes negative; the rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`. This rule applies here: `50 > 35`.
- **No points** — when `story_points_total` is `0` the rate is recorded as `n/a` (cannot divide by zero). This is only reachable when the story index has **zero** task entries; a story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)** — when the story index has task entries but **none** carry a `_(points: …)_` tag (an older branch predating story points), `story_points_total` falls back to `story_plan_tasks` (the legacy task-count denominator) and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are retained so the metric can be refined later without re-deriving them.

- **Story-index source** — `story_points_total`: `35`, `story_plan_tasks`: `4`
  - counted from `harness-runs/story_plans/fix_injection_verdict_tools_used_prefix_story_plan.md` (the `N. [x] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike).
  - per-task points (`_(points: <N>)_` tag on each entry), summed:
    - Task 1: `15`
    - Task 2: `5`
    - Task 3: `5`
    - Task 4: `10`
    - **sum (`story_points_total`)**: `35`
  - `dispositioned_points`: `0` — no commit in `origin/dev..HEAD` carries the `record disposition of ` record, so no task here was closed without a fix, and no unit token or short SHA is listed. The configured default branch `dev` has no local ref in this checkout, so the range was read against its remote-tracking ref `origin/dev` (see `## Notes`).
  - Back-compat: the fallback did not fire; all `4` entries carry a `_(points: …)_` tag.
- **User-review source** — `user_review_issues`: `4`, `issue_cost_total`: `50` (per user-review file, then summed)
  - `harness-runs/user_reviews/fix_injection_verdict_tools_used_prefix_review.md`: `4` observations → cost `50`. Counted by **arm 2, top-level list items** — `grep -cE '^[0-9]+\.|^[-*][[:space:]]' <file>` → `4`, arm 1 (`grep -cE '^#{2,4} +[0-9]+[.):]' <file>`) having returned `0`. No other file matched the glob, and none was dropped for `_fix_plan`. Each observation's assigned weight beside it:
    1. the harness notice ahead of the frame makes `verdict` refuse the result → **Major** `15` — deciding phrase: "so a real `UNSAFE` verdict parks as `malformed-verdict` and its findings are lost" (the verdict flow works incorrectly end-to-end and loses the findings).
    2. the same notice delivered inside the frame as the first indented reply line → **Major** `15` — deciding phrase: "`verdict` also parks that shape as `malformed-verdict`" (a second placement on which the verdict flow fails end-to-end, observed in a live run).
    3. a neutralized control tag (`<\system-reminder>`) in an `UNSAFE` excerpt makes invalid JSON → **Major** `15` — deciding phrase: "`verdict` parks it as `malformed-verdict` even with no notice; an excerpt quoting a control tag must keep its findings too" (the verdict flow fails and the findings are lost).
    4. keep the fix fail-closed and update the tests, docs, contract and adopted copy that pin the old behaviour → **Minor** `5` (default: a constraint and update list, not a broken flow).
  - **total**: `4` observations → `issue_cost_total` `50`
  - Each file's observation count is the count of whatever top-level enumeration that file uses, taken from the first of four arms to return non-zero and never summed across arms: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'` — here `0`; (2) top-level numbered/bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'` — here `4`, so arm 2 is this file's count; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, reserved for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted, including any a later fix plan verifies as OK — the count measures what the user found, not what survived triage.
  - Each observation is weighted in story-point units: **Major** `15` (explicit `[major]` marker, or the observation describes a broken/incorrect user-facing flow, a missing/client-only authorization gate, data loss/corruption/unprotected data, or an absent whole ported behaviour — the deciding phrase is quoted beside the observation), **Trivial** `2` (explicit `[trivial]` marker), **Minor** `5` (the default for every observation without a Major/Trivial classification).

## Status

- status: `post-user-review` — `pre-user-review` means this file was written right after the branch (code) review with no user review yet (`issue_cost_total` `0` → `100%`); `post-user-review` means it was re-written after user-review fixes, with the issues from the `fix_injection_verdict_tools_used_prefix_review*.md` files counted and weighted.
- last_updated: `2026-11-19`

## Notes

This is a deliberately basic but points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`: the denominator is the sum of the story-plan tasks' story-point complexity estimates (the scope the agent committed to, weighted by effort rather than raw task count), and the subtraction is the severity-weighted cost of user-review observations (defects found after the workflow finished, each costing Minor `5` by default, Major `15` on an explicit marker or a documented broken-flow / security / data-integrity / missing-behaviour classification — with the deciding phrase quoted in the breakdown — and Trivial `2` only on an explicit marker). The retained raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` let the metric be refined later (e.g., richer per-issue severity triage) without losing the raw data.

The `0%` is the clamp: the weighted user-review cost (`50`) exceeds the planned scope (`35`). Three of the four observations describe shapes the verdict flow still parked as `malformed-verdict`, and observation 1 says it overrides the task prompt's own line that kept the notice malformed. The story index scoped the notice out on purpose (its `## Context`, "The harness notice stays malformed"), so most of this cost comes from a scope decision the user reversed, not from a defect in the planned work. The rubric grades only the review text, so that context does not change the weights.

The specified range `dev..HEAD` could not be resolved because this checkout has no local `dev` branch. The commit messages were read over `origin/dev..HEAD` instead.
