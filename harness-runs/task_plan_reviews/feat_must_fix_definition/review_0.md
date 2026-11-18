# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **The scope register has no row for `finding_grades.md`, so Task 15's closure step must stop** — story index (`feat_must_fix_definition_story_plan.md`), `## Scope register`.
   Task 4 creates `plugin/instructions/finding_grades.md` with a `## Must Fix` heading. Derivation entry E2 searches `plugin/instructions` for `## Must Fix`, so once Task 4 is committed E2 lists that file. None of the 59 rows names it: the entry finds nothing today only because the file does not exist yet. Task 15 re-runs every command entry and says: "If an entry reaches a site with no row, stop and report it as a blocker". Followed as written, the last task always stops on the plan's own central deliverable.
   **Raised against:** "**Closure invariant:** every site any derivation entry reaches appears as a row below."
   **Must hold:** Every site a derivation entry reaches on the finished branch, including files this plan creates, appears as a register row, so Task 15's re-run finds no unlisted site.
   **Fix:** Add a row for `plugin/instructions/finding_grades.md` → `## Must Fix`, with `—` under `Copy`, evidence E2 (reached once Task 4 lands), disposition `change` and owner Task 4.

2. **Task 6's `**Depends on:**` line links to later tasks** — `task_6_plan.md`.
   The line names Task 7 and Task 11 as well as Task 4. Both run after Task 6 in the readiness list, and a `**Depends on:**` link to a later task breaks the bottom-up order. Task 6 only edits `review-plan-reviewer.md`, so it needs neither one to be done: they are later producers of the format it checks.
   **Raised against:** "Task 7 makes `branch-reviewer` and `skeptic-reviewer` write these fields in each Must Fix `finding_<N>.md`, directly after the site anchor. Task 11 adds them to `sample_code_review/finding_1.md`, the format this reviewer validates against."
   **Must hold:** Task 6's `**Depends on:**` line names only earlier tasks, and the field placement it checks is still stated in the file.
   **Fix:** Keep only Task 4 under `**Depends on:**`. Move the Task 7 and Task 11 facts to a `**Where this task stops.**` paragraph, as later work that adopts the contract this task defines, and state the placement (`**Class:**` and `**Failure:**` directly after the site anchor) as this task's own contract.

3. **Task 5's trigger table leaves a Must Fix trigger unmapped** — `task_5_plan.md`.
   The prompt requires "Every checklist trigger still graded Must Fix maps to a class", and Task 5 spells out the table's contents. Its list omits the `### Completeness (Must Fix)` bullet "Work touching application-level shared state follows the source-of-truth-and-mirror path the owning layer's `layers[].conventions` document defines". Task 5 also says "Leave every other trigger's grade unchanged", so an implementer following it keeps that trigger at Must Fix with no class. The same sentence excepts a "test-run trigger" from `### Architecture`, but that section has none: the test-run trigger is in `### Completeness`.
   **Raised against:** "**Broken contract:** story-index structure, per-task-file structure, index↔file correspondence, every `### Architecture` bullet except the test-run trigger"
   **Must hold:** Every trigger `task-plan-reviewer.md` still grades Must Fix is assigned exactly one class by Task 5, and the list refers only to triggers in the section it names.
   **Fix:** Add the shared-state source-of-truth trigger under **Broken contract**, and delete "except the test-run trigger" from the `### Architecture` item. Add a verification bullet that walks each `Must Fix` trigger in the agent against the finished table.

4. **`check-round-file` uses exit 1 for both an invalid file and a refused call, so a lagging walker fails valid rounds** — `task_2_plan.md` and `task_12_plan.md`.
   Task 2 gives an invalid round file exit 1, the status `flow-walker.sh` already uses for every refusal, including `unknown subcommand`. Task 12 treats exit 1 as a bad reviewer return. Outer-loop scripts are `create-if-absent`, and `docs/flow-graph-walker.md` → `### Item 6` records that an adopter's copies "lag a plugin upgrade until `init` is re-run". So when the new plugin runs beside an older walker, a user-review fix-plan gate that wrote a valid file gets `unknown subcommand 'check-round-file'`, exit 1. The core records nothing, dispatches that gate twice more and then takes the held binding, as if the reviewer had failed. A bad `check-round-file` call (a refused `--flow`, a missing `--findings`) is misread the same way. Task 12's "any other exit" route, written for this kind of fault, never sees these cases.
   **Raised against:** "An invalid file exits 1 with one stderr line, `flow-walker: <path>: <reason>`." (`task_2_plan.md`) and "Exit 1 is a return that fails the check under" (`task_12_plan.md`)
   **Must hold:** The status that sends a gate back means only that the walker read the file and found it invalid. A usage refusal, or a walker without the subcommand, reaches the held binding at once with no reviewer re-dispatch.
   **Fix:** In Task 2, give an invalid file its own exit status, such as `3`, keep exit 1 for usage refusals and exit 2 for faults, and cover all three in the `EXIT CODES` header and the fan-out cases. In Task 12, restate that contract in `**Depends on:**`, re-dispatch only on the invalid-file status, and send every other non-zero exit to the held binding at once.

## Should Fix
1. **`docs/flow-graph-walker.md` keeps two descriptions this branch makes incomplete** — `task_13_plan.md`. `### Item 3a` and `### Item 8` say `start` trusts a round file that "holds exactly one verdict line" (Item 3a) or "one verdict line" (Item 8), and Item 8 says "Every outcome but the last prints `action: wait`". Task 13 adds Item 9 and one driver sentence but leaves these. Nothing fails while they stay, but a one-clause pointer to Item 9 in each would keep the record accurate.

2. **Register row 50's reason does not address the sentence most affected** — story index, `## Scope register`. `docs/converging-plan-reviews.md` says "the fix-plan loop has no walker". That remains true of routing, but after Task 12 the loop runs `flow-walker.sh check-round-file`. The row's reason speaks only of the Must Fix entry; it should say why this sentence can stand, or the sentence should be narrowed to routing.

3. **Task 7 does not name `branch-reviewer`'s two-leg Must Fix triggers** — `task_7_plan.md`. The call-out rule in `## Output contract` grades "dropping the intended part" and code "matching **neither**" as Must Fix. They fit **Broken contract** while the parity phase is on, but "every parity item" could be read as only the `Parity with <reference_impl>` list. Name them in the table.
