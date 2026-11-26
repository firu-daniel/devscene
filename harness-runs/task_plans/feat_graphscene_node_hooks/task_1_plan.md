### Task 1 — Declare the planning graph's prompt sources and hooks at format 5, held to `PNL_CORE_BLOCKS`

**Goal:** Make the shipped planning graph declare, on each node, where its agent prompt comes from and which host hooks run around it, at format 5. Add a `cli` case that holds those prompt sources to the bash driver's `PNL_CORE_BLOCKS`, so the two declarations cannot drift while both exist.

**Where this layer stops.** This task writes declarations only. Three things belong to other tasks:

- **The schema that accepts them** is Task 2's. Until Task 2 lands, the graph is valid JSON but not schema-valid. That is expected: `cli` ships first in the configured layer order. Task 13 is the first suite that loads this graph under the new schema.
- **The check that every hook named here is declared** is Task 3's.
- **What each hook does** is Task 13's (`PlanningHooks`), and **how a prompt is built from a source** is Task 11's (`CorePromptBuilder`).

The bash planning libraries are not changed. They read the graph's node list with `jq` (`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_load_schemas`) and ignore the new keys.

### Targets

- `cli/templates/scripts/flows/task_plan_writing.graph.json`
- `cli/test/planning-node-lib.test.mjs`

**The contract this task writes against** (Task 2 defines it in the schema):

- **`formatVersion`** is `5`.
- **`vocabulary.hooks`** is an object whose keys are hook names, each matching `^[a-z][a-z0-9_]*$` and each declared as `{}`.
- **A dispatch node** may carry:
  - `promptSource`, a non-empty string;
  - `before` and `after`, each a non-empty array of unique hook names.
- **A round node** may carry `before` and `after`.
- **A terminal node** may carry `before`.
- **The `promptSource` string** is opaque to GraphScene. The harness spells it `<document> → <section> → <heading>`, with the `→` separators exactly as written here (U+2192 with one space each side):
  - `<document>` is relative to the plugin directory;
  - `<section>` is a `## ` heading line;
  - `<heading>` is a `### ` heading line under it.
- **The heading's fenced blocks are the node's prompts.** They are taken in `prompts` order, or as one block for a node with no `prompts`. This is `PNL_CORE_BLOCKS`'s rule (`cli/templates/scripts/lib/planning-node-lib.sh` → the comment above `PNL_CORE_SETUP_HEADING`).

**Work:**

- [ ] **`task_plan_writing.graph.json` — the format and the vocabulary.**
  - Set `"formatVersion": 5`.
  - Add `"hooks": { "commit_plan_round": {}, "flip_ledger": {}, "commit_convergence": {} }` under `vocabulary`, after `predicates`.
  - Extend `description` with one sentence: each dispatch node's `promptSource` names the core heading its dispatch blocks are cut from, and the graph's hooks are the host's commit and ledger points.
  - Keep the existing sentence that the dispatch blocks stay in the core.
- [ ] **`task_plan_writing.graph.json` — the prompt sources.** Add `promptSource` to each dispatch node, after `prompts` (or after `heartbeat` where a node has no `prompts`). The document of all six is `instructions/task_plan_writing_instructions_core.md`. The section and heading of each are taken verbatim from `PNL_CORE_BLOCKS`:
  - `plan_writer` → `## Loop` → ``### 1. Spawn `task-plan-writer` ``
  - `business_parity_review` → `## Loop` → `### 2. Business-parity review (plan-review mode)`
  - `architecture_review` → `## Loop` → `### 3. Architecture review (plan-review mode)`
  - `plan_review` → `## Loop` → ``### 4. Spawn `task-plan-reviewer` ``
  - `ui_writer` → `## UI-test-plan write loop` → ``### 1. Spawn `ui-tests-plan-writer` ``
  - `ui_review` → `## UI-test-plan write loop` → ``### 2. Spawn `ui-tests-plan-reviewer` ``
- [ ] **`task_plan_writing.graph.json` — the hooks.** Order is load-bearing in both arrays.
  - On `plan_round`, add `"after": ["commit_plan_round", "flip_ledger"]` after `revisionNote`. This is Override 6 of `plugin/instructions/task_plan_writing_instructions_autonomous.md`, which commits the round before any `P1` flip.
  - On `convergence`, add `"before": ["flip_ledger", "commit_convergence"]` after `binding`. This is Override 5's `P2` flip, then Overrides 3 and 4 and the `P3` flip.
- [ ] **`planning-node-lib.test.mjs` — the alignment case.** Add one case, with no `{ skip: SKIP }`, because it needs no walker environment. It reads two files of this checkout as read-only input: `cli/templates/scripts/lib/planning-node-lib.sh` and the shipped graph. It asserts each of the following:
  - every `PNL_CORE_BLOCKS` row (`<section>|<heading>|<keys>`) has exactly one dispatch node whose `promptSource` is `instructions/task_plan_writing_instructions_core.md → <section> → <heading>`;
  - every dispatch node's `promptSource` is one of those rows;
  - each row's key count equals that node's `prompts` length, or 1 for a node with no `prompts`.

  Write the expected node-to-row pairing as a literal in the case, from the list above, not derived from either file. Update the suite header's first paragraph to name this alignment.

**Verification:**

- `planning-node-lib.test.mjs` passes with the new case. Spot-check it on a copy of the graph in which one `promptSource` heading differs from its `PNL_CORE_BLOCKS` row: the case must fail and name that node.
- `jq -e '.formatVersion == 5 and (.vocabulary.hooks | keys == ["commit_convergence","commit_plan_round","flip_ledger"]) and ([.nodes[] | select(.kind == "dispatch") | .promptSource | type == "string"] | all)' cli/templates/scripts/flows/task_plan_writing.graph.json` prints `true`.
- Every other key of the graph is byte-unchanged: `git diff` shows only the lines the four Work bullets name.
