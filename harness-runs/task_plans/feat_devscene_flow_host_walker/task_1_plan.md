### Task 1 — Set the package's `records`, `host` and `commands` layers and hold them with `import-linter` contracts run from `tests/test_layers.py`

**Goal:** Give `devscene_flow_host` its three internal layers before any behaviour lands in them. Each layer is a subpackage whose `__init__.py` docstring states what it holds and what it may import. Two `import-linter` contracts in `devscene-flow-host/pyproject.toml` make the direction a checked rule, and `devscene-flow-host/tests/test_layers.py` runs those committed contracts against the real package and against planted packages that break one clause each, the way `graphscene/tests/test_layers.py` does for GraphScene.

**Where this task stops.** It adds no module with behaviour. `records/config.py` and `records/errors.py` are Task 2's, `records/ledger.py` Task 3's, `host/predicates.py` Task 4's, `host/store.py` Task 5's and `host/walking.py` Task 6's. Those tasks add modules and never edit the three `__init__.py` files this task writes, so every docstring here describes its layer's whole role, not a module list. The README's `## The layers` section is **Task 7's**. Registering `tests/test_layers.py` as a tree guard in `devscene.config.json` is **Task 8's**. Under `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 8, this test reads the package tree, so it registers itself, and Task 8 is the catch-all task that adds the entry. `tests/test_boundary.py` stays untouched, beside the contracts.

**What `import-linter` 2.17 provides** (`devscene-flow-host/uv.lock` pins `import-linter` 2.17, already in the `dev` group by #463, so no `lock` or `provision` step is needed). The facts below are as `refactor_graphscene_layers` read them for `graphscene/tests/test_layers.py`:

- `importlinter.cli.lint_imports(config_filename=…, no_cache=True, no_logo=True)` returns `0` when every contract is kept, writes no `.import_linter_cache` with `no_cache=True`, and inserts the working directory at `sys.path[0]`.
- A `forbidden` contract whose forbidden module is outside the root package needs `include_external_packages = true` under `[tool.importlinter]`.
- A broken contract prints `<downstream> is not allowed to import <upstream>:` and, for each chain, a line `- <importer> -> <imported> (l.<n>)`. A `forbidden` contract's chain line carries `-   ` instead.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/__init__.py` (new)
- `devscene-flow-host/src/devscene_flow_host/host/__init__.py` (new)
- `devscene-flow-host/src/devscene_flow_host/commands/__init__.py` (new)
- `devscene-flow-host/src/devscene_flow_host/__init__.py` — its module docstring only.
- `devscene-flow-host/pyproject.toml` — the `[tool.importlinter]` section and its two contracts.
- `devscene-flow-host/tests/test_layers.py` (new)

**Work:**

- [ ] **The three layer packages, each an `__init__.py` holding a docstring and nothing else.** Each states what the layer holds and opens its import rule with *"The rule:"*, as `graphscene/src/graphscene/model/__init__.py` does. Use the story index's `## Context` layer table, with no issue numbers:
  - `records`: reads the repository's records — `devscene.config.json`, the flow-progress ledger, and later the round and reviewer files — into plain values. The rule: it imports the standard library and `devscene_flow_host.records` only, **never `graphscene`**. It answers no GraphScene protocol.
  - `host`: answers GraphScene's protocols over those values — the `PredicateHost`, the walk's `StateStore`, the composed `Walker` — and holds the harness's rules over its records. The rule: it imports `records`, `graphscene` through its public surface only, and the standard library. It never imports `commands`.
  - `commands`: the command lines over the host. The rule: it may import `host`, `records`, `graphscene` through its public surface, and the standard library, and nothing imports it. It holds no module yet.
- [ ] **The package root's docstring** (`devscene_flow_host/__init__.py`). Keep the current paragraphs and the boundary rule word for word, and add one paragraph. It names the three layers, `commands` over `host` over `records`, and says that imports point down only, that only `host` and `commands` import `graphscene`, and that the layers are held by the contracts in `pyproject.toml` (`tests/test_layers.py`). It also says the package root exports nothing — `__all__` stays `[]`, because adopters never import this package — and that no module inside the package imports from the package root: each imports the defining module of what it needs. Leave `__all__: list[str] = []` as it is.
- [ ] **`pyproject.toml`**: add `[tool.importlinter]` with `root_package = "devscene_flow_host"` and `include_external_packages = true`. Then add two `[[tool.importlinter.contracts]]` tables, each with an `id`, a `name` and a `type`:
  - `id = "devscene-flow-host-layers"`, `type = "layers"`, `layers = ["devscene_flow_host.commands", "devscene_flow_host.host", "devscene_flow_host.records"]`.
  - `id = "devscene-flow-host-graphscene-outside-records"`, `type = "forbidden"`, `source_modules = ["devscene_flow_host.records"]`, `forbidden_modules = ["graphscene"]`.

  Leave every other key unchanged. Adding no dependency means no re-lock.
- [ ] **`tests/test_layers.py`: header, runner, the real tree and a clean plant.** The module docstring opens *"The rule this file exists to enforce"*. It states the three layers, the downward direction and `graphscene` kept out of `records`. It says the rule is the two committed contracts in `devscene-flow-host/pyproject.toml`, and records `import-linter` 2.17 as the version the expected lines were read from. Its *"Deliberately not covered"* list names a module name computed at run time or passed to `importlib.import_module`, which `import-linter` cannot see.
  - Mirror `graphscene/tests/test_layers.py`'s mechanism: `_PYPROJECT` is the real `pyproject.toml`, built off `__file__`. `_lint(cwd, pythonpath)` runs `[sys.executable, "-c", _PROGRAM, str(_PYPROJECT)]`, where `_PROGRAM` calls `lint_imports(config_filename=sys.argv[1], no_cache=True, no_logo=True)`. Every `cwd` is under `tmp_path`.
  - `_plant(root, extra)` writes a minimal `devscene_flow_host` package: a root `__init__.py` importing nothing, `records/__init__.py` with `records/core.py` (`import json`), `host/__init__.py` with `host/glue.py` (`import graphscene` and `import devscene_flow_host.records.core`), and `commands/__init__.py` with `commands/cli.py` (`import devscene_flow_host.host.glue`, `import devscene_flow_host.records.core`).
  - `test_the_real_package_keeps_every_layer_contract` runs `_lint(tmp_path, None)` and asserts exit `0` and no `tmp_path / ".import_linter_cache"`. `test_a_clean_planted_package_keeps_every_contract` asserts exit `0` for `_plant(tmp_path, {})`.
- [ ] **A planted case per clause**, in a parametrized `test_a_planted_violation_breaks_its_contract`. Each case adds one import line, asserts a non-zero exit, and asserts the output contains that case's exact expected text: the contract's `… is not allowed to import …:` header together with its chain line or lines, **hand-read from a first run of each case under 2.17 and written into the case table**, never computed by the test. Also assert that no case's output contains `does not exist` or `include_external_packages`. The cases:
  - `records/core.py` importing `devscene_flow_host.host.glue` (upward)
  - `records/core.py` importing `devscene_flow_host.commands.cli` (upward)
  - `host/glue.py` importing `devscene_flow_host.commands.cli` (upward)
  - `records/core.py` importing `graphscene` (the `forbidden` contract)

  Add `test_graphscene_in_host_and_commands_is_allowed`, which plants `import graphscene` in `commands/cli.py` too and asserts exit `0`. Plain `pytest` functions annotated `-> None`, `tmp_path` for every plant, no mocking.

**Verification:**

- Run this task's own test file from the repository root, as one foreground command: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_layers.py`. Every case passes and none is skipped.
- `commands.typecheck` exits zero (`ruff` and `mypy` `strict` over `src` and `tests`).
- The `forbidden` case's expected text names `graphscene` as the imported module. If `grimp` does not resolve the editable `graphscene` as an external package, that case fails with `does not exist` or passes with exit `0`. Either result is a stop to report, never a contract to loosen.
- `git status --porcelain --ignored -- devscene-flow-host` lists no `.import_linter_cache` after the run.
- `git diff -- devscene-flow-host/pyproject.toml` shows only the added `[tool.importlinter]` section and its two contract tables.
