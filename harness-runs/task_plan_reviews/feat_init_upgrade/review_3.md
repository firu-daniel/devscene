# Task plan review — round 3

verdict: FAIL
review_mode: converging

## Must Fix

1. **Scope register: three rows leave the unconditional carry-forward standing in `docs/cli.md` — story index (`feat_init_upgrade_story_plan.md`) and `task_15_plan.md`**
   The revision changed the register, so the derivation duty ran in full. D1 to D7, P1 and P2 all close: every site they reach is a row. This is disposition (iii), a row whose disposition or reason is wrong. The story index has no `## Rejected findings` entry for it.

   Task 4 makes an entry the local file supplies, or the replaced profile records as local, exempt from the carry-forward: "An on-disk entry in either set is skipped before any classification". So a deleted local `allow` entry naming a resolved plugin root is dropped by the next `init --force`, and on the no-root arm a local absolute entry is not carried either. This round's Task 4 revision amends the same claim in the module header and doc comments. Three `docs/cli.md` statements of it stay as they are:
   - Row 12, `no-change`, `## 3.` bullet "`--force` upgrades `create-if-absent` only": "A **profile entry** is kept when it names a plugin root this machine resolves". The row's reason, "`--force` keeps that behaviour", no longer holds for this entry.
   - Row 26, `no-change`, `## 7.` bullet `plugin-permissions`: the count of entries nothing can grade "is the same set `init --force` carries forward unverified on that arm (§3)". A local absolute entry is now counted there and not carried, so the two sets differ. The row's reason, "The carry-forward it describes stays", does not cover this.
   - Row 2, `change`, `## 1.` `--force` row: "every `allow` entry naming a plugin root this machine resolves". The row scopes its change to "it states that `--upgrade` refuses this flag", and Task 15's `## 1.` bullet asks for nothing more.

   Task 15 states that "rows marked `no-change` in this file stay as they are", so its implementer must leave the first two false. Its `## 5.` and `## 6.` bullet adds the true rule to §6 only, which leaves `docs/cli.md` contradicting itself.

   **Raised against:** "| 12 | `docs/cli.md` → `## 3.` bullet \"`--force` upgrades `create-if-absent` only\" | — | D2 | `no-change` | `--force` keeps that behaviour; the new policy is stated in rows 6 to 8 |"
   **Must hold:** After this branch, no statement in `docs/cli.md` says or implies that a forced run keeps every plugin-root entry, or carries every absolute entry on the no-root arm, without excepting entries the local file supplies or the replaced profile records as local; and each register row's disposition and reason agree with that.
   **Fix:** In the story index, mark rows 12 and 26 `change`, owned by Task 15 and limited to the carry-forward clause, and extend row 2's owning-task note to include its carry-forward clause. In `task_15_plan.md`, name those three clauses in the existing `## 1.`, `## 3.` and `## 7.` bullets, keeping the file at five `**Work:**` bullets.

2. **`--force` is still stated to be the only run that replaces the profile — `task_4_plan.md`**
   This round's revision scopes the `permissionProfile.ts` comment update to "every statement in `permissionProfile.ts` that the carry-forward exclusion or the local-file read makes untrue". A second group of statements in the same file is made untrue by `--upgrade` itself, which replaces the profile without `--force`. Task 5's `renderCurrentProfile` also passes `force` to `renderProfile` on that run, from `carryForward`. These statements are outside Task 4's scope sentence, and no other task owns them: Task 5 and Task 10 do not target this file.
   - Module header, in the paragraph Task 4 is editing: "`--force` is the one flag that suspends that contract, and therefore the one run under which those hand-added entries can be lost".
   - `RenderProfileOptions.force`: "The run's `--force` — the only condition under which the profile on disk is replaced, and therefore the only run whose hand-added plugin-root entries can be lost."
   - The comment before `appendCarriedPluginRootEntries`: "Gated on `force`, which is the only run that replaces the file these entries are read out of".
   - `carriedPluginRootEntries`' doc comment: "Read the profile `--force` is about to replace". The header's opening "on a forced run, the profile it is about to replace" has the same gap, and Task 4 already rewrites that sentence.

   `.claude/context/cli.md` → `## What "done" means here` requires a header rule to be satisfied or amended in the same edit: "a header a review reads as a guarantee is worth exactly what the code under it still does".

   **Raised against:** "amend every statement in `permissionProfile.ts` that the carry-forward exclusion or the local-file read makes untrue"
   **Must hold:** Every statement in `permissionProfile.ts` that presents `--force` as the only run that replaces the profile or reads it back is called out for amendment by a task on this branch, so that after the branch each one also accounts for `init --upgrade`.
   **Fix:** In `task_4_plan.md`, widen that sentence to cover what `--upgrade` makes untrue, name the four sites above, and add them to the matching `**Verification:**` bullet. The `force` option may keep its name; its comment must say it means "this render replaces the profile", set by `--force` and by `--upgrade`'s planner.
