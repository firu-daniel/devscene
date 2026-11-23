### Task 5 — Document gate 13's `devscene-runtime` legs and its audited lock in `docs/development.md`, and record the package in `ROADMAP.md`

**Goal:** Make the documents of record say what this branch built: gate 13 holds a third package through legs 13h–13j, the wrapper's table has a third row with an editable path dependency on GraphScene, the nightly `uv-audit` job audits its lock, and the roadmap's GraphScene row names the harness-side package's skeleton as shipped.

**Depends on:** Tasks 1–4. Task 1's `devscene-runtime/` (import name `devscene_runtime`, one runtime dependency `graphscene` through `[tool.uv.sources] graphscene = { path = "../graphscene", editable = true }`, its boundary test `devscene-runtime/tests/test_boundary.py`); Task 2's wrapper row (no console script, no compose project, no `models` extra; refusing `run`, `container-test` and `sync --with-models` with exit `2`) and its `devscene-runtime/tests/test_graphscene_dependency.py`; Task 3's legs — `13h` `bash scripts/python-service.sh --package devscene-runtime lint`, `13i` `… typecheck`, `13j` `… test` — and its `uv-audit` step in `.github/workflows/supply-chain.yml`. This task changes none of them; it describes them. This is the catch-all task, so its implementer reads every configured layer's conventions document.

### Targets

- `docs/development.md`
- `ROADMAP.md`

**Work:**

- [ ] `docs/development.md` → **Gate 13 — the Python packages.** (scope register row 8): add `devscene-runtime/` through 13h–13j to the opening sentence; add the three legs' commands after 13g's in the same form, saying `13j` runs the package's boundary test and its dependency test, and that none of the three depends on gate 2's build; extend *"Every unit runs 13a, 13b, 13e and 13f's checks too"* with 13h and 13i.
- [ ] `docs/development.md` → the gate 13 closing paragraph (row 9): after *"`graphscene` is that second row; …"*, add that `devscene-runtime` is the third, with the same three refusals, and that its environment reads `graphscene` from the same checkout through an editable path source, so a change to `graphscene/pyproject.toml` → `[project] dependencies` re-locks `devscene-runtime` too, its command in its own fenced block — `bash scripts/python-service.sh --package devscene-runtime lock` — and `13j` fails until it is done.
- [ ] `docs/development.md` → § 8's job table, the `uv-audit` row (row 13): add `devscene-runtime/uv.lock` to *"What it audits"*. Change no other row or column.
- [ ] `ROADMAP.md` → `## Scene products`, the `GraphScene` row (row 6): append to its *Shipped* list the harness-side package's skeleton — `devscene-runtime/`, DevScene's own Python runtime with no behaviour yet, depending on GraphScene's public surface only, enforced by its own test and gated by gate 13's legs 13h–13j (link `devscene-runtime/README.md`) — and change *"Left: the walker's port onto the engine, and the harness-side package; …"* so the harness-side package is no longer named as left; the walker's port and the format-4 cutover stay. The row's status stays *In progress*.

**Verification:**

- Re-run the story index's derivation entries A–D verbatim: each command's output is still ⊆ the files named in the scope register's rows.
- Every command this task adds sits alone in its own fenced block, one per line (`harness-runs/lessons.md` → `## Adopter-facing documentation`, first rule), and each leg's command is the exact string Task 3 wrote into `scripts/run-gates.sh`.
- `docs/development.md` § 5's count — sixteen gates, nine unattended — is unchanged, and no paragraph outside rows 8, 9 and 13 changed.
- No sentence promises the layer, the conventions document or #418's work: those are the story index's manual-setup steps, not documented pending work.

**Deviations from plan:**
- The Verification bullet "no paragraph outside rows 8, 9 and 13 changed" also forbids touching the line right after § 8's job table, "`uv-audit`, once from `docs-retrieval-service/` and once from `graphscene/`:". That line introduces the step command and would be false once `.github/workflows/supply-chain.yml` runs the step from `devscene-runtime` as well (Task 3), and no derivation entry reaches it because it contains no `uv.lock`. Implemented as "`uv-audit`, once each from `docs-retrieval-service/`, `graphscene/` and `devscene-runtime/`:". No other line outside rows 8, 9 and 13 changed.
