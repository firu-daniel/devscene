### 4. Gate 13's cache sentence in `docs/development.md` still lists only two packages as writing no pytest cache

**File:** `docs/development.md` → **Gate 13 — the Python packages.**, the paragraph opening "Without the variable the script prints `SKIPPED 13d`" — "and `graphscene`'s `addopts` carries it too (`scripts/python-service.sh` → `WHERE IT WRITES`)"

**Problem.** The branch added `-p no:cacheprovider` to `devscene-runtime/pyproject.toml` → `[tool.pytest.ini_options]`. It also updated the sentence this paragraph cites, `scripts/python-service.sh` → `WHERE IT WRITES`, which now reads "pytest writes no `.pytest_cache` for `docs-retrieval-service`, `graphscene` or `devscene-runtime`". The paragraph itself still names only `docs-retrieval-service` and `graphscene`. It now lists fewer packages than the header it cites.

**Fix.** In that sentence, replace

"and `graphscene`'s `addopts` carries it too (`scripts/python-service.sh` → `WHERE IT WRITES`)"

with

"and `graphscene`'s and `devscene-runtime`'s `addopts` carry it too (`scripts/python-service.sh` → `WHERE IT WRITES`)"

Leave the rest of the paragraph unchanged. This is a prose edit, and no test runs for it.
