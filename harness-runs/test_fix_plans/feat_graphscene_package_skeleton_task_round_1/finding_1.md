### 1. Sort the `fakes` import after the `devscene_docs_retrieval` imports in seven service test files

**Site:** `docs-retrieval-service/tests/`, the first-party import block of each of these seven files. In each one the line `from fakes import …` comes directly before the first `devscene_docs_retrieval` import (the line numbers are hints only):

| File | The misplaced line (grep-verified) | First import it must follow / where it goes |
|---|---|---|
| `docs-retrieval-service/tests/test_service.py` | `from fakes import FakeSession, InMemoryDocStore, doc_chunk` (~line 19) | after `from devscene_docs_retrieval.stubs import RETRIEVAL_STUB_ENV`, before `from model_cache import plant_model_files` |
| `docs-retrieval-service/tests/test_http_app.py` | `from fakes import FakeSession, InMemoryDocStore, doc_chunk` (~line 18) | after the last `from devscene_docs_retrieval…` import of the block (`from devscene_docs_retrieval.service import Answer, answer`) |
| `docs-retrieval-service/tests/test_mcp_parity.py` | `from fakes import FakeSession` (~line 29) | after `from devscene_docs_retrieval.wire import SEARCH_TOOL_NAME`, before `from ts_bridge import ts_fixture` |
| `docs-retrieval-service/tests/test_search.py` | `from fakes import InMemoryDocStore, doc_chunk` (~line 17) | after the closing `)` of the multi-line `from devscene_docs_retrieval.search import (…)` (the block's last import) |
| `docs-retrieval-service/tests/test_refresh.py` | `from fakes import InMemoryDocStore, doc_chunk` (~line 20) | after `from devscene_docs_retrieval.stubs import RETRIEVAL_STUB_ENV, resolve_models` |
| `docs-retrieval-service/tests/test_self_check.py` | `from fakes import InMemoryDocStore` (~line 18) | after `from devscene_docs_retrieval.stubs import RETRIEVAL_STUB_ENV`, before `from model_cache import plant_model_files` |
| `docs-retrieval-service/tests/test_mcp_shutdown.py` | `from fakes import EMPTY_REFRESH, FakeSession` (~line 24) | after `from devscene_docs_retrieval.wire import SEARCH_TOOL_NAME` |

**Failing test:** none — 13a Python lint (the `ruff check` leg; the `ruff format --check` leg passed: "42 files already formatted")

**Class:** Broken contract

**Failure:** If the running program `scripts/run-gates.sh` runs gate 13a (`bash scripts/python-service.sh lint`, whose first leg is `ruff check` in `docs-retrieval-service/`), then ruff reports the import block of the service tests as unsorted — "help: Organize imports … Found 7 errors. [*] 7 fixable with the `--fix` option." — and the gate exits 1, failing `commands.test` ("run-gates: 1 failed, 29 passed / - 13a Python lint").

**Failure quoted from the log** (`harness-runs/test_run_logs/feat_graphscene_package_skeleton/task_round_1.log`, gate `test`, section `== gate 13 — Python packages`):

```
  FAIL  13a Python lint (exit 1, 1 s)
        36 | |     open_session,
        37 | |     parse_arguments,
        38 | | )
        39 | | from devscene_docs_retrieval.store import DATABASE_URL_ENV, DIMENSIONS_META_KEY, DocStore
        40 | | from devscene_docs_retrieval.stubs import RETRIEVAL_STUB_ENV
        41 | | from model_cache import plant_model_files
        42 | | from ts_bridge import run_bridge
           | |________________________________^
        43 |
        44 |   DATABASE_URL = "postgresql://user:secret@db.invalid/index"
           |
        help: Organize imports
           |
        18 |
           - from fakes import FakeSession, InMemoryDocStore, doc_chunk
        19 | from devscene_docs_retrieval import service, wire
        --------------------------------------------------------------------------------
        39 | from devscene_docs_retrieval.stubs import RETRIEVAL_STUB_ENV
        40 + from fakes import FakeSession, InMemoryDocStore, doc_chunk
        41 | from model_cache import plant_model_files
           |
        
        Found 7 errors.
        [*] 7 fixable with the `--fix` option.
        42 files already formatted
```

The log prints the full diagnostic only for the last error (it is `docs-retrieval-service/tests/test_service.py`: its `DATABASE_URL = "postgresql://user:secret@db.invalid/index"` line and its `from ts_bridge import run_bridge` import match the quoted context exactly). The other six errors are cut off by the log tail; they are identified below from the current tree.

**Diagnosis.** Class: *new this round* in the sense that this is round 1 and no earlier log exists — there is nothing to compare against.

- Gate 13a's `lint` sub-command (`scripts/python-service.sh` → `lint)`) runs `uv run --frozen --no-sync --no-cache ruff check` from `docs-retrieval-service/` (the default package; the GraphScene lint leg, 13e, passed). Ruff there reads `docs-retrieval-service/pyproject.toml`: `[tool.ruff]` `src = ["src", "tests"]` and `[tool.ruff.lint]` `select = ["E", "F", "I", "B", "UP"]`. The `I` rules are isort.
- With `src = ["src", "tests"]`, both `devscene_docs_retrieval` (`src/devscene_docs_retrieval/`) and `fakes` (`tests/fakes.py`) — as well as `model_cache` and `ts_bridge` (`tests/model_cache.py`, `tests/ts_bridge.py`) — are first-party. Isort orders modules alphabetically within that section: `devscene_docs_retrieval…` < `fakes` < `model_cache` < `ts_bridge`. Each of the seven files puts `from fakes import …` *first* in the block, ahead of `devscene_docs_retrieval`, which is exactly the move ruff's help shows (remove at the top, insert after the last `devscene_docs_retrieval` line).
- A grep of `docs-retrieval-service/tests/` for `from fakes import` returns exactly seven files — `test_http_app.py`, `test_mcp_parity.py`, `test_mcp_shutdown.py`, `test_refresh.py`, `test_search.py`, `test_self_check.py`, `test_service.py` — and every one has the same misplacement: seven files, seven errors, matching "Found 7 errors".
- None of these files, nor `docs-retrieval-service/pyproject.toml`, is touched by this branch (their last commit is `650cd4a8`, before this branch's Task 1); the branch's GraphScene work does not change how ruff classifies these imports. The installed ruff (`.venv`, `ruff-0.16.9`) matches `docs-retrieval-service/uv.lock` (`ruff` `0.16.9`), so this is not a stale environment. Why the gate did not catch this before this branch is not established from the tree; the fix is the same either way, and it is in the tree, so it is fixable here. No sandbox-refusal signature appears in the log.

**Fix.** In each of the seven files, move the single `from fakes import …` line (unchanged, same imported names) from the top of the first-party import block to immediately after the block's last `devscene_docs_retrieval` import — so it sits before `from model_cache import …` / `from ts_bridge import …` where the file has those, and otherwise ends the block. Do not add or remove a blank line: the block stays one contiguous first-party section, followed by the existing blank line(s) before the module body. Change no other line, no imported name and no test.

- [ ] `docs-retrieval-service/tests/test_service.py`
- [ ] `docs-retrieval-service/tests/test_http_app.py`
- [ ] `docs-retrieval-service/tests/test_mcp_parity.py`
- [ ] `docs-retrieval-service/tests/test_search.py`
- [ ] `docs-retrieval-service/tests/test_refresh.py`
- [ ] `docs-retrieval-service/tests/test_self_check.py`
- [ ] `docs-retrieval-service/tests/test_mcp_shutdown.py`

Do not change `docs-retrieval-service/pyproject.toml`'s `[tool.ruff]` settings (for example, dropping `"tests"` from `src` or disabling `I`) to make the gate pass: that weakens the lint gate rather than fixing the files.
