### Task 21 — Hold every return field the driver reads to its agent's return schema

**Goal:** Replace the retired `agent-return-schemas.test.mjs` check, *"every `pd_ret_field` call in the driver names a declared field"*, with a `pytest` check against the Python driver. Each return-document field `host/run_exits.py` reads is declared by the return schema of the node's agent:
- `questions` from `plan_writer` / `ui_writer`;
- `tasks_count` from `plan_writer`;
- `tests_count` and `reason` from `ui_writer`.

**Depends on:** Task 17. `host/run_exits.py` reads those fields from `sessions.return_document(node)` and exports, as module-level `Final`s:
- nodes `PLAN_WRITER_NODE` (`"plan_writer"`) and `UI_WRITER_NODE` (`"ui_writer"`), and `QUESTION_NODES = (PLAN_WRITER_NODE, UI_WRITER_NODE)`;
- fields `QUESTIONS_FIELD`, `TASKS_COUNT_FIELD`, `TESTS_COUNT_FIELD` and `REASON_FIELD`;
- `RETURN_FIELD_READS: tuple[tuple[str, str], ...]`, every `(node, field)` pair the module reads: `(PLAN_WRITER_NODE, QUESTIONS_FIELD)`, `(UI_WRITER_NODE, QUESTIONS_FIELD)`, `(PLAN_WRITER_NODE, TASKS_COUNT_FIELD)`, `(UI_WRITER_NODE, TESTS_COUNT_FIELD)`, `(UI_WRITER_NODE, REASON_FIELD)`.

**Where this task stops.** It reads and asserts. It changes no schema and no driver code.

### Targets

- `devscene-flow-host/tests/test_driver_return_fields.py` (new)

**Work:**

- [ ] **The pairs.** `_READS: Final = run_exits.RETURN_FIELD_READS`, imported from `devscene_flow_host.host.run_exits` rather than retyped; the suite also asserts `_READS` is non-empty and that every `QUESTIONS_FIELD` pair's node is in `QUESTION_NODES`. Each node's agent comes from the real planning graph, `cli/templates/scripts/flows/task_plan_writing.graph.json`, read-only, through `graphscene.load_graph_file`.
- [ ] **The check.** For each pair, read `plugin/schemas/<agent>.return.json` read-only, and assert that some `oneOf` variant declares `field` under its `properties`. The failure message names the node, the agent and the field.
- [ ] **The planted cases and the header.** Two planted cases under `tmp_path`:
  - a schema declaring the field passes the check;
  - one lacking it fails with that exact message.

  The header states the rule, and why the pairs are imported, not listed: a field the driver starts reading is checked without editing this file.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_driver_return_fields.py` passes.
- The suite reads three fixed files of this checkout, the graph and two schemas, and writes only under `tmp_path`. It is not a tree-reading test, so it owes no `treeGuards` entry (`plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8's boundary).
