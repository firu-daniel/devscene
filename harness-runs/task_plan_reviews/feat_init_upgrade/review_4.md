# Task plan review — round 4

verdict: FAIL
review_mode: converging

## Must Fix

1. **Scope register row 12 limits the `--force` bullet to one clause and leaves two statements `--upgrade` falsifies — story index (`feat_init_upgrade_story_plan.md`) and `task_15_plan.md`**
   The revision changed the register, so the derivation duty ran in full. D1 to D7, P1 and P2 close: every site they reach is a row. This is disposition (iii), a row whose reason is wrong. The story index has no `## Rejected findings` entry for it.

   This round moved row 12 to `change` and scoped it, and Task 15's `## 3.` bullet, to "only the clause" about a profile entry. The same `docs/cli.md` bullet, "`--force` upgrades `create-if-absent` only", also says:
   - "One route replaces an artifact with **no `--force` at all**", naming `--reset-config` and `<githooksDir>/pre-push`.
   - "So the whole of what the table permits is:", which lists `--force`, the five measured keeps, and that one replacement.

   `init --upgrade` replaces the outer-loop scripts and the profile with no `--force` (Task 10 applies with `force: false`), and it refuses `--force`. Both statements become false, and the "only" wording tells the implementer to leave them. They would also contradict the `replace-if-changed` text the same Task 15 bullet adds to that section.

   **Raised against:** "Task 15 — only the clause \"A **profile entry** is kept when it names a plugin root this machine resolves\", which takes row 2's exception"
   **Must hold:** After this branch, the `docs/cli.md` §3 bullet "`--force` upgrades `create-if-absent` only" does not say or imply that `--reset-config` is the only route replacing an artifact without `--force`, and its summary of what the table permits accounts for `init --upgrade`. Register row 12 and Task 15 assign that change.
   **Fix:** In the story index, widen row 12's owning-task note to the carry-forward clause, the "One route replaces an artifact" sentence and the "So the whole of what the table permits" sentence. In `task_15_plan.md`, name the same three in the existing `## 3.` bullet and add a matching `**Verification:**` check, keeping five `**Work:**` bullets.

2. **The `command-permissions` bullet keeps an unqualified carry-forward, so round 3's first finding is not fully resolved — story index (`feat_init_upgrade_story_plan.md`) and `task_15_plan.md`**
   Round 3 required that no `docs/cli.md` statement say or imply that a forced run keeps every plugin-root entry without the local-entry exception. The `## 7.` `command-permissions` bullet says `init --force` regenerates the profile "after copying the current one to a `.bak` sibling and carrying the plugin-root entries forward". Row 24 and Task 15's `## 7.` bullet limit that site to its ownership clause. Task 15's new verification grep does not match this wording, so it passes with the sentence unchanged.

   **Raised against:** "Task 15 — only the ownership clause; the printed remedy stands"
   **Must hold:** Every `docs/cli.md` statement of what a forced run carries forward, including the one in the `command-permissions` bullet, excepts an entry the local file supplies or the replaced profile records as local, and the task's verification reaches each such statement.
   **Fix:** In the story index, extend row 24's note to this carry-forward clause. In `task_15_plan.md`, name the clause in the existing `## 7.` bullet and add `plugin-root entries forward` to the verification grep. The check's printed remedy stays as it is.

3. **An upgrade prints that `--force` left the carried entries in place — `task_4_plan.md`**
   This round's revision extends Task 4 to what `init --upgrade` makes untrue, then lists only module-header and doc-comment sites. `appendCarriedPluginRootEntries` also emits a user-visible note on the resolved-root arm: "so --force ${dryRun ? 'would leave' : 'left'} them in place". Task 5's `renderCurrentProfile` reaches that code with `force` set from `carryForward`, `planProfileUpgrade` returns `notes`, and Task 10 prints them on real and dry runs. So a run that refuses `--force` tells the adopter `--force` acted. No task names this string. The existing tests pin only "were carried forward into the regenerated" and its dry-run form, so correcting the tail does not disturb them.

   **Raised against:** "amend every statement in `permissionProfile.ts` that the carry-forward exclusion, the local-file read or `init --upgrade` makes untrue"
   **Must hold:** The carry-forward note is true on both runs that reach it: it never attributes an `init --upgrade` carry-forward to `--force`, in either tense.
   **Fix:** In `task_4_plan.md`, name this note in the existing `permissionProfile.ts` bullet, reword it to describe the run without naming `--force`, keep the pinned leading words, and add a `**Verification:**` check that `grep -n 'so --force' cli/src/generators/permissionProfile.ts` finds nothing.

## Should Fix

- `task_10_plan.md`: `cli/src/commands/init.ts` is a target, and its comment on the `force:` argument to the profile generator says "it is the only run that replaces the profile". `init --upgrade` makes that untrue, and no task names it.
- `task_11_plan.md`: `cli/src/doctor/checks.ts` is a target. The `PLUGIN_PERMISSIONS_CHECK` doc comment and the comment in its no-root arm both say the counted entries are the set `init --force` carries forward unverified. Row 26 now records that local entries make those sets differ, and no task amends these comments.
