### Task 21 — Hold every return field the driver reads to its agent's return schema

**Goal:** Replace the retired `agent-return-schemas.test.mjs` check, *"every `pd_ret_field` call in the driver names a declared field"*, with a `pytest` check against the Python driver. Each return-document field `host/run_exits.py` reads is declared by the return schema of the node's agent:
- `questions` from `plan_writer` / `ui_writer`;
- `tasks_count` from `plan_writer`;
- `tests_count` and `reason` from `ui_writer`.

**Depends on:** Task 17. `host/run_exits.py` reads those fields from `sessions.return_document(node)`, each field name a module-level `Final` constant there.

**Where this task stops.** It reads and asserts. It changes no schema and no driver code.

### Targets

- `devscene-flow-host/tests/test_driver_return_fields.py` (new)

**Work:**

- [ ] **The pairs.** `_READS: Final` is a tuple of `(node, field)` pairs, built from `host/run_exits.py`'s field constants and node names, imported rather than retyped. Each node's agent comes from the real planning graph, `cli/templates/scripts/flows/task_plan_writing.graph.json`, read-only, through `graphscene.load_graph_file`.
- [ ] **The check.** For each pair, read `plugin/schemas/<agent>.return.json` read-only, and assert that some `oneOf` variant declares `field` under its `properties`. The failure message names the node, the agent and the field.
- [ ] **The planted cases and the header.** Two planted cases under `tmp_path`:
  - a schema declaring the field passes the check;
  - one lacking it fails with that exact message.

  The header states the rule, and why the pairs are imported, not listed: a field the driver starts reading is checked without editing this file.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_driver_return_fields.py` passes.
- The suite reads three fixed files of this checkout, the graph and two schemas, and writes only under `tmp_path`. It is not a tree-reading test, so it owes no `treeGuards` entry (`plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8's boundary).
