### Task 5 — Extend `cli/test/check-machine-paths.test.mjs`'s excluded-places case to the four Python directories

**Goal:** Pin gate 6a's new exclusions. A `$HOME`-bearing file under a package's `.venv`, `.mypy_cache`, `.ruff_cache` or `.pytest_cache` prints nothing. The same text one directory away still prints.

**Depends on:** Task 2. It adds `--exclude-dir=.venv --exclude-dir=.mypy_cache --exclude-dir=.ruff_cache --exclude-dir=.pytest_cache` to `scripts/check-machine-paths.sh`'s `grep -rn` line, beside `--exclude-dir=__pycache__`. Grep matches each one against a directory's base name at any depth. This task tests that and changes no script.

### Targets

- `cli/test/check-machine-paths.test.mjs`

**Work:**

- [ ] In case `(b) the excluded places print nothing, …`, add four paths to its `silent` list: `docs-retrieval-service/.venv/pyvenv.cfg`, `docs-retrieval-service/.mypy_cache/3.12/mod.meta.json`, `docs-retrieval-service/.ruff_cache/0.1/cache` and `docs-retrieval-service/.pytest_cache/v/cache/nodeids`. Add a fifth at another package's path, `other-package/.venv/bin/activate`, so the case shows the exclusion is not tied to one package.
- [ ] In the same case, add `docs-retrieval-service/venv-notes.txt` beside the planted files, carrying the hit text and placed **outside** any excluded directory, and add its line to the expected printed list. This shows the exclusion is by directory name, not by package. Leave every other case and the header's rule untouched, except to add the four names to any sentence of the header that lists the excluded places.

**Verification:**

- `npm test --workspace cli -- test/check-machine-paths.test.mjs` passes, run from the repository root as one plain foreground command.
- Against a copy of `scripts/check-machine-paths.sh` under `harness-runs/scratch/` with the `--exclude-dir=.venv` flag removed, case `(b)` fails, naming the `.venv` lines. Check it on the copy, never by editing the script, and record the result in the return.
