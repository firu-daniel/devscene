### Task 1 — Add the step document and the round-resume document to the walk codec

**Goal:** Give `graphscene/src/graphscene/adapters/walk_json.py` the two walk JSON forms the command line exchanges that belong with the walk codec:

- `step_document`, which encodes a walk `Step` (an action or a `Refused`) as a JSON-ready object;
- `resume_from_json`, which decodes a round-resume document into a `RoundResume`.

Both reuse the codec's existing encoders and readers, so each wire shape has exactly one owner.

**Where this layer stops.** This task adds two functions to an `adapters` module and their cases. It prints nothing, parses no argv and chooses no exit status: the command line is **Task 2's**. Task 2 calls exactly these two signatures:

- `step_document(step: Step) -> dict[str, object]`
- `resume_from_json(text: str) -> RoundResume`

`graphscene/README.md`'s `src/graphscene/adapters/` row, which names this module's functions, is **Task 3's** to update. This task does not edit the README. Neither function joins the public surface (`__all__`), just as `state_to_json` and `state_from_json` stay out of it (`graphscene/tests/test_public_surface.py` → `_EXPECTED`).

### Targets

- `graphscene/src/graphscene/adapters/walk_json.py`: two new functions, and the module docstring widened to own them.
- `graphscene/tests/adapters/test_walk_json.py`: the cases for both functions, plus a header sentence extending the rule it enforces.

**Work:**

- [ ] `walk_json.py` → `step_document(step: Step) -> dict[str, object]`.
  - For an `Action`, return `_action_out(step)` unchanged. Do not write a second encoder. The step document *is* the state document's `pending` encoding (`_action_out`, `_dispatch_out`, `_passage_out`, `_record_out`).
  - For a `Refused`, return `{"kind": "refused", "reason": step.reason}`. `kind` comes first, as every action object carries it (`graphscene/src/graphscene/model/walk_actions.py` → `Refused.kind`).
  - Import `Refused` and `Step` from `graphscene.model.walk_actions`. That is a `model` import, which `adapters` may make (`graphscene/pyproject.toml` → contract `graphscene-layers`).
- [ ] `walk_json.py` → `resume_from_json(text: str) -> RoundResume`.
  - The document is exactly `{"round": <string>, "number": <integer>, "records": [<record>...]}`. Each record is the state document's `{"gate", "outcome", "detail"}` object, read with the existing `_record`.
  - Reuse `_fields`, `_str`, `_int` and `_tuple`, so a malformed document raises `ValueError("<path>: <reason>")` in the same words the state codec uses. That covers a parse failure, a missing or extra key, a wrong JSON type, a `bool` or a fractional number given as `number`, and a non-object root.
  - The document carries no `version` key. It is an input the codec reads and never writes, and `RoundResume` is never saved (`graphscene/src/graphscene/model/walk_state.py` → *"It is never saved"*).
  - Validity against a graph (a real round, number ≥ 0, gates of that round, no duplicate gate) is **not** checked here. `Walker.start` refuses each of those (`graphscene/src/graphscene/engine/walker.py` → `_unplaceable`).
  - Import `RoundResume` from `graphscene.model.walk_state`.
- [ ] `walk_json.py` module docstring: the module owns the walk's JSON forms, which are the walk-state document, the step document and the round-resume document.
  - Extend *"The rule:"* to say that the step document of an action is that action's encoding inside the state document, that a refusal is `{"kind": "refused", "reason": …}`, and that the round-resume document is read only.
  - State that **neither addition changes the state document's shape, so `_VERSION` stays 1**.
  - Add the resume document's graph-level validity to *"Deliberately not checked"*, naming `Walker.start` as where it is refused.
- [ ] `test_walk_json.py`: extend the module docstring's *"The rule this file exists to enforce"* to cover both functions, then add these cases:
  - **Every action:** for every pending action already in `_ACTIONS` (one per variant), `step_document(action)` equals the `pending` object of `json.loads(state_to_json(state))` for a state carrying that action. That holds the two encodings to one shape.
  - **A refusal:** `step_document(Refused("…"))` equals a hand-written `{"kind": "refused", "reason": "…"}`, and its first key is `kind`.
  - **A hand-written resume document** with two records, one of them with `"detail": null`, decodes field by field to the hand-written `RoundResume`.
  - **Malformed resume documents**, parametrized like `test_a_malformed_document_is_refused_naming_its_path`, each with its exact message. Cover: a missing `records`, an extra key, `"number": true`, `"number": 1.5`, a record missing `detail`, a non-JSON text, and a JSON array root.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/adapters/test_walk_json.py` passes, the existing state-codec cases included.
- Every expected value in the new cases is hand-written from reading `_action_out` and the documents in the test file, never taken from the function's output (`.claude/context/graphscene.md` → `## Tests`).
- `step_document` contains no `if isinstance(…, Dispatch)`-style dispatch of its own beyond the `Refused` branch. Its action branch is a single call to `_action_out`.
- `_VERSION` is unchanged, and `state_to_json` / `state_from_json` are byte-identical to before the change.
