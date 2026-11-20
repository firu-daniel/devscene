### Task 5 — Wire the format-4 schema, its negatives and the generated-v3 check into npm scripts and gate 3 legs

**Goal:** Make every format-4 artifact this branch adds run on every gate run. The harness's v4 source and the generic fixtures validate against the schema `graphscene/` ships, each schema negative is refused, and the committed v3 graphs are held equal to the generated one.

**Depends on:** Tasks 1–4, whose outputs this task wires by exact path:

- Task 1's `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`.
- Task 2's schema `graphscene/src/graphscene/schemas/flow-graph.schema.json`, its schema-valid `graphscene/tests/fixtures/flow_graph/valid_generic.json`, and its schema negatives in that directory: `schema_negative_format_version_3.json`, `schema_negative_no_vocabulary.json`, `schema_negative_unknown_primitive.json`, `schema_negative_interrupt_without_resume_outcome.json`, `schema_negative_outcome_verdict_and_held.json`, `schema_negative_skip_construct.json`, `schema_negative_round_three_outcomes.json`.
- Task 3's schema-valid vocabulary negatives, also in that directory: `vocabulary_negative_unknown_outcome.json`, `vocabulary_negative_unknown_binding.json`, `vocabulary_negative_interrupt_without_resume.json`, `vocabulary_negative_undeclared_reason.json`, `vocabulary_negative_round_without_fail_verdict.json`, `vocabulary_negative_end_on_an_edge.json`, `vocabulary_negative_unknown_predicate.json`.
- Task 4's `scripts/generate-flow-graph-v3.mjs`, whose bare invocation is `--check`, with exit 0 clean, 1 findings, 2 usage.

If a listed file does not exist, stop and report it. Never wire a glob in its place, because a fixture no assertion names is never run (`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, *A negative schema fixture*).

**Where this layer stops.** The `validate:flow-graph` and `validate:flow-graph:negative` scripts and gate legs 3c–3f stay exactly as they are, since they are v3's readers. The new script names deliberately do not match `validate:flow-graph*`. Prose about the new legs is **Task 6's**.

### Targets

- `package.json` (root) — two new scripts.
- `scripts/run-gates.sh` — three new gate 3 legs and their place in the round.

**Work:**

- [ ] `package.json` → `scripts`: add `"validate:graphscene-schema"`, which is one `node schemas/validate.mjs validate -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d <file>…` naming the v4 source, `valid_generic.json` and the seven `vocabulary_negative_*.json`. They are listed because each must be schema-valid for the vocabulary check alone to be what rejects it. Place it after `validate:flow-graph:negative`.
- [ ] `package.json` → `scripts`: add `"validate:graphscene-schema:negative"`, which chains one `node schemas/validate.mjs test -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d <file> --invalid` per `schema_negative_*.json` above, joined with `&&` in the form `validate:flow-graph:negative` uses.
- [ ] `scripts/run-gates.sh`: add three arms after `3f`, each with `gate_header 3 "configuration and flow-graph schemas"`:
  - `3g)` → `gate "3g format-4 graphs validate against the graphscene schema" npm run validate:graphscene-schema`
  - `3h)` → `gate "3h format-4 schema negatives are refused" npm run validate:graphscene-schema:negative`
  - `3i)` → `gate "3i v3 flow graphs equal the one generated from format 4" node scripts/generate-flow-graph-v3.mjs`

  Insert `3g 3h 3i` after `3f` in the `gr_run_round run_unit …` line. `GR_PREREQUISITES` is unchanged, because none of the three needs gate 2a's build.

**Verification:**

- The two npm scripts are checked by reading, never by running: `jq -r '.scripts["validate:graphscene-schema"], .scripts["validate:graphscene-schema:negative"]' package.json` shows a separate `-d` before every file listed under **Depends on:**. In the first script, that is the v4 source, `valid_generic.json` and each of the seven `vocabulary_negative_*.json`. In the second, each of the seven `schema_negative_*.json` appears exactly once, with `--invalid`.
- `grep -n -e "3g)" -e "3h)" -e "3i)" scripts/run-gates.sh` shows the three arms. The `3g` arm runs `npm run validate:graphscene-schema`, `3h` runs `npm run validate:graphscene-schema:negative` and `3i` runs `node scripts/generate-flow-graph-v3.mjs`.
- The three legs themselves, including Task 4's generator, are **not** run inside this unit. They are gate scripts that the configured test command reaches through `scripts/run-gates.sh`, so they run once, as gate 3's legs, in the Run gates round (`unit_loop_core.md` → `## The test-run rule`).
- `bash -n scripts/run-gates.sh` exits 0, and `grep -n "3g 3h 3i" scripts/run-gates.sh` shows them on the `gr_run_round` line.
- `npm run validate:flow-graph` and `npm run validate:flow-graph:negative` are byte-unchanged in `package.json` (`git diff package.json` shows additions only).
