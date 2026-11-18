`feat_init_upgrade` adds `devscene init --upgrade`: one command that brings an adopted repository's scripts and unattended permission profile up to the installed CLI's version, and leaves every file the adopter or `/devscene:analyze` owns alone.

It ships in the CLI, so every adopter gets it through `npx devscene@<version> init --upgrade`. It is not specific to this repository.

## Why

Plain `init` keeps every existing file, so a new script's permission entries never reach an existing profile. `init --force` does reach them, but it also replaces `.claude/CLAUDE.md`, the conventions documents, `.claude/devscene-task-offer.md` and other files that hold real work. A forced run over an adopted repository reported 39 files replaced when the goal was one profile change.

The workaround today is a forced render in a scratch clone, swapping the clone's paths for the real ones, then copying back the files that matter. `scripts/review-sweep.sh` needed exactly this to become usable in headless runs.

The profile has a second problem. It is `create-if-absent` because it may be hand-tuned, so generated changes and hand edits compete for one file.

## What `--upgrade` touches

| Artifact | Behaviour |
|---|---|
| Outer-loop scripts and their `lib/` and `flows/` files | Created when missing, and replaced when the bytes differ from the template. They are verbatim copies that read `devscene.config.json` at run time. |
| `.claude/settings.autonomous.json` | Regenerated, then merged with the local additions below. |

Everything else is left alone: the wrapper scripts (`test.sh`, `typecheck.sh` and the rest), `.claude/CLAUDE.md`, `.claude/context/*`, `.claude/review-sweep.md`, `.claude/devscene-task-offer.md`, `devscene.config.json`, the ledgers, the state-directory READMEs, the workflows (`--upgrade-workflows` owns those) and `githooks/pre-push`.

The wrappers stay out on purpose. Each holds this repository's own commands, and may hold more than the one command line: re-rendering `typecheck.sh` here keeps `npm run build` but drops the hand-added shell parse check. The profile still allow-lists them, because their invocations come from the config and not from the files.

`--dry-run` reports what would change, including the profile entries added and removed. `--upgrade` with `--force` is refused.

## The permission profile: generated file plus local additions

Neither of the two simple answers works alone:

- **Always overwrite** loses legitimate additions.
- **Merge into the existing file** cannot work safely, because no copy of the previously generated profile is stored. A merge cannot tell an adopter's entry from one a newer release retired, so retired `allow` rules would survive every upgrade.

So ownership is split:

1. `.claude/settings.autonomous.json` is fully generated and replaced on upgrade.
2. A new gitignored `.claude/settings.autonomous.local.json` holds the adopter's additions. It is merged at render time, the way the browser and retrieval fragments are (`generators/permissionProfile.ts` → `mergeInto`). The watcher still receives one file, so `run_profile_check` needs no new input.
3. The local file may only add entries to `permissions.allow`, `permissions.ask`, `permissions.deny` and `sandbox.filesystem.denyWrite`. Any other key is refused with a message naming it. It cannot remove a generated entry or change any other sandbox setting.
4. The local file joins `protectedPaths` in `generators/writeProtection.ts`, on both sides (`denyWrite` and an `Edit` deny), because a writable additions file would let a session grant itself permissions.
5. Editing the local file takes effect on the next `init --upgrade`.
6. A remote job generates its own profile, and the local file is gitignored, so jobs run without it.

**First upgrade.** Entries in the existing profile that the generator does not produce are listed in the report and are not moved automatically, because moving them would approve stale or tampered rules. The existing carry-forward of plugin-root `allow` entries stays.

## Writing files safely

- **Atomic replacement.** `core/writer.ts` writes with `writeFileSync` in place, and bash reads a running script as it executes. `--upgrade` writes to an exclusively created, randomly named temporary file in the same directory, sets its mode, and renames it over the target.
- **Active runs.** `--upgrade` refuses while the run registry shows an active local run. On success it says to restart the watcher when the watcher script changed.
- **Backups live under the main checkout's `.git`**, at `<git-common-dir>/devscene/upgrade-backups/<timestamp>/`, and not beside the originals. A backup is what someone restores from, so it needs the same write protection as the file it copies, and `.git` already has it on both sides. This also keeps them out of `git status`, out of every clone, and keeps more than one generation. A file whose bytes do not change gets no backup.

## `doctor`

A new check renders the expected profile in memory (generated output plus the local file) and compares it with the file on disk. It reports entries that are missing, which means the profile is stale, and entries nothing accounts for, which means a hand edit or tampering. Its remedy names `init --upgrade`.

Another check, or the same one, reports scripts whose bytes differ from the installed CLI's templates.

## Versions

Updating the plugin updates the agents, but the scripts already in the adopter's repository stay as they were until `init` runs from a newer CLI. An updated agent can therefore call a script that is older than it expects, or absent. `branch-reviewer`, for example, treats a missing `review-sweep.sh` as a configuration gap and skips that half of its sweep. `docs/flow-graph-walker.md` records the same lag for the walker.

`init --upgrade` is the step that closes this. The adopter docs should state it as part of updating: update the plugin, then run `init --upgrade` from the CLI of the same version. The report and `doctor` should name a plugin and CLI version mismatch when one can be read.

## Docs to update

- `docs/cli.md`: the flag table, the re-run table, and §6.
- `docs/config.md` if it describes profile ownership.
- The re-run contract table in `cli/src/core/writer.ts`.
- The re-render steps in `docs/development.md`, which can drop the scratch-clone route for self-adoption.

## Done when

- On an adopted repository with filled conventions documents, `init --upgrade` changes only the two artifact classes above, and `git status` shows nothing else.
- A second run changes nothing and takes no backup.
- A new agent-invocable script reaches the profile's `allow`, `deny` and `denyWrite` through `--upgrade` alone.
- An entry in the local file appears in the rendered profile, and survives a further upgrade.
- A local file that sets any other key is refused, and the profile is left unchanged.
- A retired generated entry disappears on upgrade.
- `doctor` passes after an upgrade, and reports a hand-added entry in the generated profile.
- A script being executed during replacement finishes on its original contents.
- The behaviour holds on macOS and Linux sandboxes, including `run_profile_check` passing on the per-run copy after an upgrade.


