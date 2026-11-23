# The `devscene-flow-host` layer

> **Read this when:** the change you are implementing or reviewing lands under `devscene-flow-host/` — the package `devscene_flow_host`, its `pytest` suite, its `pyproject.toml` or its `uv.lock`. **Skip when:** it lands in another layer; GraphScene itself is `.claude/context/graphscene.md`, and the rules that span every layer — the Python stack, the testing bar and the commit-message policy among them — are `.claude/context/conventions.md`, which this document assumes has been read.

**Purpose.** The rules this layer's implementer and its reviewer both read before they start.

## What this layer is, and what it is not

- **It is the harness's GraphScene host, imported as `devscene_flow_host`.** What belongs in it, what goes to its own `devscene`-prefixed package and what goes to `graphscene/` instead is owned by `.claude/context/conventions.md` → `## The layers` and `### Where a new responsibility goes` (`devscene-flow-host/README.md` → `## What it is`; `devscene-flow-host/src/devscene_flow_host/__init__.py` module docstring). This layer's consequence: a change that is useful without DevScene, or a DevScene Python integration that does not feed GraphScene, has drifted out of this layer.
- **It stays in this repository and is never shipped to an adopter**, a rule `.claude/context/conventions.md` → `## The layers` owns together with what it bars in `cli/templates/` and `plugin/` (`devscene-flow-host/README.md` → `## What it is`).
- **Source lives under `devscene-flow-host/src/devscene_flow_host/`, tests under `devscene-flow-host/tests/`.** The wheel packages `src/devscene_flow_host` and nothing else (`devscene-flow-host/pyproject.toml` → `[tool.hatch.build.targets.wheel]`). File naming follows the always-loaded file's **Python source module** and **Python test suite** rows.

## What it may depend on

- **A module under `devscene-flow-host/src/devscene_flow_host/` imports only the standard library, `devscene_flow_host` itself and the distributions `[project] dependencies` declares.** Static `import`, absolute `from … import` and a constant-name `importlib.import_module` / `import_module` / `__import__` call are all checked (`devscene-flow-host/tests/test_boundary.py` → `scan`, `allowed_names`; `devscene-flow-host/README.md` → `## What it may depend on`).
- **This layer's consequence of the GraphScene boundary**, which `.claude/context/conventions.md` → `## The layers` owns: a name this package needs from GraphScene is reached through `graphscene`'s public surface, so where it is missing the change is to `graphscene.__all__`, made in the `graphscene` layer, never a submodule import here (`devscene-flow-host/tests/test_boundary.py` → `_names_from_root`, `test_rule_b_flags_a_graphscene_submodule`).
- **`graphscene` stays an editable path source on `../graphscene`** (`devscene-flow-host/pyproject.toml` → `[tool.uv.sources]`; pinned by `devscene-flow-host/tests/test_graphscene_dependency.py` → `test_the_manifest_sources_graphscene_from_the_editable_sibling`), so this package imports the checkout's own `graphscene/src/graphscene/` (`test_graphscene_imports_from_this_checkouts_sibling`). When the lock must move is owned by `.claude/context/conventions.md` → `## The layers` and `## What accompanies a new unit of each kind`.
- **`devscene-flow-host/uv.lock` moves only through a re-lock** — `bash scripts/python-service.sh --package devscene-flow-host lock` — never by hand edit (`devscene-flow-host/tests/test_graphscene_dependency.py` → `_RELOCK` and the module docstring's *"only a re-lock moves them"*; `devscene-flow-host/README.md` → `## The lock follows GraphScene`).
- **A declared dependency whose import name differs from its normalised PEP 508 name gets an entry in `_IMPORT_NAMES`, keyed by that normalised name, when it is added** (`devscene-flow-host/tests/test_boundary.py` → the comment above `_IMPORT_NAMES`). Without it the boundary test flags every import of that dependency.
- **Tooling goes in the `dev` dependency group, never in `[project] dependencies`** (`devscene-flow-host/pyproject.toml` → `[dependency-groups]`): every runtime dependency widens the boundary test's allowed set (`devscene-flow-host/tests/test_boundary.py` → `allowed_names`).

## Shared code and constants

- **The suite turns a PEP 508 requirement string into a dependency name in one place, `devscene-flow-host/tests/requirement_names.py` (`dependency_name`)**: lower-cased, `-` as `_`. A test needing that normalisation imports it rather than writing another (`devscene-flow-host/tests/requirement_names.py` → *"The rule this module exists to enforce"*; imported by `test_boundary.py` and `test_graphscene_dependency.py`).
- **A name the package exports is listed in the package root's `__all__`** (`devscene-flow-host/src/devscene_flow_host/__init__.py` → `__all__`).
- **A module states the rule it holds in its docstring**, as the package root does (`devscene-flow-host/src/devscene_flow_host/__init__.py` → *"The rule: this package imports only"*).
- The stack's names and settings — `ruff`, `mypy` `strict` over `src` and `tests`, `pytest` options, every command through `scripts/python-service.sh` — are owned by `.claude/context/conventions.md` → `## The stack, in the words the rules below use`; this package's own copy is `devscene-flow-host/pyproject.toml` → `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`.

## Tests — what "done" means here

- **Runner:** `pytest` over `devscene-flow-host/tests/`, as plain module-level `test_*` functions with type-annotated signatures, since `mypy` `strict` covers `tests` (`devscene-flow-host/tests/test_boundary.py`; `devscene-flow-host/pyproject.toml` → `[tool.mypy]`). The header rule and the no-fixture-in-checkout rule are owned by `.claude/context/conventions.md` → `## The testing bar`.
- **A scanner or checker is tested against planted input under `tmp_path`, one case per rule it enforces, plus one clean case, plus one case against the real package** (`devscene-flow-host/tests/test_boundary.py` → `_plant`, `test_a_clean_module_produces_no_violation`, `test_rule_a_flags_a_static_import_outside_the_allowed_set`, `test_the_real_package_stays_inside_its_boundary`).
- **A test whose failure has a fixed remedy names the command in its assertion message** (`devscene-flow-host/tests/test_graphscene_dependency.py` → `_RELOCK`, used in the assertions of `test_the_lock_resolves_graphscene_from_the_path_with_its_declared_dependencies`).
- **One test file on its own**, run from the repository root as one plain command, with the path relative to `devscene-flow-host/`:

  ```
  bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py
  ```

  (`devscene-flow-host/README.md` → `## Running the toolchain`). A change reaching `devscene-flow-host/src/devscene_flow_host/**` or `devscene-flow-host/pyproject.toml` also runs the tree guard `tests/test_boundary.py` this way (`devscene.config.json` → `treeGuards`).
- **Lint and typecheck** are `bash scripts/python-service.sh --package devscene-flow-host lint` and `… typecheck`; the package is graded by gate 13's legs 13h–13j (`devscene-flow-host/README.md` → `## Running the toolchain`, `## Gating`; `docs/development.md` → **Gate 13**).

## What accompanies a new unit here

| New unit | What must land with it |
|---|---|
| A module under `devscene-flow-host/src/devscene_flow_host/` | A docstring stating the rule it holds; nothing to register for the boundary test, which scans every `.py` file under the package (`devscene-flow-host/tests/test_boundary.py` → `scan`, `rglob`). |
| A runtime dependency | Its `[project] dependencies` entry; an `_IMPORT_NAMES` entry where its import name differs (`devscene-flow-host/tests/test_boundary.py` → `_IMPORT_NAMES`); and a re-lock, `bash scripts/python-service.sh --package devscene-flow-host lock` (`devscene-flow-host/README.md` → `## The lock follows GraphScene`), because `provision` syncs and every gate 13 leg runs against the lock as it stands (`docs/development.md` → **Gate 13**, `uv run --frozen --no-sync`, `uv sync --frozen`). |
| A test file | The header `.claude/context/conventions.md` → `## The testing bar` requires. |
| A test-support module | Its own `<snake_case>.py` beside the tests, imported by module name, with a docstring stating its rule (`devscene-flow-host/tests/requirement_names.py`). |

## One example from this layer

> `devscene-flow-host/tests/test_boundary.py` computes the allowed import set from `pyproject.toml` rather than listing it: `allowed_names` is the standard library plus `devscene_flow_host` plus each declared dependency mapped through `_IMPORT_NAMES`. Declaring a dependency is what admits its import; importing an undeclared one fails `test_the_real_package_stays_inside_its_boundary`.

## Not determined

- Not settled by the code read, and owed by this layer's first module that carries behaviour or by a line in `devscene-flow-host/README.md`: the mandated logger and output surface, the error type and how it becomes an exit status; localization, theming and sizing accessors; shared UI components and an interactive-test attribute convention; a navigation module or route and screen registries; storage-key and environment-variable constants; wire-surface types and how a serialized field name relates to its Python attribute; which store is the source of truth for shared state and in what order a listener mirrors it.
- Whether `devscene-flow-host/tests/` may import beyond the package's boundary: `devscene-flow-host/tests/test_boundary.py` states *"`tests/` is not scanned"* under *"Deliberately not covered"*, and no source read states a rule for test imports. What would settle it: a line in `devscene-flow-host/README.md`.
- Whether a mocking aid may be used in this suite: owned by `.claude/context/conventions.md` → `## Not determined`. What would settle it: the line that entry names.
- Whether the `py.typed` marker in `devscene-flow-host/src/devscene_flow_host/` is a requirement or the package's current choice: no source read states it. What would settle it: a line in `devscene-flow-host/README.md`.

_Written by `/devscene:analyze` in `existing` mode, from `devscene-flow-host/README.md`, `devscene-flow-host/pyproject.toml`, `devscene-flow-host/src/devscene_flow_host/` (`__init__.py`, `py.typed`), `devscene-flow-host/tests/` (`requirement_names.py`, `test_boundary.py`, `test_graphscene_dependency.py`), `devscene.config.json` → `layers`, `treeGuards`, `docs/development.md` → **Gate 13**, the pre-rename `.claude/context/devscene-runtime.md` as harvested prose, and `.claude/context/conventions.md` as the vocabulary anchor; corrected by the review fix pass, which re-attributed the new-dependency row's re-lock clause to `devscene-flow-host/README.md` → `## The lock follows GraphScene` and `docs/development.md` → **Gate 13**; the never-shipped bullet cut to a citation of `.claude/context/conventions.md` → `## The layers` by hand._
