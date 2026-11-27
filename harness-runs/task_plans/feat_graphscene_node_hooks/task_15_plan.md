### Task 15 — Hold each prompt source to the planning core as core-agreement check 10

**Goal:** Extend the flow host's dev-time core-agreement checker so that every dispatch node's `promptSource` names the flow's core document, a section and heading that exist there, and as many fenced blocks as the node has prompts. The task prompt says *"If Overrides 3–6 become hooks, or prompt sources and paths move out of the core, the checker and its suite change with them"*. The prompts stay in the core, but the graph now names where. This check holds the graph to the core the way checks 4–7 hold its other duplicated values.

**Depends on:**

- **Task 1:** the planning graph's six `promptSource`s, each `instructions/task_plan_writing_instructions_core.md → <section> → <heading>`.
- **Task 8:** `parse_prompt_source(value) -> PromptSource(document, section, heading)` and `read_prompt_blocks(plugin_dir, source) -> tuple[str, ...]` in `records/prompt_blocks.py`. These raise `ValueError` and `RecordError`, with the messages Task 8 fixes.

**Where this layer stops.** This is a test-side checker over this checkout's `plugin/`, never shipped (`devscene-flow-host/tests/core_agreement.py` → module docstring). Refusing an unbuildable source at run time is `CorePromptBuilder`'s (Task 11).

### Targets

- `devscene-flow-host/tests/core_agreement.py`
- `devscene-flow-host/tests/test_core_agreement.py`

**The new check: 10, `prompt-source-in-core`.** Checks 1–3, 8 and 9 are GraphScene's static checks, and 4–7 are this module's, so the next free number is 10. It runs after check 7, over dispatch nodes in key order. `core` is `CORE_FOR_FLOW[graph.flow]`, and `plugin_dir` is `repo_root / "plugin"`. Each finding is reported at `nodes.<id>.promptSource`:

- **No source:** `prompt-source-in-core: dispatch node '<id>' declares no promptSource`.
- **A malformed source:** `prompt-source-in-core: <the ValueError message>`.
- **A document that is not the core** (`"plugin/" + document != core`): `prompt-source-in-core: '<document>' is not <core>`.
- **An unreadable section or heading:** `prompt-source-in-core: <the RecordError message>`.
- **A block count that does not match** (`len(prompts)`, or 1 with no `prompts`): `prompt-source-in-core: '<heading>' carries <n> fenced block(s) in <core>, node '<id>' declares <m> prompt(s)`.

A flow with no core already reports `findings-folder-in-core` and `cap-matches-core`. It reports `prompt-source-in-core: flow '<flow>' has no core in CORE_FOR_FLOW` too, at path `flow`.

**Work:**

- [ ] **`core_agreement.py`.**
  - **The check.** Add check 10 to `core_agreement_violations`, after `_cap_violations`, with the messages above verbatim. Import from `devscene_flow_host.records.prompt_blocks`.
  - **The docstring.** Change *"returns the findings of four checks"* to five, and add the check 10 bullet in the same form as checks 4–7. Leave *"Deliberately not covered"* naming checks 1–3, 8 and 9.
- [ ] **`test_core_agreement.py`.**
  - **Planted cases.** Add one per clause above, each asserting the exact `Violation`. Each uses an in-test graph copy that differs in one node's `promptSource`, plus a planted core under `tmp_path` for the block-count clause. Add one planted clean case.
  - **The real tree.** Extend the existing real-tree case so the real planning graph and this checkout's core produce no check 10 finding.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_core_agreement.py` passes.
- The real-tree case passing is the evidence that all six `promptSource`s name headings of `plugin/instructions/task_plan_writing_instructions_core.md` with the right block counts.
