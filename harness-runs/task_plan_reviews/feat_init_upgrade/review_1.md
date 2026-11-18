# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix

1. **The watcher message change breaks an existing test the task does not edit — `task_13_plan.md`**
   `cli/test/watcher-run-analytics.test.mjs`, subtest `a missing run-analytics.sh changes neither the status nor the notifications`, waits for a log line that includes `run analytics: `, `run-analytics.sh` and `init --force`. This task rewrites that message to name `init --upgrade`, so no line matches and the subtest fails. The test file is not in `### Targets`, and the task says it changes nothing else executable.
   **Raised against:** "change `` `devscene init --force` rewrites it `` to `` `devscene init --upgrade` rewrites it ``"
   **Must hold:** Every existing test that pins text this task changes is updated by this task, so the suite still passes once the task lands.
   **Fix:** Add `cli/test/watcher-run-analytics.test.mjs` to `### Targets`, and extend the existing `task-offer-check.sh` / `autonomous-watcher.sh` bullet to change that predicate to `init --upgrade`, which keeps the file at five `**Work:**` bullets. Add a `**Verification:**` bullet that this test file passes.

2. **The carry-forward reads local entries back, so a second upgrade can rewrite the profile — `task_4_plan.md`**
   `renderCurrentProfile` renders with `force: true`. `appendCarriedPluginRootEntries` then reads every `allow` entry on disk, including entries an earlier upgrade merged from the local file, and appends the ones shaped `Read(/<abs>/**)` or `Bash(bash <abs>/scripts/<name>:*)` before the local merge runs.
   - Take a local `allow` list of `Bash(foo:*)` then `Read(//opt/tools/**)`, on a machine where no plugin root resolves. The first upgrade writes generated entries, `Bash(foo:*)`, `Read(//opt/tools/**)`. The second carries `Read(//opt/tools/**)` first, so the merge produces the reverse order. The bytes differ, the file is replaced and a backup is taken, which the prompt's second-run requirement forbids.
   - Where a plugin root does resolve, the same local entry lands in `notPreserved`, so every upgrade warns that an entry the local file supplies is not in the regenerated profile.
   - A deleted local entry of this shape is carried from the old profile and stays, against the prompt's "Editing the local file takes effect on the next `init --upgrade`".

   **Raised against:** "After `applyWriteProtection` and before the final assertions, merge `localAdditions.fragment` with `mergeInto(profile, fragment, '', 'local additions')`"
   **Must hold:** The carry-forward treats an entry the local file supplies as local. A repeated upgrade over an unchanged repository is byte-identical for any order of local entries, no local entry is reported as left behind, and the task states what a deleted local entry of a carry-forward shape does.
   **Fix:** Pass the local `allow` entries into the carry-forward so they are neither carried nor reported. State and implement the deleted-entry behaviour. Add `profile-local-merge.test.mjs` cases for the two-entry order above across two forced renders, and for no left-behind warning naming a local entry.

3. **`profileDrift` accounts for a hand-added entry because it is on disk — `task_5_plan.md`**
   `unaccounted` subtracts a render made with `force: true`, and that render copies carry-forward-shaped entries out of the profile being graded. Where no plugin root resolves, `carriedPluginRootEntries` carries every such entry outside the checkout unverified. A tampered `Bash(bash /tmp/x/scripts/evil.sh:*)` or `Read(//tmp/x/**)` therefore accounts for itself, and `doctor` stays silent. The prompt requires entries nothing accounts for to be reported as a hand edit or tampering.
   **Raised against:** "`unaccounted` is the disk minus the render, minus the same render with `pluginRootEntries: true`, minus entries `isToolchainEntry` accepts."
   **Must hold:** No entry counts as accounted for merely because the profile under comparison contains it. A plugin-root entry is accounted for only through a plugin root this machine resolves.
   **Fix:** Have `profileDrift` compare against a render with no carry-forward, keeping the `pluginRootEntries: true` and `isToolchainEntry` allowances, and accept a carried shape only when its target is under a resolved plugin root. Add a `profile-upgrade.test.mjs` case with no plugin root resolved in which those two entries appear in `unaccounted`.

4. **Scope register: no derivation entry reaches four more sites — story index (`feat_init_upgrade_story_plan.md`)**
   D1 to D6, P1 and P2 miss these verified sites (disposition (ii)). Each becomes false or incomplete on this branch:
   - `cli/scripts/README.md` → "a copied script is upgraded by re-running `init`", which goes on to say the `create-if-absent` contract keeps an adopter's edited copy. `--upgrade` is now the route, and it replaces that copy.
   - `docs/cli.md` → `### The sandbox block and the permission mode`, "**Everything that runs outside the sandbox is write-protected on both sides**". Its enumeration of the set names "the profile itself in the main checkout" and has no place for the local file Task 3 adds.
   - `docs/remote-execution.md` → "**The step.** `Refuse a branch that changed the job's own files`". It lists the paths of `jobSurfacePaths`, which Task 3 extends and tests.
   - `docs/remote-execution.md` → "Entries you added to this machine's `.claude/settings.autonomous.json`". Such entries now belong in the local file, and a hand-added one is dropped by `--upgrade`.

   **Raised against:** "**Closure invariant:** every site each derivation entry reaches appears as a row below."
   **Must hold:** The derivation entries together reach every statement of the scripts' upgrade route, of hand additions to the profile, and of the protected and job-surface sets this branch extends, and each reached site has a row.
   **Fix:** Add this entry beside D1 to D6, which was executed and reaches all four sites, and add one row per site with a disposition:

   `grep -rnIE 'upgraded by re-running .init|the profile itself in the main checkout|paths? of .jobSurfacePaths|Entries you added to this machine' cli/scripts/README.md docs/cli.md docs/remote-execution.md docs/watcher.md`

   For each `change` row, extend the owning task's existing bullet: `task_13_plan.md` for `cli/scripts/README.md` (with its `### Targets`), `task_15_plan.md` for `docs/cli.md`, `task_16_plan.md` for `docs/remote-execution.md`.

5. **Scope register: row 19's `no-change` leaves a false cross-reference — story index (`feat_init_upgrade_story_plan.md`) and `task_15_plan.md`**
   The `docs/cli.md` paragraph says turning retrieval on later "is the configuration change and forced re-run in §2's fenced block". Row 4 and Task 15 replace that block with a plain `init` followed by `init --upgrade`, so the sentence will describe a block that no longer exists. Row 19's reason covers the browser half and `init`'s note, and does not engage this clause (disposition (iii); no `## Rejected findings` entry applies).
   **Raised against:** "| 19 | `docs/cli.md` → `## 6.` \"Both conditions are the gate\" | — | D1, D2 | `no-change` |"
   **Must hold:** After Task 15, `docs/cli.md` gives one retrieval route, and no sentence describes §2's retrieval block as a forced re-run.
   **Fix:** Change row 19 to `change`, owned by Task 15, limited to the retrieval clause, and add that edit to Task 15's `## 5.` and `## 6.` bullet.

## Should Fix

- `task_2_plan.md`: *"a character device that reads empty"* still defines an accepted shape by reading it, which can block on a device other than the placeholder. `harness-runs/lessons.md` says: "When a trust check meets a file an actor outside your control creates on every run, accept only its provably inert shape". Identify the null device by its device numbers without reading it, and add a refusal case for another character device.
- `task_11_plan.md`: the check that warns about an unignored local file needs `PROFILE_LOCAL_PATH`, but `**Depends on:**` and the restated contracts do not name Task 2 or that constant's module, `cli/src/generators/profileEntries.ts`.

## Nice to Have

- `task_15_plan.md`: the `## 7.` sentence "an unreadable profile makes the three profile checks unanswerable" is worth correcting while the check list changes, since `profile-drift` is one more check it does not count.
