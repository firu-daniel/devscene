### Task 6 — Document format 4, the generated v3 graph and the new gate 3 legs

**Goal:** Bring the project's documents of record in line with what Tasks 1–5 built. Format 4 is the generic, vocabulary-declaring flow-graph format whose schema `graphscene/` ships. The harness authors its planning graph in format 4. The format-3 graph the bash walker reads is generated from it and held equal by gate 3. The cutover is still to come.

**Depends on:** Task 5. It wires `npm run validate:graphscene-schema` (the v4 source, `valid_generic.json` and the vocabulary negatives against `graphscene/src/graphscene/schemas/flow-graph.schema.json`), `npm run validate:graphscene-schema:negative` (each `schema_negative_*.json` refused) and `node scripts/generate-flow-graph-v3.mjs` (both v3 copies equal the generated one) as `scripts/run-gates.sh` legs `3g`, `3h` and `3i`. This task describes those, and Task 1's `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, Task 3's `graphscene.vocabulary.vocabulary_violations` and Task 4's generator. It changes none of them.

**How this task reads the conventions.** As the catch-all (`general`, path `.`) task, it reads every configured layer's conventions document, because its prose describes work in `cli`, `graphscene` and the root. `.claude/context/conventions.md` → `## Documents of record` binds it: a measured fact states its command, and a document of record is not rewritten to say something different about the past.

### Targets

- `docs/development.md` → **Gate 3 — configuration and flow-graph schemas.**
- `docs/flow-graph-walker.md` — *What it owns* and `## 2. The decisions`.
- `schemas/README.md`.
- `ROADMAP.md` → `## Scene products` → the GraphScene row.

**Work:**

- [ ] `docs/development.md` → **Gate 3**: add the three commands to the code block after `bash scripts/check-flow-graph.sh --negatives`: `npm run validate:graphscene-schema`, `npm run validate:graphscene-schema:negative` and `node scripts/generate-flow-graph-v3.mjs`. Then add one paragraph after *"The last four lines cover the flow graph…"*:
  - The format-3 graph is now generated from `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` by `scripts/generate-flow-graph-v3.mjs`, whose header is `THE RULE` and is not restated.
  - The last of the three commands fails when either committed copy differs from what it generates, and `--write` regenerates both.
  - The first two validate the format-4 source and the generic fixtures under `graphscene/tests/fixtures/flow_graph/` against `graphscene/src/graphscene/schemas/flow-graph.schema.json`, and refuse each schema negative, through the same `node schemas/validate.mjs` forms as above.
  - The used-against-declared names check is `graphscene/tests/test_vocabulary.py`'s, run by gate 13's leg 13g.

  Name the legs `3g`–`3i` as `scripts/run-gates.sh` prints them. Leave the *"Nine of the sixteen"* paragraph alone, because the count of gates does not change.
- [ ] `docs/flow-graph-walker.md`:
  - In *What it owns*, extend *"the graph's shape (`schemas/flow-graph.schema.json`)"* to name the generic format-4 schema in `graphscene/` beside it.
  - Add a decision section after `### The iteration cap — …`, titled `### Format 4 — the graph declares its vocabulary, and format 3 is generated from it`, in the file's **Decision.** / **Reason.** / **Cost.** shape:
    - **Decision.** Each declared name maps to an engine primitive (outcome `verdict`/`held`; binding `interrupt`/`stop`/`end`; skip predicates with `records` and `inRoundCounts`), and node kinds stay the engine's. The schema lives in `graphscene/`. The harness authors the v4 source, which `init` does not ship. Both v3 copies are generated, and gate 3's `3i` holds them. The walker, `scripts/check-flow-graph.sh`, `cli/test/agent-return-schemas.test.mjs` and the `validate:flow-graph*` scripts stay on format 3.
    - **Reason.** A generic engine cannot ship a closed list of one host's names. Declaring the names alone would only move the coupling the walker's fixed behaviour has, which is why each name maps to a primitive.
    - **Cost.** The planning graph exists twice until the cutover. The generator holds the mapping back to v3 names as harness knowledge. The v4 source sits inside the npm tarball, because `files` carries `templates`, but `init` never writes it.
  - Cite the cutover as the GraphScene row of `ROADMAP.md` (`## Scene products`), as `### Item 8` cites `ROADMAP.md` for its follow-up. Leave the `wc -c` figure in `## 1.` untouched: the bytes it measured do not change.
- [ ] `schemas/README.md`: after the paragraph on `flow-graph.schema.json`, add that the graph it validates is now generated from a format-4 source by `scripts/generate-flow-graph-v3.mjs`. Add that the generic format-4 schema, in which a graph declares its own vocabulary, is `graphscene/src/graphscene/schemas/flow-graph.schema.json` and is validated by `npm run validate:graphscene-schema`, and that this directory's format-3 schema stays as it is for the file the bash walker reads.
- [ ] **Commands in prose.** Every command a reader is meant to run that this task adds to any of the four files sits in a fenced block, one command per line, never inline (`harness-runs/lessons.md` → *Adopter-facing documentation*, the first rule). In `schemas/README.md` that means the `npm run validate:graphscene-schema` line.
- [ ] `ROADMAP.md` → GraphScene row: *Shipped* gains the generic flow-graph schema (format 4, a graph declaring its own vocabulary) and its used-against-declared names check, with the harness's planning graph authored in it and its format-3 copy generated. *Left* gains the cutover: the walker and the format-3 readers moving to format 4, and the generated copy and its generator retired. Keep the row's status `In progress`.

**Verification:**

- Every command the new prose names is checked **by reading, never by running**. Each `npm run <name>` the prose names is a key that `jq -r '.scripts | keys[]' package.json` prints. `node scripts/generate-flow-graph-v3.mjs` is the command on `scripts/run-gates.sh`'s `3i)` arm (`grep -n "3i)" scripts/run-gates.sh`). Those commands are gate 3's legs `3g`–`3i`, and they run once, in the Run gates round, never inside this unit (`unit_loop_core.md` → `## The test-run rule`).
- Every path the new prose names exists: `git ls-files` lists each of `graphscene/src/graphscene/schemas/flow-graph.schema.json`, `graphscene/src/graphscene/vocabulary.py`, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` and `scripts/generate-flow-graph-v3.mjs`.
- Re-run the story index's `## Scope register` derivation entries 1 and 2. Every file they print is a register row, and every row whose disposition is `change` is one of this branch's edited files.
- `grep -n "7075" docs/flow-graph-walker.md` still shows the measured line unchanged.
