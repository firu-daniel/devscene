# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **Scope register gap — story index (`fix_default_branch_diff_base_story_plan.md`), `## Scope register`.** No derivation entry reaches two durable-corpus sites. Both describe `defaultBranch` / `<default_branch>` as the base of a diff or commit range, and neither is a row. Disposition (ii).
   - Entry A matches only the `…HEAD` / `diff_base:` / `git show` revision forms. Entry B matches only `## Resolved values` token rows under `plugin`. Neither reaches prose that names the base in words.
   - Sites newly reached:
     - `docs/config.md` → `## 5`-area key table, `defaultBranch` row (*"also the diff base for a branch review"*).
     - `plugin/samples/sample_statistics.md` → the opening **Placeholders used below** note (*"`<default_branch>` is `devscene.config.json` → `defaultBranch`, the base of the commit range the `dispositioned_points` line is derived over"*). Task 3 moves this sample's `## Counts breakdown` line to `origin/<default_branch>..HEAD` but leaves this note naming the bare branch as the range's base.
   - Neither sentence gives a step that fails, so this is not a Must Fix.
   - Corrected derivation entry, strictly wider than entry B (read-only, runs as written from the checkout root): `git grep -niE 'diff base|commit range' -- plugin docs README.md ARCHITECTURE.md`. Running it also reaches `docs/cli.md` (the `default-branch` detection prose and check-grading prose) and `docs/development.md` (the self-adoption paragraph). Each says a review's diff base is "taken from" the configured value, which is still true, so each takes a `no-change` row with that reason.

## Nice to Have

1. **Quoted anchor split across a comment wrap — story index (`fix_default_branch_diff_base_story_plan.md`), `## Context` → *Freshness*.** The quotation *"Default mode fetches and merges `origin/<base>`"* from `cli/templates/scripts/refresh-branch.sh`'s header does not match any single line verbatim, because the header wraps after "Default mode". The substance resolves, and the quote is rationale no task acts on.
2. **Layer order — story index, `## Context` → *Ship order*.** The plugin tasks come before the `cli` test, which is the reverse of the configured `layers[]` order (`cli` before `plugin`). The index argues the choice explicitly: the test asserts the plugin text, so running it first would make it fail. No `**Depends on:**` link points forward, and the order fires no trigger. This is recorded only so a reader sees that the deviation was checked.
