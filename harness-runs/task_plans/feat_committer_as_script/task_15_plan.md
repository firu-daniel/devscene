### Task 15 — Move both planning forks' plan, round, UI-test-plan and lessons commits onto `--artifact`

**Goal:** Rewrite the two autonomous planning forks. Every fixed-subject commit they spell becomes one literal `--artifact … --push` call, and each "not a committer dispatch" argument goes:

- **`task_plan_writing_instructions_autonomous.md`:** the UI-test plan, the task plan, each plan-review round, the planning-pause partial commit (pause and API-overload self-pause), the `## Planning` ledger flips;
- **`user_review_fix_plan_writing_instructions_autonomous.md`:** the fix plan, each fix-plan round, the fix-planning-pause partial commit (pause and API-overload self-pause), the lessons ledger, the `## Fix planning` flips.

**Depends on:**

- **Task 3**, whose front end is `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact <kind> [--round <n>] [--iteration <k>] [--entry <id>] --push`. One call commits, re-syncs a landed exit 1 and pushes after exit 0 or exit 3.
- **Task 1's kinds**, each carrying exactly the paths these forks pass today, in the same order:
  - `ui-test-plan` → `chore: Add UI-test plan for <branch>`;
  - `task-plan` → `chore: Add task plan for <branch>`, the seven planning paths;
  - `plan-round` with `--round <n>` → `chore: Plan round <n> for <branch>`, the first six;
  - `fix-plan` with `--round <N>` → `chore: Add user-review fix plan for <branch>`;
  - `fix-plan-round` with `--round <N> --iteration <k>` → `chore: Fix plan <N> round <k> for <branch>`;
  - `plan-round-partial` with `--round <n>` → `chore: Plan round <n> partial for <branch>`, `plan-round`'s six paths;
  - `fix-plan-round-partial` with `--round <N> --iteration <k>` → `chore: Fix plan <N> round <k> partial for <branch>`, `fix-plan-round`'s paths;
  - `lessons` → `chore: Record lessons for <branch>`;
  - `ledger` and `ledger-flip --entry <id>`.
  
  **The round suffix.** The fix-plan kinds derive `<round_suffix>` from `--round`: empty for round 1, `_<N>` otherwise. If Task 1's implementer recorded a **Deviations from plan:** note against that derivation, spell the flags that note states.
- **Task 13**, which rewrites `autonomous_pause_and_ledger.md` §1.6 under its unchanged heading, and turns §2.2 → **Planning artifacts only (the two plan-writing forks)** steps 1–2 into one call, `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --artifact <the fork's partial kind> <the fork's round flags> --push`, with the fork naming its planning path set, its partial kind and its round flags. §2.5 step 0 reuses that step by reference.

**What does not change.** `lib/planning-record-lib.sh` keeps its own plain calls; Task 2's suite pins its subjects and paths against the same table. `plugin/instructions/plan_review_rounds.md` still finds the previous round by its unchanged subject `chore: Plan round <iteration − 1> for <branch>`.

### Targets

- `plugin/instructions/task_plan_writing_instructions_autonomous.md`
- `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md`

**Work:**

- [ ] **`task_plan_writing_instructions_autonomous.md` — Overrides 3 and 4.**
  - **The commits.** Override 3's UI-test-plan commit becomes `… --artifact ui-test-plan --push`. Override 4's convergence commit becomes `… --artifact task-plan --push`.
  - **What goes.** Delete each **Commit mechanism (via the `commit-on-branch.sh` wrapper in the fork, not a committer dispatch).** rationale about modes not fitting. Delete each "matches the committer's no-blanket-add rule" parenthesis. Delete the "Pass all seven unconditionally" list, now the table's.
  - **What stays.** Keep each **Trigger** and each exit-reading paragraph, rewritten to read the printed `error:` line.
  - **The cross-references.** Rewrite them as the commit step's behaviour:
    - "The Phase E `mode: ui_test_pass` committer stages **only** the index";
    - "(`committer.md` `ui_test_pass`)";
    - "the `committer.md` `task` / `review_item` modes stage `<task_file>` *conditionally*";
    - "the later Phase A `task`-mode committer".
  
  The per-task file is now staged whenever the implementer changed it.
- [ ] **`task_plan_writing_instructions_autonomous.md` — Overrides 5 and 6, and the table.**
  - **The flips.** Override 5's `## Planning` flips become `--artifact ledger-flip --entry <entry-id> --push` in §1.6's form.
  - **The round commit.** Override 6's round commit becomes `… --artifact plan-round --round <n> --push`, with "never a `committer` dispatch" dropped and the exit-3-on-re-print paragraph kept.
  - **`## Resolved values`.** The parenthesis "the committer's own arg name `<task_file>`" goes. Keep the `<MAIN_REPO>` row byte-for-byte.
- [ ] **`user_review_fix_plan_writing_instructions_autonomous.md`.**
  - **The commits.** Override 3's commit becomes `… --artifact fix-plan --round <N> --push`. The round commit becomes `… --artifact fix-plan-round --round <N> --iteration <k> --push`. The lessons commit becomes `… --artifact lessons --push`.
  - **`## Fix planning`.** Its flips become `--artifact ledger-flip --entry <entry-id> --push`.
  - **What goes.** Delete each "not a committer dispatch" / "never a committer" rationale and each separate push.
  - **The "Why a commit is needed here" paragraph.** Rewrite its committer sentences: "committed opportunistically by the Phase A `committer` (`mode: review_item`)", "(Phase A dispatches no committer at all)" and "never staged by the `review_item` committer". They become the commit step's `--unit review_item`, which stages the index, the work files and every changed path.
  - **Retained wording.** Keep the "unchanged and complementary" paragraph with the commit step named. Keep the `<MAIN_REPO>` row byte-for-byte.
- [ ] **The pause and self-pause partial commits, in both forks.** Each binds the kind and flags §2.2's one-call step takes, in place of the subject it spells today:
  - **`task_plan_writing_instructions_autonomous.md` → `## Override 5 — pause/resume + flow-progress ledger (planning half)`**, in **Honoring a PAUSE during planning.** and **Self-pause on API overload during planning.**: "with Override 6's path set and the subject `chore: Plan round <n> partial for <branch>`" → "with Override 6's path set and `--artifact plan-round-partial --round <n>`". Keep every definition of `<n>` (the walker's `arg.iteration:` for the interrupted or dead dispatch, the set's shared `arg.iteration:`) byte-for-byte. The self-pause paragraph's "this fork binds only Override 6's path set and the subject …" names the kind and `--round <n>` instead, and the PAUSE paragraph's "this fork's commit at that point is Override 6's, with its path set and subject" stays.
  - **`user_review_fix_plan_writing_instructions_autonomous.md` → `## Safety scaffolding (delta — the core states none)`** items 2 (**PAUSE check.**) and 3 (**API-overload self-pause.**): "with `## Override 6`'s path set and the subject `chore: Fix plan <N> round <k> partial for <branch>`" → "with `## Override 6`'s path set and `--artifact fix-plan-round-partial --round <N> --iteration <k>`". Keep each `<k>` definition (the `fix_round` of the interrupted or dead dispatch, the set's `fix_round`) and item 2's "the path set and the subject stay as above" reworded to "the path set and the kind's flags stay as above".
  - Neither subject is read back from history by any reader (`plan_review_rounds.md` reads only the non-partial `chore: Plan round <iteration − 1> for <branch>`), so neither stays in prose; each lives only in the library's table, and for the task-plan kind in `lib/planning-record-lib.sh` → `prl_partial_commit`, pinned by Task 2.
- [ ] **Fixed subjects leave the prose.** Each fixed subject these forks spelled as a command argument now lives in the library's table. Keep it in prose only where a sentence names the subject a reader looks for in history, and keep that wording byte-for-byte. Override 6's `chore: Plan round <n> for <branch>` is one such sentence: `plan_review_rounds.md` reads that subject.

**Verification:**

- `git grep -n -e 'committer' -- plugin/instructions/task_plan_writing_instructions_autonomous.md plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` prints nothing.
- `git grep -n -F -e '--artifact task-plan --push' -e '--artifact ui-test-plan --push' -e '--artifact plan-round --round' -e '--artifact fix-plan --round' -e '--artifact fix-plan-round --round' -e '--artifact lessons --push' -e '--artifact plan-round-partial --round' -e '--artifact fix-plan-round-partial --round' -- plugin/instructions` shows one call per commit point, the partial kinds once in each of their two paragraphs.
- `git grep -n -F 'partial for <branch>' -- plugin/instructions/task_plan_writing_instructions_autonomous.md plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` prints nothing.
- `git grep -n -F -e '-- "chore:' -- plugin/instructions/task_plan_writing_instructions_autonomous.md plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` prints nothing: no plain-form subject argument is left in either fork.
- `git diff -- plugin/instructions/task_plan_writing_instructions_autonomous.md` changes no heading line. That keeps `cli/test/flow-walker-resume.test.mjs`'s citations of `## Override 2 — resumability` and `## Override 5 — pause/resume + flow-progress ledger (planning half)` valid.
