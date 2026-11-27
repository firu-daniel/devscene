### 4. Register the driver's return-field check as a tree guard over `plugin/schemas/**`

**Site:** `devscene-flow-host/tests/test_driver_return_fields.py` → `_SCHEMAS` and `test_every_field_the_driver_reads_is_declared_by_its_agents_schema`. The registry is `devscene.config.json` → `treeGuards`.

**The problem.**

The new suite reads `plugin/schemas/<agent>.return.json`, choosing the file by agent from `cli/templates/scripts/flows/task_plan_writing.graph.json`. It checks that every return field `host/run_exits.py` → `RETURN_FIELD_READS` reads is declared there. Its own header says it *"replaces the retired `agent-return-schemas.test.mjs` check that every `pd_ret_field` call named a declared field"*.

The retired check ran as a tree guard. `devscene.config.json` → `treeGuards` maps `test/agent-return-schemas.test.mjs` to `plugin/schemas/**`. So a unit that edited a return schema ran it under `plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 7.

The replacement carries no `treeGuards` entry. Today, a unit that removes `questions` or `tasks_count` from `plugin/schemas/task-plan-writer.return.json` passes its own run, and the break surfaces only at Run gates. The same rule's point 8 asks a test that reads repository files as text to register itself.

This test reads only the schema files the graph names, not a glob, so whether it counts as a "tree" read is arguable. That is why this is a Should Fix rather than a Must Fix. The coverage regression against the retired guard is real either way.

**The fix.** In `devscene.config.json` → `treeGuards`, add:

```json
{ "test": "tests/test_driver_return_fields.py", "covers": "plugin/schemas/**" }
```

Add a second entry with `"covers": "cli/templates/scripts/flows/task_plan_writing.graph.json"`, because the test also takes the node-to-agent map from that graph.

Keep the `test` value in the form the existing `devscene-flow-host` entries use (`tests/test_boundary.py`, relative to the package).
