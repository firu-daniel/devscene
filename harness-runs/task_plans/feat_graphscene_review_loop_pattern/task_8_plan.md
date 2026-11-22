### Task 8 — Wire the new fixtures into the root scripts and update the root documents

**Goal:** `ajv` validates the new plain-round fixture and rejects the new schema negative from the repository root. The root documents of record say that the review loop's rules on the engine have shipped, as a pattern a graph opts into.

**Depends on:**
- Task 4, which adds `graphscene/tests/fixtures/flow_graph/valid_plain_round.json`, schema-valid, and `graphscene/tests/fixtures/flow_graph/schema_negative_writer_without_counter.json`, which the format-4 schema must reject.
- Task 3, whose split is what the documents describe:
  - checks 8 and 9's round rules run on every round: a gate is a dispatch node, and a gate's verdict outcomes and skips go to the round;
  - their review-loop rules run only on a round that declares `writer`;
  - check 8's *uncapped fail verdict is a gate of exactly one round* runs only when the graph declares a review loop.
- Tasks 5–7, which land the tests and the package README this task points at.

**This is the catch-all task** (`layers[]` row with `path` `"."`), so it ships last and reads every configured layer's conventions document. Its targets sit at the repository root.

### Targets

- `package.json`
- `docs/development.md`
- `ROADMAP.md`

**Work:**

- [ ] `package.json`:
  - `validate:graphscene-schema`: add `-d graphscene/tests/fixtures/flow_graph/valid_plain_round.json` after the `valid_generic.json` entry.
  - `validate:graphscene-schema:negative`: append `&& node schemas/validate.mjs test -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d graphscene/tests/fixtures/flow_graph/schema_negative_writer_without_counter.json --invalid`. This is the chained assertion `.claude/context/conventions.md` → `## What accompanies a new unit of each kind` requires of a `schema_negative_<name>.json`.
- [ ] `docs/development.md` → `## 5. Verifying a change`, **Gate 3**, the paragraph opening *"The generic static checks live at `graphscene.engine.static_check.static_violations`"*: after the list of check ids, add one sentence. The round rules of `gate-in-round` and `round-fan-out` run on every round. Their review-loop rules run only on a round that declares `writer`, the opt-in `graphscene.engine.review_loop` reads, and the clause holding a dispatch node's uncapped fail verdict inside exactly one round runs only on a graph that declares a review loop. The harness's planning graph opts in through `plan_round`'s `writer`, so it is held to every clause. Every other sentence stays.
- [ ] `ROADMAP.md` → `## Scene products`, the GraphScene row:
  - Move *"the review loop's rules on the engine"* out of **Left:**.
  - Add a **Shipped:** clause: the review-loop pattern — a round is a plain fan-out and join unless it declares `writer`, and the review loop's checks and walk rules apply only where a graph declares one ([`graphscene/README.md`](graphscene/README.md)).
  - The row's status stays `In progress`, because the walker's port, the harness-side package and the cutover are still left.

**Verification:**

- `git diff --name-only` for this unit lists only the three targets; `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` and both format-3 copies are untouched.
- Every fixture path added to `package.json` exists under `graphscene/tests/fixtures/flow_graph/`, and every `schema_negative_*.json` file in that directory has its own `--invalid` assertion in `validate:graphscene-schema:negative`: `git ls-files 'graphscene/tests/fixtures/flow_graph/schema_negative_*.json'` ⊆ the file names in that script.
- The `ROADMAP.md` row still names what is left, and it names nothing this branch did not ship.
