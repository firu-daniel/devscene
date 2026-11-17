# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **The two planning-pause partial commits are fixed-subject orchestrator commit points that no task moves onto `--artifact`. Affects `task_1_plan.md`, `task_2_plan.md`, `task_13_plan.md` and `task_15_plan.md`.**
   The task prompt's goal 2 says every fixed-subject commit point the orchestrator owns uses the same step and "names an artifact kind rather than spelling a subject and a path set in prose". Two such points exist in the plugin today. The plan covers neither of them:
   - `plugin/instructions/autonomous_pause_and_ledger.md` §2.2 → **Planning artifacts only (the two plan-writing forks)** spells the plain form `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> <path>... -- "<subject>"`, then pushes in a separate call. §2.5 step 0 reuses it on an API-overload self-pause.
   - Each fork supplies its own subject and path set for that step:
     - `plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 5 — pause/resume + flow-progress ledger (planning half)` (**Honoring a PAUSE during planning.** and **Self-pause on API overload during planning.**) uses `chore: Plan round <n> partial for <branch>` with Override 6's path set.
     - `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` → `## Safety scaffolding (delta — the core states none)` items 2 and 3 use `chore: Fix plan <N> round <k> partial for <branch>` with `## Override 6`'s path set.
   - `plugin/instructions/plan_orchestration_instructions_autonomous.md` clean-tree entries 17 and 19 register both as commit points "followed by its own push".

   The plan skips these points because of a factual error. Task 2 exempts `chore: Plan round <n> partial for <branch>` from its drift test as "driver-only, with no orchestrator commit point". The two fork sections above show that premise is false. Task 1's artifact table carries no partial kind. Task 13's §2.2 bullets edit only the Dirty-tracked wording. Task 15's Work never reaches the pause paragraphs. Task 11's **Post-commit push.** rewrite would then claim the docs flows are "the one exception" to `--push`, which would be untrue while the partial commits keep their two-call form.
   **Raised against:** "`prl_partial_commit`'s `chore: Plan round <n> partial for <branch>` is driver-only, with no orchestrator commit point. The header says so and exempts it by name." (`task_2_plan.md`)
   **Must hold:** Every fixed-subject commit point an orchestrator session issues reaches the wrapper through one named artifact kind, the planning-pause partial commits included. Or the plan records, with a true reason, that a named point stays on the plain form. No task's premise or verification may rest on the claim that the partial subject has no orchestrator commit point.
   **Fix:**
   - In `task_1_plan.md`, add two artifact rows: `plan-round-partial` (`chore: Plan round <round> partial for <b>`, `plan-round`'s six paths) and `fix-plan-round-partial` (`chore: Fix plan <round> round <iteration> partial for <b>`, `fix-plan-round`'s paths). Each needs its test case.
   - In `task_2_plan.md`, drop the "driver-only" exemption. Pin `prl_partial_commit` against `plan-round-partial` like the other four.
   - In `task_13_plan.md`, rewrite §2.2's **Planning artifacts only** steps 1–2 (and, by reference, §2.5 step 0) as one `--artifact <the fork's partial kind> … --push` call. The fork names the kind and its round flags.
   - In `task_15_plan.md`, bind the kind and flags in both forks' pause and self-pause paragraphs.
   - In `task_11_plan.md`, change clean-tree entries 17 and 19 to the one-call form, and keep **Post-commit push.** true.
   - Alternatively, if the plan keeps these on the plain form, state in `## Context` that they are the exception and why. Then correct Task 2's premise and Task 11's "the one exception" wording.

## Should Fix
1. **`task_12_plan.md` leaves a sentence in `plugin/commands/branch-start-user-review-fix-autonomous.md` that Task 15 makes false.** Its `## Resolved values` paragraph says the fix-plan fork's "Override 3 / Override 4 commit and push both name the main checkout's copies, `commit-on-branch.sh` with `--repo` and `push-branch.sh`, spelled exactly as that fork's `## Override 3 — commit the fix plan + source review after the gates converge` states them". After Task 15, Override 3 is one `--artifact fix-plan --round <N> --push` call and names no `push-branch.sh`. Task 12 owns this file but rewrites only its three `<committer_push>` mentions. Add the sentence to Task 12's Work. D3's regex (`commit-on-branch\.sh (--repo|<|\[)`) does not reach a mention written as "`commit-on-branch.sh` with `--repo`". The prompt's own `grep -rn "commit-on-branch.sh" plugin/` does reach it.
2. **`task_16_plan.md` contradicts itself on `branch-reviewer.md`.** It asks for "the committing-role sentence above", which is byte-fixed and ends "the orchestrator itself in the supervised flow, which runs none". In the same breath it says "keeping 'supervised fix flow'". Both cannot hold. Also, the replacement is longer than the parenthesis it replaces, so the **No new words.** bullet's "adds no sentence, so no definition's up-front word count grows" overstates. Say which wording wins.
3. **`task_1_plan.md` → `ucl_tick` does not say what happens to its temporary file on failure.** The temporary `.ucl-tick.XXXXXX` file sits beside the index, inside the target's tracked state directory. If the `chmod` or `mv` fails, the file is left behind, and the next stage-set read would list it as untracked. Every exit path should remove a temporary file the library created (`harness-runs/lessons.md` → `## Remote and branch-scoped operations`, the temporary-copy rule, by analogy).
