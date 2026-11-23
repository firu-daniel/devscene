# The `devscene-runtime` layer

> **Read this when:** the change you are implementing or reviewing lands under `devscene-runtime/` — the package `devscene_runtime`, its `pytest` suite, its `pyproject.toml` or its `uv.lock`. **Skip when:** it lands in another layer; GraphScene itself is `.claude/context/graphscene.md`, and the rules that span every layer, the Python stack and the commit-message policy among them, are `.claude/context/conventions.md`, which this document assumes has been read.

**Purpose.** The rules this layer's implementer and its reviewer both read before they start.

## What this layer is, and what it is not

- **It is DevScene's own Python runtime, imported as `devscene_runtime`** (`devscene-runtime/README.md` → `## What it is`; `devscene-runtime/src/devscene_runtime/__init__.py` module docstring). Where its boundary with GraphScene sits is owned by `.claude/context/conventions.md` → `## The layers`.
- **It stays in this repository and is never shipped to an adopter:** the package stays outside `cli/package.json` → `files`, and adopters never import it (`devscene-runtime/README.md` → `## What it is`; `cli/package.json` → `files`).
- **Source lives under `devscene-runtime/src/devscene_runtime/`, tests under `devscene-runtime/tests/`.** The wheel packages `src/devscene_runtime` and nothing else (`devscene-runtime/pyproject.toml` → `[tool.hatch.build.targets.wheel]`). File naming follows the always-loaded file's **Python source module** and **Python test suite** rows.

## What it may depend on

- **A module under `devscene-runtime/src/devscene_runtime/` imports only the standard library, `devscene_runtime` itself and the distributions `[project] dependencies` declares.** Static `import`, absolute `from … import` and a constant-name `importlib.import_module` / `import_module` / `__import__` call are all checked (`devscene-runtime/tests/test_boundary.py` → `scan`, `allowed_names`). Its README states the rule and names that test as its enforcement (`devscene-runtime/README.md` → `## What it may depend on`).
- **This layer's consequence of the GraphScene boundary**, which `.claude/context/conventions.md` → `## The layers` owns: a name this package needs from GraphScene is reached through `graphscene`'s public surface, so where it is missing the change is to `graphscene.__all__`, made in the `graphscene` layer, never a submodule import here (`devscene-runtime/tests/test_boundary.py` → `_names_from_root`).
- **`graphscene` stays an editable path source on `../graphscene`** (`devscene-runtime/pyproject.toml` → `[tool.uv.sources]`; pinned by `devscene-runtime/tests/test_graphscene_dependency.py` → `test_the_manifest_sources_graphscene_from_the_editable_sibling`), so this package always imports the checkout's own `graphscene/src/graphscene/` (`test_graphscene_imports_from_this_checkouts_sibling`). When the lock must move is owned by `.claude/context/conventions.md` → `## The layers` and `## What accompanies a new unit of each kind`.
- **`devscene-runtime/uv.lock` moves only through a re-lock** — `bash scripts/python-service.sh --package devscene-runtime lock` — never by hand edit (`devscene-runtime/tests/test_graphscene_dependency.py` → `_RELOCK` and the module docstring's *"only a re-lock moves them"*; `devscene-runtime/README.md` → `## The lock follows GraphScene`).
- **A declared dependency whose import name differs from its normalised PEP 508 name gets an entry in `_IMPORT_NAMES`, keyed by that normalised name, when it is added** (`devscene-runtime/tests/test_boundary.py` → the comment above `_IMPORT_NAMES`). Without it the boundary test flags every import of that dependency.
- **Tooling goes in the `dev` dependency group, never in `[project] dependencies`** (`devscene-runtime/pyproject.toml` → `[dependency-groups]`), because a runtime dependency widens the boundary test's allowed set.

## Shared code and constants

- **The suite turns a PEP 508 requirement string into a dependency name in one place, `devscene-runtime/tests/requirement_names.py` (`dependency_name`)**: lower-cased, `-` as `_`. A test needing that normalisation imports it rather than writing another (`devscene-runtime/tests/requirement_names.py` → *"The rule this module exists to enforce"*; imported by `test_boundary.py` and `test_graphscene_dependency.py`).
- **The package root declares `__all__` with a `list[str]` annotation** (`devscene-runtime/src/devscene_runtime/__init__.py` → `__all__`); a name the package exports is added there.
- **A module states the rule it holds in its docstring**, as the package root does (`devscene-runtime/src/devscene_runtime/__init__.py` → *"The rule: this package imports only…"*).
- The stack's settings — `ruff` rule sets and line length, `mypy` `strict` over `src` and `tests`, `pytest` options — are owned by `.claude/context/conventions.md` → `## The stack, in the words the rules below use`; this package's own copy is `devscene-runtime/pyproject.toml` → `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`.

## Tests — what "done" means here

- **Runner:** `pytest` over `devscene-runtime/tests/`, as plain module-level `test_*` functions with type-annotated signatures, since `mypy` `strict` covers `tests` (`devscene-runtime/tests/test_boundary.py`, `devscene-runtime/pyproject.toml` → `[tool.mypy]`). The header rule and the no-fixture-in-checkout rule are owned by `.claude/context/conventions.md` → `## The testing bar`.
- **A scanner or checker is tested against planted input under `tmp_path`, one case per rule it enforces, plus one clean case, plus one case against the real package** (`devscene-runtime/tests/test_boundary.py` → `_plant`, `test_a_clean_module_produces_no_violation`, `test_rule_a_flags_a_static_import_outside_the_allowed_set`, `test_the_real_package_stays_inside_its_boundary`).
- **A test whose failure has a fixed remedy names the command in its assertion message** (`devscene-runtime/tests/test_graphscene_dependency.py` → `_RELOCK`, used in each assertion of `test_the_lock_resolves_graphscene_from_the_path_with_its_declared_dependencies`).
- **One test file on its own**, run from the repository root, with the path relative to `devscene-runtime/`:

  ```
  bash scripts/python-service.sh --package devscene-runtime test tests/<file>.py
  ```

  (`devscene-runtime/README.md` → `## Running the toolchain`). A change reaching `devscene-runtime/src/devscene_runtime/**` or `devscene-runtime/pyproject.toml` also runs the tree guard `tests/test_boundary.py` this way (`devscene.config.json` → `treeGuards`).
- **Lint and typecheck** are `bash scripts/python-service.sh --package devscene-runtime lint` and `… typecheck`; the package is graded by gate 13's legs 13h–13j (`devscene-runtime/README.md` → `## Running the toolchain`, `## Gating`; `docs/development.md` → **Gate 13**).

## What accompanies a new unit here

| New unit | What must land with it |
|---|---|
| A module under `devscene-runtime/src/devscene_runtime/` | A docstring stating the rule it holds; nothing to register for the boundary test, which scans every `.py` file under the package (`devscene-runtime/tests/test_boundary.py` → `scan`, `rglob`). |
| A runtime dependency | Its `[project] dependencies` entry, an `_IMPORT_NAMES` entry where its import name differs, and a re-lock (`devscene-runtime/tests/test_boundary.py` → `_IMPORT_NAMES`). |
| A test file | The header `.claude/context/conventions.md` → `## The testing bar` requires. |
| A test-support module | Its own `<snake_case>.py` beside the tests, imported by module name, with a docstring stating its rule (`devscene-runtime/tests/requirement_names.py`). |

## One example from this layer

> `devscene-runtime/tests/test_boundary.py` computes the allowed import set from `pyproject.toml` rather than listing it: `allowed_names` is the standard library plus `devscene_runtime` plus each declared dependency mapped through `_IMPORT_NAMES`. Declaring a dependency is what admits its import; importing an undeclared one fails `test_the_real_package_stays_inside_its_boundary`.

## Not determined

- Not settled by the code read, and owed by this layer's first module that carries behaviour or by a line in `devscene-runtime/README.md`: the mandated logger and output surface, the error type and how it becomes an exit status; localization, theming and sizing accessors; shared UI components and an interactive-test attribute convention; a navigation module or route and screen registries; storage-key and environment-variable constants; wire-surface types and how a serialized field name relates to its Python attribute; which store is the source of truth for shared state.
- Whether `devscene-runtime/tests/` may import beyond the package's boundary: `devscene-runtime/tests/test_boundary.py` states *"`tests/` is not scanned"* under *"Deliberately not covered"*, and no source states a rule for test imports. What would settle it: a line in `devscene-runtime/README.md`.
- Whether a mocking aid may be used in this suite: owned by `.claude/context/conventions.md` → `## Not determined`. What would settle it: the line that entry names.
- Whether the `py.typed` marker in `devscene-runtime/src/devscene_runtime/` is a requirement or the package's current choice: no source states it. What would settle it: a line in `devscene-runtime/README.md`.
- Reviewer finding not applied — C4, its second half only: moving the clause "nothing under `cli/templates/` or `plugin/` may depend on it" into `.claude/context/conventions.md` → `## The layers`. Reason: this dispatch writes only `.claude/context/devscene-runtime.md`; the clause is removed here and restated as this layer's own obligation. What would settle it: a dispatch of the shared cross-layer document adding that cross-layer rule.

_Written by `/devscene:analyze` in `existing` mode, from `devscene-runtime/README.md`, `devscene-runtime/pyproject.toml`, `devscene-runtime/uv.lock` (header), `devscene-runtime/src/devscene_runtime/` (`__init__.py`, `py.typed`), `devscene-runtime/tests/` (`requirement_names.py`, `test_boundary.py`, `test_graphscene_dependency.py`), `cli/package.json` → `files`, `devscene.config.json` → `layers`, `treeGuards`, `docs/development.md` → **Gate 13**, and `.claude/context/conventions.md` as the vocabulary anchor; corrected by the review fix pass (a repo-rooted path in `## What accompanies a new unit here`, a census clause dropped from `## Not determined`); corrected by the corpus fix pass (the restated GraphScene boundary cut to a citation, a rule over other layers' files restated as this layer's own obligation); corrected by a second corpus fix pass (the test-file row of `## What accompanies a new unit here` cut to a citation of the shared testing bar)._
