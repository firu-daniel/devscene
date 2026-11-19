### 1. Five durable sites say pytest writes an in-tree `.pytest_cache`, but `docs-retrieval-service` turns pytest's cache off

**File:** `scripts/python-service.sh` (header, `WHERE IT WRITES.`): "`.venv`, `.ruff_cache`, `.mypy_cache` and `.pytest_cache` sit under the package". The same claim appears at four more sites, listed under **Fix**.

`docs-retrieval-service/pyproject.toml` → `[tool.pytest.ini_options]` sets `addopts = "-p no:cacheprovider -rs"`. That disables pytest's cache provider, so no gate-13 leg and no hand run of `bash scripts/python-service.sh test` ever writes `docs-retrieval-service/.pytest_cache`. The branch nevertheless describes `.pytest_cache` as one of the directories the wrapper keeps in the package directory. It says so in the wrapper header, in `docs/development.md` (the gate-13 paragraph and the gate-6 exclusion sentence), in `scripts/check-machine-paths.sh`'s `THE EXCLUDED DIRECTORIES.` paragraph and in the root `.gitignore` comment.

The exclusion and the ignore rule cause no harm. They are a reasonable backstop for a later table package whose `pyproject.toml` does not disable the cache. The prose, however, describes a write that does not happen. The person affected is the maintainer who adds the next table row: they read that pytest's cache already lands in-tree for the existing package, and they conclude that their own package needs no thought about it either way. No command fails, so this is a Should Fix. It states the project falsely and gives no step to follow.

**Fix:** reword each site so `.pytest_cache` is a backstop, not a write the existing package makes. Leave the `--exclude-dir=.pytest_cache` flag, the `.gitignore` rule and the `cli/test/check-machine-paths.test.mjs` case as they are.

1. `scripts/python-service.sh`: replace the first two lines of the `WHERE IT WRITES.` paragraph:
   ```
   # WHERE IT WRITES. `.venv`, `.ruff_cache`, `.mypy_cache` and `.pytest_cache` sit under the package
   # directory: per checkout by construction, ignored by the root `.gitignore`, and skipped by gate 6a.
   ```
   with:
   ```
   # WHERE IT WRITES. `.venv`, `.ruff_cache` and `.mypy_cache` sit under the package directory: per
   # checkout by construction, ignored by the root `.gitignore`, and skipped by gate 6a. pytest writes
   # no `.pytest_cache` for `docs-retrieval-service` (its `pyproject.toml` `addopts` carries
   # `-p no:cacheprovider`); a row whose package leaves it on gets one there, covered the same way.
   ```
2. `docs/development.md`, the gate-13 paragraph that begins "**Each Python package's environment and tool caches live in that package's directory**":
   - Replace "and pytest's `.pytest_cache` sits there too (`scripts/python-service.sh` → `WHERE IT WRITES`)" with "while `docs-retrieval-service`'s pytest writes no cache at all, because its `pyproject.toml` `addopts` carries `-p no:cacheprovider` (`scripts/python-service.sh` → `WHERE IT WRITES`)".
   - Replace "the root `.gitignore` keeps all four directories out of every commit, and gate 6a skips them" with "the root `.gitignore` keeps those three, and the `.pytest_cache` a later package's pytest may write, out of every commit, and gate 6a skips all four".
3. `docs/development.md`, the gate-6 sentence that begins "`--exclude-dir=.venv`, `--exclude-dir=.mypy_cache`": replace "and `.pytest_cache` the test runner's." with "and `.pytest_cache` the test runner's, where a package's pytest writes one; `docs-retrieval-service` turns it off with `-p no:cacheprovider`, so that flag is a backstop for a later package."
4. `scripts/check-machine-paths.sh`, `THE EXCLUDED DIRECTORIES.` paragraph: after "so the exclusion holds for every table package." add the sentence "`.pytest_cache` is a backstop: `docs-retrieval-service` turns pytest's cache off (`-p no:cacheprovider`), and a later package may not." Re-wrap the comment to the paragraph's width.
5. `.gitignore`: replace the comment
   ```
   # scripts/python-service.sh keeps each package's environment (.venv) and tool caches (.mypy_cache,
   # .pytest_cache, .ruff_cache) inside the checkout; none of these is ever committed.
   ```
   with
   ```
   # scripts/python-service.sh keeps each package's environment (.venv) and tool caches (.mypy_cache,
   # .ruff_cache, and .pytest_cache where a package's pytest writes one) inside the checkout; none of
   # these is ever committed.
   ```

This fix edits only comments and prose and touches no test file, so it runs no test. The full suite runs later, in the Run gates phase.
