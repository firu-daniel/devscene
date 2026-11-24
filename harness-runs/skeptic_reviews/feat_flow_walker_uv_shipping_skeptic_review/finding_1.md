### 1. In the self-adopted repository the write protection of `scripts/python/` covers two symlinks, not the package trees `setup-worktree.sh` step 6 builds outside the sandbox

**File:** `cli/src/generators/writeProtection.ts` (`protectedPaths`) — "the main checkout's Python packages are built outside the sandbox when the flow walker's environment is provisioned"
**Class:** Wrong behaviour
**Failure:** If a run session in this repository uses its `Write` file tool on `<main checkout>/devscene-flow-host/pyproject.toml` (or on `<main checkout>/graphscene/…`), then the next run copy `create-worktree.sh` bootstraps executes that session-written build code outside the sandbox, in `setup-worktree.sh` step 6's `uv sync`.

**The rule being broken.** `writeProtection.ts`'s own header: "anything that runs outside the sandbox must not be writable from inside it". The story index's second top risk is exactly this case ("An unsandboxed build of run-written source … So Task 5 protects the main checkout's `<scriptsDir>/python/`, and Task 4 builds a run copy's environment from that protected tree"), and `cli/templates/scripts/setup-worktree.sh`'s header now claims "Step 6 is outside this residual under `--target`, because it builds from the main checkout's protected packages".

**Why it does not hold here.** Task 12 commits `scripts/python/graphscene` and `scripts/python/devscene-flow-host` as symbolic links (`git ls-files -s` mode `120000`, targets `../../graphscene` and `../../devscene-flow-host`). The entry Task 5 adds protects the path `join(repoRoot, flowHostDir(config))` = `<main>/scripts/python` as a `directory`: one `sandbox.filesystem.denyWrite` entry and one `Edit(//<main>/scripts/python/**)` deny rule. The package sources actually live at `<main>/devscene-flow-host/` and `<main>/graphscene/`, which no entry names. The profile grants the file tools `Edit(/{{repoRoot}}/**)` over the whole main checkout (`cli/templates/claude/settings.autonomous.json`), so a write addressed to the real path, such as `<main>/devscene-flow-host/pyproject.toml`, matches the allow and no deny.

**Why it is reachable and executes.** `create-worktree.sh` bootstraps every new run copy with `setup-worktree.sh --target <copy>`, where `cfg_root` is the main checkout (`setup-worktree.sh`: `cfg_root="$main_repo"`). Step 6 then calls `hr_flow_host_provision "$cfg_root/$scripts_rel" "$top/$scripts_rel"`, which runs `uv sync --frozen --no-dev --no-editable --project <main>/scripts/python/devscene-flow-host` outside any sandbox. Through the link, that is `<main>/devscene-flow-host/pyproject.toml`, and its `[tool.uv.sources]` path source `../graphscene`. `uv` builds both projects as wheels with their declared PEP 517 backend. A `pyproject.toml` that names an in-tree backend (`backend-path = ["."]`), or a hatchling custom build hook (`[tool.hatch.build.hooks.custom]` → `hatch_build.py` in the project root), runs that file's code during the build. Before this branch, no unsandboxed step read the main checkout's working tree outside the protected set. The `commands.depInstall` residual runs in the copy, from the copy's own branch content. This step adds a cross-run route: one session's write lands in every later run's bootstrap.

Adopters are unaffected, because their `<scriptsDir>/python/<pkg>` are real directories inside the protected one. Only the self-adopted layout (Task 12) opens it.

**Confirmed by reading, not by executing:** `protectedPaths` and `fileToolDenyRules` in `cli/src/generators/writeProtection.ts`; the `Edit(/{{repoRoot}}/**)` allow in `cli/templates/claude/settings.autonomous.json`; step 6 and the `--target` anchors in `cli/templates/scripts/setup-worktree.sh`; `hr_flow_host_provision` in `cli/templates/scripts/lib/harness-run-lib.sh`; the two link entries in `git ls-files -s scripts/python`. That a PEP 517 build runs `backend-path` / hatch build-hook code is documented build-backend behaviour, taken on trust. No probe was run: it would need a write into the main checkout and an unsandboxed `uv sync`.

**Fix:**

1. In `cli/src/generators/writeProtection.ts`:
   - Import `realpathSync` from `node:fs`.
   - Import `lstatOrUndefined` from `../core/paths.js`, beside `defaultProjectName` and `worktreeGlob`.
   - Import `FLOW_HOST_PACKAGES` from `../flowHost/layout.js`, beside `flowHostDir`.
   - In `protectedPaths`, directly after the `paths.push({ path: join(repoRoot, flowHostDir(config)), kind: 'directory', … })` call, add:

   ```ts
   // In the harness's own repository each package is a link to the tree at the root; the build
   // reads the target, so the target is what must be unwritable. A real directory is already
   // covered by the entry above, and an absent or dangling link has nothing to build.
   for (const pkg of FLOW_HOST_PACKAGES) {
     const link = join(repoRoot, flowHostDir(config), pkg);
     if (lstatOrUndefined(link, ['ENOENT', 'ENOTDIR'])?.isSymbolicLink() !== true) continue;
     let target: string;
     try {
       target = realpathSync(link);
     } catch {
       continue;
     }
     paths.push({
       path: target,
       kind: 'directory',
       reason: `the main checkout's ${pkg} package, which ${flowHostDir(config)}/${pkg} links to, is built outside the sandbox when the flow walker's environment is provisioned`,
     });
   }
   ```

   - In the module header's "The set:" sentence, after "the main checkout's `<scriptsDir>/python/` (…)", add: "and, where a package there is a symbolic link (the harness's own repository), the directory it resolves to".

   `jobSurfacePaths` calls this with `PLACEHOLDER_REPO_ROOT`, where nothing exists, so `lstatOrUndefined` returns `undefined` and the job surface is unchanged.

2. Add a case to `cli/test/flow-host-protection.test.mjs`:
   - Take a `wiredFixture`.
   - Create `<dir>/graphscene/` holding an empty `pyproject.toml`.
   - Replace `<dir>/<flowHostDir(config)>/graphscene` (`rm` recursive) with a symbolic link to `../../graphscene`.
   - Call `protectedPaths({ repoRoot: dir, workRoot: dirname(dir), config, additionalDirectories: [] })`, imported from `../dist/generators/writeProtection.js`.
   - Assert that an entry has `path === realpathSync(join(dir, 'graphscene'))` and `kind === 'directory'`.
   - Assert that no entry names `realpathSync(join(dir, flowHostDir(config), 'devscene-flow-host'))` separately, because that one is still a real directory.

   Run that one file: `npm test --workspace cli -- test/flow-host-protection.test.mjs`.

Not this fix's work: once merged, a maintainer regenerates this repository's own main-checkout profile (`.claude/settings.autonomous.json`), which a run cannot write, so it carries the two new entries. Until then `doctor`'s `profile-write-protection` check names the missing ones.
