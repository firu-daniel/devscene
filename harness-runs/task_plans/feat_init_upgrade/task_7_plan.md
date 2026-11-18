### Task 7 — Add the run-registry reader and the installed plugin version reader

**Goal:** Provide the two read-only facts `--upgrade` and `doctor` share: what the run registry holds and whether a local run may be executing, and which plugin version this machine has installed.

**Where this task stops.** Task 8 turns the registry answer into a refusal. Task 11 rewrites `doctor`'s `liveRunCount` over `readRegistryRecords` and removes its private `pidIsAlive` and `RUNNING_STATUS`, because `cli/src/doctor/checks.ts` belongs to that task.

### Targets

- `cli/src/core/runRegistry.ts` (new)
- `cli/src/machine/plugins.ts`
- `cli/test/upgrade-inputs.test.mjs` (new)

**Work:**

- [ ] `runRegistry.ts`: export `RUNNING_STATUS = 'running'` and `pidIsAlive(pid: JsonValue | undefined): boolean` with the semantics of `doctor/checks.ts` → `pidIsAlive`, including `EPERM` as alive and non-positive pids as dead. The header states the module's rule: the registry file's parsing and record walk live here once, and each caller keeps its own grading.
- [ ] `runRegistry.ts`: export `type RegistryRecords = { state: 'read'; records: readonly { key: string; record: JsonObject }[]; malformedKeys: readonly string[] } | { state: 'unreadable'; detail: string }` and `readRegistryRecords(registryPath: string): RegistryRecords`. A missing file is `read` with no records. A file that cannot be read or parsed, or that is not `{"runs": {…}}`, is `unreadable` with the cause in `detail`. A `runs` value that is not an object is left out of `records` and its key is listed in `malformedKeys`.
- [ ] `runRegistry.ts`: export `type ActiveRuns = { state: 'none' } | { state: 'active'; branches: readonly string[] } | { state: 'unreadable'; detail: string }` and `readActiveRuns(registryPath: string): ActiveRuns`, built on `readRegistryRecords`. A non-empty `malformedKeys` is `unreadable` naming those keys, because a refusal cannot prove such a record is not a run. A record is active when its `status` is `running` and its `pid` is alive or is not yet a number, because the watcher writes the pid after it spawns the run. `branches` holds the active records' keys.
- [ ] `plugins.ts`: export `installedPluginVersion(repoRoot?: string): string | undefined`, reading `version` from `<root>/.claude-plugin/plugin.json` at `pluginRuntimeRoot`, then at `pluginInstallRoot` if that answers nothing. Every failure is `undefined`. Amend the module header: name the plugin manifest under a resolved root among the files the module reads, state that its `version` is the one field read for something other than navigating to a root, and keep the read-only, navigated-not-validated and every-failure-is-`undefined` statements true of it.
- [ ] `upgrade-inputs.test.mjs`: with compiled imports, cover `readRegistryRecords` on a missing file, malformed JSON, a wrong `runs` shape and a non-object record, and each `readActiveRuns` state, including a live pid, a dead pid, a running record with no pid, a finished record with a live pid and a non-object record. For the plugin version, use a temporary `CLAUDE_CONFIG_DIR`-style home through the module's own path variable, with a readable manifest, a missing manifest and a non-string version.

**Verification:**

- `cli/test/upgrade-inputs.test.mjs` passes.
- `runRegistry.ts` takes the registry path as an argument and imports nothing from `generators/` or `doctor/`.
