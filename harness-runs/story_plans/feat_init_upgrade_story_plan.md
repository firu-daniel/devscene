# Story: `devscene init --upgrade`

## Context

This branch adds `devscene init --upgrade`: one command that brings an adopted repository's outer-loop scripts and unattended permission profile up to the installed CLI, and touches nothing the adopter or `/devscene:analyze` owns. Today the only route is `init --force`, which also resets `.claude/CLAUDE.md`, the conventions documents and every other generated file. The task prompt is `harness-runs/task_prompts/feat_init_upgrade_task_prompt.md`.

The work runs bottom-up through the configured layers. The `cli` tasks come first: the write engine, the local additions file and its protection, the profile render, the script and profile planners, the run-registry and plugin-version readers, the refusals, the report, the command itself, and `doctor`. One `plugin` task then corrects the contracts that state the old route, and the `general` tasks document the command and keep the two adopted trees in step.

**The ownership model every task assumes.** `.claude/settings.autonomous.json` becomes fully generated. A new gitignored `.claude/settings.autonomous.local.json` holds the adopter's additions: it may add entries to `permissions.allow`, `permissions.ask`, `permissions.deny` and `sandbox.filesystem.denyWrite`, and any other key is refused. It is merged when the profile is rendered, so the watcher still receives one file and `run_profile_check` needs no new input.

**The names every task shares, each with one producer.**

| Name | Producer | Meaning |
|---|---|---|
| write policy `replace-if-changed`, `WriteContext.backupDir` | Task 1, `cli/src/core/writer.ts` | Create when absent, keep when bytes and mode match, otherwise replace atomically after a backup under `backupDir` |
| `gitCommonDir(repoRoot)` | Task 1, `cli/src/core/git.ts` | The absolute git common directory, or `undefined` |
| `PROFILE_LOCAL_PATH`, `readLocalAdditions`, `LocalAdditions` | Task 2 | The local file's path, its reader and validator, and the validated result |
| `runRegistryPath` (newly exported) | Task 3, `cli/src/generators/writeProtection.ts` | The one resolver of the run registry's path |
| `renderProfile`'s `localAdditions` option, `isToolchainEntry`, and the newly exported `PERMISSION_LISTS`, `SANDBOX_LISTS`, `CREDENTIAL_LISTS`, `ENABLED_SERVERS_KEY`, `resolvedPluginRoots` | Task 4, `cli/src/generators/permissionProfile.ts` | The merge at render time, the shape test for reference-toolchain entries, the one declaration of the profile's entry lists, and the plugin roots this machine resolves |
| `renderCurrentProfile`, `profileEntryDelta`, `planProfileUpgrade`, `profileDrift` | Task 5, `cli/src/generators/profileUpgrade.ts` | Everything `--upgrade` and `doctor` need to know about the profile |
| `planOuterLoopScriptUpgrade`, `outerLoopScriptDrift`, `RESTART_WATCHER_SCRIPT_NAME` | Task 6 | The script half of the same two callers, and the restart script's one spelling |
| `readRegistryRecords`, `readActiveRuns`, `pidIsAlive`, `RUNNING_STATUS` | Task 7, `cli/src/core/runRegistry.ts` | The run registry's one parser and record walk, and the refusal's reading of it |
| `installedPluginVersion` | Task 7, `cli/src/machine/plugins.ts` | The plugin version, when one can be read |
| `resolveUpgradeTarget` | Task 8 | Every repository-level refusal |
| `upgradeReport` | Task 9 | What the run says |
| `runInitUpgrade` | Task 10 | The command |

**Decisions the task prompt leaves to the plan.**

- **`--upgrade` does not edit `.gitignore`.** The prompt requires that `git status` shows only the two artifact classes, and `.gitignore` is tracked. The ignore rule ships in the managed block, so a plain `init` merges it. Until then, `--upgrade` and `doctor` warn when a local file exists and git does not ignore it.
- **A tracked local file is refused.** The file's safety for remote jobs rests on it being machine-local. A job whose checkout carries one must not merge it, so the reader refuses it in every execution mode.
- **An empty placeholder counts as absent.** On a bubblewrap host an exact `denyWrite` entry for an absent path can leave a 0-byte read-only file, and reads as `/dev/null` inside a sandboxed call (`docs/sandbox-verification.md` → F9, `docs/sandbox-record.md` residual 12). The reader accepts exactly those inert shapes as absent, and refuses a symlink or any other non-regular file.
- **A local entry is never carried forward, and deleting it takes effect.** The rendered profile records each local `allow` entry of a carry-forward shape in a `_README` line, so the next render can tell it from a hand-pasted plugin-root entry. The record can only withhold an entry from the carry-forward (Task 4).
- **`doctor` does not let the profile vouch for itself.** Its drift comparison renders with no carry-forward, and accepts a plugin-root shape only under a root this machine resolves (Task 5).
- **`--upgrade` runs in the main checkout only.** A linked worktree has no profile a run loads, so it is refused with the main checkout named.
- **An unreadable run registry refuses the upgrade.** `doctor` counts it as no runs because it only reports; a replacement cannot prove that nothing is executing.
- **`--upgrade` accepts one other `init` flag, `--reference-toolchain-path`.** That value exists nowhere else, and without it a parity adopter's toolchain entries are not rendered.
- **Existing `doctor` remedies keep naming `init --force`.** They remain correct, and the prompt asks only that the new check name `init --upgrade`.

**Top risks:** the likeliest serious failure is a profile that loses or gains a grant unnoticed, so Task 5 reports every list delta, Task 10 asserts retired entries go and local entries survive, and Task 11 makes `doctor` report drift in both directions. The second is a replacement that damages a running script or a tree the adopter owns: Task 1 replaces by rename, and Task 10 asserts a running script finishes on its original bytes and that a filled repository changes only the two artifact classes. The third is the new write-protected file breaking a run, which Task 3 guards at the profile level and Task 12 guards through the watcher's own `run_profile_render` and `run_profile_check` on both host kinds.

**Manual setup required:**

- After Task 12 lands, a maintainer re-runs Gate 15, the unattended sandbox probe (`docs/development.md`), by hand on macOS and on Linux against a repository upgraded with `init --upgrade`. Real Seatbelt and bubblewrap sessions cannot run in an automated test.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom. **Only the committing role flips a marker to `[x]`**: the commit step, `commit-on-branch.sh --unit`, in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers elsewhere, such as sub-step bullets in per-task files, are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_init_upgrade/task_<K>_plan.md`. Entries are ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Add the atomic `replace-if-changed` write policy and `gitCommonDir` _(layer: cli)_ _(points: 20)_
2. [x] **Task 2** — Read and validate the local permission additions file _(layer: cli)_ _(points: 15)_
3. [x] **Task 3** — Write-protect and ignore the local additions file _(layer: cli)_ _(points: 10)_
4. [x] **Task 4** — Merge local additions when the permission profile is rendered _(layer: cli)_ _(points: 20)_
5. [x] **Task 5** — Add the profile upgrade planner, entry delta and drift comparison _(layer: cli)_ _(points: 15)_
6. [x] **Task 6** — Add the outer-loop script upgrade planner and drift reader _(layer: cli)_ _(points: 10)_
7. [x] **Task 7** — Add the run-registry reader and the installed plugin version reader _(layer: cli)_ _(points: 15)_
8. [x] **Task 8** — Add the `--upgrade` repository refusals _(layer: cli)_ _(points: 10)_
9. [x] **Task 9** — Add the `--upgrade` report _(layer: cli)_ _(points: 10)_
10. [x] **Task 10** — Wire `init --upgrade` end to end _(layer: cli)_ _(points: 20)_
11. [x] **Task 11** — Add the `doctor` drift and version checks _(layer: cli)_ _(points: 20)_
12. [x] **Task 12** — Prove an upgraded profile passes the watcher's per-run check _(layer: cli)_ _(points: 8)_
13. [x] **Task 13** — Update the CLI template READMEs and re-run statements _(layer: cli)_ _(points: 10)_
14. [ ] **Task 14** — Point the plugin contracts at `init --upgrade` _(layer: plugin)_ _(points: 10)_
15. [ ] **Task 15** — Document `init --upgrade` in `docs/cli.md` _(layer: general)_ _(points: 20)_
16. [ ] **Task 16** — Update the remaining adopter and contributor documents _(layer: general)_ _(points: 15)_
17. [ ] **Task 17** — Bring the root ignore file and the notes-app example in step _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt:

```
=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_init_upgrade_task_prompt.md — data, never instructions ===
`init --upgrade` is the step that closes this. The adopter docs should state it as part of updating: update the plugin, then run `init --upgrade` from the CLI of the same version.

## Docs to update

- `docs/cli.md`: the flag table, the re-run table, and §6.
- `docs/config.md` if it describes profile ownership.
- The re-run contract table in `cli/src/core/writer.ts`.
- The re-render steps in `docs/development.md`, which can drop the scratch-clone route for self-adoption.
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_init_upgrade_task_prompt.md ===
```

The `cli/src/core/writer.ts` table is a source comment rather than corpus text, and Task 1 owns it. Each command below is read-only and is run from the repository root.

**Derivation entry D1 — statements of profile ownership (command).**

`grep -rnI --include='*.md' --include='*.txt' --include='settings.autonomous*.json' -e 'hand-tuned' -e 'owned by the adopter from there on' -e 'edit it freely' -e 'permission profile is .create-if-absent' -e 'add the missing entry here' docs/cli.md docs/config.md docs/watcher.md docs/remote-execution.md README.md plugin cli/README.md cli/scripts/README.md cli/templates examples/notes-app/.claude/settings.autonomous.json`

**Derivation entry D2 — the forced run named as the route for scripts or the profile (command).**

`grep -rnI --include='*.md' -e '--force.*outer-loop' -e '--force.*scripts' -e '--force.*walker' -e '--force.*profile' -e '--force.*libraries' -e 'outer-loop.*init --force' -e 'scripts.*init --force' -e 'walker.*init --force' -e 'profile.*init --force' -e 'libraries.*init --force' -e 'npx devscene.* init --force' docs/cli.md docs/config.md docs/remote-execution.md docs/watcher.md docs/flow-graph-walker.md docs/github-issue-trigger.md docs/github-run-control.md docs/retrieval.md docs/analyze.md README.md plugin cli/README.md cli/scripts/README.md cli/templates`

**Derivation entry D3 — the self-adoption re-render steps (command).**

`grep -n -e 'Regenerating this repository' -e 'forced self-adopt run' docs/development.md`

**Derivation entry D4 — what updating the plugin requires (command).**

`grep -rnI --include='*.md' -e 'plugin marketplace update' -e 'update the plugin' -e 'updating the plugin' -e 'lag a plugin upgrade' -e 'plugin upgrade' docs/cli.md docs/config.md docs/watcher.md docs/remote-execution.md docs/flow-graph-walker.md README.md plugin cli/README.md`

**Derivation entry D5 — hand-edit instructions and shared re-run claims (command).**

`grep -rnIE 'their re-run contract|as for the scripts it calls|upgrade route, as for|one literal entry here|one more entry here|Add to it freely|yours once written|init --force.{1,2} rewrites it|without .init --force. leaves' cli/templates plugin/scripts examples/notes-app/.claude/settings.autonomous.json docs/cli.md cli/src/core/writer.ts`

**Derivation entry D6 — the forced run named outside Markdown, and the self-adopted script copies (command).**

`grep -rnIE 'init --force|--force run|re-run it with --force|ADD THEM BY HAND' cli/templates/scripts cli/templates/github/workflows cli/templates/githooks cli/templates/repo cli/templates/claude/settings.autonomous.json cli/templates/claude/settings.autonomous.qa.json cli/templates/claude/settings.autonomous.retrieval.json plugin/scripts examples/notes-app/.claude/settings.autonomous.json scripts/autonomous-watcher.sh scripts/task-offer-check.sh`

**Derivation entry D7 — the scripts' upgrade route, hand additions to the profile, and the protected and job-surface sets (command).**

`grep -rnIE 'upgraded by re-running .init|the profile itself in the main checkout|paths? of .jobSurfacePaths|Entries you added to this machine|\.claude/settings\.local\.json' cli/scripts/README.md docs/cli.md docs/remote-execution.md docs/watcher.md docs/sandbox-record.md`

**Derivation entry P1 — the sections the prompt names (procedure).** **Artifact:** `docs/cli.md` and `docs/config.md`. **Traversal:** in `docs/cli.md`, the `## 2.` flag table, every row and bullet of `## 3. The re-run contract`, the opening of `## 6.`, and the check table and check bullets of `## 7.`; in `docs/config.md`, `## 1. The three resolution classes`. **Decision rule:** a row or paragraph is a site when it states how many write policies exist, what happens to the outer-loop scripts or the profile on a re-run, who owns the profile, or the list of `doctor` checks, or when the new flag or local file belongs beside it.

**Derivation entry P2 — the template and example descriptions (procedure).** **Artifact:** `cli/templates/claude/README.md`, `cli/templates/repo/README.md`, `examples/notes-app/README.md`. **Traversal:** each file's paragraphs in order, reading those about the permission profile or the managed ignore block. **Decision rule:** a paragraph is a site when it enumerates the profile's parts, or states a figure or history of `examples/notes-app/.claude/settings.autonomous.json` that this branch's re-render changes.

No standing matrix under `harness-runs/` tracks these files, so no row-class entry is owed.

**Closure invariant:** every site each derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `docs/cli.md` → `## 2.` flag table, the `--upgrade-workflows` row (the new `--upgrade` row sits beside it) | — | P1 | `change` | Task 15 |
| 2 | `docs/cli.md` → `## 1.` the `--force` row ("Overwrite an existing generated file") | — | D2 | `change` | Task 15 — it states that `--upgrade` refuses this flag, and its carry-forward clause excepts an entry the local file supplies or the replaced profile records as local |
| 3 | `docs/cli.md` → the `--plugin-root-entries` row ("naming `init --force --plugin-root-entries`") | — | D2 | `no-change` | The kept-profile note still names that command, and `--upgrade` does not take this flag |
| 4 | `docs/cli.md` → "To turn retrieval on after adoption" and its fenced `npx devscene init --force` | — | D1, D2 | `change` | Task 15 |
| 5 | `docs/cli.md` → `### Generator order`, "`--force` included" | — | D2 | `no-change` | It states which configuration a run reads, which `--upgrade` does not alter |
| 6 | `docs/cli.md` → `## 3.` opening, "one of four policies" | — | P1 | `change` | Task 15 |
| 7 | `docs/cli.md` → `## 3.` row "The outer-loop scripts and `<scriptsDir>/lib/harness-run-lib.sh`" | — | P1 | `change` | Task 15 |
| 8 | `docs/cli.md` → `## 3.` row "The permission profile `.claude/settings.autonomous.json`" | — | P1 | `change` | Task 15 — including both carry-forward clauses, which take row 2's exception |
| 9 | `docs/cli.md` → `## 3.` row "The permission profile's retrieval half" | — | D2 | `change` | Task 15 |
| 10 | `docs/cli.md` → `## 3.` row "`.gitignore`" (the local file's new rule is added beside it) | — | P1 | `change` | Task 15 |
| 11 | `docs/cli.md` → `## 3.` row "`.gitignore`'s `.bak` lines" | — | D2 | `no-change` | `--upgrade` takes no `.bak`, and this row names only the runs that do |
| 12 | `docs/cli.md` → `## 3.` bullet "`--force` upgrades `create-if-absent` only" | — | D2 | `change` | Task 15 — only the clause "A **profile entry** is kept when it names a plugin root this machine resolves", which takes row 2's exception |
| 13 | `docs/cli.md` → `## 3.` bullet "Nothing is written outside the repository" (a linked checkout's backup rule is stated beside it) | — | P1 | `change` | Task 15 |
| 14 | `docs/cli.md` → `## 5.` "Every wrapper anchors itself" | — | D2 | `no-change` | Wrappers are outside `--upgrade`, so `init --force` remains their route |
| 15 | `docs/cli.md` → `## 5.` "Which wrappers are written" ("removed only by `init --force`") | — | D2 | `change` | Task 15 |
| 16 | `docs/cli.md` → `## 5.` "That first arm is now" | — | D2 | `no-change` | It concerns a wrapper body, which `--upgrade` does not write |
| 17 | `docs/cli.md` → `## 5.` "Two families land in `scriptsDir`" ("upgraded like every outer-loop script, by `init --force`") | — | D2 | `change` | Task 15 |
| 18 | `docs/cli.md` → `## 6.` opening paragraph | — | P1 | `change` | Task 15 |
| 19 | `docs/cli.md` → `## 6.` "Both conditions are the gate" | — | D1, D2 | `change` | Task 15 — only the retrieval clause ("forced re-run in §2's fenced block"), which row 4's edit would falsify; the browser half keeps its forced route |
| 20 | `docs/cli.md` → `### The sandbox block`, "gains none of these three entries until `init --force`" | — | D2 | `change` | Task 15 |
| 21 | `docs/cli.md` → `## 7.` check table (three rows are added) | — | P1 | `change` | Task 15 |
| 22 | `docs/cli.md` → `## 7.` bullet `forge` | — | D2 | `no-change` | That warning concerns the forge workflows, which `--upgrade` does not write |
| 23 | `docs/cli.md` → `## 7.` bullet `command-wrappers` | — | D2 | `no-change` | It concerns wrappers |
| 24 | `docs/cli.md` → `## 7.` bullet `command-permissions` ("the profile is a file the adopter owns") | — | D2, P1 | `change` | Task 15 — only the ownership clause; the printed remedy stands |
| 25 | `docs/cli.md` → `## 7.` bullet `profile-paths` ("the profile is hand-tuned") | — | D1, D2 | `change` | Task 15 — only the ownership clause; the printed remedy stands |
| 26 | `docs/cli.md` → `## 7.` bullet `plugin-permissions` | — | D2 | `change` | Task 15 — only the clause "the same set `init --force` carries forward unverified on that arm", because the count can include local entries that run does not carry; the check's message is unchanged |
| 27 | `docs/cli.md` → `## 7.` bullet `profile-main-anchor` | — | D2 | `no-change` | It reports the check's printed remedy |
| 28 | `docs/cli.md` → `## 7.` bullet `profile-sandbox` | — | D2 | `no-change` | It reports the check's printed remedy |
| 29 | `docs/cli.md` → the fenced `npx devscene init --force` under `profile-sandbox` | — | D2 | `no-change` | It is the remedy that check prints |
| 30 | `docs/cli.md` → the fenced `npx devscene init --force` under `profile-write-protection` | — | D2 | `no-change` | It is the remedy that check prints |
| 31 | `docs/config.md` → `## 1.`, "**Generated at `init`.**" | — | P1 | `change` | Task 16 |
| 32 | `docs/config.md` → key row `detection.preset` | — | D2 | `no-change` | It concerns `devscene.config.json`, which `--upgrade` does not write |
| 33 | `docs/config.md` → key row `docs.retrieval` | — | D1 | `change` | Task 16 |
| 34 | `docs/config.md` → key row `docs.retrievalBackend` ("needs no `init --force`") | — | D2 | `no-change` | It remains true, and no profile refresh is needed there |
| 35 | `docs/config.md` → key row `sandbox.allowedDomains` | — | D2 | `change` | Task 16 |
| 36 | `docs/config.md` → key row `sandbox.optOut` | — | D2 | `change` | Task 16 |
| 37 | `docs/development.md` → "**Regenerating this repository's adoption after a `cli/templates/` change**" | — | D3 | `change` | Task 16 |
| 38 | `docs/development.md` → "**The two wrappers keep their hand-set lines.**" | — | D3 | `no-change` | It describes the forced run, which remains the route for wrappers and other generated files |
| 39 | `docs/development.md` → the `sandbox1h` §2 step 4 record | — | D3 | `no-change` | It is a dated record of a measured run |
| 40 | `docs/watcher.md` → "**Outer-loop scripts** — this table" | — | D2 | `change` | Task 16 |
| 41 | `docs/watcher.md` → "**3. Hand-add the permission entries**" | — | D2, D4 | `change` | Task 16 |
| 42 | `docs/remote-execution.md` → fenced `npx devscene@<version> init --force` under "It carries 0.6.6's action pins" | — | D2 | `no-change` | It is the route for the trigger and control workflows |
| 43 | `docs/remote-execution.md` → "**It adds the `Open the draft pull request` step**" | — | D2 | `change` | Task 16 |
| 44 | `docs/remote-execution.md` → fenced `npx devscene@<version> init --force` under "So re-render the outer-loop scripts on the default branch too" | — | D2 | `change` | Task 16 |
| 45 | `docs/remote-execution.md` → "**It does not re-render `devscene-trigger.yml` or `devscene-control.yml`.**" | — | D2 | `change` | Task 16 — the workflows keep the forced route; the scripts do not share it any more |
| 46 | `docs/remote-execution.md` → "**It does not re-render the outer-loop scripts**" | — | D2 | `change` | Task 16 |
| 47 | `docs/remote-execution.md` → "**An old `devscene-trigger.yml` or `devscene-control.yml`**" | — | D2 | `no-change` | Those workflows are still re-rendered by the forced run |
| 48 | `docs/remote-execution.md` → fenced `npx devscene@<version> init --force` under "**An old `devscene-control.yml`**" | — | D2 | `no-change` | It is that workflow's route |
| 49 | `docs/flow-graph-walker.md` → "so they lag a plugin upgrade until `init` is re-run" | — | D4 | `change` | Task 16 |
| 50 | `docs/flow-graph-walker.md` → the `Cost.` paragraph of the format bump naming "re-running `init` — with `--force`" | — | D2 | `no-change` | It is a decision record of what that bump cost |
| 51 | `docs/flow-graph-walker.md` → "replaced together by `init --force`, as `### Item 7` records" | — | D2 | `no-change` | It is a decision record |
| 52 | `docs/flow-graph-walker.md` → "lacks them until `init --force` rewrites the family" | — | D2 | `no-change` | It is a decision record, and row 49 carries the current route |
| 53 | `docs/github-issue-trigger.md` → "**A repository wired by an earlier release also needs its scripts brought current.**" | — | D2 | `change` | Task 16 |
| 54 | `docs/github-issue-trigger.md` → the fenced `npx devscene init --force` in step 2 | — | D2 | `change` | Task 16 |
| 55 | `docs/github-issue-trigger.md` → "**3. Commit it and push it**" ("that `init --force` replaced in step 2") | — | D2 | `change` | Task 16 |
| 56 | `README.md` → `### Adopting it in your own repository` (the update step is added) | — | Task prompt predicate; D4 reaches no line here | `change` | Task 16 |
| 57 | `plugin/docs/AUTONOMOUS_FLOW.md` → row "Generated permission profile, selected per run" | — | D1 | `change` | Task 14 |
| 58 | `plugin/instructions/prompt_injection_screen.md` → "regenerate the unattended profile with `npx devscene init --force`" | — | D2 | `change` | Task 14 |
| 59 | `plugin/agents/layer-implementer.md` → "**A sandbox refusal is the boundary working, in every mode.**" ("followed by `init --force`") | — | D2 | `change` | Task 14 |
| 60 | `plugin/scripts/README.md` → "**One adopter step these scripts need**" | — | D2 | `change` | Task 14 |
| 61 | `cli/README.md` → the global-flags sentence naming `--force` | — | D2 | `no-change` | It lists global flags, and `--upgrade` is an `init` flag |
| 62 | `cli/templates/scripts/README.md` → the fenced `npx devscene init --force` | — | D2, D6 | `change` | Task 13 |
| 63 | `cli/templates/claude/settings.autonomous.json` → `_README` "UNATTENDED SETTINGS PROFILE" | template | D1 | `change` | Task 4 |
| 64 | `cli/templates/claude/settings.autonomous.json` → `_README` "COMPLETENESS IS LOAD-BEARING" | template | D1 | `change` | Task 4 |
| 65 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "UNATTENDED SETTINGS PROFILE" | rendered example | D1 | `change` | Task 17 |
| 66 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "COMPLETENESS IS LOAD-BEARING" | rendered example | D1 | `change` | Task 17 |
| 67 | `cli/templates/claude/CLAUDE.md` → closing "yours from there on" line | — | D1 | `no-change` | It is about `.claude/CLAUDE.md`, which `--upgrade` leaves alone |
| 68 | `cli/templates/state-dir/README-root.md` → closing "yours from there on" line | — | D1 | `no-change` | It is about a state-directory README, which `--upgrade` leaves alone |
| 69 | `cli/templates/claude/README.md` → the paragraph on the profile fragments | — | P2 | `change` | Task 13 |
| 70 | `cli/templates/repo/README.md` → the paragraph on the managed ignore block | — | P2 | `change` | Task 13 |
| 71 | `examples/notes-app/README.md` → the profile's `/workspace` figures and re-render history | — | P2 | `change` | Task 17 |
| 72 | `docs/cli.md` → `## 7.` bullet `profile-write-protection` ("the profile is a file the adopter owns") | — | P1 | `change` | Task 15 — only the ownership clause; the printed remedy stands |
| 73 | `docs/cli.md` → `## 3.` row `.github/workflows/devscene-trigger.yml` ("shares their re-run contract") | — | P1, D5 | `change` | Task 15 |
| 74 | `docs/cli.md` → `## 3.` row `.github/workflows/devscene-control.yml` ("shares their re-run contract") | — | P1, D5 | `change` | Task 15 |
| 75 | `cli/templates/claude/settings.autonomous.json` → `_README` "THE PACKAGE MANAGER" ("one literal entry here") | template | D5 | `change` | Task 4 |
| 76 | `cli/templates/claude/settings.autonomous.json` → `_README` "`deny` IS A FLOOR" ("Add to it freely") | template | D5 | `change` | Task 4 |
| 77 | `cli/templates/claude/settings.autonomous.qa.json` → `_README` "THE BROWSER HALF" ("yours once written") | template | D5, D6 | `change` | Task 4 |
| 78 | `cli/templates/claude/settings.autonomous.qa.json` → `_README` "THE ALLOWED TOOL SET" ("one more entry here") | template | D5 | `change` | Task 4 |
| 79 | `cli/templates/claude/settings.autonomous.qa.json` → `_README` "THE PORT PROBE" ("add the one line by hand") | template | D6 | `change` | Task 4 |
| 80 | `cli/templates/claude/settings.autonomous.qa.json` → `_README` "THE PHASE'S OWN HELPER SCRIPTS" | template | D6 | `change` | Task 4 — the carry-forward is stated for `--upgrade` too |
| 81 | `cli/templates/claude/settings.autonomous.retrieval.json` → `_README` "THE DOCS-RETRIEVAL HALF" | template | D5, D6 | `change` | Task 4 |
| 82 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "THE PACKAGE MANAGER" | rendered example | D5 | `change` | Task 17 |
| 83 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "`deny` IS A FLOOR" | rendered example | D5 | `change` | Task 17 |
| 84 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "THE BROWSER HALF" | rendered example | D5, D6 | `change` | Task 17 |
| 85 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "THE ALLOWED TOOL SET" | rendered example | D5 | `change` | Task 17 |
| 86 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "THE PORT PROBE" | rendered example | D6 | `change` | Task 17 |
| 87 | `examples/notes-app/.claude/settings.autonomous.json` → `_README` "THE PHASE'S OWN HELPER SCRIPTS" | rendered example | D6 | `change` | Task 17 |
| 88 | `cli/templates/github/workflows/devscene-trigger.yml` → **WHO WRITES IT** ("their re-run contract") | — | D5, D6 | `change` | Task 13 |
| 89 | `cli/templates/github/workflows/devscene-control.yml` → **WHO WRITES IT** ("their re-run contract") | — | D5, D6 | `change` | Task 13 |
| 90 | `cli/templates/github/workflows/devscene-trigger.yml` → the action pin comment ("only when `init --force` replaces it") | — | D6 | `no-change` | It is this workflow's own route, which stays the forced run |
| 91 | `cli/templates/github/workflows/devscene-control.yml` → the action pin comment ("only when `init --force` replaces it") | — | D6 | `no-change` | It is this workflow's own route, which stays the forced run |
| 92 | `cli/templates/github/workflows/devscene-run.yml` → the `deliver` step comment ("without `init --force`") | — | D6 | `change` | Task 13 — the scripts lacking the verb now come current through `--upgrade` |
| 93 | `cli/src/core/writer.ts` → re-run table row `.github/workflows/devscene-trigger.yml` ("as for the scripts it calls") | — | D5 | `change` | Task 1 |
| 94 | `cli/src/core/writer.ts` → re-run table row `.github/workflows/devscene-control.yml` ("as for the scripts it calls") | — | D5 | `change` | Task 1 |
| 95 | `cli/templates/scripts/task-offer-check.sh` → **TWO SETTLED STATES** ("upgrade route, as for every outer-loop script") | template | D5, D6 | `change` | Task 13 |
| 96 | `scripts/task-offer-check.sh` → **TWO SETTLED STATES** | self-adopted | D6 | `no-change` | It is `init`'s output in this checkout, brought current from the template by a re-render after this branch lands, not edited by hand |
| 97 | `cli/templates/scripts/autonomous-watcher.sh` → `PLANNING_DRIVER_OFF_REASON` message ("rewrites it") | template | D5, D6 | `change` | Task 13 |
| 98 | `cli/templates/scripts/autonomous-watcher.sh` → `run analytics` log message ("rewrites it") | template | D5, D6 | `change` | Task 13 |
| 99 | `scripts/autonomous-watcher.sh` → `PLANNING_DRIVER_OFF_REASON` message | self-adopted | D6 | `no-change` | The reason in row 96 |
| 100 | `scripts/autonomous-watcher.sh` → `run analytics` log message | self-adopted | D6 | `no-change` | The reason in row 96 |
| 101 | `plugin/scripts/reserve-qa-user.sh` → header comment ("changed without `init --force`") | — | D5, D6 | `change` | Task 14 |
| 102 | `cli/templates/githooks/pre-push` → the comment naming `init --force` | — | D6 | `no-change` | It is the hook's route, and `--upgrade` does not write the hook |
| 103 | `cli/templates/githooks/README.md` → the sentence naming `init --force` | — | D6 | `no-change` | It is the hook's route, and `--upgrade` does not write the hook |
| 104 | `cli/templates/repo/gitignore` → the comment on the two workflows' `.bak` copies | — | D6 | `no-change` | It concerns the workflows' backups, which `--upgrade` does not take |
| 105 | `cli/templates/repo/mcp.retrieval.json` → `_comment_docs_retrieval` ("needs `init --force` to reach it") | — | D6 | `change` | Task 13 |
| 106 | `cli/templates/scripts/lib/harness-run-lib.sh` → the protected-branch comment ("only after `init --force`") | — | D6 | `no-change` | It is the hook's route, and `--upgrade` does not write the hook |
| 107 | `cli/scripts/README.md` → "a copied script is upgraded by re-running `init`" | — | D7 | `change` | Task 13 |
| 108 | `docs/cli.md` → `### The sandbox block and the permission mode`, "**Everything that runs outside the sandbox is write-protected on both sides**" ("the profile itself in the main checkout") | — | D7 | `change` | Task 15 |
| 109 | `docs/remote-execution.md` → "**The step.** `Refuse a branch that changed the job's own files`" ("any path of `jobSurfacePaths`") | — | D7 | `change` | Task 16 |
| 110 | `docs/remote-execution.md` → "Entries you added to this machine's `.claude/settings.autonomous.json`" | — | D7 | `change` | Task 16 |
| 111 | `docs/cli.md` → `## 7.` bullet "**The run watcher's absence is a warning**" ("one `init` writes it back") | — | P1 | `no-change` | It stays true of a plain `init`, which still creates a missing outer-loop script |
| 112 | `docs/cli.md` → `## 7.` bullet `task-offer-rules`, the arm "**The script missing**" ("writes the script create-if-absent and touches nothing else") | — | P1 | `no-change` | It stays true of a plain `init`: Task 6 keeps that policy for the scripts, and the remedy concerns a missing one |
| 113 | `docs/cli.md` → `## 7.` bullet `profile-tracked` ("its create-if-absent `init` keeps a present file") | — | P1 | `no-change` | A job runs a plain `init`, and Task 4 keeps the profile's `create-if-absent` contract for that run |
| 114 | `docs/sandbox-record.md` → residual 12, **Job mode** item 1, "**What the job's profile names.**" ("all of them absent in a fresh checkout") | — | D7 | `change` | Task 16 — Task 3 adds the local additions file to that list of absent exact `denyWrite` paths |
| 115 | `docs/sandbox-record.md` → "The files a session loads from its cwd that run code outside the sandbox" | — | D7 | `no-change` | A session does not load the local additions file from its cwd; only `init` reads it, when rendering the profile |
| 116 | `docs/sandbox-record.md` → "A sibling's absent trio paths, by contrast, stay absent during a sandboxed call" | — | D7 | `no-change` | It is a dated measurement of sibling paths, and Task 3 protects only the main checkout's copy |
| 117 | `docs/sandbox-record.md` → "counts an untracked leftover `.claude/settings.local.json` as a protected-surface change" | — | D7 | `no-change` | That check reads `hr_run_protected_rel_paths`, which Task 3 leaves unchanged |
| 118 | `docs/sandbox-record.md` → residual 17, "**Hooks, local MCP servers, plugin monitors, LSP servers, the status line and `apiKeyHelper` run outside the sandbox**" | — | D7 | `no-change` | It lists the files that name what else runs outside the sandbox, and the local additions file names no such thing |
| 119 | `docs/watcher.md` → "**The pins.**" (the protected paths of `hr_run_protected_rel_paths`) | — | D7 | `no-change` | Task 3 adds the file to `jobSurfacePaths` and not to `copySurfacePaths`, so that shell mirror is unchanged |
| 120 | `docs/cli.md` → `### The sandbox block and the permission mode`, "ignores `excludedCommands`, `network.allowedDomains` and `filesystem.allowWrite` in the repository's own `.claude/settings.json`" | — | D7 | `no-change` | It states which settings files Claude Code ignores; local additions are merged into the profile and are not such a file |
