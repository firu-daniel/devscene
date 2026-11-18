# Branch statistics: feat_init_upgrade

## Summary

- `success_rate`: **`87.4%`** — headline metric.
- `story_points_total`: `238` — denominator (sum of every task's `_(points: <N>)_` story-point estimate in the story index's `## Phase 2 Readiness — Ordered Fix List`).
- `issue_cost_total`: `30` — subtraction (sum of each user-review observation's severity weight, in story-point units).
- `story_plan_tasks`: `17` — retained raw count of `## Phase 2 Readiness — Ordered Fix List` task entries.
- `user_review_issues`: `6` — retained raw count of observations across all `feat_init_upgrade_review*.md` user-review files.

Formula:

```
success_rate = round(clamp((story_points_total - issue_cost_total) / story_points_total, 0, 1) * 100, 1) percent
```

Worked example: `round(clamp((238 - 30) / 238, 0, 1) * 100, 1)` = `round(87.3949…, 1)` = `87.4%`.

Edge cases (the rate is always computed via the formula, then adjusted by these rules):

- **No issues** — when `issue_cost_total` is `0` (no user review yet, or a fully clean review) the rate is `100%`.
- **Clamped at zero** — when `issue_cost_total > story_points_total` (weighted defect load exceeds the planned story points), the raw value goes negative; the rate is **clamped to `0%`** rather than recorded as a negative number. The rate never exceeds `100%`.
- **No points** — when `story_points_total` is `0` the rate is recorded as `n/a` (cannot divide by zero). This is only reachable when the story index has **zero** task entries; a story index that has tasks but no `_(points: …)_` tags falls back to the legacy task-count denominator (see below), so it still produces a number.
- **No points tags (back-compat fallback)** — when the story index has task entries but **none** carry a `_(points: …)_` tag (an older branch predating story points), `story_points_total` falls back to `story_plan_tasks` (the legacy task-count denominator) and `## Notes` records that points were unavailable.

## Counts breakdown

Per-source raw numbers and per-issue costs are retained so the metric can be refined later without re-deriving them.

- **Story-index source** — `story_points_total`: `238`, `story_plan_tasks`: `17`
  - counted from `harness-runs/story_plans/feat_init_upgrade_story_plan.md` (the `N. [x] **Task K** — … _(layer: …)_ _(points: <N>)_` entries under its `## Phase 2 Readiness — Ordered Fix List`, counting `[ ]` and `[x]` alike; all 17 are `[x]`).
  - per-task points (`_(points: <N>)_` tag on each entry), summed:
    - Task 1: `20`
    - Task 2: `15`
    - Task 3: `10`
    - Task 4: `20`
    - Task 5: `15`
    - Task 6: `10`
    - Task 7: `15`
    - Task 8: `10`
    - Task 9: `10`
    - Task 10: `20`
    - Task 11: `20`
    - Task 12: `8`
    - Task 13: `10`
    - Task 14: `10`
    - Task 15: `20`
    - Task 16: `15`
    - Task 17: `10`
    - **sum (`story_points_total`)**: `238`
  - `dispositioned_points`: `0` — none of the 83 commits in `origin/dev..HEAD` carries the `record disposition of ` record, so no unit was closed without a fix and no unit token is listed. The range uses `origin/dev` because the configured `defaultBranch`, `dev`, has no local ref in this checkout (see `## Notes`).
  - Back-compat fallback: did not fire — all 17 entries carry a `_(points: …)_` tag.
- **User-review source** — `user_review_issues`: `6`, `issue_cost_total`: `30` (per user-review file, then summed)
  - `harness-runs/user_reviews/feat_init_upgrade_review.md`: `6` observations → cost `30`. It is the only file the glob `feat_init_upgrade_review*.md` matches, and no match was dropped for containing `_fix_plan`. Counted by **arm 2, top-level list items** — `grep -cE '^[0-9]+\.|^[-*][[:space:]]' <file>` → `6`, arm 1 (`grep -cE '^#{2,4} +[0-9]+[.):]' <file>`) having returned `0`. Each observation's assigned weight beside it:
    1. `init --upgrade` to refuse before writing anything on a readable plugin and CLI version mismatch, with a refusal that moves the adopter forward → **Minor** `5`
    2. `init --upgrade --dry-run` to report the mismatch as a note and still show the changes, and the upgrade to proceed when the plugin version cannot be read → **Minor** `5`
    3. a mismatch to stay a warning under `HARNESS_SELF_ADOPT=1` in this harness repository → **Minor** `5`
    4. the documented adopter route to become the plugin update followed by the unpinned `npx devscene@latest init --upgrade`, with the pinned form kept for rollback and `init --upgrade-workflows` called out → **Minor** `5`
    5. `doctor`'s `plugin-cli-version` remedy and the upgrade report's wording to follow observation 1 → **Minor** `5`
    6. the removed-entries warning to stop pointing bare MCP-server `permissions.allow` entries and browser-tool `permissions.deny` entries at the local additions file that refuses them → **Minor** `5`
  - **total**: `6` observations → `issue_cost_total` `30`
  - Each file's observation count is the count of whatever top-level enumeration that file uses, taken from the first of four arms to return non-zero and never summed across arms: (1) numbered `##`–`####` headings with required trailing punctuation, `grep -cE '^#{2,4} +[0-9]+[.):]'` — here `0`; (2) top-level numbered/bulleted list items, `grep -cE '^[0-9]+\.|^[-*][[:space:]]'` — here `6`, so arm 2 is this file's count; (3) an explicit per-observation marker the file itself uses, with the matching grep recorded beside the count; (4) `1`, reserved for a file with no enumeration of any kind. Every observation the user wrote is counted and weighted, including any a later fix plan verifies as OK — the count measures what the user found, not what survived triage.
  - Each observation is weighted in story-point units: **Major** `15` (explicit `[major]` marker, or the observation describes a broken/incorrect user-facing flow, a missing/client-only authorization gate, data loss/corruption/unprotected data, or an absent whole ported behaviour — the deciding phrase is quoted beside the observation), **Trivial** `2` (explicit `[trivial]` marker), **Minor** `5` (the default for every observation without a Major/Trivial classification).

**Why all six here took the Minor default.** The weight is assigned from the observation as the reviewer wrote it, not from what a later fix plan concluded about it. None of the six carries an explicit `[major]` or `[trivial]` marker. Observations 1 to 5 change a decision the review says the task prompt had specified (its opening line: "I am changing that decision in this review"), so they describe new required behaviour and not a flow that fails end to end. Observation 6 is the closest to a Major condition: it describes wrong advice in a warning for two kinds of entry, while the upgrade itself still completes, so it is a partial defect and not a broken flow.

## Status

- status: `post-user-review` — `pre-user-review` means this file was written right after the branch (code) review with no user review yet (`issue_cost_total` `0` → `100%`); `post-user-review` means it was re-written after user-review fixes, with the issues from the `feat_init_upgrade_review*.md` files counted and weighted.
- last_updated: `2026-11-18`

## Notes

This is a deliberately basic but points-weighted estimate of the agentic-workflow success rate. The headline rate is `(story_points_total - issue_cost_total) / story_points_total`: the denominator is the sum of the story-plan tasks' story-point complexity estimates (the scope the agent committed to, weighted by effort rather than raw task count), and the subtraction is the severity-weighted cost of user-review observations (defects found after the workflow finished, each costing Minor `5` by default, Major `15` on an explicit marker or a documented broken-flow / security / data-integrity / missing-behaviour classification — with the deciding phrase quoted in the breakdown — and Trivial `2` only on an explicit marker). The retained raw counts (`story_plan_tasks`, `user_review_issues`) and per-issue costs under `## Counts breakdown` let the metric be refined later (e.g., richer per-issue severity triage) without losing the raw data. A unit closed via the unit loop's dispositioned outcome keeps its points in the denominator, so the rate counts them as delivered.

The disposition check ran over `origin/dev..HEAD` rather than `dev..HEAD`: `devscene.config.json` sets `defaultBranch` to `dev`, but this checkout has no local `dev` branch, so `dev..HEAD` does not resolve. `origin/dev` (`e63fb5f2`) is the merge base of this branch.
