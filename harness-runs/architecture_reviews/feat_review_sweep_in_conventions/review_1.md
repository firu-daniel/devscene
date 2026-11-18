# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix
1. **`task_1_plan.md` — the `writer.ts` header edit adds a table row but leaves the per-request `forceOverride` paragraph incomplete.** Rule source: `.claude/context/cli.md` → `## What "done" means here` (*"A reviewer holds a change to its module's own header. Where the header states a rule, the change either satisfies it or amends the header in the same edit"*). `cli/src/core/writer.ts` → `## The re-run contract, per artifact` lists, in the paragraph after the table, every caller that sets `forceOverride` per request: for `generators/claudeContext.ts`, *"`'never'` on a conventions stub that is already a skeleton whose `.bak` holds a filled document"* and on `.claude/CLAUDE.md`. Task 1 gives `.claude/review-sweep.md` that same `'never'` keep. Its Work bullet for `writer.ts` adds only the table row ("its reason: … the `--force` keep as for a stub"). Name the review-sweep document in that paragraph too, so the header still lists every per-request `'never'` this engine honours.

## Nice to Have
1. **`task_3_plan.md` — the outer-loop script family has no row in `writer.ts`'s re-run-contract table.** `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, row *A generated or copied artifact*, asks for "its row in `cli/src/core/writer.ts`'s re-run-contract table with its write policy". That table carries a `wrapper scripts` row and no outer-loop row. The gap predates this branch, and every outer-loop script shares it (`task-offer-check.sh`, `prompt-injection-screen.sh`), so it does not block this plan. Task 3 could widen the `Git hook pre-push, wrapper scripts` row to name the outer-loop family, or leave that to a later branch.
