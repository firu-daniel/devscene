`chore_rename_devscene_runtime` renames `devscene-runtime/` to `devscene-flow-host/` (import name `devscene_flow_host`) and narrows what the package may hold, before #418 writes any code into it. Part of #376.

## Why

#451 described the package as "DevScene's own Python runtime" that "holds only DevScene's meanings". That wording drew one line, generic code to GraphScene and DevScene's code here, and nothing else. Every planned item in #418, #419, #421, #422, #423 and #424 is the harness side of GraphScene: the walker host, the `flow-walker.sh` compatibility command, the ported checks 4–7, the harness's `claude` executor configuration, the STOP/PAUSE markers and observation rows, the hook implementations, and the planning driver's entry. None of them is unrelated to GraphScene. With a name as generic as `devscene-runtime`, any future DevScene Python code passes the package's only rule, and the package becomes a dumping ground where the GraphScene host can no longer be told apart. `docs-retrieval-service/` already shows the other pattern: a different runtime concern gets its own package.

## Decided (2026-11-23)

- **The new name is `devscene-flow-host`, import name `devscene_flow_host`.** It keeps the `devscene` prefix that `graphscene/README.md` → `## The boundary` asks harness-side code to carry. "Flow" is the harness's own word (`flow-walker.sh`, flow graphs), and "host" is #418's word for what the package is. A `graphscene-*` name was rejected because, at extraction (#425), it would read as a GraphScene companion package, while this one is harness glue that stays in this repository.
- **The package holds only the harness's GraphScene host:** the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it. Other DevScene Python integrations get their own `devscene`-prefixed package. The package's `README.md` → `## What it is` says so. That line settles the open question in `.claude/context/conventions.md` → `## Not determined` about whether harness-side Python may live in a second `devscene`-prefixed distribution.
- **No behaviour changes.** This branch renames and re-scopes; the package still holds no code beyond its skeleton.
- **The workflow file is pushed by the maintainer.** `.github/workflows/supply-chain.yml` names the package (its header comment and a `working-directory: devscene-runtime` step). A run's push of a change under `.github/workflows/` is refused, so **when the workflow change is committed and ready, the run parks and asks the maintainer to push it**. It does not try to push it, and it does not work around the refusal. It resumes once the maintainer answers that the push is done.

## Leads

_The leads below are starting points, not requirements. The planning session decides what holds when this branch is planned._

- **Where the old name appears outside the package** (from a repository-wide grep on 2026-11-23, outside `harness-runs/`):
  - `scripts/python-service.sh`: the closed `PACKAGES` table;
  - `scripts/run-gates.sh`: gate legs `13h`–`13j`;
  - `docs/development.md`: Gate 13's legs and the re-lock instruction;
  - `cli/test/python-service.test.mjs`: the `RUNTIME` constant and an expected `provisioned devscene-runtime` line;
  - `ROADMAP.md`: the GraphScene row;
  - `.github/workflows/supply-chain.yml`: see the park above.
- **Inside the package:** the directory, `pyproject.toml` (`name`, `[tool.hatch.build.targets.wheel]` → `packages`), `src/devscene_runtime/`, `README.md`, the two test files' docstrings and imports, and `uv.lock`. The lock is re-made with `bash scripts/python-service.sh --package <name> lock`, never edited by hand. Check whether that needs network access a run copy lacks (#411's provisioning rules; never sync a run copy's environment).
- **`graphscene/tests/test_boundary.py`** refuses any `devscene`-prefixed import under `graphscene/src/`, so the new name stays covered with no change there. Confirm it.
- **`devscene.config.json` names the old path twice in `treeGuards`** (`devscene-runtime/src/devscene_runtime/**` and `devscene-runtime/pyproject.toml`, covered by `tests/test_boundary.py`) and once in `layers`. Check what a gate round does when a `treeGuards` path no longer exists, so the branch's own rounds don't grade on a stale entry. The `layers` row is a maintainer step after merge (below).
- **Historical text keeps the old name:** merged commits, closed issues, `harness-runs/`. Only live files move.

## After merge, as a user step

`.claude/**` is not writable by a run, and the layer profile is changed through `devscene config set`:

- `devscene config set layers` with the renamed row (`name`, `path`, `conventions: .claude/context/devscene-flow-host.md`), plus a `detection.review` record. Fix the two `treeGuards` entries if the branch did not.
- Rename `.claude/context/devscene-runtime.md` to the new name. Replace the old name in it, in `.claude/CLAUDE.md` (the Python-packages paragraph and the routing row), in `.claude/context/conventions.md` and in `.claude/review-sweep.md` (the "GraphScene reached below its public surface" row's `Covers` and `Exempts`).
- In `.claude/context/conventions.md` → `## The layers`, add the cross-layer clause the last `/devscene:analyze` corpus pass left in neither document, worded so it holds after #419: adopters never import the package, and only the scripts `init` writes launch it.
- Optionally, `/devscene:analyze <new layer>` to confirm the document against the renamed package.

## Depends on

None open. The `devscene-runtime` layer and its conventions are on `chore_devscene_runtime_conventions`, which should merge first.
