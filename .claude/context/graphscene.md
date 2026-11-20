# The `graphscene` layer

> **Read this when:** the change you are implementing or reviewing lands under `graphscene/` — the GraphScene flow-graph navigation library, its `pytest` suite or its `pyproject.toml`. **Skip when:** it lands anywhere else, harness-side code that drives GraphScene included: that goes in its own distribution outside `graphscene/`, below. The rules that span every layer are in `.claude/context/conventions.md`, which this document assumes has been read.

**Purpose.** The rules this layer's implementer and its reviewer both read before they start.

## What this layer owns, and what it is not

- **It owns the generic library and nothing harness-specific.** Reading the harness's configuration, executing its agents and its planning hooks go in a separate distribution outside `graphscene/`, named with a `devscene` prefix, which depends on `graphscene`; `graphscene` never depends on it, so extracting the library means moving this one directory (`graphscene/README.md` → `## The boundary`; `graphscene/src/graphscene/__init__.py` → module docstring). A task that needs any of those has drifted out of this layer.
- **It owns its own toolchain configuration**: `graphscene/pyproject.toml` and `graphscene/uv.lock`. Gate 13's wiring and `scripts/python-service.sh` are not this layer's files (`docs/development.md` → `## 5. Verifying a change`, *Gate 13*).

## What it may depend on

**The boundary.** Code under `graphscene/src/graphscene/` imports only the standard library, `graphscene` itself and the runtime dependencies `graphscene/pyproject.toml` declares under `[project] dependencies`. It names no `devscene`-prefixed module, even one that is declared; never names `devscene.config.json`; and `pyproject.toml` declares no `devscene`-prefixed dependency (`graphscene/README.md` → `## The boundary`; `graphscene/tests/test_boundary.py` → `scan`, `test_the_real_library_stays_inside_its_boundary`, `test_no_declared_dependency_is_devscene_prefixed`).

- **A relative import inside the package is always in bounds**, static or dynamic with a leading `.` or a non-zero `level` (`graphscene/tests/test_boundary.py` → `_dynamic_import_target`, `test_a_relative_dynamic_import_is_not_flagged`).
- **The gate does not see every import, and the rule still binds what it misses**: a module name computed at run time, an importer bound to another name (`from importlib import import_module as load`), a module name passed by keyword, and `builtins.__import__`. A reviewer checks those by reading them (`graphscene/tests/test_boundary.py` → module docstring, *"Deliberately not covered"*).
- **A new runtime dependency whose import name differs from its normalised PEP 508 name gets an entry in `_IMPORT_NAMES`**, keyed by that normalised name — otherwise the boundary test flags the dependency's own imports (`graphscene/tests/test_boundary.py` → `_IMPORT_NAMES` and the comment above it).
- **`graphscene/tests/` is outside the scan** and may name the forbidden literal; the boundary binds `graphscene/src/graphscene/` (`graphscene/tests/test_boundary.py` → module docstring).

## The stack, in the words the rules below use

- **Python `>=3.11`**, packaged with `hatchling` from a `src` layout: the wheel ships `src/graphscene` (`graphscene/pyproject.toml` → `requires-python`, `[tool.hatch.build.targets.wheel]`).
- **The package is typed**: `graphscene/src/graphscene/py.typed` ships with it, and `mypy` runs `strict = true` over `src` **and** `tests`, so every function and test carries full annotations (`graphscene/pyproject.toml` → `[tool.mypy]`).
- **`ruff`** targets `py311` with `line-length = 100` and the rule sets `E`, `F`, `I`, `B` and `UP` (`graphscene/pyproject.toml` → `[tool.ruff]`, `[tool.ruff.lint]`).
- **`pytest`** over `tests`, with `addopts = "-p no:cacheprovider -rs"`: the suite writes no `.pytest_cache`, and a skip prints its reason. Keep both flags (`graphscene/pyproject.toml` → `[tool.pytest.ini_options]`; `docs/development.md` → *"`graphscene`'s `addopts` carries it too"*).
- **Development tools are a `[dependency-groups] dev` group**, never runtime dependencies; `graphscene/uv.lock` pins them (`graphscene/pyproject.toml` → `[dependency-groups]`).

## Naming and layout

- File naming is owned by `.claude/CLAUDE.md` → `## File naming conventions` (the *Python source module* and *Python test suite* rows).
- **The public surface is `__all__` in `graphscene/src/graphscene/__init__.py`, annotated `list[str]`.** Under `mypy`'s `strict`, a name imported into `__init__.py` and not listed there is not re-exported (`graphscene/src/graphscene/__init__.py` → `__all__: list[str]`; `graphscene/pyproject.toml` → `strict = true`).
- **A module opens with a docstring stating what it owns** and, where it holds a rule, that rule (`graphscene/src/graphscene/__init__.py` → *"The boundary: this package imports only…"*). The test-file form of this rule is owned by `.claude/context/conventions.md` → `## The testing bar` (*"A test file opens with the rule it exists to enforce"*); here it is the module docstring, with a *"Deliberately not covered:"* list where something is out of reach (`graphscene/tests/test_boundary.py` → module docstring).

## Tests

- **Plain `pytest` test functions annotated `-> None`.** Observed: a test that needs a throwaway tree plants it under `pytest`'s `tmp_path` fixture and passes the path in — the code under test takes its directory and `pyproject.toml` as parameters rather than reading fixed locations — and no mocking is used (`graphscene/tests/test_boundary.py` → `_plant`, `scan(package_dir, allowed)`, `allowed_names(pyproject)`). Committed JSON fixtures live in `graphscene/tests/fixtures/flow_graph/`, read from `Path(__file__).parent / "fixtures" / "flow_graph"` (`graphscene/tests/test_vocabulary.py`, `graphscene/tests/test_flow_graph_schema.py` → `_FIXTURES`); their wiring is owned by `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`. The no-fixture-inside-the-checkout rule is owned by `.claude/context/conventions.md` → `## The testing bar`.
- **A rule enforced by a scanner gets a planted case per clause, each asserting the exact violation text**, plus one clean case and one run against the real tree (`graphscene/tests/test_boundary.py` → `test_rule_a_…` through `test_rule_d_…`, `test_a_clean_module_produces_no_violation`, `test_the_real_library_stays_inside_its_boundary`).

## What accompanies a new module

- **A module under `graphscene/src/graphscene/` lands with its opening docstring** stating what it owns and any rule it holds, per `## Naming and layout` (`graphscene/src/graphscene/__init__.py` → module docstring).
- **A name the module makes public lands with its `__all__` entry** in `graphscene/src/graphscene/__init__.py` (`graphscene/src/graphscene/__init__.py` → `__all__: list[str]`).
- **A new runtime dependency lands with its `[project] dependencies` declaration** and, where its import name differs, its `_IMPORT_NAMES` entry, per `## What it may depend on`.
- Whether a test suite must land with it is in `## Not determined`.

## Not determined

- Logger, localization, theming and sizing accessors; shared components; a test-attribute convention and its helper; navigation, route and screen registries; shared constant owners and storage-key constants; wire-surface types and serialized-name mapping; the source of truth for shared state and listener order — no source in `graphscene/` states a rule for any of them. What would settle each: a rule stated in `graphscene/README.md` or in the module that needs one, raised as a `stale-rule` entry for a supervised `/analyze` re-run or a hand edit.
- Which command a unit runs for its own verification, and whether `bash scripts/python-service.sh --package graphscene test` accepts a single test file: `docs-retrieval-service/README.md` → `## Testing` states that `test` forwards paths to `pytest`, relative to `docs-retrieval-service/`, for that package; `graphscene/README.md` documents only the whole-suite form, and the wrapper itself is outside this document's evidence. What would settle it: `graphscene/README.md` → `## Running the toolchain` stating whether forwarding holds under `--package graphscene` and against which base directory.
- Whether a new module under `graphscene/src/graphscene/` requires its own test suite: no source in `graphscene/` states it, and `.claude/context/conventions.md` → `## What accompanies a new unit of each kind` carries no row for this layer. What would settle it: a row there or a line in `graphscene/README.md`.
- Whether a mocking library (the standard library's `unittest.mock` included) may be used in `graphscene/tests/`: `graphscene/tests/test_boundary.py` uses none, and the shared prohibition in `.claude/context/conventions.md` → `## The testing bar` sits under its `node --test` runner paragraph, so whether it binds this layer is not stated. What would settle it: that rule stated as binding every layer, or a line in `graphscene/README.md`.
- Whether adding a runtime dependency is a free choice or a decision to raise: the boundary admits any declared, non-`devscene`-prefixed dependency, and no source states a policy beyond that. What would settle it: a line in `graphscene/README.md` → `## The boundary` stating it.

_Written by `/devscene:analyze` in `existing` mode, from `graphscene/README.md`, `graphscene/pyproject.toml`, `graphscene/src/graphscene/__init__.py`, `graphscene/src/graphscene/py.typed`, `graphscene/tests/test_boundary.py`, `docs/development.md` (gate 13 and gate 6a), `docs-retrieval-service/README.md` (`## Testing`), `.claude/context/conventions.md` and `.claude/CLAUDE.md`; corrected by one fix pass on the reviewer's findings; the `## Tests` fixture observation then edited by hand._
