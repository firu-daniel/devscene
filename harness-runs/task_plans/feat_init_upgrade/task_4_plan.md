### Task 4 — Merge local additions when the permission profile is rendered

**Goal:** Make the rendered permission profile equal the generated profile plus the adopter's validated local additions, on every run that writes it, and make the profile templates say so.

**Depends on:** Task 2, for `readLocalAdditions(repoRoot): LocalAdditions | undefined` and `LocalAdditions { fragment, count }`. Task 3, so the render already carries the local file's protection entries.

**Where this task stops.** `renderProfile` gains the merge and `writePermissionProfile` keeps its `create-if-absent` contract. The `--upgrade` planner is Task 5's. The story index's `## Scope register` rows 63, 64 and 75 to 81 are this task's template sites; Task 17 carries the same text into the rendered example.

### Targets

- `cli/src/generators/permissionProfile.ts`
- `cli/templates/claude/settings.autonomous.json`
- `cli/templates/claude/settings.autonomous.qa.json`
- `cli/templates/claude/settings.autonomous.retrieval.json`
- `cli/test/profile-local-merge.test.mjs` (new)

**Work:**

- [ ] `renderProfile`: add `localAdditions?: LocalAdditions` to `RenderProfileOptions`. After `applyWriteProtection` and before the final assertions, merge `localAdditions.fragment` with `mergeInto(profile, fragment, '', 'local additions')`, so generated entries stay first and duplicates collapse. Screen adopter input before the merge, with `HarnessError` rather than `internal()`: a `deny` entry for which `namesBrowserTool` is true, and an `allow` entry naming an `mcp__<server>__` tool whose server `enabledServers` does not start. Each message names `PROFILE_LOCAL_PATH` and the entry.
- [ ] `writePermissionProfile`: call `readLocalAdditions` and pass the result only when this run will write the file, meaning `force` is set or nothing exists at the profile path. A plain re-run that keeps the profile must not read, or fail on, the local file.
- [ ] Export `isToolchainEntry(entry: string, config: HarnessConfig): boolean`: true when `phases.parity` is on and the entry has the shape `appendToolchainAllowances` writes, `Bash(<absolute dir>/<command>:*)`, for a configured `parity.toolchainCommands` value. Update the module header's statements that the profile is hand-tuned.
- [ ] Rewrite these `_README` statements, keeping each line's other statements. In `settings.autonomous.json`: `UNATTENDED SETTINGS PROFILE` and `COMPLETENESS IS LOAD-BEARING` say the file is generated and replaced by `npx devscene init --upgrade`, and that an added entry belongs in `.claude/settings.autonomous.local.json`; `THE PACKAGE MANAGER` ("one literal entry here") and `` `deny` IS A FLOOR `` ("Add to it freely") send the addition to that file. In `settings.autonomous.qa.json`: `THE BROWSER HALF` ("yours once written", the forced route) and `THE PORT PROBE` ("add the one line by hand", "a --force run") name `init --upgrade` as what brings an existing profile current; `THE ALLOWED TOOL SET` ("one more entry here") sends the entry to the local file; `THE PHASE'S OWN HELPER SCRIPTS` keeps its opening words and says that resolved plugin-root lines are carried forward by `--force` and `--upgrade` alike. In `settings.autonomous.retrieval.json`: `THE DOCS-RETRIEVAL HALF` says the plain `init` adds the server to `.mcp.json`, and `init --upgrade` then brings the profile current. A command an adopter is told to run is spelled with `npx`, and no line may describe an entry as already "here" or "below".
- [ ] `profile-local-merge.test.mjs`: cover a fresh `init` and `init --force` carrying a local entry from each list, a plain re-run leaving a kept profile unchanged while the local file is invalid, a forced run with an invalid local file refused with the profile byte-identical, and the browser-deny and unstarted-MCP refusals.

**Verification:**

- `cli/test/profile-local-merge.test.mjs` passes.
- A local entry appears after every generated entry of its list and appears once.
- The rendered profile's non-list sandbox settings are identical with and without a local file.
- The story index's D1, D5 and D6 entries reach these three templates only at sites the register lists, and each `change` row's site states the new route.
