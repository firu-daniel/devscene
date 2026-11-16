### Task 3 — Give `commit-on-branch.sh` its `--unit` and `--artifact` front end, with `--push` and the printed return

**Goal:** Extend `cli/templates/scripts/commit-on-branch.sh` with the five call forms the story index's `## Context` fixes. Each form ticks, stages, builds its subject and record, commits, optionally pushes, and prints the committer's return lines, all inside the one excluded command. The plain form `--repo <root> <path>… -- <subject> [<body>…]` keeps its behaviour, its stdout line and its exit map byte-for-byte, because `prl_commit`, the watcher and the docs flows depend on them.

**Depends on:** Task 1. It provides these functions in `lib/unit-commit-lib.sh`, each returning through `UCL_*` globals with status 0 / 1 (not found) / 2 (bad input):

- `ucl_entry_find <index_file> <Task|Finding|Test> <K>`
- `ucl_tick <index_file> <lineno>`
- `ucl_short_title`
- `ucl_normalise`
- `ucl_severity`
- `ucl_index_kind <state_dir> <plan_rel>`, which sets `UCL_KIND` and `UCL_FINDINGS_DIR`
- `ucl_unit_label`
- `ucl_branch_prefix`
- `ucl_unit_prefix <kind> <branch> <severity> <prefix_arg>`
- `ucl_subject <prefix> <label> <title>`
- `ucl_detail_file`
- `ucl_record_cause <detail_abs> <Disposition|Already passing>`
- `ucl_body_record`
- `ucl_stage_set <listing> <plan_rel> <findings_rel> <detail_rel> <findings_dir_rel>`, whose listing is the diff section, a lone `--others` record, then the untracked section, all NUL-separated
- `ucl_artifact <kind> <state_dir> <branch> <round> <iteration> <entry>`
- `ucl_review_kind_subject`
- `ucl_ui_pass_subject`

Task 2 ships the library beside this script.

**Where this task stops.** No plugin file changes here. Tasks 8–20 move every caller onto these forms, and until then nothing calls them. This task does not change the permission profile: the literal `allow` entry and the `sandbox.excludedCommands` entry for the main checkout's copy already admit any argument (`cli/templates/claude/settings.autonomous.json` → its `FOUR COMMANDS RUN OUTSIDE THE SANDBOX` note).

### Targets

- `cli/templates/scripts/commit-on-branch.sh`.
- `cli/test/commit-on-branch-unit.test.mjs` (new) — this task's own test file.

**Work:**

- [ ] **Parse and refuse before the first write.**
  - **Sourcing and parsing.** Source `lib/unit-commit-lib.sh` beside `lib/harness-run-lib.sh`, by the same `${BASH_SOURCE[0]}`-relative path; an unreadable one is the existing `cannot read … — refusing to commit` exit 1. Parse `--unit <task|review_item|review_plan_file|ui_test_pass>`, `--artifact <kind>`, `--plan`, `--id`, `--findings`, `--extra`, `--prefix`, `--round`, `--iteration`, `--entry`, a repeatable `--path` and `--push`, in any order.
  - **Usage errors** (exit 1, each with its own line and the usage hint):
    - a front-end flag mixed with `--`;
    - `--unit` together with `--artifact`;
    - a flag its form does not take;
    - a missing `--id` on `task` / `review_item` / `ui_test_pass`, or a non-numeric one.
  - **Order of checks.** Keep every existing check exactly where it runs: the target and `config.worktree` checks, the configuration load, the hooks pin, the branch read, the protected-branch decision, the clone sync-in and the `old_tip` read. The front end starts only after them, so a protected branch still exits 2 with **nothing ticked**.
  - **`stateDir`.** Resolve it from the **main** checkout through `hr_state_dir "$main_top"`, never from the target's configuration (**THE TARGET'S `devscene.config.json` IS NOT TRUSTED EITHER**).
  - **What the arguments may decide.** `--unit`, `--artifact` and the path flags decide only *what* is staged inside the target the existing checks already admitted. Every trust input — which target, which branch, the protected set, `stateDir` — stays read from the main checkout's records, never from an argument's shape (`harness-runs/lessons.md` → `## Trust checks`, the unsandboxed-script rule).
  - **Path refusals.** Refuse, with exit 1 and a `refusing to commit:` line naming the flag and never the file's content:
    - a `--plan` that is absolute or has a `..` segment;
    - a `--plan` that does not sit under `<state_dir>/`;
    - a `--plan` whose path or any parent component under the target is a symbolic link;
    - a `--plan` that is not a regular file;
    - a `--findings`, `--extra` or `--path` value that is absolute or carries `..`;
    - a `--findings` / `--extra` value outside `<state_dir>/`;
    - an index the library cannot classify (`ucl_index_kind` returns 1), or one whose kind does not match the `--unit` value. `task` takes `story`; `ui_test_pass` takes `ui_test`; `review_item` and `review_plan_file` take every review kind.
- [ ] **The unit flow.**
  - **Locate.** For `task` / `review_item` / `ui_test_pass`, find the entry by `--id` (`Task` for `story`, `Test` for `ui_test`, `Finding` otherwise). No entry → `error: --id <K> matched no readiness entry in <plan>`, exit 1, nothing edited.
  - **`ui_test_pass`.** An entry already `[x]` → print `noop: UI test K already marked`, exit 0, no commit and no push. Otherwise tick it. The stage set is the plan alone. The subject is `ucl_ui_pass_subject`.
  - **`task` / `review_item`.**
    - **Tick.** Tick an open entry; an already-`[x]` entry is not edited, and `plan_flipped:` reports it.
    - **Stage set.** Then read the stage set with the wrapper's own `wt_git` runner, so the reads take the `GIT_DIR` / `GIT_INDEX_FILE` / `GIT_WORK_TREE` triple the commit uses. The reads are `diff --name-status -z --no-renames <old_tip>` and `ls-files -z --others --exclude-standard`, written into one listing file under the existing `$work` directory. Never `git status`, which compares against the main checkout's `HEAD` rather than `refs/heads/<branch>`.
    - **Nothing to commit.** When the entry was already `[x]` and the listing names no path, print `error: nothing to commit` and exit 3.
    - **Build.** Then build the stage set with `ucl_stage_set`, the subject with `ucl_unit_prefix`, `ucl_unit_label`, `ucl_short_title`, `ucl_normalise` and `ucl_subject`, and the one body line with `ucl_body_record`. The cause is read only from the detail file `ucl_detail_file` names, and only when that file is in the stage set.
  - **`review_plan_file`.** Stage the plan, `UCL_FINDINGS_DIR` and `--extra` unconditionally. Tick nothing. The subject is `ucl_review_kind_subject`.
  - **`--artifact`.** Take the subject and paths from `ucl_artifact`. `rescreened-input` takes the `--path` values instead and refuses an empty set. Tick nothing.
  - **Commit.** Hand the resulting path list and message lines to the existing staging loop and `hr_commit_paths_var`, unchanged, so every existing path refusal, the filter-driver refusal and the no-hook commit apply to front-end calls too.
- [ ] **The return, the re-sync and the push.**
  - **The return block.** In a front-end form, print it on stdout instead of the plain form's `committed` line: `commit_sha:`, `subject:`, `files_committed:` (the count of paths the new commit changes against `old_tip`), `plan_flipped:` and `pushed:`.
    - `plan_flipped:` holds the ticked entry line, `already-[x]: <entry> — not flipped by this call`, or `none`.
    - `pushed:` holds `yes`, `no` or `failed`.
    - Add `staged: index-only — <UCL_INDEX_ONLY_SET> was the whole diff; no work file was staged` exactly when `UCL_WORK_COUNT` is 0 on `task` / `review_item`.
  - **A landed exit 1** — the commit landed but the index could not take it. Run **one** identical plain-form call of this same script as a child process to re-sync the index. Add `index_sync: failed — <its exit and last stderr line>` when that call does not exit 3. Exit 0, because the commit stands. Every other non-zero outcome prints one `error: <the wrapper's own refusal line>` with the wrapper's exit code (1, or 2 for protected).
  - **`--push`.** After exit 0 or exit 3 — never after a refusal — run `bash <this script's directory>/push-branch.sh <target top>` as a child. Report `pushed: failed` when its output carries one of the failure lines `push-branch.sh`'s header names under **EVERY FAILURE PATH IS NON-FATAL (exit 0)**: read the header for the exact prefixes and pin them in the test. Otherwise report `pushed: yes`; without `--push`, `pushed: no`. On exit 3 with `--push`, print `error: nothing to commit` and still push, so a resumed run's earlier unpushed commit reaches the remote.
- [ ] **Header.**
  - **New paragraphs.** Add one paragraph per new decision, in the header's upper-case style, after **MESSAGE ARGUMENTS**:
    - **THE UNIT AND ARTIFACT FORMS** — the five forms, and why they are this wrapper rather than a new script: no new excluded command, no new profile entry.
    - **THE PLAN PATH IS NOT TRUSTED** — each refusal above.
    - **THE TICK** — only the readiness section, only the one entry, through a temporary file beside the index and `mv`.
    - **THE STAGE SET** — the triple, the tip, deletions as parent directories, the findings folder staged and excluded from the work files.
    - **THE SUBJECT AND ITS RECORD** — built by the library from the index and the table, the 72-byte cap, the body-line precedence, the cause read from the detail file and never from the command line.
    - **THE RETURN** — the lines and the exit map.
    - **THE PUSH**.
  - **Corrections.** **WHAT IT NEVER DOES** must stop saying it never pushes and never flips a checkbox: state that only the front-end forms do either. Extend the usage block and the `REPRO` block with one case per front-end form and per new refusal.
- [ ] **`cli/test/commit-on-branch-unit.test.mjs`.**
  - **Header.** It opens with the rule: every unit and artifact commit is ticked, staged, worded and returned by the wrapper alone, and every refusal leaves the target byte-identical.
  - **Fixture.** It builds throwaway repositories under `os.tmpdir()` the way `cli/test/commit-on-branch-plumbing.test.mjs` does: a main checkout with `devscene.config.json` and a copied `scripts/` tree from `cli/templates/scripts`, plus a linked worktree target and a bare origin.
  - **Cases, each asserting the commit message, the tree and the printed lines:**
    - `task` with a work file;
    - `task` index-only, with `staged:` and the `mark Task K done — ` body line;
    - a dispositioned `task` whose detail file carries `## Disposition` with `**Cause:** `, with the body line and the subject still the title;
    - `review_item` on a code-review index, with the label `Code review finding K` and prefix `fix`;
    - a `user_reviews` Should Fix entry with and without `--prefix`;
    - an already-`[x]` entry on a dirty tree, then on a clean tree (exit 3);
    - `review_plan_file` with `--extra`;
    - `ui_test_pass`, then the `noop:` case;
    - each artifact kind's subject;
    - `--push`, with `pushed: yes` against the bare origin;
    - a deletion staged as its parent;
    - a findings folder;
    - every new refusal, with the target's bytes and the index unchanged;
    - a protected branch, exiting 2 with the index unticked.
  - **No regression.** The existing `commit-on-branch-plumbing` and `commit-on-branch-target-check` suites stay untouched, and the plain form's behaviour must not change under them.

**Verification:**

- `npm test --workspace cli -- test/commit-on-branch-unit.test.mjs`, from the repository root as one plain foreground command, exits zero with `fail 0`.
- `grep -n 'git status' cli/templates/scripts/commit-on-branch.sh` matches no executed command, only header prose.
- Every refusal case in the suite asserts on the bytes on disk — the index unticked and no new commit on `refs/heads/<branch>` — not only on the message (`.claude/context/cli.md` → `## What "done" means here`).
