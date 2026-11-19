### Task 4 — Pin the `graphscene` row, its two refusals and the two-row `provision` in `cli/test/python-service.test.mjs`

**Goal:** Bring the wrapper's suite in line with its two-row table. Each leg under `--package graphscene` has to be shown to run in `graphscene/` with that directory's four values. `run` and `container-test` on that row have to be shown to refuse with exit `2` and touch nothing. `provision` has to be shown to sync both rows, in table order, each in its own directory.

**Depends on:** Task 2, which changed `scripts/python-service.sh`. This task asserts these contracts, quoted from that task:
- `PACKAGES="docs-retrieval-service graphscene"`. The default package stays `docs-retrieval-service`.
- The unknown-package line is `python-service: unknown package '<dir>'; the packages are: docs-retrieval-service, graphscene`, followed by the usage line.
- `--package graphscene run …` prints `python-service: package 'graphscene' has no console script`, then the usage line, and exits `2`. `--package graphscene container-test` prints `python-service: package 'graphscene' has no container tests`, then the usage line, and exits `2`. Neither calls `uv`, and both refuse before `require_env` and before the `docker` probe.
- `provision` prints `python-service: provisioned docs-retrieval-service` and then `python-service: provisioned graphscene` on stdout. It runs `uv sync --frozen --group dev` once per row, in that row's directory. A failing sync prints `python-service: provision: <row> failed (exit <n>)` for that row and makes the run exit `1`.

The suite fails from Task 2's commit until this task lands.

### Targets

- `cli/test/python-service.test.mjs`

**Work:**

- [ ] **Fixture and constants.**
  - Add `const LIBRARY = 'graphscene';`. `buildFixture` creates `repo/graphscene/` with a minimal `pyproject.toml`, as it does for `PACKAGE`.
  - `UNKNOWN_PACKAGE_LINE` names both rows, `${PACKAGE}, ${LIBRARY}`.
  - `assertCalls` takes the package as an optional fourth argument defaulting to `PACKAGE`, and passes it to `expectedSite`. Every current call site keeps its meaning.
  - In the file header's rule paragraph, say that the table has two rows, and that a row with no console script or compose project refuses `run` / `container-test` with exit `2`.
- [ ] **The legs under `--package graphscene`.** In the existing provisioned-legs case, or a sibling case, plant `graphscene/.venv/pyvenv.cfg` with `plantVenv(LIBRARY)`. Run `lint`, `typecheck`, `test` and `test tests/a.py` under `['--package', LIBRARY]`. Assert each recorded call's argv, a `cwd` of `repo/graphscene`, and the four values under `repo/graphscene/` (`.venv`, `.ruff_cache`, `.mypy_cache`, `PYTHONDONTWRITEBYTECODE=1`). Finish with `assertNothingUnderHome`.
- [ ] **The two refusals.** Add a case that plants `graphscene`'s venv, then runs `['--package', LIBRARY, 'run', 'serve']` and `['--package', LIBRARY, 'container-test']`. Each exits `2`. Stderr's first line is the exact refusal line above, and its second starts with `USAGE_PREFIX`, with no third line. No `uv` call is recorded. Use the base `PATH` with the stub, so that `container-test`'s result is `2` whether or not the host has `docker`.
- [ ] **`provision` over two rows.** Rework `provision syncs the one row …`:
  - Assert the two-line stdout in table order.
  - Assert two recorded `sync --frozen --group dev` calls, the first with `PACKAGE`'s site and the second with `LIBRARY`'s.
  - Assert `assertNothingUnderHome`.
  - In the failing variant (`FAKE_UV_STATUS: '1'`), assert exit `1` and a failure line for each row.

  Rename the case to say *the rows* rather than *the one row*. In `provision takes no argument and no --package`, add `['--package', LIBRARY, 'provision']` to the refused set.

**Verification:**

- `npm test --workspace cli -- test/python-service.test.mjs` passes. This is the file this task edits (`## The test-run rule` point 3).
- The unknown-package case, the existing `OTHER_PACKAGE` refusal, still exits `2`, with the two-row package list in its first line.
- No case starts a real `uv` or `docker`. The stub records every `uv` call, and the refusal case passes on a host with or without `docker`.
