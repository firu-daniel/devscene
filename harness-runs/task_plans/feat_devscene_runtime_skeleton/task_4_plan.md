### Task 4 — Pin the `devscene-runtime` row, its refusals and the three-row `provision` and `check` in `cli/test/python-service.test.mjs`

**Goal:** Make the `cli` suite that drives `scripts/python-service.sh` from a throwaway fixture pin the wrapper's third row: its legs, its three refusals, its place in `provision`'s and `check`'s table order, and the unknown-package line that now lists three packages.

**Depends on:** Task 2, which extends the wrapper's table to `PACKAGES="docs-retrieval-service graphscene devscene-runtime"` with a `package_row` arm `devscene-runtime)` whose `row_console_script`, `row_compose_prefix` and `row_models_extra` are all empty. So, observably:
- `--package devscene-runtime lint|typecheck|test [path…]` calls `uv run --frozen --no-sync --no-cache ruff check` + `… ruff format --check` / `… mypy` / `… pytest [path…]` from `<repo>/devscene-runtime`, with `UV_PROJECT_ENVIRONMENT`, `RUFF_CACHE_DIR` and `MYPY_CACHE_DIR` under `<repo>/devscene-runtime/`.
- `--package devscene-runtime run …`, `container-test` and `sync --with-models` exit `2`, printing `python-service: package 'devscene-runtime' has no console script` / `… has no container tests` / `… has no models extra`, then the usage line, and call no `uv`.
- `provision` prints `python-service: provisioned docs-retrieval-service`, `… graphscene`, `… devscene-runtime`, in that order, one `uv sync --frozen --group dev` per row in its own directory.
- `check` prints one `python-service: check: <row> <leg> PASS|FAIL|BLOCKED` line per row and leg, rows in table order, `lint` then `typecheck`.
- The unknown-package line reads `python-service: unknown package '<dir>'; the packages are: docs-retrieval-service, graphscene, devscene-runtime`.

This task changes no wrapper behaviour; it pins what Task 2 landed.

### Targets

- `cli/test/python-service.test.mjs`

**Work:**

- [ ] **The fixture and the constants.** Add `const RUNTIME = 'devscene-runtime';` beside `PACKAGE` and `LIBRARY`; create `<repo>/devscene-runtime/` with its own one-line `pyproject.toml` in `buildFixture`, as `LIBRARY` gets; extend `UNKNOWN_PACKAGE_LINE` to the three-package list. Update the header's *"The table has two rows"* to three, and its rule sentence if it names the row count.
- [ ] **The legs and the refusals.** Run the existing `--package ${LIBRARY}` legs case and the refusal case over `RUNTIME` too — a loop over `[LIBRARY, RUNTIME]` rather than a copied case — asserting each row's own directory and four values, and each refusal's exact first line, the usage line and no `uv` call.
- [ ] **`provision` and `check` in table order.** `provision`'s stdout is the three `provisioned` lines in table order, one recorded sync per row at its own directory, and each row's `provision: <row> failed (exit 1)` line on failure. `checkLines` covers three rows; the all-provisioned case asserts the calls per row at each row's site; the partly provisioned and failing cases plant `PACKAGE` alone and expect `BLOCKED` for both other rows; the no-`uv` case plants all three. Let `checkLines` derive its row list from one `ROWS` constant, so the next row is one edit.

**Verification:**

- `npm test --workspace cli -- test/python-service.test.mjs` — this task's own test file — passes, run from the repository root as one plain foreground command.
- Each expected line is the literal the wrapper prints, written out in the test, never read back from the script (`.claude/context/conventions.md` → `## The testing bar`, *"Assert against the contract stated literally"*).
- No case reaches a real `uv` or `docker`: every call is the recording stub's, and `HOME` and `XDG_CACHE_HOME` stay empty.
