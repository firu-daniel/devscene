# The `docs-retrieval` layer

> **Read this when:** the change you are implementing or reviewing lands under `docs-retrieval-service/` — the opt-in Python docs-retrieval backend, its `pytest` suite, its compose stack and its images. **Skip when:** it lands in another layer — the default TypeScript backend under `cli/src/retrieval/` is the `cli` layer's (`.claude/context/cli.md`), and `graphscene/` has its own document. The rules that span every layer are in `.claude/context/conventions.md`, which this one assumes has been read.

**Purpose.** The rules this layer's implementer and its reviewer both read before they start.

## What this layer is, and what it is not

- **It is a second implementation of docs retrieval, answering the same `search_docs` wire as `cli/src/retrieval/`.** Each module that ports a TypeScript one names it in its header as *"a port of `cli/src/retrieval/<file>.ts`"* and names each departure from it, in a `Departures from …` paragraph or a `Departure from …` sentence. A behaviour difference not named there is a defect. (`docs-retrieval-service/src/devscene_docs_retrieval/store.py`, `service.py`, `mcp_server.py`, `search.py`; `docs-retrieval-service/README.md` → `**Deliberate wire differences.**`, `## The seam, as found`)
- **Byte parity with the TypeScript backend is the contract, asserted against the compiled code under `cli/dist`, never against a copy of it.** A parity case whose build or bridge is missing fails rather than skips, because a skipped parity case reads as a passing one (`docs-retrieval-service/tests/ts_bridge.py` header). A mismatch is first assumed to be a port defect and fixed in the module that owns the rule; one that traces to engine behaviour is recorded in `docs-retrieval-service/README.md` → `## The seam, as found`, never papered over by normalising either output or loosening the comparison (`docs-retrieval-service/tests/test_backend_parity_e2e.py` header).
- **It is not the place to change the wire.** The server name, tool name and permission string are quoted by `plugin/agents/*.md` and the CLI templates; they are defined once in `docs-retrieval-service/src/devscene_docs_retrieval/wire.py` (`DOCS_SERVER_NAME`, `SEARCH_TOOL_NAME`, `SEARCH_TOOL_PERMISSION`, `SEARCH_TOOL`), every other module imports them, and no file that quotes them is edited from this package (`wire.py` header).
- **It is not a query logger.** `queryLog.ts` is not ported: `answer()` writes no log record and reads no query-log variable; timing is exposed (`search_ms`, the `TIMING_LINE_PREFIX` stderr line), never recorded (`service.py` header; `mcp_server.py` → `TIMING_LINE_PREFIX`).
- **It reads `devscene.config.json` read-only, for `docs.root` and `layers[]` alone, and applies no `phases.docs` / `docs.retrieval` gate** (`service.py` → `load_service_config`, header).
- **The Markdown is the source of truth and the index is always rebuildable from it**; nothing stored is authoritative. A refresh never keeps a chunk the corpus no longer has, an embedder change discards every stored vector, and every refresh that wrote — and every index not marked `INDEX_STATE_REBUILT` — ends with `DocStore.rebuild_indexes` (`refresh.py` header, `refresh_index`).
- **Local only.** Every published compose port binds `127.0.0.1`, the compose credentials are throwaway, and `serve-http` defaults to `--host 127.0.0.1` (`docs-retrieval-service/compose.yaml` header; `cli.py` → `_configure_serve_http`).

## The stack, in the words the rules below use

- Python `>=3.11` (`requires-python`, mypy `python_version = "3.11"`, ruff `target-version = "py311"`); the service image runs CPython 3.12 (`docs-retrieval-service/pyproject.toml`, `docs-retrieval-service/Dockerfile`).
- `uv` with a committed `docs-retrieval-service/uv.lock`, `hatchling` build backend, `src/` layout, console script `devscene-docs-retrieval` → `devscene_docs_retrieval.cli:main`.
- Runtime: `fastapi` + `uvicorn` (HTTP), the `mcp` SDK's **low-level** `Server` (stdio), `psycopg` 3 async with `AsyncRawCursor`, `huggingface_hub`. The `models` extra carries `sentence-transformers>=4.0` and `torch`, CPU-only on Linux from the `pytorch-cpu` index (`pyproject.toml` → `[tool.uv.sources]`).
- Postgres 18 with `vector` (pgvector) and `pg_textsearch`, built in `docs-retrieval-service/postgres/Dockerfile`.
- Lint `ruff` with `select = ["E", "F", "I", "B", "UP"]` and `line-length = 100`; `mypy` `strict = true` over `src` **and** `tests`; `pytest` with `-p no:cacheprovider -rs` (`pyproject.toml`).

## Dependencies and imports

- **Imports of this package are absolute — `from devscene_docs_retrieval.<module> import …` — never relative** (every module under `docs-retrieval-service/src/devscene_docs_retrieval/`). Tests import their helpers by bare module name (`from fakes import …`, `from ts_bridge import …`, `from model_cache import …`).
- **`sentence_transformers` and `torch` are imported inside `models.load_models` alone**, so importing any module loads neither; (`models.py` header, `load_models`); the gate environment never installs the `models` extra (`docs-retrieval-service/pyproject.toml` comment above `[[tool.mypy.overrides]]`; `docs-retrieval-service/tests/test_models.py` header). A new heavy optional import follows the same rule.
- **Package presence is resolved with `importlib.util.find_spec`, never by importing** (`self_check.py` → `_resolves`).
- **A version floor on a dependency carries a comment naming the API that needs it** (`pyproject.toml` → `psycopg[binary]>=3.2`, `sentence-transformers>=4.0`).
- **The driver stays behind `DocStore`**: a package module other than `store.py` never imports `psycopg`, and every store access goes through the `DocStore` protocol, and `search.py` holds no SQL (`search.py` header).

## Single owners — keep each one single

- **SQL**: every statement lives in `store.py` → `statements`, character for character `store.ts`'s, bound with native `$1` placeholders through `AsyncRawCursor` — never rewritten into `%s`. Every value reaches SQL as a bound parameter; the spliced tokens are the ones the `store.py` header enumerates (checked integer column width, constant index, extension and table names), and adding one is a decision to state there (`store.py` header).
- **JavaScript string and number semantics**: `jscompat.py`. Every other module imports its helpers (`js_trim`, `utf16_slice`, `utf16_sort_key`, `js_to_fixed`, `json_stringify`, …) and never re-derives one; UTF-16 round trips use `surrogatepass` (`jscompat.py` header).
- **Outgoing JSON on the wire** is serialized by `jscompat.json_stringify`: every MCP message (`mcp_server.py` header) and every `POST /search` response (`http_app.py` → `_json`), because the stock serializers refuse a lone surrogate.
- **The answer path**: `service.answer()`. every entry point — `serve_mcp`, the HTTP app — answers through it; `POST /search` validates nothing but `mode`, every other refusal is `service.parse_arguments`' (`service.py`, `http_app.py` headers).
- **Store concurrency**: `RetrievalSession.lock` serialises every use of the one async connection; `answer()` takes it, `probe()` takes it itself and is not re-entrant, so `GET /health` never takes it (`service.py` → `RetrievalSession`, `answer`; `http_app.py` header).
- **Downloads**: `fetch_models` is the only code that reaches the network. No caller but `fetch_models` passes `allow_remote=True`, every other load passes `local_files_only`, every load names the pin in `MODEL_REVISIONS`, and `fetch-models` refuses under the stub (`models.py` → `load_models`, `fetch_models`; `service.py` header; `cli.py` → `_run_fetch_models`).
- **Exit statuses**: `cli.main` is the only place an anticipated failure becomes one — `0` success, `1` a `ServiceError` printed as one line `devscene-docs-retrieval: <message>` on stderr with no traceback, `2` a missing or unknown sub-command (`cli.py` header).
- **The stub variable**: `RETRIEVAL_STUB_ENV` in `stubs.py` is the only spelling of that name in the package and `_stub_env_value` its only read (`stubs.py` header).

## Registries

- `cli.py` → `SUB_COMMANDS` is the single source for usage text and dispatch; a sub-command is one `SubCommand` row and nothing else is edited to make it appear (`cli.py` header).
- `http_app.py` → `create_app` registers the HTTP routes; `wire.SEARCH_TOOL` is the one tool `serve_mcp` lists (`mcp_server.py` header).
- `self_check.py` → `SELF_CHECK_QUESTIONS` fixes the `self-check` lines and their order, a contract with `doctor`'s `retrieval-python-*` checks (`self_check.py` header).

## Constants, keys and environment variables

- **A constant is imported from its owner, never retyped**: wire names in `wire.py`; search constants (`DEFAULT_RESULTS`, `MAX_RESULTS`, `ABSTAIN_SCORE_THRESHOLD`, `ABSTAIN_MESSAGE`, `SEARCH_MODES`) in `search.py`; model ids, pins, `MODEL_VERSION`, `MANIFEST_NAME` in `models.py`; `PROG` in `cli.py`.
- **Values taken from the TypeScript side are not re-derived here.** `ABSTAIN_SCORE_THRESHOLD` comes from `search.ts` and is asserted against its export (`search.py` header; `docs-retrieval-service/tests/test_render_parity.py`).
- **Storage keys** — the `meta` table's keys and `index_state` values — are the `store.py` constants `DIMENSIONS_META_KEY`, `EMBEDDER_META_KEY`, `INDEX_STATE_META_KEY`, `INDEX_STATE_PENDING`, `INDEX_STATE_REBUILT`, and the table and index names `CHUNKS_TABLE` and the BM25 index constant beside them.
- **An environment variable this package defines is a `<NAME>_ENV` constant in the module that reads it**; a platform variable such as `XDG_CACHE_HOME` is read by its own name (`models.py`): `DATABASE_URL_ENV` (`store.py`), `MODEL_CACHE_ENV` (`models.py`), `RETRIEVAL_STUB_ENV` (`stubs.py`), `TEST_DATABASE_URL_ENV` (`docs-retrieval-service/tests/conftest.py`). Configuration reaches the service through an injected `environ` mapping where the reader is a function of config (`service.py` → `load_service_config`).
- **The model id is namespaced under `ID_NAMESPACE` (`py-st`) and encodes the precision**; a stored embedder id that differs forces a rebuild (`models.py` header).

## The wire

- **The MCP tool definition is `server.ts`'s, key for key**, so its serialized keys are the TypeScript ones (`inputSchema`, `additionalProperties`, `readOnlyHint`) written as literal mapping keys in `wire.SEARCH_TOOL`; the expected listing is never typed into a test, it is read from the running TypeScript server (`wire.py` header; `docs-retrieval-service/tests/test_mcp_parity.py` header).
- **An HTTP response is a dict literal whose keys equal the Python attribute names they read** — `best_rerank_score`, `search_ms`, `hits[].ref` … (`http_app.py` → `create_app`'s `search`). Responses stay dict literals: adding a model class or alias layer between them is a decision to state.
- **Nothing but the MCP transport writes to stdout under `serve-mcp`**; every refusal that precedes the transport is raised before it starts (`mcp_server.py` header).
- **`serverInfo.version` is `__version__`, kept equal to `pyproject.toml`'s `[project] version`** — bump both together (`docs-retrieval-service/src/devscene_docs_retrieval/__init__.py`).

## Errors and output

- **An anticipated failure — a refusal, a missing cache, an unreachable database — is raised as `ServiceError` and nothing else**; anything else is a bug and propagates with its traceback (`errors.py` header). A programming error in the store raises `ValueError`, the port of `store.ts`'s `internal(…)` (`store.py` header).
- **A `ServiceError` message is one line**: a driver message is flattened through `errors.one_line`, and a connection failure replaces the connection string with `<connection string>` — the URL is never quoted back (`errors.py` → `one_line`; `store.py` → `open_postgres_store`).
- **Diagnostics go through `print(…, file=sys.stderr)`; adding a logging module is a decision to state.** They are written with a fixed prefix: `devscene-docs: warning: <text>` from the server path, `devscene-docs-retrieval: warning: <text>` from `index` (`service.py`, `cli.py` → `_run_index`). A sub-command's result is one line on stdout.
- **Inside `self-check`, every exception in a check becomes that check's `FAIL` line**, never a traceback (`self_check.py` header).

## Testing — what "done" means here

- **Runner: `pytest` over `docs-retrieval-service/tests/`**, run through the wrapper. **The one command that runs a single test file of this layer, from the repository root:** `bash scripts/python-service.sh test tests/test_cli.py` — the path is relative to `docs-retrieval-service/` (`docs-retrieval-service/README.md` → `## Testing`). How it is run — one plain foreground command — is `.claude/context/conventions.md` → `## The testing bar`'s rule. The layer's gate legs are `bash scripts/python-service.sh lint`, `bash scripts/python-service.sh typecheck` and `bash scripts/python-service.sh test`; gate 13 grades them (`docs/development.md` → `## 5. Verifying a change`, **Gate 13**). Parity cases need `npm run build`'s `cli/dist` first.
- **The test-file header rule is owned by `.claude/context/conventions.md` → `## The testing bar`.** Here it takes the form of a module docstring stating *"The rule this file exists to enforce"* / *"The rule this module exists to enforce"*, and it binds test helpers as well as test files (`docs-retrieval-service/tests/test_http_app.py`, `test_models.py`, `test_lock.py`, `fakes.py`).
- **Tests are typed**: `mypy --strict` covers `tests`, so every test function carries its annotations (`-> None`) (`pyproject.toml` → `[tool.mypy]`).
- **Async code is driven with `asyncio.run(…)` inside synchronous test functions**; adding an async test plugin is a decision to state (`docs-retrieval-service/tests/test_http_app.py`, `test_backend_parity_e2e.py`).
- **Substitutes in use**: the shared fakes in `docs-retrieval-service/tests/fakes.py` (`InMemoryDocStore`, `FakeSession`), the `hash-v1` / `hash-v2` stubs selected through `RETRIEVAL_STUB_ENV`, a planted weight cache from `docs-retrieval-service/tests/model_cache.py` (`plant_model_files`), and `pytest`'s `monkeypatch` for environment and attributes. **No test needs model weights or a network** (`docs-retrieval-service/README.md` → `## Testing`; `fakes.py`, `model_cache.py`).
- **The no-fixture-inside-the-checkout rule is owned by `.claude/context/conventions.md` → `## The testing bar`.** Here corpora and caches go under `tmp_path` or the system temp directory and are removed on every exit path (`docs-retrieval-service/tests/conftest.py`, `ts_bridge.py`, `test_corpus.py` headers).
- **A case that needs a real Postgres is marked `container`** — by module-level `pytestmark` when every case needs it, by its own decorator otherwise — runs only against `DEVSCENE_DOCS_RETRIEVAL_TEST_DATABASE_URL`, skips loudly when that is unset, and uses a throwaway database dropped on every exit path (`conftest.py` → `pytest_collection_modifyitems`, `_throwaway_database`; `docs-retrieval-service/tests/test_launcher_e2e.py` header). Those cases run in `bash scripts/python-service.sh container-test`.
- **Expected literals are hand-written from reading the TypeScript, printed by Node for the same JS expression and annotated `# JS: <expression>` beside the case, or compared against the running TypeScript through `run_bridge`** — never computed by the port under test (`test_chunk.py`, `test_search.py`, `test_jscompat.py` headers). Reading a TypeScript source file or `uv.lock` instead of behaviour is a last resort with its reason written in the header (`test_store_statements.py`, `test_lock.py`).
- **No duration is asserted**: `search_ms` is checked for presence and type only (`test_service.py`, `test_http_app.py` headers).

## What accompanies a new unit of each kind

| New unit | What must land with it |
|---|---|
| A module under `docs-retrieval-service/src/devscene_docs_retrieval/` | A header docstring with *"The rule this module exists to enforce"*; if it ports a TypeScript module, *"a port of `cli/src/retrieval/<file>.ts`"* and its departures. |
| A test file | Its *"The rule this file exists to enforce"* header, typed cases, the `container` marker if it needs Postgres. |
| A sub-command | Its `SubCommand` row in `SUB_COMMANDS`, the row pinned in `docs-retrieval-service/tests/test_cli.py` → `test_sub_command_table_rows`, and its row in `docs-retrieval-service/README.md`'s sub-command table. |
| An environment variable | Its `<NAME>_ENV` constant in the reading module and its row in `docs-retrieval-service/README.md` → `### Environment variables`. |
| A SQL statement | Its entry in `store.py` → `statements`, identical to `store.ts`'s, compared in `docs-retrieval-service/tests/test_store_statements.py`. |
| A runtime dependency | Its `pyproject.toml` entry with the floor's reason, the re-locked `uv.lock`, and its import name in `self_check.py` → `BASE_PACKAGES` (or `MODEL_PACKAGES` for the `models` extra) so `self-check`'s `packages` line grades it. |
| A departure from the TypeScript backend | Its entry in the module header's `Departures from …` paragraph or `Departure from …` sentence, and in `docs-retrieval-service/README.md` → `## The seam, as found` or `**Deliberate wire differences.**`. |
| A model pin bump | `EMBEDDING_REVISION` / `RERANK_REVISION` together with `MODEL_VERSION` in `docs-retrieval-service/src/devscene_docs_retrieval/models.py`, and the pin table in `docs/retrieval.md` → **Models.** The cross-backend half — the TypeScript pins moving with these where both move — spans two layers and belongs to `.claude/context/conventions.md` (source: `docs/development.md` → **Model pins and the drift notice.**); see `## Not determined`. |
| A version bump | `__version__` and `pyproject.toml`'s `version` together. |

## Commit messages

This layer has no rule of its own: `.claude/context/conventions.md` → `## Commit-message policy` governs.

## One real example — the shape a rule takes here

> An anticipated failure is a `ServiceError` with one line of message, and the sub-command raises it rather than exiting; `cli.main` alone turns it into exit `1`.
>
> ```python
> def _run_fetch_models(args: argparse.Namespace) -> int:
>     if stub_models_selected():
>         raise ServiceError(
>             f"fetch-models: refusing to download while {RETRIEVAL_STUB_ENV} is set, because a "
>             "stub run never downloads; unset it to fetch the real models"
>         )
> ```
>
> (`docs-retrieval-service/src/devscene_docs_retrieval/cli.py` → `_run_fetch_models`)

## Not determined

- Application-UI conventions — the localization, theming and sizing accessors, the test-attribute convention an interactive test locates elements by and its shared helper, and the navigation and screen registries — are not stated: this layer serves an MCP tool and a JSON HTTP endpoint and presents no user-facing surface. What would settle them: a change adding such a surface, raised as a `stale-rule` entry for a supervised `/analyze` re-run, per the same entry in `.claude/context/conventions.md` → `## Not determined`.
- Who may know the `meta` layout is not settled: `docs-retrieval-service/src/devscene_docs_retrieval/service.py`'s header says *"The store's meta layout is known here and to `store.py` only"*, while `refresh.py` → `refresh_index` imports and writes `EMBEDDER_META_KEY` and `INDEX_STATE_META_KEY`. What would settle it: that header naming `refresh.py` as a third owner, or the refresh's meta access moving behind `store.py`.
- The byte-parity contract between `cli/src/retrieval/` and this layer spans two layers, and `.claude/context/conventions.md` states no rule for it — in particular, whether a behaviour change to the TypeScript backend must land with its Python counterpart, and the model-pin case, which `docs/development.md` → **Model pins and the drift notice.** states (a bump moves the pins and `MODEL_VERSION` on both paths where both move) but no conventions document yet carries. What would settle it: the shared cross-layer document stating the parity rule and the both-backends pin rule, which this document then cites rather than restates.

_Written by `/devscene:analyze` in `existing` mode, from `docs-retrieval-service/`: pyproject, Dockerfiles, compose, README, the module headers under `src/` and the headers under `tests/`; plus the retrieval and development pages under `docs/`, `ARCHITECTURE.md`, `graphscene/README.md` and `.claude/context/conventions.md` for vocabulary._
