### Task 7 — Add the run-registry reader and the installed plugin version reader

**Goal:** Provide the two read-only facts `--upgrade` and `doctor` share: whether a local run may be executing, and which plugin version this machine has installed.

**Where this task stops.** Task 8 turns the registry answer into a refusal. Task 11 replaces `doctor`'s private `pidIsAlive` and `RUNNING_STATUS` with these exports, because `cli/src/doctor/checks.ts` belongs to that task.

### Targets

- `cli/src/core/runRegistry.ts` (new)
- `cli/src/machine/plugins.ts`
- `cli/test/upgrade-inputs.test.mjs` (new)

**Work:**

- [ ] `runRegistry.ts`: export `RUNNING_STATUS = 'running'` and `pidIsAlive(pid)` with the semantics of `doctor/checks.ts` → `pidIsAlive`, including `EPERM` as alive and non-positive pids as dead. The header states why a shared module holds them.
- [ ] `runRegistry.ts`: export `type ActiveRuns = { state: 'none' } | { state: 'active'; branches: readonly string[] } | { state: 'unreadable'; detail: string }` and `readActiveRuns(registryPath: string): ActiveRuns`. A missing file is `none`. Unparsable JSON or a wrong `{"runs": {…}}` shape is `unreadable`. A record is active when its `status` is `running` and its `pid` is alive or is not yet a number, because the watcher writes the pid after it spawns the run.
- [ ] `plugins.ts`: export `installedPluginVersion(repoRoot?: string): string | undefined`, reading `version` from `<root>/.claude-plugin/plugin.json` at `pluginRuntimeRoot`, then at `pluginInstallRoot` if that answers nothing. Every failure is `undefined`.
- [ ] `upgrade-inputs.test.mjs`: with compiled imports, cover each registry state, including a live pid, a dead pid, a running record with no pid, a finished record with a live pid and malformed JSON. For the plugin version, use a temporary `CLAUDE_CONFIG_DIR`-style home through the module's own path variable, with a readable manifest, a missing manifest and a non-string version.

**Verification:**

- `cli/test/upgrade-inputs.test.mjs` passes.
- `runRegistry.ts` takes the registry path as an argument and imports nothing from `generators/` or `doctor/`.
