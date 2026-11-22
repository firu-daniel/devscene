### Task 9 — Bring `graphscene/README.md` up to date with the walker, its state and its store

**Goal:** Make the package's own README describe what the package now holds: an engine that walks a graph, the walk's state and protocols in `model`, and a file store in `adapters`. This task owns every `change` row of the story index's `## Scope register` that sits in `graphscene/README.md` (rows 3–6 and 10–14).

**Depends on:** Task 8. The README describes the public surface that task makes:

- `Walker` with `start` / `next` / `current`, where a refusal is returned as `Refused` and never raised;
- `FileStateStore(path, *, lock_timeout=120.0)`, which writes only that file and `<name>.lock`, replaces it atomically, and locks with `fcntl.flock`;
- `StateStore` and `PredicateHost` declared in `model`;
- the actions `Dispatch`, `DispatchSet`, `Wait`, `Interrupt`, `Stop`, `End` and `Refused`.

The modules are `model/walk_actions.py`, `model/walk_state.py`, `engine/transitions.py`, `engine/rounds.py`, `engine/walker.py`, `adapters/walk_json.py` and `adapters/state_file.py`. This task changes no code.

### Targets

- `graphscene/README.md`

**Work:**

- [ ] **`## What it is`, opening paragraph.** Replace "Nothing walks a graph yet: its `engine` layer holds the vocabulary check and the static checker." with sentences stating that the `engine` also holds the walker, which walks a loaded graph and says what runs next without launching anything, and that a walk's state is kept through a `StateStore` the caller supplies.
- [ ] **`## What it is` table rows.** Extend the rows:
  - **`model`**: `walk_actions.py` (the steps a walk returns and the passages it records) and `walk_state.py` (`WalkState`, `OpenRound`, and the `StateStore` and `PredicateHost` protocols);
  - **`engine`**: `transitions.py`, `rounds.py` and `walker.py` (`Walker`);
  - **`adapters`**: `walk_json.py` (the state's JSON form, not public) and `state_file.py` (`FileStateStore`).
- [ ] **`## The layers` table rows.** Extend the rows:
  - **`engine`**: from "Checks over the built model: the vocabulary check and the static checker." to also name the walk and its rounds;
  - **`adapters`**: add keeping a walk's state in a file;
  - **`model`**: add the walk state, its actions and the protocols the engine drives.
- [ ] **`## The layers` bullets.**
  - Replace "None exists yet." in the Protocol bullet with the two that now exist, `StateStore` (implemented by `FileStateStore`) and `PredicateHost` (implemented by the caller).
  - Restate "keeps no persisted or shared state" in the never-logs bullet: the library keeps no state of its own, and a walk's state is written only where the caller's `StateStore` puts it. `FileStateStore` writes only the file it is given and its `.lock` sibling.
  - Add that a walk refusal is a returned `Refused`, never an exception, and that the file store raises `ValueError` naming the file for a malformed state and `TimeoutError` naming the lock file.

**Verification:**

- [ ] Re-run the story index's command derivation entry. No README line it prints still says that nothing walks a graph, that no Protocol exists, or that the package keeps no persisted state.
- [ ] Every module name the README now cites exists under `graphscene/src/graphscene/`, and every public name it cites is in `graphscene/src/graphscene/__init__.py` → `__all__`.
