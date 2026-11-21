### Task 2 — Hold the layer direction with `import-linter` contracts in `pyproject.toml`, run from `tests/test_layers.py`

**Goal:** Make the layer direction Task 1 built a checked rule that travels with the library. Two `import-linter` contracts go in `graphscene/pyproject.toml`: a `layers` contract with `engine` and `adapters` as independent siblings, and a `forbidden` contract keeping `jsonschema` out of `model` and `engine`. A test, `graphscene/tests/test_layers.py`, runs those contracts against the real package and against planted packages that break each clause.

**Depends on:** Task 1, which creates the four layer subpackages under these exact import names: `graphscene.facade`, `graphscene.adapters`, `graphscene.engine` and `graphscene.model`. It also places `jsonschema` only in `graphscene.adapters.schema`. This task names those four modules in its contracts and changes no source module. If a contract fails against the real tree, the move in Task 1 is wrong, and the fix is not to loosen the contract.

**Where this task stops.** The README's description of the layers and of this test is **Task 3's**. Registering this test as a tree guard in `devscene.config.json` is **Task 4's**: per `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 8, a test that reads a tree of repository files registers itself, and Task 4 is the catch-all task that adds the entry. `tests/test_boundary.py` stays untouched. The contracts sit beside it and do not replace it.

**What 2.17 provides, read from the pinned package** (`graphscene/uv.lock` pins `import-linter` 2.17 and `grimp` 3.20; it is already in the `dev` group, so no `lock` or `provision` step is needed):

- `importlinter.cli.lint_imports(config_filename: str | None = None, …, no_cache: bool = False, no_logo: bool = False, …) -> int` returns `0` when every contract is kept. With `no_cache=True` it writes no `.import_linter_cache`. It inserts the working directory at `sys.path[0]`. The CLI spelling of the same switch is `--no-cache`.
- In a `layers` contract, `|` inside one entry declares independent siblings (`importlinter/contracts/layers.py` → `_INDEPENDENT_LAYER_DELIMITER`).
- A `forbidden` contract whose forbidden module is outside the root package raises *"The top level configuration must have include_external_packages=True when there are external forbidden modules."* unless `[tool.importlinter]` sets `include_external_packages = true` (`importlinter/contracts/forbidden.py` → `_validate_external_forbidden_modules`). A broken `forbidden` contract prints `<downstream> is not allowed to import <upstream>:`, followed by one `-   <importer> -> <imported> (l.<n>)` line per chain (`render_broken_contract`).

### Targets

- `graphscene/pyproject.toml` — the `[tool.importlinter]` section and its two contracts.
- `graphscene/tests/test_layers.py` (new) — the contract test.

**Work:**

- [ ] **`graphscene/pyproject.toml`**: add `[tool.importlinter]` with `root_package = "graphscene"` and `include_external_packages = true`. Add two `[[tool.importlinter.contracts]]` tables, each with an `id`, a `name` and a `type`:
  - `id = "graphscene-layers"`, `type = "layers"`, `layers = ["graphscene.facade", "graphscene.adapters | graphscene.engine", "graphscene.model"]`. That is one entry for the two siblings, never two stacked entries.
  - `id = "graphscene-jsonschema-in-adapters-only"`, `type = "forbidden"`, `source_modules = ["graphscene.model", "graphscene.engine"]`, `forbidden_modules = ["jsonschema"]`.

  Leave every other key in the file unchanged.
- [ ] **`test_layers.py` header and runner.** The module docstring opens *"The rule this file exists to enforce"*. It states the four layers, the downward direction, the sibling independence and the `jsonschema` confinement, and that the contracts live in `graphscene/pyproject.toml` so they travel with the library. It records the version the expected report lines were read from (`import-linter` 2.17). Its *"Deliberately not covered"* list names what `import-linter` cannot see: a module name computed at run time or passed to `importlib.import_module`, as `tests/test_boundary.py`'s docstring already lists for its own scan. A reviewer checks those by reading.
  - One private helper, `_lint(cwd: Path, pythonpath: Path | None) -> subprocess.CompletedProcess[str]`, runs `[sys.executable, "-c", <program>, str(_PYPROJECT)]` with `cwd=cwd`, `capture_output=True` and `text=True`. When `pythonpath` is set, it sets `PYTHONPATH` to `pythonpath` on a copy of `os.environ`. `<program>` calls `lint_imports(config_filename=sys.argv[1], no_cache=True, no_logo=True)` and exits with its result.
  - `_PYPROJECT` is `Path(__file__).resolve().parents[1] / "pyproject.toml"`, the **real** configuration, so every case grades the committed contracts and never a copy of them.
  - Every run is a subprocess, because an in-process run would find the `graphscene` that `sys.modules` already holds, not a planted one. Every `cwd` is under `tmp_path`, so no run can leave a cache in the checkout.
- [ ] **The real tree, and a clean planted tree.** `test_the_real_package_keeps_every_layer_contract` runs `_lint(tmp_path, None)` and asserts exit status `0`. It also asserts that `tmp_path / ".import_linter_cache"` does not exist afterwards, which proves `no_cache=True` is honoured. A private `_plant(root: Path, extra: dict[str, str]) -> Path` writes a minimal `graphscene` package under `root`: a root `__init__.py` that imports `graphscene.facade`, the four layer packages, and one module per layer. In the planted `adapters` module, `jsonschema` is imported. Each layer module imports only what its layer may. `extra` maps a module's relative path to one added import line. `test_a_clean_planted_package_keeps_every_contract` plants it with no `extra` and asserts exit status `0`.
- [ ] **A planted case per clause.** In `test_a_planted_violation_breaks_its_contract`, each case plants one forbidden import and asserts a non-zero exit status. It also asserts that the output carries the exact report line that names the importing and the imported module. Hand-read those lines from a first run of each planted case under 2.17 and write them into the case table, never computed by the test. The cases:
  - `model` importing `engine` (upward)
  - `model` importing `adapters` (upward)
  - `engine` importing `adapters` (sibling)
  - `adapters` importing `engine` (sibling)
  - `engine` importing `facade` (upward)
  - `engine` importing the package root `graphscene`, which reaches `facade` indirectly
  - `model` importing `jsonschema`
  - `engine` importing `jsonschema`

  `test_jsonschema_in_adapters_is_allowed` covers the allowed direction: the clean plant already imports it there, and the case asserts exit status `0` with an explicit `import jsonschema` in a second planted `adapters` module.
- [ ] **Keep the suite's toolchain rules.** The file uses plain `pytest` functions annotated `-> None`, `tmp_path` for every planted tree, no mocking, and full annotations for `mypy` `strict`. It adds no `pytest` plugin and changes no `addopts`.

**Verification:**

- Run this task's own test file from the repository root, one foreground command: `bash scripts/python-service.sh --package graphscene test tests/test_layers.py`. Every case passes and none is skipped.
- `commands.typecheck` exits zero (`ruff` and `mypy` `strict` over `src` and `tests`).
- Check that each planted case breaks for the reason it names, not for a configuration error. Its expected line is an `<importer> -> <imported>` report line, and no case's output contains `does not exist` or `include_external_packages`.
- After the test file runs, `git status --porcelain --ignored -- graphscene` lists no `.import_linter_cache`.
- `git diff -- graphscene/pyproject.toml` shows only the added `[tool.importlinter]` section and its contract tables.

**Deviations from plan:** Each planted case's expected text in `_VIOLATIONS` is the contract's `<downstream> is not allowed to import <upstream>:` header together with its `<importer> -> <imported> (l.<n>)` chain line, not the chain line alone, so the case also proves which contract clause broke. The `engine` → package-root case carries both chain lines (`graphscene.engine.rules -> graphscene (l.2)`, `graphscene -> graphscene.facade (l.1)`), which together prove the indirect reach to `facade`. All were hand-read from a first run under import-linter 2.17.
