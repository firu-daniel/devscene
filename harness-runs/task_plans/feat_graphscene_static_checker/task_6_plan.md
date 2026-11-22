### Task 6 — Wire the static fixtures into `validate:graphscene-schema` and update the root documents of record

**Goal:** Hold the six `static_negative_*.json` fixtures to the format-4 schema from the repository root, as the `vocabulary_negative_*.json` fixtures already are. Then make `docs/development.md` and `ROADMAP.md` state what this branch shipped: the static checker, its place in loading, and the fact that the bash checker of the harness's format-3 graph stays.

**Depends on:** Task 4, and through it Tasks 1–3. Tasks 1 and 2 commit the six fixtures under `graphscene/tests/fixtures/flow_graph/`:
- `static_negative_node_known.json`
- `static_negative_reachable_from_start.json`
- `static_negative_reaches_terminal.json`
- `static_negative_fail_cycle_capped.json`
- `static_negative_gate_in_round.json`
- `static_negative_round_fan_out.json`

Task 3 makes loading schema → build → vocabulary → static, with stage `"static"`. Task 4 exports `graphscene.static_violations` and makes `graphscene/tests/facade/test_loading.py` assert that each fixture is rejected at the static stage. This is the **catch-all** task (`general`, `path` `"."`): it wires up and documents what the `graphscene` tasks built, which is why it ships last. Its implementer reads every configured layer's conventions document.

### Targets

- `package.json` (repository root)
- `docs/development.md`
- `ROADMAP.md`

**Work:**

- [ ] `package.json` → `validate:graphscene-schema`: append one `-d graphscene/tests/fixtures/flow_graph/<name>` per fixture above, after the last `vocabulary_negative_*.json` entry, in the order listed. Nothing else in the script changes (`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, the fixture-a-check-rejects row, applied to the new family).
- [ ] `docs/development.md` → `## 5. Verifying a change`, **Gate 3**, the paragraph on legs `3g`, `3h` and `3i`: the sentence on `graphscene/tests/facade/test_loading.py` also names the `static_negative_*.json` files, rejected at stage `static`. The stage list then reads `schema`, `vocabulary` or `static`.
- [ ] `docs/development.md`, the following paragraph (*"The check that every name a format-4 graph uses is one it declares has two homes"*): keep the two homes, and say `graphscene.load_graph` now runs the vocabulary check on the built model after the build. Then add, in the same paragraph or one right after it:
  - The generic static checks live at `graphscene.engine.static_check.static_violations`, exported as `graphscene.static_violations` and tested by `graphscene/tests/engine/test_references.py` and `graphscene/tests/engine/test_static_check.py`, run by gate 13's leg `13g`. They are that every id a graph names exists, then `reachable-from-start`, `reaches-terminal`, `fail-cycle-capped`, `gate-in-round` and `round-fan-out`, restated on declared primitives.
  - `load_graph` runs them last, as stage `static`, and each violation's reason opens with its check id.
  - The harness's format-3 graph is still checked by `scripts/check-flow-graph.sh` (legs `3e` / `3f`), which keeps checks 4–7 and is unchanged until the format-4 cutover that `ROADMAP.md` → the GraphScene row owns.

  Cite no issue number: the deferral points at the roadmap row (`.claude/context/conventions.md` → `## Documents of record`).
- [ ] `ROADMAP.md` → `## Scene products`, the GraphScene row: append to its *Shipped* list the static checker, `static_violations`, which checks that every id a graph names exists and ports the generic flow-graph checks, run by `load_graph` after the vocabulary check, which now reads the built model. Leave *Left* as it is, since the cutover is still left.

**Verification:**

- Every `-d` path added to `validate:graphscene-schema` exists. `git ls-files graphscene/tests/fixtures/flow_graph` lists each of the six names, and `grep -o "static_negative_[a-z_]*\.json" package.json` prints exactly the set of `static_negative_*.json` names that listing shows.
- `node -e "JSON.parse(require('fs').readFileSync('package.json','utf8'))"` exits 0.
- Re-run the story index's `## Scope register` command entry. The hits in `docs/development.md` and `ROADMAP.md` match the new wording, and every symbol and path they cite exists: `graphscene/src/graphscene/engine/static_check.py`, `graphscene/tests/engine/test_references.py`, `graphscene/tests/engine/test_static_check.py`, and `static_violations` in `graphscene/src/graphscene/__init__.py` → `__all__`.
