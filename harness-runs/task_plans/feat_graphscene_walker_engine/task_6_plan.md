### Task 6 — Add the walk state's JSON codec in `adapters/walk_json.py`

**Goal:** Turn a `WalkState` into JSON text and back with no loss, so a file store can persist it. Every action and passage variant is tagged by its `kind`, and a malformed document is refused with a `ValueError` naming the dotted path.

**Depends on:** Task 1 and Task 2. The codec covers every type they declare.

- From `graphscene.model.walk_actions`:
  - `GateRecord(gate, outcome, detail)`;
  - `SkipPassage(node, status)` (`kind` `"skip"`), `RoundPassage(round, number, verdict)` (`"round"`) and `LedgerPassage(entry)` (`"ledger"`);
  - `Dispatch(node, agent, prompt, counters, round_number, converging, closed_round, passed)` (`"dispatch"`) and `DispatchSet(round, number, dispatches, passed)` (`"set"`);
  - `Wait(round, recorded, pending)` (`"wait"`) and `Interrupt(binding, node, agent, resume, resume_outcome, passed)` (`"interrupt"`);
  - `Stop(binding, node, agent, reason, summary, evidence, round_counts, held, closed_round, passed)` (`"stop"`) and `End(binding, node, reports, passed)` (`"end"`).
- From `graphscene.model.walk_state`:
  - `OpenRound(round, number, due, records)`;
  - `WalkState(flow, node, awaiting, pending, counters, round_numbers, open_round, prompts, reports, skipped)`.

**Where this layer stops.** Reading and writing a file, locking and atomic replacement are **Task 7's** `FileStateStore`, which calls `state_to_json` and `state_from_json`. The codec is not public: Task 8 does not export it.

### Targets

- `graphscene/src/graphscene/adapters/walk_json.py` (new)
- `graphscene/tests/adapters/test_walk_json.py` (new)

**Work:**

- [ ] **Docstring and the document form.** The module docstring has a *"The rule:"* paragraph: the document's top level carries `"version": 1` beside the state's fields; every key is the attribute's own name, with no case mapping; each action and passage object carries its `kind`; a `tuple` is a JSON array and a `Mapping` a JSON object in key order. It also says the codec reads only what it writes: a document of another version is refused.
- [ ] **`state_to_json(state: WalkState) -> str`.** Output is `json.dumps(..., ensure_ascii=False, sort_keys=False, indent=1)` plus a trailing newline. `End.reports` pairs are 2-element arrays.
- [ ] **`state_from_json(text: str) -> WalkState`.** It rebuilds the frozen types, with `tuple`s and `MappingProxyType`s over fresh `dict`s, as `graphscene/src/graphscene/adapters/builder.py` → *"Containers"* builds the graph. It refuses with `ValueError(f"{path}: {reason}")`, where `path` is dotted from the root as `graphscene/src/graphscene/model/errors.py` → *"The rule:"* spells one (`""` for the root):
  - a parse failure;
  - a `version` other than 1;
  - a missing or extra key;
  - a value of the wrong JSON type (a `bool` is never an `int`);
  - an unknown `kind`;
  - an `awaiting` or `verdict` outside its `Literal`.
- [ ] **`test_walk_json.py`.** Its module docstring opens *"The rule this file exists to enforce"*. Cover these:
  - a round trip `state_from_json(state_to_json(s)) == s` for one hand-built `WalkState` per pending-action variant (`Dispatch`, `DispatchSet`, `Wait`, `Interrupt`, `Stop`, `End`), together carrying every passage kind, an `OpenRound` with records and every optional field both set and `None`;
  - one hand-written JSON document asserted field by field after decoding;
  - one planted malformed document per refusal clause, each asserting the exact `ValueError` text.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/adapters/test_walk_json.py` passes.
- [ ] `walk_json.py` imports only `graphscene.model` modules and the standard library, never `graphscene.engine`.

**Deviations from plan:**

- The plan spells the refusal `ValueError(f"{path}: {reason}")` with `path` `""` for the root, which would render a root refusal as `": <reason>"`. Implemented as `f"{path or '(root)'}: {reason}"`, the rendering `graphscene/src/graphscene/model/errors.py` → `Violation.__str__` and `graphscene/src/graphscene/adapters/builder.py` → `_object` already use, so a root refusal reads `(root): not valid JSON: …` / `(root): expected object`. Every non-root path is as the plan spells it.
- Reasons chosen where the plan names only the clause: `missing key`, `unexpected key`, `expected string|integer|boolean|array|object`, `expected 2-element array` (an `End.reports` pair), `unknown kind '<kind>'` (also for a non-`dispatch` kind inside `DispatchSet.dispatches`), `unsupported version <json value>`, `expected one of '…', …` for `awaiting` and `verdict`, and `not valid JSON: <msg> (line <n>, column <n>)` as `graphscene/src/graphscene/adapters/json_file.py` words it. A JSON number with a fraction part (`1.0` included) is refused as an integer, since the codec reads only what it writes.
