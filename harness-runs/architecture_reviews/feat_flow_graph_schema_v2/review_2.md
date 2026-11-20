# Architecture review — round 2

verdict: PASS
review_mode: converging

Scope: `review_1.md` (PASS, no Must Fix), the round-2 revision note, and the plan diff since `chore: Plan round 1 for feat_flow_graph_schema_v2` (7a1fc52f). Only `task_2_plan.md`, `task_5_plan.md` and `task_6_plan.md` changed, and the story index has no `## Rejected findings` section.

- **`task_2_plan.md`.** The changed text is the harness-name walk in `graphscene/tests/test_flow_graph_schema.py`, which now skips key-name positions, plus three planted cases and a second "Deliberately not covered" note. Placement is unchanged: the test stays under `graphscene/tests/`, and the schema stays under `graphscene/src/graphscene/schemas/`. The cited exemption is real: `jq '.properties.counters.additionalProperties.required' schemas/flow-graph.schema.json` prints `["cap"]`. The planted cases follow `.claude/context/graphscene.md` → `## Tests`, which asks for one planted case per clause, each asserting the exact violation. The change adds no dependency and no `devscene` name to `graphscene/src/graphscene/` (`## What it may depend on`).
- **`task_5_plan.md` / `task_6_plan.md`.** The changed text is the verification bullets. The npm scripts and the `3g`/`3h`/`3i` arms are now checked by reading (`jq`, `grep`, `bash -n`), and the gate legs are left to the Run gates round. No bullet now asks for a gate script or `bash scripts/test.sh` (`unit_loop_core.md` → `## The test-run rule`, point 4). Layer placement of the targets (root `package.json`, `scripts/run-gates.sh`) is unchanged and stays in the `general` layer.

## Should Fix

1. **Carried from round 1, still unchanged: `task_1_plan.md` places the format-4 source `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` in `cli/templates/`. That tree holds the files `init` writes into an adopting repository, and `init` never writes this one.** Rules: `.claude/context/cli.md` → `## What this layer owns, and what it is not`; `.claude/context/conventions.md` → `### Where a new responsibility goes`. The full reasoning and both suggested fixes are in `review_1.md` → `## Should Fix` 1.

## Incidental findings (not gating)

1. **`task_2_plan.md` → `**Verification:**` bullets 1–2 run `node schemas/validate.mjs validate|test -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d …` directly.** These are the same invocations that Task 5's `validate:graphscene-schema` / `validate:graphscene-schema:negative` scripts, and so gate legs `3g`/`3h`, wrap. Round 2 rewrote Tasks 5 and 6 so that those legs run only in the Run gates round, and Task 2 was left as it was. `schemas/validate.mjs` is a validator CLI, not a gate script, so this is not graded here. It is a lead to check against `unit_loop_core.md` → `## The test-run rule`, point 1.
