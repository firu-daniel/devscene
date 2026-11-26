### Task 17 — Record format 5 and the hook seam in the flow-graph decision record, Gate 3, the schemas README and the roadmap

**Goal:** Record, in the documents of record at the repository root, three things this branch decided and shipped:

- the flow-graph format moved to 5;
- a graph now declares each node's prompt source and its host hooks;
- GraphScene's run mode runs those hooks through a host's `HookHost`.

This is the catch-all task, so it ships last. It documents what the layers below built.

**Depends on:**

- **Task 2:** format 5's keys: `vocabulary.hooks`, `promptSource`, `before` / `after` on dispatch and round nodes, and `before` on a terminal node.
- **Task 6:** the firing points and the once-per-attempt before-dispatch rule.
- **Task 7:** the public names and `graphscene/README.md`'s description.
- **Task 13:** the planning graph's three hooks and the overrides they carry.

This task cites those, and restates no rule beyond the one line each document needs.

**How this task's implementer reads the conventions.** This is the catch-all layer, so read every configured `layers[].conventions` document. The text describes a change that spans `cli`, `graphscene` and `devscene-flow-host`. `.claude/context/conventions.md` → `## Documents of record` binds the edits: a decision of record keeps the text as it was decided, and a change appends a dated **Changed** note.

### Targets

- `docs/flow-graph-walker.md`
- `docs/development.md`
- `schemas/README.md`
- `ROADMAP.md`

**Work:**

- [ ] **`docs/flow-graph-walker.md`.** Under the item whose **Decision.** opens *"The planning graph is authored in format 4"*, append a paragraph, in the same form as the item's existing **Changed 2026-11-25 (#459).** notes. It opens **Changed 2026-11-26 (`feat_graphscene_node_hooks`).** and records:
  - format 5's four keys, and why the version rose: the schema's *"A change to the key set raises it"*;
  - that the planning graph declares each dispatch node's core heading as `promptSource`, `plan_round`'s `after` hooks and `convergence`'s `before` hooks;
  - that the bash planning driver still makes those commits and flips itself, and still cuts its prompts from `PNL_CORE_BLOCKS`, until the run-mode cutover (#424);
  - that `cli/test/planning-node-lib.test.mjs` and core-agreement check 10 hold the two prompt declarations aligned meanwhile.

  Leave every earlier paragraph unedited.
- [ ] **`docs/development.md`.** Change each *"format 4"* / *"format-4"* phrase to format 5:
  - **Gate 3:** the paragraph on legs `3g` and `3h` (*"cover format 4"*), and the two paragraphs after it (*"validates against the format-4 schema"*, *"stated on the format-4 graph's declared primitives"*). Where Gate 3 says every name a graph uses is one it declares, add that a hook a node names is one of those names;
  - **Gate 13:** the `devscene-flow-host` legs' *"walk of the harness's format-4 planning graph"*.
- [ ] **`schemas/README.md`.** In the opening paragraph, change *"format 4"* to *"format 5"*.
- [ ] **`ROADMAP.md` → the GraphScene row.**
  - Change each of its three format-4 phrases (*"the generic flow-graph schema, format 4"*, *"the format-4 schema"*, *"the harness's format-4 graph"*) to say format 5.
  - Append to its shipped list: node and round hooks, and prompt sources, declared in the graph and run by run mode through the host's `HookHost`.
  - Also append the flow host's planning hooks, prompt builder and entry decision, which the run-mode cutover (#424) will call.

  Keep the row's existing link style: `graphscene/README.md`, and `docs/flow-graph-walker.md` → *Format 4*.

**Verification:**

- Re-run the story index's `## Scope register` format derivation entry verbatim: `git grep -lE 'format 4|format-4|"formatVersion": ?4' -- '*.md' 'cli/templates/**' ':!harness-runs/**' ':!examples/**'`. Every path it prints must be ⊆ the register's `no-change` rows, plus `docs/flow-graph-walker.md`, whose decisions of record keep their format-4 text above the new **Changed** note. There must be no hits outside those.
- `git grep -nE 'format 4|format-4' -- docs/development.md schemas/README.md` prints nothing.
- Read the new **Changed** note against `graphscene/README.md`'s hooks paragraph (Task 7). The two describe the same keys and the same firing points, in the same words.
