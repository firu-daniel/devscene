# Architecture review — round 1

verdict: PASS
review_mode: full

Round 0's two Must Fix items are resolved. `finding_2.md` step 1 now names `pnl_reap` as the only owner of the node-session manifest, amends `planning-node-lib.sh`'s header sentence *"Every durable write is `lib/planning-record-lib.sh`'s"*, and leaves `planning-record-lib.sh`'s header unchanged. Its new step 6 brings `docs/watcher.md` → `### Run analytics` and the `docs/` / `ARCHITECTURE.md` sweep into scope, and readiness entry 3 is tagged `_(layer: cli, plugin, general)_`.

A full re-read of the index and all four findings against `.claude/context/conventions.md`, `.claude/context/cli.md`, `.claude/context/plugin.md` and `harness-runs/lessons.md` turned up no new Must Fix:
- Each fix target sits in the layer its tag names.
- The configuration key follows the four-place contract.
- The run-analytics record shape starts in `cli/` before its `plugin/` reader.
- No finding asks for a test run.
- No line outside the markers fails the laundering check.

## Should Fix

1. **`finding_1.md` step 1, read with readiness entry 4's tag `_(layer: cli, general)_`: the fix asks for an order the unit loop cannot run in.** Step 1 says "Add it in this order": `schemas/devscene.config.schema.json` (`general`), then `cli/src/config/model.ts` and `check.ts` (`cli`), then `docs/config.md` §5 (`general`). This follows `.claude/context/conventions.md` → `### The order files are created…`, item 1. `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## Layer routing table` runs the tag's layers in bottom-up order, and the `"."` layer always runs last. So the `cli` implementer writes the model and the check before any schema property exists, and it cannot add that property itself, because `schemas/` is outside `cli`. The unit's single commit keeps the tree coherent once it lands, so this does not block the loop. Still, step 1 should say which sub-bullets the `cli` pass takes (model, check, shell reader, watcher, tests) and which the `general` pass takes (schema, `docs/config.md`, the three docs). Otherwise the `cli` implementer may read "in this order" as permission to edit `schemas/` (a placement violation) or report a blocker.

2. **`finding_1.md` step 2: `hr_config_load` is still not named** (round 0 Should Fix 1, not acted on, as `plan_review_rounds.md` → `## The writer's revision` item 3 provides). `hr_script_driven_planning` reads through `hr_cfg_scalar_var`. That function answers only for the keys in the closed `s(...)` list of `hr_config_load`'s jq program, and the function's header paragraph lists those keys (`execution.progressComments`, `execution.keepAwake`). If neither edit is made, the reader sees every configuration as "absent" and the pilot never switches on.

3. **`finding_1.md` step 3: the shell mirror of `pluginRuntimeRoot` retypes constants owned elsewhere** (round 0 Should Fix 3). Navigating `installed_plugins.json` / `known_marketplaces.json` needs the plugin key and the marketplace name. Those are owned by `cli/src/generators/projectSettings.ts` (`PLUGIN_KEY`, `MARKETPLACE_NAME`) and `cli/src/core/pluginIdentity.ts` (`PLUGIN_NAME`). `.claude/context/conventions.md` → *"The shared constants have owners"* and the *A persisted machine-state key* row of `## What accompanies a new unit of each kind` call for declaring the shell copy in those owners' headers, as well as in `cli/src/machine/plugins.ts`'s, which step 3 already names.

## Nice to Have

1. **`finding_1.md` step 6, `docs/flow-graph-walker.md` → `### Which runs when` → **Reason.**:** the rewritten reason could also acknowledge the older ledger entry under `## Evidence and measurement`. That entry says an unmeasured seam ships "behind an environment variable rather than a configuration key". This branch's newer `## Unattended control loops` entry now overrides it for a switch whose benefit holds in every execution mode. Stating which rule governs keeps the decision of record from contradicting the ledger.
