# Review plan meta-review — iteration 2

## Must Fix
1. **The `cli` layer was touched, but no check drawn from `.claude/context/cli.md` appears in the review** — refers to "Structure" (missed check). Offending file: the index, `harness-runs/code_reviews/feat_script_driven_planning_pilot_code_review.md` (`## Context`).
   Most of the diff is under `cli/`: `cli/src/generators/outerLoopScripts.ts` (`OUTER_LOOP_SCRIPTS`, the three `planning-*-lib.sh` rows), the three new libraries and the watcher under `cli/templates/scripts/`, and seven suites under `cli/test/`. The Context checks the cli-layer work against other sources:
   - the task prompt and `docs/flow-graph-walker.md`;
   - `.claude/context/conventions.md` → `## What accompanies a new unit of each kind` (the outer-loop-script row);
   - the Pass 0 sweep (`## Shell assets`, also in `conventions.md`);
   - `harness-runs/lessons.md`.

   Findings 1 and 3, the two cli-layer findings, come from `docs/sandbox-record.md` and from the lessons ledger. No finding and no clean-pass sentence comes from the cli layer's own conventions document. The general missed-check rule therefore fails for `cli`, just as iteration 1's item 2 failed for `plugin`. These `cli.md` rules apply directly to this diff:
   - `## What "done" means here`: *"A change to a command or a generator lands with a case that drives the compiled CLI against a throwaway fixture repository"*. The rows were added to the generator table `cli/src/generators/outerLoopScripts.ts`.
   - `## How a module in this layer is written` → **One string, one producer.**: the shipped tables are single declarations of their sets, and *"A `.sh` name spelled as a string literal elsewhere in this layer is a second source … where it is resolved, joined or read as a path"*.
   - `## What "done" means here`: *"A reviewer holds a change to its module's own header"*. This covers the `OUTER_LOOP_SCRIPTS` rows' comment and the header of `outerLoopScripts.ts`.

   A spot-check suggests all three hold. `cli/test/outer-loop-scripts.test.mjs` adds `test("the planning driver's three libraries land verbatim under scriptsDir/lib, and a re-run keeps them", …)` and drives `initOk` against `fixtureFor`. `git grep` finds the three library names in `cli/src` only in the `OUTER_LOOP_SCRIPTS` rows. But the review states none of this. A cli-layer change with no rationale drawn from `cli.md` is exactly what this check exists to catch.
   **Fix:** In the index's `## Context`, add a clean-pass paragraph drawn from `.claude/context/cli.md`. Cover each of the three rules above:
   - the compiled-CLI fixture case in `cli/test/outer-loop-scripts.test.mjs` for the new `OUTER_LOOP_SCRIPTS` rows;
   - that the library basenames appear in `cli/src` only as those table rows, and why the watcher's `PLANNING_DRIVER_LIBS` string is outside the rule's scope (a template under `cli/templates/`, not a `cli/src` source);
   - that the `outerLoopScripts.ts` header and the rows' comment still describe what the rows do.

   If any of them does not hold, add a new `finding_<N>.md` at its site anchor, with its index pointer and its readiness entry.

## Should Fix

_None._

## Nice to Have

_None._
