### Task 4 — Export `RoundResume`, document the round entry, walk it end to end

**Goal:** Make the round entry reachable by a caller who imports only from `graphscene`. Export `RoundResume`, document `rounds.py`'s and `walker.py`'s new entry in the package README, and walk a resumed round end to end through `load_graph` and `FileStateStore`. The end-to-end walk proves the saved walk-state document is still `"version": 1`.

**Depends on:**

- **Task 1:** `RoundResume(round: str, number: int, records: tuple[GateRecord, ...] = ())`, defined in `graphscene.model.walk_state`.
- **Task 3:** `Walker.start(entry: str | None = None, *, resume: RoundResume | None = None) -> Step`. A resume at its own round with some gates recorded returns the `DispatchSet` of the gates still out. With every due gate recorded it returns the join's step. Its counters stay at 0.

This task changes no engine or model code, and no adapter: `graphscene/src/graphscene/adapters/walk_json.py` stays untouched, because a resumed walk is an ordinary `WalkState`.

### Targets

- `graphscene/src/graphscene/facade/__init__.py`: import and `__all__` entry.
- `graphscene/src/graphscene/__init__.py`: import and `__all__` entry, in the same position.
- `graphscene/tests/test_public_surface.py`: `_EXPECTED` and `_DEFINED_IN`.
- `graphscene/tests/facade/test_walking.py`: one end-to-end resume case.
- `graphscene/README.md`: the `src/graphscene/model/` and `src/graphscene/engine/` rows of `## What it is`.

**Work:**

- [ ] **The public name lands in all four places in one order**, per `.claude/context/graphscene.md` → `## What accompanies a new module`, *"A name made public lands with…"*. Insert `"RoundResume"` directly after `"OpenRound"` in the `__all__` of both `facade/__init__.py` and `__init__.py`, each importing it from its defining module or the facade as its neighbours do. In `test_public_surface.py`, insert `"RoundResume"` after `"OpenRound"` in `_EXPECTED`, and add `"RoundResume": graphscene.model.walk_state` to `_DEFINED_IN`. The `_EXPECTED[7:28]` slice for `flow_graph` names sits before `"Walker"` and is unaffected.
- [ ] `test_walking.py`: add `test_a_round_resumed_with_recorded_gates_dispatches_the_rest_and_joins(tmp_path)`, importing `RoundResume` from `graphscene` as a caller does. Over `_four_gate_graph()` (`review_round` gating `edit_check`, `style_check`, `fact_check`, `legal_check`), call `start("review_round", resume=RoundResume("review_round", 2, (GateRecord("fact_check", "rejected", "f/review_2.md"), GateRecord("edit_check", "approved", None))))`. Note the records are not in gates order. Assert the hand-written `DispatchSet` of `style_check` and `legal_check` at number 2. Read the state file with `json.loads` and assert `"version"` is `1`, `open_round.number` is `2` and both records are under `records`. Record the two remaining gates `approved` through fresh `_walker(path, graph)` instances on the same path. Assert the last call returns the writer `draft` dispatch from `_editor`'s sibling shape: `prompt="rework"`, round number 3, `attempt` 1, and `closed_round` holding all four records in gates order with their details.
- [ ] `test_walking.py` module docstring: add to the rule sentence that a round resumed through `RoundResume` dispatches only its unrecorded gates, saves a version-1 state, and joins on the rest.
- [ ] `graphscene/README.md` → `## What it is`. On the `src/graphscene/model/` row, the `walk_state.py` entry reads *"`WalkState`, `OpenRound`, `RoundResume` and `Awaiting`, where a walk stands and the round a host resumes it in"*. On the `src/graphscene/engine/` row, the `rounds.py` entry adds *"and entering a round with gates already recorded"*. The `walker.py` entry adds that `start` takes an optional `RoundResume`: the walk starts at that round's number with the given gate outcomes recorded, every counter at 0, and the host decides which round and which records. Edit no other row or section. These are register rows 6 and 7 of the story index's `## Scope register`.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py` and `bash scripts/python-service.sh --package graphscene test tests/facade/test_walking.py` each pass. These are the two test files this task edits.
- The end-to-end case is the story index's first `Top risks:` guard. Its state-file assertions read the JSON as text, not through the codec, so a new key or a version change would fail it.
- `git diff --name-only` for this task lists no file under `graphscene/src/graphscene/adapters/`, `engine/` or `model/`.
- The register's command entry (story index, `## Scope register`), re-run after this task, reaches the README's lines 14 and 15 as before. Both now name `RoundResume` or the round entry.
