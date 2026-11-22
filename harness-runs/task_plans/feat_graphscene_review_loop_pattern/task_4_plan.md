### Task 4 — Make a round's writer, counter and convergingFrom an optional group

**Goal:** Let a format-4 graph declare a round that is not a review loop. `writer`, `counter` and `convergingFrom` leave the round node's `required` list and become a group that is present together or absent together. `plan` and `revisionNote` are allowed only with `writer`. The model carries the three as `| None`. The key set does not change, so `formatVersion` stays `4`, and every graph that is valid today stays valid with the same meaning.

**Depends on:**
- Task 1, whose `graphscene.engine.review_loop.review_loop(node)` already returns `None` when any of the three values is `None`;
- Task 2, after which `graphscene/src/graphscene/engine/transitions.py` reads none of the three fields directly;
- Task 3, after which `graphscene/src/graphscene/engine/static_check.py` and `graphscene/src/graphscene/engine/references.py` read none of them as non-optional.

So the field-type change below breaks no reader. If `mypy` still names a reader outside this task's targets, that is a hand-off defect to report, not a file to edit here.

**Where this task stops.** This task adds the two fixtures and checks that they parse and build. Loading them through `load_graph` and walking the plain round is Task 6's (`graphscene/tests/facade/test_loading.py`, `graphscene/tests/facade/test_walking.py`). Planting plain rounds in the engine suites is Task 5's. Listing the fixtures in the root `validate:graphscene-schema` and `validate:graphscene-schema:negative` scripts is Task 8's (`package.json`, `general` layer), as `.claude/context/conventions.md` → `## What accompanies a new unit of each kind` requires of a schema negative.

### Targets

- `graphscene/src/graphscene/schemas/flow-graph.schema.json`
- `graphscene/src/graphscene/model/flow_graph.py`
- `graphscene/src/graphscene/adapters/builder.py`
- `graphscene/tests/fixtures/flow_graph/valid_plain_round.json` (new)
- `graphscene/tests/fixtures/flow_graph/schema_negative_writer_without_counter.json` (new)
- `graphscene/tests/adapters/test_builder.py`
- `graphscene/tests/test_flow_graph_schema.py`

**Work:**

- [ ] **Schema**, `definitions.roundNode`:
  - `required` becomes `["kind", "parallel", "gates", "outcomes"]`.
  - Add `"dependencies": { "writer": ["counter", "convergingFrom"], "counter": ["writer"], "convergingFrom": ["writer"], "plan": ["writer"], "revisionNote": ["writer"] }`.
  - Add a `description` to `roundNode`: a round that declares `writer` is a review loop, whose writer writes what the gates review and revises it when the round fails, and which requires `counter` and `convergingFrom` and alone may carry `plan` and `revisionNote`; a round without `writer` dispatches its gates as one set and joins them, and nothing more.
  - Restate `writer`'s description: declaring it makes the round a review loop.
  - `formatVersion` stays `const: 4`, and no key is added or renamed.
  - No description string may equal a name in `graphscene/tests/test_flow_graph_schema.py` → `_HARNESS_NAMES` or contain `devscene`.
- [ ] **Model and builder:**
  - `flow_graph.py` → `RoundNode`: `writer: str | None`, `counter: str | None`, `converging_from: int | None`, keeping the field order. Add a docstring line: the three are `None` together on a round that is not a review loop (`graphscene.engine.review_loop`).
  - `builder.py`: build the three with `_opt_str` and a new `_opt_int(fields, key, path) -> int | None` beside `_opt_str`, which keeps `_int`'s integral-float rule.
  - `builder.py`'s *"Absent keys"* docstring paragraph is unchanged in substance.
- [ ] **`valid_plain_round.json`** — a schema-, vocabulary- and static-valid format-4 graph with a round that declares no `writer`:
  - `flow` `release_checks`, with a one-sentence `description`.
  - `vocabulary.outcomes`: `done: {}`, `accepted: {"verdict": "pass"}`, `rejected: {"verdict": "fail"}`, `crashed: {"held": true}`.
  - `vocabulary.bindings`: `<halt>` `stop` with `reasons` `["failed", "crash"]`, and `<finish>` `end`.
  - `vocabulary.predicates`, `counters` and `paths` are `{}`, and `reports` is `[]`.
  - `start` `intake`, `entries` `["intake", "checks"]`.
  - `nodes`:
    - `intake` is a dispatch node (agent `release-intake`). It routes `accepted` → `checks`, `rejected` → `discarded` with no increment (a fail verdict routed outside any round, which check 8's graph-wide clause would name if the graph declared a review loop), and `crashed` → `<halt>` with reason `crash`.
    - `lint` and `license` are dispatch nodes (agents `lint-checker` and `license-checker`). Each routes `accepted` and `rejected` → `checks`, and `crashed` → `<halt>` with reason `crash`.
    - `checks` is a round with `parallel: true` and `gates` `["lint", "license"]`, and no `writer`, `counter`, `convergingFrom`, `plan` or `revisionNote`. Its outcomes are `accepted` → `published` and `rejected` → `{"binding": "<halt>", "reason": "failed"}`.
    - `published` and `discarded` are terminals with `<finish>`.
  - Every `heartbeat` carries `{iteration}`.
- [ ] **`schema_negative_writer_without_counter.json`** — a copy of `valid_generic.json` with one change: `nodes.review_round.counter` removed, so `writer`'s dependency fails. The schema reports it at `nodes.review_round`, the object carrying `writer`; that path is Task 6's `_SCHEMA_NEGATIVES` entry.
- [ ] **Tests:**
  - `test_builder.py`: a case that builds `valid_plain_round.json` and asserts `checks` is a `RoundNode` whose `writer`, `counter`, `converging_from`, `plan` and `revision_note` are all `None` and whose `gates` is `("lint", "license")`, hand-written from reading the fixture. The existing `review_round` assertions stay.
  - `test_flow_graph_schema.py` → `_FIXTURE_NAMES`: add both new fixture names.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/adapters/test_builder.py` passes.
- `bash scripts/python-service.sh --package graphscene test tests/test_flow_graph_schema.py` passes, including `test_the_schema_names_no_harness_vocabulary` over the restated descriptions.
- The key set is unchanged. `git diff graphscene/src/graphscene/schemas/flow-graph.schema.json` shows changes only to `required`, a new `dependencies` and descriptions, and `formatVersion` stays `4`.
- `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` is not in the unit's diff. Its `plan_round` declares `writer`, `counter` and `convergingFrom`, so it opts in unchanged.
