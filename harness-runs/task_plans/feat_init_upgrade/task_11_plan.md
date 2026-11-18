### Task 11 — Add the `doctor` drift and version checks

**Goal:** Make `doctor` report a profile or script set that no longer matches the installed CLI, and name the remedy `init --upgrade`.

**Depends on:** Task 5 (`profileDrift`), Task 6 (`outerLoopScriptDrift`), Task 7 (`readRegistryRecords`, `pidIsAlive`, `RUNNING_STATUS`, `installedPluginVersion`) and Task 10, so the command each remedy names exists.

**The contracts this task calls.**

- `profileDrift({ repoRoot: string, config: HarnessConfig, onDisk: JsonObject }): { missing: readonly ProfileEntry[], unaccounted: readonly ProfileEntry[] }`, from `cli/src/generators/profileUpgrade.ts`. `ProfileEntry` is `{ list: string, entry: string }`. A refusal from the local file or the render throws `HarnessError`.
- `outerLoopScriptDrift(repoRoot: string, config: HarnessConfig): { missing: readonly string[], changed: readonly string[] }`, from `cli/src/generators/outerLoopScripts.ts`. Paths are relative to `scriptsDir`, in table order.
- `installedPluginVersion(repoRoot?: string): string | undefined`, from `cli/src/machine/plugins.ts`.
- From `cli/src/core/runRegistry.ts`: `RUNNING_STATUS`, the string `'running'`; `pidIsAlive(pid: JsonValue | undefined): boolean`; and `readRegistryRecords(registryPath: string)`, which returns `{ state: 'read', records: readonly { key: string, record: JsonObject }[], malformedKeys: readonly string[] }` or `{ state: 'unreadable', detail: string }`. A missing file is `read` with no records.

### Targets

- `cli/src/doctor/checks.ts`
- `cli/test/doctor.test.mjs`
- `cli/test/doctor-upgrade-drift.test.mjs` (new)

**Work:**

- [ ] Add `PROFILE_DRIFT_CHECK` (`profile-drift`), directly after `profile-write-protection` in `CHECKS`. It grades `ctx.profile` at `ctx.profileRoot` with `profileDrift`. Missing entries are named as a stale profile, and unaccounted entries as a hand edit or tampering. Both warn, name `npx devscene init --upgrade`, and say an entry to keep belongs in the local file. A refused local file also warns, with the refusal's message. It is unevaluated when the configuration or profile cannot be read, and it also warns when an existing local file is not ignored.
- [ ] Add `OUTER_LOOP_SCRIPTS_CHECK` (`outer-loop-scripts`) directly after `profile-drift`. It warns naming each missing and changed row from `outerLoopScriptDrift` at the same root, with the same remedy, and notes that a deliberately patched script is replaced by that command.
- [ ] Add `PLUGIN_CLI_VERSION_CHECK` (`plugin-cli-version`) directly after `plugin-permissions`. It warns when `installedPluginVersion` is readable and differs from this CLI's version, naming both and telling the adopter to run `init --upgrade` from the CLI of the plugin's version. It passes on a match, and passes saying nothing could be compared when no version is readable.
- [ ] Remove this file's private `pidIsAlive` and `RUNNING_STATUS` in favour of the `core/runRegistry.js` exports, and rewrite `liveRunCount` over `readRegistryRecords`, keeping its behaviour and its path: `unreadable` counts `0`, `malformedKeys` are ignored, and only a `running` record with a live pid counts. Update the module header's account of its checks. In `cli/test/doctor.test.mjs`, add the three ids to `PRE_BRANCH_CHECK_IDS` in `CHECKS` order, and beside the subtest `a live run is counted by status and by pid, not by pid alone`, add one where a non-object record is not counted and one where an unparsable registry counts `0` without failing the check.
- [ ] `doctor-upgrade-drift.test.mjs`: all three checks pass after `init` and again after `init --upgrade`; a hand-added `allow` entry warns as unaccounted; a removed generated entry warns as missing; an entry in the local file not yet rendered warns as missing and passes after `init --upgrade`; a plugin-root entry under a root this machine resolves and a parity toolchain entry do not warn; an entry of the plugin-root shape with no root resolved warns as unaccounted; an edited script warns; a linked worktree grades the main checkout's files; a plugin manifest with another version warns; none of these changes the exit status.

**Verification:**

- `cli/test/doctor-upgrade-drift.test.mjs` and `cli/test/doctor.test.mjs` pass.
- Each new warning contains `init --upgrade`.
- `doctor` writes nothing while evaluating the new checks.
- `cli/src/doctor/checks.ts` no longer reads the registry's `runs` key itself.

**Deviations from plan:** `liveRunCount` keeps its path and its `unreadable` / `malformedKeys` / `running` grading, but one behaviour moves with the plan's own swap to `core/runRegistry.js`: the exported `pidIsAlive` also accepts a pid stored as digit text, which is how `hr_registry_set` writes it, so a live `running` record with a text pid now counts where the private copy, which took numbers only, did not. Implemented as the plan's export requires.
