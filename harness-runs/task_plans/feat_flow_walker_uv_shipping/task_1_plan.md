### Task 1 — Stage `graphscene/` and `devscene-flow-host/` into the npm tarball under `dist/python/`, with the layout module that names them

**Goal:** Make the published `devscene` package carry both Python packages' sources. The build copies them from the repository root into `cli/dist/python/`, which `cli/package.json` → `files` already ships through `dist`. Every name the later tasks use for that tree and for its destination in an adopting repository is declared once, in a new module.

**Where this task stops.** It stages the packages and names the layout. It writes nothing into an adopting repository: Task 2 does, through the names below. It runs no `uv`: Task 3 does. It mirrors no name into a shell asset: Task 3 declares that mirror in this module's header.

### Targets

- `cli/src/flowHost/layout.ts` (new): the area `flowHost/` is new, because no existing area names this responsibility (`.claude/context/cli.md` → `## Naming and file layout`).
- `cli/src/flowHost/stage.ts` (new): the build-time staging entry.
- `cli/src/core/errors.ts`: the module header's rule 1 only.
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
  - A missing `pyproject.toml`, `uv.lock` or `src/` throws, naming the path. It never calls `process.exit()`: an uncaught throw is what ends the build.
  - It exports `stagePythonPackages({ workspaceRoot, outDir })`. Both are parameters so a test can stage a planted tree into a temp directory. The main-module guard, which is how `node dist/flowHost/stage.js` runs it, passes the CLI defaults: the parent of `packageRoot()` and `stagedPythonDir()`.
  - The header states that it writes outside `cli/src/core/writer.ts` because it writes this package's own build output, never an adopting repository; that monopoly covers only adopting repositories. For the exit-code monopoly, the header points at `cli/src/core/errors.ts` rule 1, which names this module as its one exception (next bullet). A justification in this header alone does not license it.
  - The header also states that the compiled `dist/flowHost/stage.js` ships in the tarball, because `files` carries all of `dist`, and that it never runs there: its main-module guard is reached only through `cli/package.json` → `build` in a source checkout.
- [ ] `cli/src/core/errors.ts`, the module header's rule 1: name `cli/src/flowHost/stage.ts` as the one build-time entry point under `cli/src/`. It runs from `cli/package.json` → `build`, never from `cli/src/cli.ts`'s dispatch, and its uncaught throw ends the build rather than a command, so `cli.ts` remains the only place a thrown value of a **command** becomes an exit code. Change nothing else in that file. The conventions bullet this falsifies (`.claude/context/conventions.md` → `### Where a new responsibility goes`, *"`cli/src/cli.ts` is the only place a thrown value becomes an exit code"*) is a `stale-rule` entry in the story index, never edited here.
- [ ] `cli/package.json` → `build` becomes `tsc -p tsconfig.json && node dist/flowHost/stage.js`. That way `pretest` and `prepublishOnly`, which already run `build`, both stage. `files` is unchanged, since it already carries `dist`. `.github/workflows/release-npm.yml` is untouched, because `npm publish --workspace cli` runs `prepublishOnly`.
- [ ] `python-packages-staged.test.mjs`, its header stating the rule: the tarball carries exactly the tracked shipped files, byte for byte. It asserts:
  - For each package, the files under `cli/dist/python/<package>/` equal, as a set and byte for byte, the tracked files `git ls-files <package>` lists that pass the shipped-file rule. It reads the tracked files read-only, which `.claude/context/conventions.md` → `## The testing bar` allows.
  - No `__pycache__`, `.venv`, `tests/` or `README.md` appears there.
  - The exclusion, against a planted tree: a case builds a package tree under `os.tmpdir()` carrying `pyproject.toml`, `uv.lock`, `src/<pkg>/mod.py`, `src/<pkg>/__pycache__/x.pyc`, a `src/<pkg>/other.pyc`, `tests/test_x.py` and `README.md`. It calls `stagePythonPackages({ workspaceRoot, outDir })` from the compiled `dist/flowHost/stage.js` with a temp `outDir`, and asserts that only the first three are staged. It tears both temp trees down in process. Nothing is written inside the checkout.
  - `npm pack --dry-run --json`, run in `cli/`, lists `dist/python/devscene-flow-host/pyproject.toml`, `dist/python/devscene-flow-host/uv.lock` and `dist/python/graphscene/src/graphscene/schemas/flow-graph.schema.json`.
  - **Registration.** This test reads a tree of repository files as text, so it needs `treeGuards` entries (`plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 8). **Task 12 adds them** to `devscene.config.json`. Each entry's `covers` is a path only a `cli`-layer unit changes, so the `cli` layer's `<test_file_cmd>` is the one that runs it: `test/python-packages-staged.test.mjs`, covering `cli/src/flowHost/**` and `cli/package.json`. A guard covering `graphscene/**` or `devscene-flow-host/**` would be run by those layers' pytest command, which cannot run a `.mjs` suite, so none is registered. The test's header states the consequence: a change under either Python package reaches this suite at Run gates, where `pretest` re-stages the tree from the tracked files before it is compared.

**Verification:**

- `npm test --workspace cli -- test/python-packages-staged.test.mjs` passes. Its `pretest` build is what stages the tree it reads.
- `git grep -n "\.venv" -- cli/src` finds the environment's name only in `cli/src/flowHost/layout.ts`. `'python'` already has unrelated owners: `docs.retrievalBackend`'s value in `cli/src/config/model.ts`, `cli/src/detect/presets.ts` and `cli/src/retrieval/setup.ts`. So check instead that no module other than `layout.ts` joins `'python'` onto a `scriptsDir` path or onto `dist`.
