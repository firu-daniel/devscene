# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix

1. **Scope register: procedure P1 reaches sites that are not rows — story index (`feat_init_upgrade_story_plan.md`)**
   Re-walking P1 over `docs/cli.md` reaches three sites the table does not carry, so the closure invariant fails (disposition (i)):
   - `## 7.` bullet `profile-write-protection`, *"the profile is a file the adopter owns"*. This states who owns the profile, which is P1's decision rule. Row 30 covers only the fenced command under that bullet.
   - `## 3.` row `.github/workflows/devscene-trigger.yml`, *"shares their re-run contract: `--force`"*.
   - `## 3.` row `.github/workflows/devscene-control.yml`, the same clause.

   The two `## 3.` rows state what the outer-loop scripts' re-run route is, and after this branch the scripts have a route those workflows do not share. Row 45 already marks the same claim `change` in `docs/remote-execution.md`.
   **Raised against:** "**Closure invariant:** every site each derivation entry reaches appears as a row below."
   **Must hold:** Every `docs/cli.md` site P1's decision rule selects appears as a register row with a disposition.
   **Fix:** Add the three rows to the story index, each `change` and owned by Task 15, and add the three edits to `task_15_plan.md`.

2. **Scope register: row 24's `no-change` reason is wrong — story index (`feat_init_upgrade_story_plan.md`) and `task_15_plan.md`**
   The `command-permissions` bullet says, in the document's own prose, *"the profile is a file the adopter owns"*. That clause is not a message the check prints, and this branch makes it false: the profile becomes fully generated. Row 25 marks the same kind of clause `change` for `profile-paths`. Task 15 then limits its `## 7.` edit to that one bullet, so the false statement would ship (disposition (iii); no `## Rejected findings` entry applies).
   **Raised against:** "| 24 | `docs/cli.md` → `## 7.` bullet `command-permissions` | — | D2 | `no-change` | It reports the message the check prints, which still names `init --force` |"
   **Must hold:** No `docs/cli.md` bullet still states that the adopter owns the generated profile after Task 15, and no register reason misdescribes the text it covers.
   **Fix:** Change row 24 to `change`, owned by Task 15, and widen Task 15's `## 7.` bullet (*"change only the ownership clause of the `profile-paths` bullet"*) to cover the ownership clauses of `command-permissions` and `profile-write-protection`, printed remedies staying as they are.

3. **Scope register: no derivation entry reaches further ownership and route statements — story index (`feat_init_upgrade_story_plan.md`)**
   D1 to D4 and P1, P2 miss these verified sites (disposition (ii)). Several tell an adopter to do what this branch makes unsafe, because `--upgrade` replaces the profile and drops a hand-added entry:
   - `cli/templates/claude/settings.autonomous.json` → `_README` "THE PACKAGE MANAGER, THE BUILD AND THE DEPENDENCY INSTALL" (*"one literal entry here"*) and "`deny` IS A FLOOR, NOT A PREFERENCE" (*"Add to it freely"*).
   - `cli/templates/claude/settings.autonomous.qa.json` → `_README` "THE BROWSER HALF" and "THE ALLOWED TOOL SET" (*"one more entry here"*).
   - `cli/templates/claude/settings.autonomous.retrieval.json` → `_README` "THE DOCS-RETRIEVAL HALF" (*"it is yours once written"*, *"run `init --force`"*, and *"copy the two entries in"*), which also contradicts Task 15's new retrieval route.
   - `examples/notes-app/.claude/settings.autonomous.json` → the rendered copies of "THE PACKAGE MANAGER", "`deny` IS A FLOOR", "THE BROWSER HALF" and "THE ALLOWED TOOL SET".
   - `cli/templates/github/workflows/devscene-trigger.yml` and `devscene-control.yml` → the header comment *"their re-run contract"*, and `cli/src/core/writer.ts` → the same two workflows' table rows (*"as for the scripts it calls"*), which the register says Task 1 owns and Task 1 does not list.
   - `cli/templates/scripts/task-offer-check.sh` → *"upgrade route, as for every outer-loop script"*.
   - `cli/templates/scripts/autonomous-watcher.sh` → the two log messages ending *"`devscene init --force` rewrites it"*, about outer-loop files.
   - `plugin/scripts/reserve-qa-user.sh` → *"changed without `init --force` leaves the sandboxed `mkdir`"*.

   **Raised against:** "**Derivation entry D1 — statements of profile ownership (command).**"
   **Must hold:** The register's derivation entries, taken together, reach every statement that the generated profile is hand-editable or that the forced run is the scripts' or the profile's route, and each reached site has a row.
   **Fix:** Add this entry beside D1 to D4, which it was executed to confirm reaches every site above, and give each site one row per copy, either `change` with an owning task or `no-change` with a reason:

   `grep -rnIE 'their re-run contract|as for the scripts it calls|upgrade route, as for|one literal entry here|one more entry here|Add to it freely|yours once written|init --force.{1,2} rewrites it|without .init --force. leaves' cli/templates plugin/scripts examples/notes-app/.claude/settings.autonomous.json docs/cli.md cli/src/core/writer.ts`

   Extend Task 4's `_README` bullet, Task 1's table bullet and Task 17's example bullet for the rows marked `change`.

4. **Profile delta and drift skip most of the sandbox grant lists — `task_5_plan.md`**
   `PROFILE_ENTRY_LISTS` leaves out `sandbox.excludedCommands`, `sandbox.filesystem.allowWrite`, `sandbox.network.allowedDomains`, `sandbox.credentials.files`, `sandbox.credentials.envVars` and `enabledMcpjsonServers`, all list-valued in the rendered profile. A hand-added `allowWrite` path, unsandboxed command or network host is therefore neither listed by the first upgrade nor reported by `doctor`, and `--upgrade` removes it without a word. The prompt requires both reports, and the story index's first risk claims "Task 5 reports every list delta". `doctor`'s existing `profile-sandbox` check grades missing and stale entries and does not account for every added one.
   **Raised against:** "Export `PROFILE_ENTRY_LISTS` (`permissions.allow`, `permissions.ask`, `permissions.deny`, `permissions.additionalDirectories`, `sandbox.filesystem.denyWrite`)"
   **Must hold:** Every list-valued grant or restriction in the rendered profile takes part in the entry delta and the drift comparison, so no entry changes or disappears unreported.
   **Fix:** Extend `PROFILE_ENTRY_LISTS` to every list the render can produce, comparing `sandbox.credentials` lists by each element's identifying field, and add test cases for a hand-added `allowWrite`, `excludedCommands` and `allowedDomains` entry in both `profileEntryDelta` and `profileDrift`.

5. **New module has no required header — `task_9_plan.md`**
   `.claude/context/conventions.md` → `## What accompanies a new unit of each kind` requires a header comment on every module under `cli/src/`, and `.claude/context/cli.md` requires the rule wording where a module holds a rule. Tasks 2, 5, 7 and 8 call theirs out; this task does not.
   **Raised against:** "`cli/src/upgrade/report.ts` (new)"
   **Must hold:** The task calls out the module header its new module must open with.
   **Fix:** Add to the `**Work:**` list a header stating what `report.ts` owns and, in the mandated words, its rule that it reads no file and prints nothing.

6. **New module has no required header — `task_10_plan.md`**
   The same requirement as finding 5 applies to the command's new module.
   **Raised against:** "`cli/src/upgrade/initUpgrade.ts` (new)"
   **Must hold:** The task calls out the module header its new module must open with.
   **Fix:** Add a header to the `initUpgrade.ts` bullet stating what the module owns and the rule it enforces: only the two artifact classes are planned, through one plan applied once.

7. **Refusal notes and render warnings never reach the adopter — `task_10_plan.md`**
   Task 8 returns `UpgradeTarget.notes`, the only place a dry run says a real run would refuse. Task 5's `planProfileUpgrade` returns `warnings` and `notes`, including the carry-forward and toolchain messages. `upgradeReport`'s input takes none of them, and this task sends only that function's output. A dry run during an active run would therefore read as clean, and those units have no consumer.
   **Raised against:** "then send `upgradeReport`'s `notes`, `warnings` and `result` through `ctx.report`"
   **Must hold:** Every note and warning produced by `resolveUpgradeTarget` and `planProfileUpgrade` reaches the `Reporter`, on real and dry runs.
   **Fix:** Send those lists through `ctx.report` here, or add them to `upgradeReport`'s input in Task 9, and assert in `init-upgrade.test.mjs` that a dry run with an active run prints the would-refuse note.

8. **The example's ignore file has no such anchor — `task_17_plan.md`**
   `examples/notes-app/.gitignore` carries no `.claude/settings.autonomous.json` rule: the example commits its profile, and the file's comment speaks of "the committed profiles". The bullet cannot be carried out as written for that file.
   **Raised against:** "add `.claude/settings.autonomous.local.json` and its comment directly after the `.claude/settings.autonomous.json` rule"
   **Must hold:** Each ignore-file edit names a position that exists in that file.
   **Fix:** Keep the anchor for the root `.gitignore` only. For the example, name an existing anchor, such as directly after its `.claude/settings.local.json` rule, and word the comment so it does not imply the example's profile is ignored.

9. **Consumer does not restate the contracts it calls — `task_10_plan.md`**
   The task calls `resolveUpgradeTarget`, `planOuterLoopScriptUpgrade`, `planProfileUpgrade`, `upgradeReport` and `installedPluginVersion` by name only. Their parameters and return shapes exist only in Tasks 5 to 9, and the story index lists names without signatures, so the implementer has to read other task files.
   **Raised against:** "**Depends on:** Task 1 (`WriteContext.backupDir`), Task 5 (`planProfileUpgrade`), Task 6 (`planOuterLoopScriptUpgrade`), Task 7 (`installedPluginVersion`), Task 8 (`resolveUpgradeTarget`) and Task 9 (`upgradeReport`)."
   **Must hold:** The file can be implemented without opening another per-task file.
   **Fix:** Restate each called signature and the return fields this task reads, including `upgradeReport`'s full input object.

10. **Consumer does not restate the contracts it calls — `task_11_plan.md`**
    `profileDrift`, `outerLoopScriptDrift`, `installedPluginVersion` and the `core/runRegistry.js` exports are named with no signature or result shape.
    **Raised against:** "**Depends on:** Task 5 (`profileDrift`), Task 6 (`outerLoopScriptDrift`), Task 7 (`pidIsAlive`, `RUNNING_STATUS`, `installedPluginVersion`) and Task 10, so the command each remedy names exists."
    **Must hold:** The file can be implemented without opening another per-task file.
    **Fix:** Restate `profileDrift({ repoRoot, config, onDisk })` with its `{ missing, unaccounted }` entries, `outerLoopScriptDrift(repoRoot, config)` with its `{ missing, changed }`, `installedPluginVersion(repoRoot?)`, and the two run-registry exports.

11. **Consumer does not restate `ProfileEntryDelta` — `task_9_plan.md`**
    The report is built from this type, and the task gives neither its fields nor their types.
    **Raised against:** "**Depends on:** Task 5, for `ProfileEntryDelta`."
    **Must hold:** The shape this task consumes is stated in this file.
    **Fix:** Restate `{ readonly list: string; readonly added: readonly string[]; readonly removed: readonly string[] }`.

12. **Consumer does not restate `isToolchainEntry` — `task_5_plan.md`**
    `profileDrift` depends on this function, but its parameters and meaning are stated only in Task 4.
    **Raised against:** "Task 4 (`renderProfile`'s `localAdditions` option and `isToolchainEntry`)"
    **Must hold:** The contract this task calls is stated in this file.
    **Fix:** Restate `isToolchainEntry(entry: string, config: HarnessConfig): boolean` and what it accepts.

## Should Fix

- `task_2_plan.md`: *"a character device that reads empty"* defines an accepted shape by reading it, which can block or never end on a device other than the placeholder. `harness-runs/lessons.md` says: "When a trust check meets a file an actor outside your control creates on every run, accept only its provably inert shape". Identify the null device by its device numbers, without reading it, and add a refusal case for another character device.

## Nice to Have

- `task_9_plan.md`: `localAdditionCount` is in `upgradeReport`'s input, but no bullet says what the report does with it.
