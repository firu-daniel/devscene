### Task 1 — Create the `graphscene/` package: manifest, empty typed `graphscene` package, the import-boundary test and its README

**Goal:** Create GraphScene as an isolated Python library at `graphscene/`. It holds no engine code. It is set up like `docs-retrieval-service/`, and a test inside the library itself enforces its boundary with the harness from this first commit.

**Where this task stops.** This task creates the package directory and nothing outside it.
- **Task 2** owns the package's row in `scripts/python-service.sh` and the `graphscene/uv.lock` that row needs. This task writes no lock and runs no `uv`.
- **Task 3** owns gate 13's legs that run this package (13e `lint`, 13f `typecheck`, 13g `test`).
- **Task 5** owns `docs/development.md` and `ROADMAP.md`.

No unit runs this package's `pytest`, `ruff` or `mypy` (`## The test-run rule`). Their evidence is gate 13's legs 13e–13g in the Run gates round. So this task's code must satisfy the house settings below by construction.

### Targets

- `graphscene/pyproject.toml` (new)
- `graphscene/src/graphscene/__init__.py` (new)
- `graphscene/src/graphscene/py.typed` (new, empty)
- `graphscene/tests/test_boundary.py` (new)
- `graphscene/README.md` (new)

**Work:**

- [ ] `pyproject.toml`: model it on `docs-retrieval-service/pyproject.toml`, keeping only what a generic library needs.
  - `[project]`: `name = "graphscene"`, `version = "0.1.0"`, a one-line description of a generic flow-graph navigation library that names no harness, `requires-python = ">=3.11"`, and `dependencies = []`.
  - `[dependency-groups]`: `dev = ["ruff", "mypy", "pytest"]`.
  - Build: `hatchling` in `[build-system]`, and `[tool.hatch.build.targets.wheel]` → `packages = ["src/graphscene"]`.
  - `[tool.mypy]`: `strict = true`, `python_version = "3.11"`, `files = ["src", "tests"]`, `mypy_path = "src"`.
  - `[tool.ruff]`: `target-version = "py311"`, `line-length = 100`, `src = ["src", "tests"]`. `[tool.ruff.lint]`: `select = ["E", "F", "I", "B", "UP"]`.
  - `[tool.pytest.ini_options]`: `testpaths = ["tests"]` and `addopts = "-p no:cacheprovider -rs"`. The cache flag keeps the in-tree `.pytest_cache` from ever being written, as `docs-retrieval-service` does.
  - Leave out the `[project.scripts]` console script, the `models` extra, the `torch` index, the mypy overrides and the `container` marker.
- [ ] `src/graphscene/__init__.py` and `py.typed`: the package is empty apart from its contract. `__init__.py` holds a module docstring and `__all__: list[str] = []`. The docstring says that GraphScene is a generic flow-graph navigation library, and states the boundary rule: the library imports only the standard library, itself and its declared runtime dependencies, and it never reads the harness's configuration file. Harness integration lives in a separate distribution that depends on this one, never the reverse. Do not write the configuration file's name as a literal here (see Verification). `py.typed` is an empty marker file, so that the package's type information is exported.
- [ ] `tests/test_boundary.py`, the scanner. The module docstring opens with the rule the file enforces: *the library at `src/graphscene/` reaches nothing outside the standard library, itself and its declared runtime dependencies, never names `devscene.config.json`, and declares no `devscene`-prefixed dependency*. The docstring also states what is deliberately not covered:
  - `tests/` is not scanned, because this file has to carry the forbidden literal.
  - An import whose module name is computed at run time cannot be checked statically.

  Write a pure function `scan(package_dir: Path, allowed: frozenset[str]) -> tuple[list[Path], list[str]]`. It returns the `.py` files it visited and one violation line per finding, each `<path relative to package_dir>:<line>: <what>`. It flags:
  - (a) any `ast.Import` or absolute `ast.ImportFrom` whose top-level name is not in `allowed`. A relative import (`level > 0`) is allowed.
  - (b) any call to `importlib.import_module(<str constant>)`, `import_module(<str constant>)` or `__import__(<str constant>)` whose top-level name is not in `allowed`.
  - (c) any top-level name, from (a) or (b), that starts with `devscene`, even if it is allowed.
  - (d) any `str` constant that contains `devscene.config.json`.

  `allowed` is `sys.stdlib_module_names`, plus `graphscene`, plus each `[project].dependencies` entry of `pyproject.toml`, read with `tomllib`. A dependency's name is its PEP 508 name, lower-cased, with `-` mapped to `_`. A comment in the file says that a dependency whose import name differs from that is added to an explicit mapping there when it arrives.
- [ ] `tests/test_boundary.py`, the cases. Use `tmp_path`, and annotate every test function `-> None` (strict mypy covers `tests/`). Write these cases:
  - (1) One planted module per rule (a), (b), (c) and (d), each in its own `tmp_path` package. Assert that each produces exactly its own violation line and that a clean planted module produces none. These cases prove the scanner fires, so the real-tree case cannot pass vacuously.
  - (2) The real tree. Resolve `src/graphscene` from `Path(__file__).resolve().parents[1]`. Assert that the visited files include `src/graphscene/__init__.py` and that the violation list is empty, and print the list in the assertion message.
  - (3) The real `pyproject.toml`. Assert that no `[project].dependencies` entry's name starts with `devscene`, because a declared harness dependency would otherwise make rule (a) pass.

  Name no harness module other than through the `devscene` prefix and the `devscene.config.json` literal.
- [ ] `README.md`: this file is GraphScene's own statement of who reads it and what it owns. Its sections:
  - **What it is:** a generic flow-graph navigation library. It has no engine code yet and no runtime dependency.
  - **The boundary:** the decision-2 and decision-3 rules from the story index's `## Context`. The harness side goes in a separate `devscene`-prefixed distribution outside this directory, and the dependency points one way. `tests/test_boundary.py` enforces the boundary.
  - **Running the toolchain:** every command goes through `scripts/python-service.sh` from the repository root. Give each command its own fenced block, one command per line, and never inline it (`harness-runs/lessons.md` → *Adopter-facing documentation*, first rule): `bash scripts/python-service.sh --package graphscene lint`, `… typecheck`, `… test`, and `bash scripts/python-service.sh provision`.
  - **Gating:** the package is gated by gate 13's legs 13e–13g (`docs/development.md` → `## 5. Verifying a change`).

  Write no deferral promise and no roadmap number. Use no absolute machine path.

**Verification:**

- `graphscene/` holds exactly the five targets above. Nothing outside `graphscene/` changed, and no `uv.lock`, `.venv` or cache directory was created.
- Read `test_boundary.py` against the four rules. Each rule has a planted case that only that rule makes fail, and the real-tree case asserts on the visited set, not only on an empty violation list.
- `grep -rn 'devscene' graphscene/src` finds no line other than the docstring's statement of the rule, which names `devscene.config.json` in prose. Rule (d) flags string constants, and a module docstring is one. So write that statement so that the docstring carries no `devscene.config.json` literal, for example *"the harness's configuration file"*, and keep the literal out of `src/` entirely.
- Every function and test in the two Python files carries full annotations, and imports are grouped and sorted as ruff's `I` rule expects (standard library, then first-party `graphscene`). That is what 13e and 13f grade.
- **Deviations from plan:** `graphscene/tests/test_boundary.py` was not run: the stated `<test_file_cmd>` (`npm test --workspace cli -- test/<name>.test.mjs`) cannot run a `pytest` file, and no `ruff` or `mypy` ran over the package. The line-length, import-order, annotation and formatting claims rest on reading the two Python files (an `awk 'length > 100'` probe over both printed nothing); gate 13's legs 13e–13g verify them in the Run gates round.
- This file is not a tree guard and owes no `treeGuards` entry (`## The test-run rule` point 8). A `treeGuards[].test` value is run through the `cli` workspace's `npm test` as `<test_file_cmd>`'s argument, and a `pytest` file cannot be run that way. Gate 13's leg 13g runs it in every Run gates round instead (Task 3).
