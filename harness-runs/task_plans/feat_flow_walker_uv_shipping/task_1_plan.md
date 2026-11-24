### Task 1 — Stage `graphscene/` and `devscene-flow-host/` into the npm tarball under `dist/python/`, with the layout module that names them

**Goal:** Make the published `devscene` package carry both Python packages' sources. The build copies them from the repository root into `cli/dist/python/`, which `cli/package.json` → `files` already ships through `dist`. Every name the later tasks use for that tree and for its destination in an adopting repository is declared once, in a new module.

**Where this task stops.** It stages the packages and names the layout. It writes nothing into an adopting repository: Task 2 does, through the names below. It runs no `uv`: Task 3 does. It mirrors no name into a shell asset: Task 3 declares that mirror in this module's header.

### Targets

- `cli/src/flowHost/layout.ts` (new): the area `flowHost/` is new, because no existing area names this responsibility (`.claude/context/cli.md` → `## Naming and file layout`).
- `cli/src/flowHost/stage.ts` (new): the build-time staging entry.
- `cli/package.json`: the `build` script.
- `cli/test/python-packages-staged.test.mjs` (new).

**Work:**

- [ ] `layout.ts` opens with a header stating *"The rule this module exists to enforce"*: it is the one owner of every name the shipped Python layout is reached by. It exports these, and no other module spells them:
  - `FLOW_HOST_DIRNAME = 'python'`, the directory under `scriptsDir`.
  - `FLOW_HOST_PACKAGES = ['graphscene', 'devscene-flow-host']`, in that order, because the second sources the first from `../graphscene`.
  - `FLOW_HOST_PROJECT = 'devscene-flow-host'`.
  - `FLOW_HOST_ENV_DIRNAME = '.venv'`.
  - `stagedPythonDir()`, which returns `join(packageRoot(), 'dist', 'python')` through `cli/src/core/paths.ts` → `packageRoot`.
  - `flowHostDir(config)`, returning `<scriptsDir>/python`, built on `cli/src/generators/outerLoopScripts.ts` → `outerLoopScriptsDir` rather than a second normalisation.
  - `flowHostProjectDir(config)` and `flowHostEnvDir(config)`.
  - `isShippedPythonFile(relativePath)`, which states the shipped set: `pyproject.toml`, `uv.lock`, and every file under `src/` except a `__pycache__` directory's contents and a `*.pyc`.
- [ ] `stage.ts`, its header stating its rule. It is the one producer of `dist/python/`, and it runs only from a source checkout. It resolves the workspace root as the parent of `packageRoot()`, and for each of `FLOW_HOST_PACKAGES`:
  - It removes `dist/python/<package>/` in process (`fs.rmSync`, never a shelled-out `rm`; `.claude/context/conventions.md` → `## Shell assets`).
  - It copies every file `isShippedPythonFile` admits from `<workspace>/<package>/`, byte for byte, in sorted order.
  - A missing `pyproject.toml`, `uv.lock` or `src/` throws, naming the path. It runs as `node dist/flowHost/stage.js` through a main-module guard and exports `stagePythonPackages()`.
  - The header argues two exceptions:
    - It writes outside `cli/src/core/writer.ts` because it writes this package's own build output, never an adopting repository.
    - It lets a throw end the process because it is a build step, not a command `cli/src/cli.ts` dispatches.
- [ ] `cli/package.json` → `build` becomes `tsc -p tsconfig.json && node dist/flowHost/stage.js`. That way `pretest` and `prepublishOnly`, which already run `build`, both stage. `files` is unchanged, since it already carries `dist`. `.github/workflows/release-npm.yml` is untouched, because `npm publish --workspace cli` runs `prepublishOnly`.
- [ ] `python-packages-staged.test.mjs`, its header stating the rule: the tarball carries exactly the tracked shipped files, byte for byte. It asserts:
  - For each package, the files under `cli/dist/python/<package>/` equal, as a set and byte for byte, the tracked files `git ls-files <package>` lists that pass the shipped-file rule. It reads the tracked files read-only, which `.claude/context/conventions.md` → `## The testing bar` allows.
  - No `__pycache__`, `.venv`, `tests/` or `README.md` appears there.
  - `npm pack --dry-run --json`, run in `cli/`, lists `dist/python/devscene-flow-host/pyproject.toml`, `dist/python/devscene-flow-host/uv.lock` and `dist/python/graphscene/src/graphscene/schemas/flow-graph.schema.json`.
- [ ] This test reads a tree of repository files as text, so it needs `treeGuards` entries (`plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 8). **Task 12 adds them** to `devscene.config.json`: `test/python-packages-staged.test.mjs`, covering `graphscene/src/**`, `graphscene/pyproject.toml`, `graphscene/uv.lock`, `devscene-flow-host/src/**`, `devscene-flow-host/pyproject.toml` and `devscene-flow-host/uv.lock`.

**Verification:**

- `npm test --workspace cli -- test/python-packages-staged.test.mjs` passes. Its `pretest` build is what stages the tree it reads.
- Plant a file `graphscene/src/graphscene/__pycache__/x.pyc` by hand and rebuild: the staged tree does not carry it. Delete the planted file afterwards.
- `git grep -n "\.venv" -- cli/src` finds the environment's name only in `cli/src/flowHost/layout.ts`. `'python'` already has unrelated owners: `docs.retrievalBackend`'s value in `cli/src/config/model.ts`, `cli/src/detect/presets.ts` and `cli/src/retrieval/setup.ts`. So check instead that no module other than `layout.ts` joins `'python'` onto a `scriptsDir` path or onto `dist`.
