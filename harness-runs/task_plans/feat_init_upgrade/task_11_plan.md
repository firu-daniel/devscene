### Task 11 — Add the `doctor` drift and version checks

**Goal:** Make `doctor` report a profile or script set that no longer matches the installed CLI, and name the remedy `init --upgrade`.

**Depends on:** Task 5 (`profileDrift`), Task 6 (`outerLoopScriptDrift`), Task 7 (`pidIsAlive`, `RUNNING_STATUS`, `installedPluginVersion`) and Task 10, so the command each remedy names exists.

### Targets

- `cli/src/doctor/checks.ts`
- `cli/test/doctor.test.mjs`
- `cli/test/doctor-upgrade-drift.test.mjs` (new)

**Work:**

- [ ] Add `PROFILE_DRIFT_CHECK` (`profile-drift`), directly after `profile-write-protection` in `CHECKS`. It grades `ctx.profile` at `ctx.profileRoot` with `profileDrift`. Missing entries are named as a stale profile, and unaccounted entries as a hand edit or tampering. Both warn, name `npx devscene init --upgrade`, and say an entry to keep belongs in the local file. A refused local file also warns, with the refusal's message. It is unevaluated when the configuration or profile cannot be read, and it also warns when an existing local file is not ignored.
- [ ] Add `OUTER_LOOP_SCRIPTS_CHECK` (`outer-loop-scripts`) directly after `profile-drift`. It warns naming each missing and changed row from `outerLoopScriptDrift` at the same root, with the same remedy, and notes that a deliberately patched script is replaced by that command.
- [ ] Add `PLUGIN_CLI_VERSION_CHECK` (`plugin-cli-version`) directly after `plugin-permissions`. It warns when `installedPluginVersion` is readable and differs from this CLI's version, naming both and telling the adopter to run `init --upgrade` from the CLI of the plugin's version. It passes on a match, and passes saying nothing could be compared when no version is readable.
- [ ] Replace this file's private `pidIsAlive` and `RUNNING_STATUS` with imports from `core/runRegistry.js`, leaving `liveRunCount`'s behaviour unchanged. Update the module header's account of its checks. In `cli/test/doctor.test.mjs`, add the three ids to `PRE_BRANCH_CHECK_IDS` in `CHECKS` order.
- [ ] `doctor-upgrade-drift.test.mjs`: all three checks pass after `init` and again after `init --upgrade`; a hand-added `allow` entry warns as unaccounted; a removed generated entry warns as missing; an entry in the local file not yet rendered warns as missing and passes after `init --upgrade`; carried plugin-root and parity toolchain entries do not warn; an edited script warns; a linked worktree grades the main checkout's files; a plugin manifest with another version warns; none of these changes the exit status.

**Verification:**

- `cli/test/doctor-upgrade-drift.test.mjs` and `cli/test/doctor.test.mjs` pass.
- Each new warning contains `init --upgrade`.
- `doctor` writes nothing while evaluating the new checks.
