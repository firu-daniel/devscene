# Architecture review — round 1

verdict: FAIL
review_mode: full

## Must Fix

1. **`finding_5.md` makes `upgradeReport` read a file through the mismatch warning** — violates the rule in the module header of `cli/src/upgrade/report.ts` ("{@link upgradeReport} is a pure function that reads no file and prints nothing"), which `.claude/context/cli.md` → `## What "done" means here` binds: "Where the header states a rule, the change either satisfies it or amends the header in the same edit".
   Finding 5 has `upgradeReport` call `pluginCliMismatchWarning`. Finding 1 builds that sentence from `pluginCliMismatchRemedy`, and the remedy builds its command from `pinnedCliCommand('latest')`. In `cli/src/generators/githubWorkflows.ts`, `pinnedCliCommand` calls `ownManifestString('name')`, and `cli/src/core/paths.ts` → `ownManifest` reads this package's `package.json` from disk on each call. So the report would read a file on every self-adopted mismatch. The module already avoids this: `cliCommand` and `pluginCliCommand` reach `UpgradeReportInput` as computed values, and Finding 6 passes `browserMcpServers` as an input for the same stated reason.
   **Raised against:** "when `pluginMismatch` is set, `upgradeReport` pushes `pluginCliMismatchWarning(pluginMismatch)`"
   **Must hold:** `upgradeReport` reads no file on any path, and the complete mismatch warning still has `cli/src/machine/pluginCliVersion.ts` as its one producer, with `cli/src/upgrade/report.ts` neither assembling nor capitalizing it.
   **Fix:** In `finding_5.md`, replace `pluginVersion` and `pluginCliCommand` on `UpgradeReportInput` with `pluginMismatchWarning: string | undefined`, documented as the `pluginCliMismatchWarning(mismatch)` value and set only for a self-adopted run. Have `upgradeReport` push that string unchanged, with no import from `cli/src/machine/pluginCliVersion.ts`. In `runInitUpgrade`, pass `pluginMismatchWarning: target.selfAdopted && mismatch !== undefined ? pluginCliMismatchWarning(mismatch) : undefined`. Change the `cli/test/upgrade-report.test.mjs` bullet to assert that the supplied string appears exactly once in `warnings` in both modes and that no warning appears when the field is `undefined`. The exact sentences stay covered by Finding 1's `cli/test/plugin-cli-version.test.mjs` cases and by the `cli/test/doctor-upgrade-drift.test.mjs` and `cli/test/init-upgrade.test.mjs` bullets.

## Should Fix

1. **`finding_1.md` calls `pluginVersionNotes` "a pure function", and it is not one.** On a mismatch it calls `pluginCliMismatchRemedy`, which reaches `ownManifestString` through `pinnedCliCommand`. `cli/src/upgrade/preconditions.ts` permits reads ("Everything here only reads"), so the placement is sound, but the word should go. The same applies to "pure cases" in `finding_2.md`.

2. **`finding_1.md` places a comparison and remedy wording in `cli/src/machine/`.** This repeats round 0's Should Fix. `.claude/context/cli.md` → `## Naming and file layout` puts a module in the area whose responsibility it serves, and the existing `cli/src/machine/` modules resolve or read machine-scoped state. The conventions do not settle a better home, so this stays non-blocking.
