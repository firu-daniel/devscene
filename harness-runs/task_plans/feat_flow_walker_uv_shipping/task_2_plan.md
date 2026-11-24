### Task 2 — Write the staged packages under `<scriptsDir>/python/` on `init` and replace them on `init --upgrade`

**Goal:** Put the staged packages into an adopting repository, at the layout the story index's `## Context` fixes: `<scriptsDir>/python/graphscene/` and `<scriptsDir>/python/devscene-flow-host/`. Plain `init` keeps an existing copy, and `init --upgrade` brings each file to the shipped bytes after a backup. Both are the outer-loop scripts' re-run contracts.

**Depends on:** Task 1. It provides:

- `cli/src/flowHost/layout.ts`: `FLOW_HOST_PACKAGES`, `stagedPythonDir()`, `flowHostDir(config)` and `isShippedPythonFile(relativePath)`.
- the staged tree at `cli/dist/python/<package>/`, which this task reads and never re-derives.

**Where this task stops.** It writes files and provisions nothing: the environment is Task 3's route, which Task 7 offers from `init`. It adds no `.gitignore` line (Task 6), no write protection (Task 5) and no `doctor` check. Task 8 consumes this task's drift reader.

### Targets

- `cli/src/generators/flowHostPackages.ts` (new).
- `cli/src/commands/init.ts`.
- `cli/src/upgrade/initUpgrade.ts`.
- `cli/src/core/writer.ts`: the re-run-contract table in its header.
- `cli/test/flow-host-packages.test.mjs` (new).

**Work:**

- [ ] `flowHostPackages.ts`. Its header states the rule and argues that it copies verbatim, with no rendering and so no `assertNoneSurvive` setting (`.claude/context/cli.md` → `## How a module in this layer is written`). It exports three functions:
  - **`writeFlowHostPackages({ repoRoot, config, plan })`** enqueues the files, `create-if-absent`:
    - one `ensure-dir` per directory;
    - one write per file under `stagedPythonDir()/<package>/`, each file's text read from there, to `<repoRoot>/<flowHostDir(config)>/<package>/<relative path>`, mode `0o644`.
    - It returns `{ written: string[] }`, the repo-relative paths enqueued.
  - **`planFlowHostPackageUpgrade(...)`** enqueues the same set under `replace-if-changed`.
  - **`flowHostPackageDrift(repoRoot, config)`** returns `{ missing, changed }`, repo-relative and in shipped order, comparing bytes as buffers, as `cli/src/generators/outerLoopScripts.ts` → `outerLoopScriptDrift` does.
  - A staged tree that is absent or empty is a packaging fault, thrown through `internal()`.
  - The header's *"Deliberately not covered"* names one case: a file a later release stops shipping stays on disk, because nothing here removes.
- [ ] `init.ts`: call `writeFlowHostPackages` beside `writeOuterLoopScripts`, before `plan.apply`.
  - When `selfAdoptionOf(repoRoot)` holds (the local `selfAdopt`), skip the call and push one note: in the harness's own repository the packages live at the root, and `scripts/python/` links to them. Writing through those links would overwrite the sources, and `--force` would back them up into `src/`.
  - Keep `written` available for Task 7. Task 7 reads it as the condition for its post-plan note, and adds no second walk of the staged tree.
- [ ] `initUpgrade.ts`: call `planFlowHostPackageUpgrade` beside `planOuterLoopScriptUpgrade`, skipped under self-adoption by the same predicate `init.ts` uses.
  - In `init.ts` → `assertUpgradeFlagsUsable`, the refusal sentence *"it replaces only the outer-loop scripts and the permission profile"* now names the shipped Python packages too. Any other upgrade text that states the replaced set changes with it: grep `cli/src/upgrade/` for that phrase.
- [ ] `writer.ts` header table: add the row *"The shipped Python packages under `<scriptsDir>/python/` | `create-if-absent` for `init`; `replace-if-changed` under `init --upgrade` | Copied from the package's `dist/python/`, staged at build from the repository root; `init` skips them in the harness's own self-adopted repository"* (`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, the generated-or-copied-artifact row).
- [ ] `flow-host-packages.test.mjs`, its header stating the rule. It runs the compiled CLI against a throwaway fixture repository (`cli/test/helpers/fixture.mjs`) and asserts:
  - `init` writes `<scriptsDir>/python/devscene-flow-host/pyproject.toml` and `<scriptsDir>/python/graphscene/src/graphscene/__init__.py`, byte-identical to `cli/dist/python/`, under both the default `scriptsDir` and `--scripts-dir tools/harness`.
  - A second `init` changes nothing (idempotence).
  - An edited copy survives a plain re-run.
  - `--force` replaces it and leaves a `.bak` (`.claude/context/cli.md` → `## What "done" means here`).
  - `init --upgrade` restores the shipped bytes after a backup.
  - `flowHostPackageDrift` is not exported through a command. Its missing and changed cases are Task 8's to assert through `doctor`.

**Verification:**

- `npm test --workspace cli -- test/flow-host-packages.test.mjs` passes.
- `grep -n "flowHost" cli/src/commands/init.ts cli/src/upgrade/initUpgrade.ts` shows both calls, and both sit behind the self-adoption predicate.
- Existing `init` suites whose expected action logs list every written path may now list the new files. Update only the expectations this change moves, and only in suites this task edits.

**Deviations from plan:**

- `init.ts` adds a note when the packages are written (count, directory, the three re-run contracts), beside the self-adoption skip note the plan asks for. It is what keeps `written` in use under `noUnusedLocals`; Task 7 reads the same `written`.
- The plan's grep `grep -n "flowHost" … cli/src/upgrade/initUpgrade.ts` matches the import line only: the call is `planFlowHostPackageUpgrade` (capital `F`), behind `if (!target.selfAdopted)`. Verified by reading; `grep -n "FlowHost"` shows the call.
- `flowHostPackageDrift` also compares the owner-execute bit, as `outerLoopScriptDrift` does, beside the bytes.
- Verification bullet 3 (existing `init` suites whose action logs list every written path): not run — those suites (`cli/test/init.test.mjs`, `cli/test/init-upgrade.test.mjs` and others) are test files this unit neither created nor edited, which the test-run rule forbids a unit to run; deferred to the Run gates phase, where `commands.test` runs them. No expectation in them was edited.
- Out of this layer's path: `docs/cli.md` (`--upgrade` row, `## Updating an adopted repository`, the `--force` bullet) and `README.md` still state the upgrade replaces "the outer-loop scripts and the permission profile". Left for a `general`-layer change.
