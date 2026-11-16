### Task 1 — Add `unit-commit-lib.sh`, the library that ticks an entry, builds every subject and record, and holds the artifact table

**Goal:** Create `cli/templates/scripts/lib/unit-commit-lib.sh`, a sourced library of pure functions. Given an index file, a status listing and a few closed values, it answers every question the committer used to answer by judgement:

- which readiness entry a token names, and how to tick it;
- the subject;
- the body record;
- the stage set;
- every artifact kind's subject and path set.

It makes no git call and reads no configuration. Task 3's front end in `commit-on-branch.sh` does the git reads and passes their output in. That is also what lets the future script-driven driver source it beside `prl_commit` (`ROADMAP.md` → **Script-driven autonomous flow**).

**Where this task stops.** This task does not touch `commit-on-branch.sh`; Task 3 wires these functions into it. It does not add the library to the shipped outer-loop table; Task 2 does. It changes no plugin prose.

### Targets

- `cli/templates/scripts/lib/unit-commit-lib.sh` (new).
- `cli/test/unit-commit-lib.test.mjs` (new) — this task's own test file.

**Work:**

- [ ] **Header, and the shape every function shares.**
  - **Header.** Open the file with `#!/usr/bin/env bash` and a `# unit-commit-lib.sh — …` header comment. The header states *"The rule this library exists to enforce: every unit and artifact commit subject is built from the readiness index or this file's artifact table, never from a caller's text"*. It names its sourcer: `commit-on-branch.sh`, and later the script-driven driver. It records the Bash 3.2 / jq 1.5 floors; the library uses no jq.
  - **Shell options.** Set no shell option at all, as a sourced library must (`.claude/context/conventions.md` → `## Shell assets`).
  - **Results and statuses.** Every function returns its result in `UCL_*` globals rather than on stdout. It returns 0 on success, 1 for a "not found / not applicable" answer, and 2 for bad input, with one `unit-commit-lib: <cause>` line on stderr.
  - **REPRO.** Carry a `REPRO` block that drives each public function against a throwaway index file under `mktemp -d "${TMPDIR:-/tmp}/ucl-repro.XXXXXX"`.
  - **Temporary files.** Every `mktemp` names an explicit template; the `test/shipped-scripts-mktemp.test.mjs` tree guard covers this file.
- [ ] **Index functions.**
  - **`ucl_entry_find <index_file> <word> <K>`.** `<word>` is `Task`, `Finding` or `Test`. Search **only** inside the section opened by the exact line `## Phase 2 Readiness — Ordered Fix List` and closed by the next `## ` line. Match the first line of the form `<N>. [ ] **<word> <K>** — …` or `<N>. [x] **<word> <K>** — …`, by the token and never by position. Set `UCL_ENTRY_LINE`, `UCL_ENTRY_LINENO` and `UCL_ENTRY_STATE` (`open` | `done`); return 1 when no entry carries the token.
  - **`ucl_tick <index_file> <lineno>`.** Rewrite that one line's `[ ]` to `[x]` through a temporary file created beside the index (`mktemp "<dir>/.ucl-tick.XXXXXX"`), `chmod 644`, then `mv`. Every other byte stays unchanged, sub-step `- [ ]` bullets included.
  - **`ucl_short_title <entry_line>`.** Take the text after the first `** — `. Remove every `_(layer: …)_` and `_(points: …)_` tag and trim.
  - **`ucl_normalise <text>`.** Drop `` ` ``, `$`, `|`, `<` and `>`, turn every control character (newline and CR included) into a space, collapse runs of spaces and trim. Keep every word.
  - **`ucl_severity <index_file> <K>`.** Find the `### <K>. ` pointer heading. Set `UCL_OUT` to `must`, `should` or `nice` from the nearest preceding `## Must Fix` / `## Should Fix` / `## Nice to Have` heading, or to empty.
- [ ] **Subject and record functions.**
  - **`ucl_index_kind <state_dir> <plan_rel>`.** Classify by the directory directly under `<state_dir>`:
    - `story_plans` → `story`
    - `code_reviews` → `code_review`
    - `business_parity_branch_reviews` → `parity_review`
    - `architecture_branch_reviews` → `arch_review`
    - `skeptic_reviews` → `skeptic_review`
    - `qa_reviews` → `qa_review`
    - `test_fix_plans` → `test_fix`
    - `user_reviews` → `user_review`
    - `ui_test_plans` → `ui_test`
    
    Set `UCL_KIND` and `UCL_FINDINGS_DIR`, the per-finding folder: `${plan%.md}/` for a sibling-`.md` index, and `${plan%/*}/` for the QA merged index named `qa_review_<i>.md` inside its own folder. Return 1 for anything else.
  - **`ucl_unit_label <kind> <K>`.** `story` → `Task K`, `code_review` → `Code review finding K`, `parity_review` → `Parity review finding K`, `arch_review` → `Architecture review finding K`, `skeptic_review` → `Skeptic review finding K`, `qa_review` → `QA finding K`, `test_fix` → `Test fix K`, `user_review` → `User review finding K`. The body-record token stays `Task K` for `story` and `Finding K` for every other kind.
  - **`ucl_branch_prefix <branch>`.** `feat_` → `feat`, `fix_` → `fix`, `refactor_` → `refactor`, else `chore`.
  - **`ucl_unit_prefix <kind> <branch> <severity> <prefix_arg>`.** `story` → the branch prefix. Every other kind → `fix`, except `user_review`: `must` → `fix`, `nice` → `chore`, `should` → `<prefix_arg>`, which must be `refactor` or `chore`. Return 2 when a `--prefix` value arrives on any other arm, or is missing or illegal on the `should` arm.
  - **`ucl_subject <prefix> <label> <title>`.** Build `<prefix>: <label> — <title>`, at most 72 bytes counted under `LC_ALL=C`; the em dash counts as its three bytes, which keeps the cap conservative. Cut the title at the last space that fits. Drop it, with its ` — `, when not even its first word fits.
  - **`ucl_record_cause <detail_abs> <section>`.** `<section>` is `Disposition` or `Already passing`. Return 1 when the file has no `## <section>` heading. Otherwise set `UCL_OUT` to the normalised text after `**Cause:** ` on the first such line inside the first such section. When that line is absent, set it to `cause not recorded — see <detail_rel>`.
  - **`ucl_detail_file`.** `story` → `<state_dir>/task_plans/<branch>/task_<K>_plan.md`. A review index → the first `*.md` path the `### <K>. ` pointer section names under `UCL_FINDINGS_DIR`, else `UCL_FINDINGS_DIR` + `finding_<K>.md`.
  - **`ucl_body_record`.** Pick one line, lower-case, in precedence:
    1. `record disposition of <token> — <cause>`
    2. `mark <token> already passing — <cause>`
    3. `mark <token> done — <staged set>`, only when the stage set is index-only
    4. none
    
    `record disposition of ` and its ` — ` are byte-identical to what `plugin/instructions/improvement_observations_instructions.md` and `plugin/agents/statistics-plan-writer.md` parse.
- [ ] **Stage set and artifact table.**
  - **`ucl_stage_set <listing> <plan_rel> <findings_rel> <detail_rel> <findings_dir_rel>`.**
    - **Input.** `<listing>` is a file holding two NUL-separated sections, which Task 3 writes: first the output of `git diff --name-status -z --no-renames <old_tip>`, then a lone `--others` marker record, then `git ls-files -z --others --exclude-standard`.
    - **What it writes.** It writes the NUL-separated stage set to the file `UCL_STAGE_FILE` names: the plan, the findings folder when given (unconditionally), and every changed or untracked path, each relative to the repository top.
      - A `D` entry is passed as its **parent directory**, never as the file (`commit-on-branch.sh` → **STAGING POLICY, AND THE ONE TRAP IN IT**).
      - Every path at or under `<findings_rel>` is excluded from the work files.
    - **What it sets.** `UCL_WORK_COUNT` is the number of stage-set paths other than the plan, the unit's detail file, any path under the per-finding folder, and the findings folder. `UCL_INDEX_ONLY_SET` describes the non-work paths staged, comma-separated, for the `staged: index-only` line.
  - **`ucl_artifact <kind> <state_dir> <branch> <round> <iteration> <entry>`.** Set `UCL_SUBJECT` and the array `UCL_PATHS` from the table below, which is the single declaration of these strings. Return 2 for an unknown kind, a missing or non-numeric `<round>` / `<iteration>` where the row requires one, or an `<entry>` outside `[A-Za-z0-9.]+`. Write `<s>` for `<state_dir>`, `<b>` for `<branch>`, and `<sfx>` for the empty string when `<round>` is `1` and `_<round>` otherwise:

    | kind | subject | paths, in this order |
    |---|---|---|
    | `task-plan` | `chore: Add task plan for <b>` | `<s>/story_plans/<b>_story_plan.md` `<s>/task_plans/<b>/` `<s>/task_plan_reviews/<b>/` `<s>/business_parity_reviews/<b>/` `<s>/architecture_reviews/<b>/` `<s>/plan_revisions/<b>/` `<s>/ui_test_plan_reviews/<b>/` |
    | `plan-round` | `chore: Plan round <round> for <b>` | the first six `task-plan` paths |
    | `ui-test-plan` | `chore: Add UI-test plan for <b>` | `<s>/ui_test_plans/<b>_ui_test_plan.md` `<s>/ui_test_plans/<b>/` |
    | `ledger` | `chore: Add flow-progress ledger for <b>` | `<s>/flow_progress/<b>_progress.md` |
    | `ledger-flip` | `chore: Flow progress <entry> for <b>` | `<s>/flow_progress/<b>_progress.md` |
    | `statistics` | `chore: Add branch statistics for <b>` | `<s>/branch_statistics/<b>/statistics.md` |
    | `statistics-update` | `chore: Update branch statistics for <b>` | `<s>/branch_statistics/<b>/statistics.md` |
    | `observations` | `chore: Log improvement observations for <b>` | `<s>/improvement_observations/<b>.md` |
    | `dispatch-additions` | `chore: Log dispatch additions for <b>` | `<s>/dispatch_additions/<b>.md` |
    | `clarification-digest` | `chore: Record clarification digest for <b>` | `<s>/clarification_digests/<b>.md` |
    | `lessons` | `chore: Record lessons for <b>` | `<s>/lessons.md` |
    | `fix-plan` | `chore: Add user-review fix plan for <b>` | `<s>/user_reviews/<b>_fix_plan<sfx>.md` `<s>/user_reviews/<b>_review<sfx>.md` `<s>/user_reviews/<b>_fix_plan<sfx>/` `<s>/business_parity_user_review_reviews/<b>/` `<s>/architecture_user_review_reviews/<b>/` `<s>/plan_revisions/<b>/` |
    | `fix-plan-round` | `chore: Fix plan <round> round <iteration> for <b>` | `<s>/user_reviews/<b>_fix_plan<sfx>.md` `<s>/user_reviews/<b>_fix_plan<sfx>/` `<s>/business_parity_user_review_reviews/<b>/user_review_<round>/` `<s>/architecture_user_review_reviews/<b>/user_review_<round>/` `<s>/plan_revisions/<b>/` |
    | `rescreened-input` | `chore: Commit re-screened input edit for <b>` | none from the table — the caller's `--path` values |
  - **Before writing the two fix-plan rows,** read `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` → `## Override 3` and the round commit after it. Confirm that `<round_suffix>` is empty for user-review round 1 and `_<N>` for round `N`. Where it is bound differently, implement what that file binds and record the difference under **Deviations from plan:**, so Task 15 spells the matching flags.
  - **Spell the branch as `$branch`** inside each subject string of the table and of the two functions below. The fixed-form-subject probe that `cli/templates/claude/context/conventions.md` hands an adopter, and that `.claude/context/conventions.md` → `## Commit-message policy` runs over `scripts`, matches a `$branch` token. That keeps every subject reachable once the flow files stop spelling them.
  - Also export `ucl_review_kind_subject`, which returns `chore: add code review for <b>`, and `ucl_ui_pass_subject <K> <b>`, which returns `chore: Mark UI test <K> passing for <b>`. Those are the two fixed `--unit` subjects, byte-for-byte as `.claude/context/conventions.md` → `## Commit-message policy` → **Fixed-form subjects** lists them.
- [ ] **`cli/test/unit-commit-lib.test.mjs`.**
  - **Header.** It opens with the rule it enforces, which is the library header's rule.
  - **How it runs.** It drives the template library in a `bash` subprocess (`spawnSync('bash', ['-c', '. <lib>; <call>; printf …'])`) against index, detail and listing files built under `os.tmpdir()` and removed in process. No fixture is created inside this checkout.
  - **Cases:**
    - a token resolved by `K` when the walk position `N` differs;
    - a sub-step `- [ ] **Task 3**` outside the readiness section is never matched;
    - the tick changes exactly one line and leaves the file mode `644`;
    - title-tag stripping;
    - normalisation of each of the five marks;
    - a 72-byte cut at a word boundary, and the drop of a title whose first word cannot fit;
    - every unit label;
    - the three `user_review` severities, the `--prefix` refusal on a non-`should` arm and on an illegal token;
    - `**Cause:**` read, with its absent-line fallback;
    - each body record, and the precedence order;
    - a deletion staged as its parent directory;
    - a findings-folder path excluded from the work count;
    - an index-only stage set;
    - every artifact row's subject and path list byte-for-byte;
    - the refusals for an unknown kind, a missing round and an illegal entry id.

**Verification:**

- `npm test --workspace cli -- test/unit-commit-lib.test.mjs`, from the repository root as one plain foreground command, exits zero with `fail 0`.
- `grep -n 'set -' cli/templates/scripts/lib/unit-commit-lib.sh` finds no line that sets a shell option, and `grep -n '\bgit\b' cli/templates/scripts/lib/unit-commit-lib.sh` finds no git invocation, only prose.
- Each subject in the artifact table matches the corresponding line of `.claude/context/conventions.md` → `## Commit-message policy` → **Fixed-form subjects**, read side by side. The two round kinds are the exception: that list does not carry them, and `## Corpus staleness` reports it.
