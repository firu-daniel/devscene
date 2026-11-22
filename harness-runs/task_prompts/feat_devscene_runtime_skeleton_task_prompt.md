`feat_devscene_runtime_skeleton` creates `devscene-runtime/`, DevScene's own Python package, with its toolchain, gates and import boundary, and no behaviour yet. Part of #376.

## Why

#418 builds the harness's walker host in this package. If the same branch also created the package, the host would be written under the catch-all `general` layer, with no conventions document and no layer reviewer of its own. `graphscene` went the same way: the package first (#412), then its layer and conventions as a user step (#430), then the code.

## Decided (2026-11-22)

- **`devscene-runtime/` sits at the repository root** beside `graphscene/` and `docs-retrieval-service/`, import name `devscene_runtime`. It is DevScene's own Python runtime and stays in this repository for good: it gets no repository of its own and is not extracted with GraphScene (#425).
- **It holds only DevScene's meanings.** Anything useful without DevScene goes into GraphScene instead. LangGraph splits things the same way: generic stores and patterns ship as packages (`langgraph-checkpoint-*`, prebuilt agents), and an application's glue stays application code.
- **Dependencies point one way.** It depends on `graphscene`, and GraphScene never imports it. `graphscene/tests/test_boundary.py` already refuses any `devscene*` import under `graphscene/src/`.
- **Adopters never import it.** It ships inside the `devscene` npm package with `graphscene` (#419), and an adopter reaches it only through the scripts `init` writes.

- **No internal layers in the skeleton.** No layer folders and no `import-linter` layers contract: the boundary test is the package's only structural rule here. With no code yet there is nothing to name layers after, and `/devscene:analyze` would have nothing to read in empty folders. #418 decides the internal structure while it plans the walker host, so its code lands in that structure from the start. `graphscene` took the other route (skeleton #429, model #433, then `refactor: graphscene layers` #440), which cost a refactor.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- **Shape like #412's skeleton:** `pyproject.toml` and `uv.lock`, `src/devscene_runtime/`, `tests/`, `ruff` and strict `mypy` matching the other two packages, and a `README.md` that says what the package is and what it may depend on.
- **The `graphscene` dependency is a `uv` path dependency on `../graphscene`,** so one sync provisions both and no release is needed while both live here. Check that `uv run --frozen --no-sync` from `devscene-runtime/` imports `graphscene` in a run copy (#411's provisioning rules; never sync a run copy's environment).
- **Toolchain wiring:** a row in `scripts/python-service.sh`'s closed `PACKAGES` table, and gate 13 legs alongside `13e`–`13g` (`docs/development.md` → Gate 13), so every unit's `commands.typecheck` lints and type-checks it.
- **Its own boundary test,** the counterpart of `graphscene/tests/test_boundary.py`: `devscene_runtime` may import `graphscene`'s public surface only (`graphscene`, never `graphscene.engine.*` and the like), plus its declared dependencies.
- **Where it reads the repository from:** later branches read `devscene.config.json`, the ledger and plugin documents, so the skeleton may settle how the root is found (a bare `git rev-parse --show-toplevel`, as the bash scripts do, or an argument).
- **After merge, a user step:** add the layer to `devscene.config.json` → `layers`, its row in `.claude/CLAUDE.md`, and its conventions document through `/devscene:analyze`, as #430 did. #418 is queued only after that.

## Depends on

None open. `graphscene` is on `dev`.


