### Task 8 — Restate Gate 3 and the schemas README without the format-3 bridge

**Goal:** The development guide's **Gate 3** and `schemas/README.md` describe the gate as it runs after Task 7. Both say where the checks the bash checker carried now run.

**Depends on:** Task 7, Task 6 and Task 1.
- **Task 7** removes legs `3c`–`3f` and `3i`, the `validate:flow-graph*` scripts, `scripts/check-flow-graph.sh`, `scripts/generate-flow-graph-v3.mjs`, `schemas/flow-graph.schema.json` and both of its fixture families. It keeps legs `3a`, `3b`, `3g` and `3h` under those ids, with `validate:graphscene-schema` validating `cli/templates/scripts/flows/task_plan_writing.graph.json`.
- **Task 6** adds `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`, which holds checks 4 `run-mode-id-known`, 5 `ledger-id-known`, 6 `findings-folder-in-core` and 7 `cap-matches-core` over the format-4 graph, run by `devscene-flow-host/tests/test_core_agreement.py` and so by gate 13's leg `13j`.
- **Task 1** ships that graph under the shipped name.

This task documents those facts and changes no file they changed.

**Document-of-record rule.** `docs/development.md` → `## 5. Verifying a change` is the authority on what each gate runs (`.claude/context/conventions.md` → `## The testing bar`). Every sentence written here must name a command or file that exists after Task 7. A measured statement about a removed leg is removed, not re-dated.

### Targets

- `docs/development.md` — `## 5. Verifying a change`, **Gate 3**: the command block and the four paragraphs after it on the flow graph, format 4, the vocabulary check and the static checks.
- `schemas/README.md` — the paragraphs opening *"`flow-graph.schema.json` is the second schema"* and *"That graph is now generated"*.

**Work:**

- [ ] **Gate 3's command block** keeps `npm run validate:config`, `npm run validate:config:negative`, `npm run validate:graphscene-schema` and `npm run validate:graphscene-schema:negative`, in that order. It drops the two `validate:flow-graph*` lines, both `check-flow-graph.sh` lines and the generator line. The *"The first validates … The second asserts …"* paragraph stays as it is.
- [ ] **Gate 3's flow-graph paragraphs.** Remove the paragraph opening *"The third to sixth lines cover the flow graph"* and the generator's `--write` block. Rewrite the format-4 paragraph so the last two lines, legs `3g` and `3h`, cover the planning graph `cli/templates/scripts/flows/task_plan_writing.graph.json` and the generic fixtures, and drop every sentence about the format-3 copies and their regeneration. Keep its `graphscene/tests/facade/test_loading.py` sentences.
- [ ] **The vocabulary and static-check paragraphs.**
  - The vocabulary-check paragraph keeps one home, `graphscene.vocabulary_violations`. The sentence about the generator's refusal goes.
  - In the static-check paragraph, *"the ids `scripts/check-flow-graph.sh` gives them"* becomes the ids themselves.
  - The closing sentence about the format-3 graph still being checked by `scripts/check-flow-graph.sh` is replaced. The new text says that the checks that hold the planning graph to the plugin documents it duplicates are checks 4 `run-mode-id-known`, 5 `ledger-id-known`, 6 `findings-folder-in-core` and 7 `cap-matches-core`. They live in `devscene-flow-host/tests/core_agreement.py` → `core_agreement_violations`, run by `devscene-flow-host/tests/test_core_agreement.py` in gate 13's leg `13j`, reading `plugin/instructions/run_mode_instructions.md`, `plugin/instructions/autonomous_pause_and_ledger.md` and the planning core at run time. The flow-to-core table is that module's `CORE_FOR_FLOW`.
- [ ] **`schemas/README.md`.** Remove the two paragraphs on the format-3 schema and its generation. In their place, one paragraph says that flow-graph shape is no longer a schema of this directory. The format-4 schema is `graphscene/src/graphscene/schemas/flow-graph.schema.json`, which ships with GraphScene, and the existing `npm run validate:graphscene-schema` block stays as the command that checks it. Check the opening paragraph's reference to the sibling `negative/` directory against what Task 7 leaves there.

**Verification:**

- `git grep -n -E 'check-flow-graph|generate-flow-graph-v3|validate:flow-graph|flow-graph-check|flow-graph-schema-|format-3|format 3|v4\.graph\.json' -- docs/development.md schemas/README.md` prints nothing.
- Every command left in Gate 3's block is a `package.json` script that exists after Task 7: `node -e "const s=require('./package.json').scripts; for (const k of ['validate:config','validate:config:negative','validate:graphscene-schema','validate:graphscene-schema:negative']) if (!s[k]) process.exit(1)"` exits 0.
- Every leg id the Gate 3 text names is an arm of `scripts/run-gates.sh`. Compare the ids the text names with `grep -n -E '^ +3[a-z]\)' scripts/run-gates.sh`: the named ids must be a subset of the arms.
- `devscene-flow-host/tests/core_agreement.py` exists and defines `core_agreement_violations` and `CORE_FOR_FLOW`, the names the new sentence cites.
