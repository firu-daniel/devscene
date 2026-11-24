### Task 3 — Ship `flow-host-provision.sh` and the library function `hr_flow_host_provision`

**Goal:** Give every place that needs the walker's environment one route to build it. A library function performs the sync. A new outer-loop script, which takes no argument, runs that function for the checkout it sits in. `init` (Task 7), `doctor`'s remedy (Task 8) and a person all invoke that script, and `setup-worktree.sh` (Task 4) calls the library function directly.

**Depends on:** Task 1, whose `cli/src/flowHost/layout.ts` owns `FLOW_HOST_DIRNAME` (`python`), `FLOW_HOST_PROJECT` (`devscene-flow-host`) and `FLOW_HOST_ENV_DIRNAME` (`.venv`). The shell side spells those three literals as a **declared mirror**. This task adds a `MIRRORS` paragraph to `layout.ts`'s header naming `hr_flow_host_provision` in `cli/templates/scripts/lib/harness-run-lib.sh`, and its test holds the two equal.

**The contract this task produces, which Tasks 4, 7 and 8 consume verbatim:**

- **`hr_flow_host_provision <source_scripts_dir> <env_scripts_dir>`**. Both arguments are absolute paths to a checkout's `scriptsDir`.
  - The project is `<source_scripts_dir>/python/devscene-flow-host`, and the environment is `<env_scripts_dir>/python/.venv`.
  - It runs `uv sync --frozen --no-dev --no-editable --project <project>` with `UV_PROJECT_ENVIRONMENT=<environment>` exported for that one command only.
- **What it prints and returns:**
  - No `uv` on `PATH`: prints `flow-host: provision: SKIPPED — uv is not on PATH; install uv, then run <invocation> outside the sandbox` to stderr and returns `0`.
  - No `<project>/pyproject.toml`: prints `flow-host: provision: SKIPPED — no flow host at <project>; run npx devscene init --upgrade` to stderr and returns `0`.
  - Success: prints `flow-host: provisioned <environment>` to stdout and returns `0`.
  - Any `uv` failure: prints `flow-host: provision: failed (exit <n>)` to stderr and returns `1`.
  - `<invocation>` is `bash <scriptsDir>/flow-host-provision.sh`, built from the checkout's real scripts directory.
- **`flow-host-provision.sh`**, run as `bash <scriptsDir>/flow-host-provision.sh` with **no argument**. It resolves its own checkout through `hr_script_root`, then calls `hr_flow_host_provision <own scripts dir> <own scripts dir>`.
  - Exit `0`: provisioned or skipped. Exit `1`: the library or configuration could not be read, or the sync failed. Exit `2`: any argument was given (usage).
  - It takes no argument, so nothing a session writes chooses which tree is built (`harness-runs/lessons.md` → `## Trust checks`, *"never from the argument's shape"*).

**Where this task stops.** The bootstrap step that calls the function with a run copy as `<env_scripts_dir>` is Task 4's. `init`'s call of the script is Task 7's. Write-protecting the main checkout's `<scriptsDir>/python/` is Task 5's.

### Targets

- `cli/templates/scripts/flow-host-provision.sh` (new).
- `cli/templates/scripts/lib/harness-run-lib.sh`.
- `cli/src/generators/outerLoopScripts.ts`: `OUTER_LOOP_SCRIPTS`.
- `cli/src/flowHost/layout.ts`: its header's `MIRRORS` paragraph only.
- `cli/test/flow-host-provision.test.mjs` (new).
- `cli/test/init.test.mjs`: its `OUTER_LOOP_SCRIPT_FILES` constant only.

**Work:**

- [ ] `harness-run-lib.sh`: add `hr_flow_host_provision` with the contract above. Its header entry states the three mirrored literals and names `cli/src/flowHost/layout.ts` as their owner. Follow the library's own rules: it sets no shell option, and every global it assigns is listed in the header's assigned-before-read paragraph.
- [ ] `flow-host-provision.sh`: `#!/usr/bin/env bash`, a `# flow-host-provision.sh — …` header, an exit map and a `REPRO` block against a throwaway fixture, in the shape `cli/templates/scripts/setup-worktree.sh`'s header uses. The header states:
  - It runs outside any sandbox. Inside one it fails closed, because the sandbox refuses the network and the shared `uv` cache, which the task prompt measured (exit `2`, `Failed to initialize cache at ~/.cache/uv`).
  - It changes nothing outside `<scriptsDir>/python/.venv`.
  - This is why it needs no `DENY_SCRIPT_BASENAMES` entry, the same argument `scripts/python-service.sh` → `WHO RUNS lock, sync AND provision` makes.
- [ ] `OUTER_LOOP_SCRIPTS`: add the row `{ file: 'flow-host-provision.sh', mode: 0o755, agentInvocable: false }` after `setup-worktree.sh`, with a comment saying who runs it: `init`, a person and `doctor`'s remedy. `false` is a calling convention, so it owes no `DENY_SCRIPT_BASENAMES` entry. Leave `runsUnsandboxed` unset: `writeProtection.ts` → `protectedPaths` then protects the main checkout's copy as a script *"the run watcher, the remote job or a person runs … outside the sandbox"*.
  - `cli/test/init.test.mjs` → `OUTER_LOOP_SCRIPT_FILES`: add `'flow-host-provision.sh'`. That list is spelled out by hand rather than imported from the table, and `writtenWrappers` subtracts only it. Without the entry, the new script counts as a wrapper: `assert.deepEqual(await writtenWrappers(dir), [])` fails, and `assertWrapperPairing` demands two allow entries an `agentInvocable: false` row never gets. The other suites under `cli/test/` that spell outer-loop script names literally (`script-root-callers.test.mjs` → `SCRIPTS`, `setup-worktree-checkout-sparse.test.mjs` → `SCRIPTS`, `create-worktree.test.mjs`'s fixture copy list) each read a fixed subset of named scripts and assert nothing about the whole set, so the new row moves none of them.
- [ ] `layout.ts` header: the `MIRRORS` paragraph naming `hr_flow_host_provision` and the suite that holds it equal.
- [ ] `flow-host-provision.test.mjs`, its header stating the rule. It builds a throwaway fixture repository with the script and `lib/` copied in, and puts a stub `uv` on `PATH` that records its argv and `UV_PROJECT_ENVIRONMENT`. That is the stub-binary pattern `cli/test/job-layout-root.test.mjs` uses, not a mocking framework. It asserts:
  - The exact argv `sync --frozen --no-dev --no-editable --project <root>/<scriptsDir>/python/devscene-flow-host`, with the environment `<root>/<scriptsDir>/python/.venv`.
  - Each `SKIPPED` line and exit `0`: with no `uv` reachable, a `PATH` holding links to only the binaries the script needs; and with no project directory.
  - The failure line and exit `1` when the stub exits non-zero.
  - Exit `2` for any argument.
  - Mirror equality: the three literals in the library equal the compiled `cli/dist/flowHost/layout.js` exports.

**Verification:**

- `npm test --workspace cli -- test/flow-host-provision.test.mjs` passes.
- Running the header's `REPRO` block by hand reproduces each exit status it lists.
- `grep -n "'flow-host-provision.sh'" cli/test/init.test.mjs` finds the new entry inside `OUTER_LOOP_SCRIPT_FILES`, and `npm test --workspace cli -- test/init.test.mjs`, a suite this task edits, passes.
