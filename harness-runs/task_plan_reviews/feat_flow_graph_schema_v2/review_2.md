# Task plan review — round 2

verdict: PASS
review_mode: converging

## Should Fix
- **`task_5_plan.md` → Work, first `package.json` bullet.** The bullet still spells the script as one `node schemas/validate.mjs validate -s … -d <file>…` (raised in rounds 0 and 1). This round's Verification now requires *"a separate `-d` before every file"*, and `schemas/validate.mjs` → `parseArgs` accepts repeated `-d` flags, so the Verification already settles the form. Spelling `-d` before each file in the Work bullet too would make the two match.

## Nice to Have
- **Round 1's Must Fix items are resolved, as checked this round:**
  - **Must Fix 1 (`task_2_plan.md`).** The walk now skips the members of `required` and `dependencies` and the `properties` keys. I listed every string value in `schemas/flow-graph.schema.json` that equals a forbidden name outside those positions: `jq -c '[paths(type=="string") as $p | …]'`. Every hit sits in a shape that Task 2's Work replaces in format 4: `bindingName.enum`, `dispatchNode.outcomes.propertyNames.enum`, `skipEntry` `construct`/`phase`, the `onCap` `reason` const, and `bindingEdge`/`askEdge`/`escalateEdge`. None sits in the carried-over `start`/`entries`/`counters`/`paths`/`reports` shapes. So a schema built as the Work says can pass the walk. The three planted cases fix what the walk must reject and accept.
  - **Must Fix 2 (`task_6_plan.md`) and Must Fix 3 (`task_5_plan.md`).** Their Verification bullets now check by reading (`jq`, `grep`, `bash -n`) and run no gate leg. `scripts/run-gates.sh` has `3e)`/`3f)` arms of the form the grep checks expect, and `3f` is on the `gr_run_round run_unit …` line, which the `3g 3h 3i` insertion follows.
- **Story index → `## Scope register`.** I re-ran derivation entries 1 and 2 verbatim, and every file they print is a row. I re-ran entry 3's first step over `harness-runs/lessons.md` (unchanged since round 1). This round's revision changes no register row, derivation entry or target set.

## Incidental findings (not gating)
- `task_6_plan.md` → `docs/development.md`. The paragraph *"The last four lines cover the flow graph"* is still not reworded, though Task 6 appends three commands after those four lines (round 1 Should Fix, still open).
- The other Should Fix items from round 1 are still open. These are the `heartbeat` and `findingsFolder` patterns that `valid_generic.json` must satisfy (`task_2_plan.md`), the `nodes` object printer layout (`task_4_plan.md`), and the wider derivation entry 1 that reaches `docs/cli.md`, `cli/README.md` and `plugin/instructions/task_plan_writing_instructions_core.md`.
