### Task 5 — Document gate 13's GraphScene legs in `docs/development.md` and move GraphScene's roadmap row to in progress

**Goal:** Make the documents of record state what the earlier tasks built. Gate 13 now covers the Python packages, including the GraphScene library's legs 13e–13g, and `graphscene` is the wrapper table's second row. GraphScene's roadmap row now names what has shipped and what is left.

**Depends on:** Tasks 1–3. The facts this task documents, restated so that no other file is needed:
- **The package (Task 1).** `graphscene/` is a Python `>=3.11` library with no runtime dependency, using `ruff`, strict `mypy` and `pytest` with `-p no:cacheprovider`. `graphscene/tests/test_boundary.py` holds it to its boundary: no import beyond the standard library, itself and its declared dependencies; no `devscene`-prefixed module or dependency; no `devscene.config.json` literal.
- **The wrapper (Task 2).** `scripts/python-service.sh` has two rows, `docs-retrieval-service` (the default) and `graphscene`. `provision` syncs both. `run` and `container-test` on `graphscene` exit `2`.
- **The gates (Task 3).** `scripts/run-gates.sh` runs 13e `--package graphscene lint`, 13f `typecheck` and 13g `test` through `python_gate`. They are graded `BLOCKED` on exit `3` exactly as 13a–13c are, depend on no build, and appear under the heading `Python packages`.

This is the catch-all task and ships last, because it documents what the other tasks built.

### Targets

- `docs/development.md` — `## 5. Verifying a change`, gate 13's paragraphs.
- `ROADMAP.md` — `## Scene products`, the `GraphScene` row.

**Work:**

- [ ] **Re-derive the readers first.** Before retitling, run `git grep -n 'Gate 13 — the Python docs-retrieval service' -- ':!harness-runs'`. Any hit outside `docs/development.md` that cites the bold lead as an anchor is repointed in this same edit. The register predicts none.
- [ ] **Gate 13's lead paragraph** in `docs/development.md`:
  - Retitle `**Gate 13 — the Python docs-retrieval service.**` as `**Gate 13 — the Python packages.**`.
  - Open it with one sentence saying that the gate holds each package in the wrapper's table to the same bar: `docs-retrieval-service/` through 13a–13d and `graphscene/` through 13e–13g.
  - Keep the 13a–13d text as it is. After 13d's sentence, add **13e** `bash scripts/python-service.sh --package graphscene lint`, **13f** `… typecheck` and **13g** `… test`. Say that 13g runs the library's import-boundary test, that none of the three depends on gate 2's build, and that their `BLOCKED` grading is the one this paragraph already states for exit `3`.
  - Each command an adopter or maintainer is meant to run stays in its own fenced block, one per line (`harness-runs/lessons.md` → *Adopter-facing documentation*, first rule). A command named inline as a leg's definition, as 13a–13d already are, stays inline.
- [ ] **The closing paragraph of gate 13**, which ends *"so a later Python package joins the same wrapper as one more row rather than as a second wrapper"*. Add that `graphscene` is that second row, and that it has no console script and no compose project, so `run` and `container-test` on it exit `2`. In the same paragraph, note that `graphscene`'s pytest also carries `-p no:cacheprovider`, beside the existing sentence about `docs-retrieval-service`'s.
- [ ] **`ROADMAP.md`'s GraphScene row.** Change the status cell from `Open` to `In progress`. Extend the description in the form the `## Security and containment` rows use: *Shipped:* the library skeleton at `graphscene/`, with no engine code, its import boundary enforced by its own test, and gated by gate 13's legs 13e–13g. *Left:* the engine, the walker's port onto it, and the harness-side package. Keep the existing `docs/flow-graph-walker.md` link.

**Verification:**

- `git grep -n 'Python docs-retrieval service' -- docs/development.md` returns no hit.
- Derivation entries A and B of the story index's `## Scope register`, re-run verbatim after this edit, output only files the register names (⊆ the register rows).
- The 13e–13g sentences name exactly the three commands Task 3's arms run, and the heading text `Python packages` matches Task 3's `gate_header` title.
- Neither file gains an absolute machine path or a roadmap deferral number.
