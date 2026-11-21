# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_5_plan.md` — the module's roster rule forbids the pointer Task 7 adds**
   Task 5 has `plugin/instructions/probe_route.md` → `## Who may cite this` close on a sentence saying no document outside its five-agent roster points at the module. Task 7 then adds a pointer from `docs/development.md` (Gate 13) to `plugin/instructions/probe_route.md` → `## The route`. Both tasks are planned in this set, so the merged tree contradicts itself. The corpus already has a form that settles this: `plugin/instructions/plan_review_rounds.md` → `## Who may cite this` (*"A document outside the plugin cites this file by its repo-relative path and is not a roster member"*), and `plugin/instructions/finding_grades.md` → `## Who may cite this` limits its ban to *"no plugin asset beyond this list"*.
   **Raised against:** "A citer points and never restates, and no other document points at this file."
   **Must hold:** The exclusion sentence Task 5 plans for the module's `## Who may cite this` must allow every pointer the plan's own tasks create. In particular, Task 7's repo-relative citation from `docs/development.md` must not break the module's own rule.
   **Class:** Wrong build
   **Failure:** If the Task 5 implementer writes the roster sentence as planned and the Task 7 implementer adds the planned `plugin/instructions/probe_route.md` → `## The route` citation to `docs/development.md` → Gate 13, then the merged tree holds a pointer from a document that the module's own `## Who may cite this` says may not point at it.
   **Fix:** In `task_5_plan.md`'s `## Who may cite this` bullet, limit the ban to plugin assets (*"no plugin asset beyond this list points at this file"*), and add that a document outside the plugin cites the module by its repo-relative path and is not a roster member, as `plan_review_rounds.md` does. Alternatively, drop the module citation from `task_7_plan.md`'s Gate 13 sentence. Do not keep both as they stand.

2. **`task_6_plan.md` (with `task_5_plan.md`) — one rule copied into four agent definitions with no static check, against a ledger lesson**
   After Task 5 and Task 6, four agent definitions (`layer-reviewer.md`, `branch-reviewer.md`, `skeptic-reviewer.md`, `review-plan-reviewer.md`) each carry the same pointer paragraph, which states a rule itself (*"A probe reads and computes; it never writes into the tree under review."*) plus the background-run clause. Three of them also carry the byte-identical write-bounding clause at up to three sites each. The plan keeps these copies aligned only with the one-time greps in Task 6's Verification. No task ships a static check. The ledger requires one: `harness-runs/lessons.md` → `## Agent prose`: *"When a change makes agent definitions state one rule in two places, such as a checklist and a table, the same change ships the static check that holds the two aligned."* _(taught by: feat_must_fix_definition)_.
   **Raised against:** "Insert the two pointer paragraphs at the end of `## Process`, after step 4 and before `## What to check`." / "The clause every write-bounding sentence takes, byte-identical at each site"
   **Must hold:** Every rule the branch leaves stated in more than one agent definition must either be held aligned by a static check that ships in this branch, or be stated once in the shared module, so that the agent definitions carry only a citation.
   **Class:** Broken contract
   **Failure:** If the Task 5 and Task 6 implementers follow the plan as written, the branch ends with the reviewer probe rule and the write-bounding clause copied byte-for-byte into four and three agent definitions, and no test fails when one copy is later edited. That is the state the cited ledger entry forbids, and the branch diff will show no check.
   **Fix:** Choose one route:
   - (a) Move the reviewer-only rule (*"a probe reads and computes; it never writes into the tree under review"*, and the background-run clause if it is to be shared) into the module. For example, put it under a heading that Task 6 cites in place of restating it, so the four agents carry only the `→ heading` citations. Then state in `task_5_plan.md` / `task_6_plan.md` what each agent still carries.
   - (b) Add a `cli`-layer task, after Task 6, with a static check that asserts the copies are byte-identical. It may be a case in an existing suite or a new suite. If it reads a tree of files, the adding task must also name the later catch-all-layer task that adds its `treeGuards` entry to `devscene.config.json` (`unit_loop_core.md` → `## The test-run rule` point 8).

## Should Fix
- **Story index — readiness order places the catch-all layer first.** Tasks 1 and 2 (`_(layer: general)_`) come before the `cli` and `plugin` tasks. That goes against `### Architecture`'s *"the adopter's configured layer order, with the catch-all layer … last"*. The plan argues it (`## Context` → **Ship order.**): the scripts live under `.`, and the `cli` suites pin them. No `**Depends on:**` link points to a later task, and no dependent task comes before its dependency, so no failure sentence can be completed. Recorded so a human sees the deviation. The alternative is that the plan cannot pin the verbs without an inverted dependency.
- **`task_5_plan.md` — `<scripts_dir>` is left orphaned in `layer-reviewer.md`.** `layer-reviewer.md`'s `## Resolved values` declares `<scripts_dir>`, and its only use in the body is the **Run the probe that would settle it.** paragraph, which Task 5 replaces. Task 5 should drop that row, or say why it stays, so the table declares only tokens the body uses.

## Nice to Have
- `task_6_plan.md` locates the three write-bounding sentences as "line 10's …". Each also carries a quoted anchor that resolves, so the coordinate is a stale-prone hint in a point-in-time artifact only.
- `task_7_plan.md`'s Verification re-runs "the story index's `## Scope register` derivation entry C2 verbatim" without restating the command. The file would be more self-contained if it carried the command.
