### Task 1 — Add the `RoundResume` model type beside `OpenRound`

**Goal:** Give the `model` layer the plain, immutable input a host hands `Walker.start` to begin inside a round. It is `RoundResume`, with fields `round: str`, `number: int` and `records: tuple[GateRecord, ...] = ()`, declared in `graphscene/src/graphscene/model/walk_state.py` beside `OpenRound`.

**Where this layer stops.** This task declares the type and validates nothing. A `RoundResume` naming a node that is not a round, a negative number, or a record for a foreign or repeated gate builds without complaint here. Refusing those is **Task 3's** (`Walker.start`), and recording the records is **Task 2's** (`enter_round`). Making the name public is **Task 4's**, so this task does not touch `graphscene/src/graphscene/__init__.py`, `graphscene/src/graphscene/facade/__init__.py` or `graphscene/tests/test_public_surface.py`.

### Targets

- `graphscene/src/graphscene/model/walk_state.py`: the new dataclass and its docstring lines.
- `graphscene/tests/model/test_walk_state.py`: a frozen-instance case for the new class.

**Work:**

- [ ] `walk_state.py`: declare `RoundResume` as a `@dataclass(frozen=True)` directly after `OpenRound`, with exactly three fields in this order: `round: str`, `number: int` and `records: tuple[GateRecord, ...] = ()`. A sequence is a `tuple`, per `.claude/context/graphscene.md` → `## The model and its wire forms`. A tuple rather than a mapping keyed by gate keeps a second record for one gate visible, so Task 3 can refuse it. `GateRecord` is already imported from `graphscene.model.walk_actions`. The import stays model-internal, inside the `model` layer's standard-library-only rule.
- [ ] `walk_state.py` module docstring: widen the opening line so it says the module also holds the input a host hands `start` to begin inside a round. Under *Field meanings*, add a bullet: `RoundResume` is a host's entry into a round at `Walker.start`. `round` is the round node, `number` is its round number, and `records` holds outcomes already recorded, in any order. It carries no counter, because `start` sets every counter to 0. `RoundResume` is never saved. A resumed walk is saved as an ordinary `WalkState`, so the walk-state document is unchanged.
- [ ] `test_walk_state.py`: add a module-level `_RESUME = RoundResume(round="review_round", number=2, records=(_RECORD,))`. Add it to the `test_every_class_is_frozen` parametrize tuple, so its first field (`round`) refuses assignment. Add one case asserting that `RoundResume("review_round", 0).records == ()`, the default, hand-written. Extend the module docstring's rule sentence so it names the new class among the immutable plain types.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/model/test_walk_state.py` passes, and both new cases are among those it runs. This is the one test file this task edits.
- `RoundResume`'s field order and names are exactly `round`, `number`, `records`, because Tasks 2–4 construct it positionally and by keyword.
- `walk_state.py` imports nothing new outside `graphscene.model` and the standard library.
