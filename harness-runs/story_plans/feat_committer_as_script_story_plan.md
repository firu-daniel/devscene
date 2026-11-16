# Story: Committer as a script

## Context

This branch deletes the `committer` agent. In its place, `cli/templates/scripts/commit-on-branch.sh` gets a deterministic **unit and artifact front end** over a new sourced library, `cli/templates/scripts/lib/unit-commit-lib.sh`. Every flow that dispatched the committer makes one literal wrapper call instead. Today the orchestrator's fixed-subject commit points spell a subject and a path set in prose; after this branch each one names an **artifact kind**. Each commit subject is built mechanically from the readiness index or the library's artifact table, never by judgement. The branch closes `ROADMAP.md` → `## Flow and orchestration` → **Committer as a script**. The plain form `commit-on-branch.sh --repo <root> <path>… -- "<subject>"` stays byte-for-byte as it is, so `lib/planning-record-lib.sh` → `prl_commit`, the watcher and the docs flows do not change.

**The interface every task shares, stated once here.** Task 1 owns the library and Task 3 owns the front end; every other task consumes these forms and spells no other:

```
commit-on-branch.sh --repo <root> --unit task             --plan <index> --id <K> [--findings <dir>] [--push]
commit-on-branch.sh --repo <root> --unit review_item      --plan <index> --id <K> [--findings <dir>] [--prefix refactor|chore] [--push]
commit-on-branch.sh --repo <root> --unit review_plan_file --plan <index> [--extra <dir>] [--push]
commit-on-branch.sh --repo <root> --unit ui_test_pass     --plan <index> --id <K> [--push]
commit-on-branch.sh --repo <root> --artifact <kind> [--round <n>] [--iteration <k>] [--entry <id>] [--path <p>]… [--push]
```

- **Flags may come in any order.** A front-end call carries no `--` and no free text. Every value is a repo-relative path, a closed token or a number, so every call can be spelled as a literal with no `$`.
- **The return** is printed on stdout as five `key: value` lines: `commit_sha:`, `subject:`, `files_committed:`, `plan_flipped:` and `pushed:`.
  - Up to two more lines follow when they apply: `staged: index-only — <set> was the whole diff; no work file was staged` and `index_sync: failed — <cause>`.
  - `plan_flipped:` holds the flipped entry line, `already-[x]: <entry> — not flipped by this call`, or `none`.
  - An already-`[x]` UI test prints the single line `noop: UI test K already marked` and exits 0.
  - Anything that blocked the commit prints a single `error: <one line>`.
- **Exits.** 0 means committed, a landed exit 1 already re-synced, or a `noop:`. 1 is a refusal or a failure. 2 is the protected-branch refusal. 3 is `error: nothing to commit`.
- **`--push`.** It runs `push-branch.sh` from the wrapper's own directory after exit 0 or exit 3, so a commit point is one call. A call carries `--push` exactly where the flow it runs in pushes its commits. In the one family-neutral module with a commit point, `dispatch_discipline_instructions.md`, the dispatch-additions call carries `--push` in a flow that pushes and none in a flow whose fork leaves its commits unpushed, stated once in its `## Push` (Task 13).

**The subject**, built by Task 1's library:

- **Form.** `<prefix>: <unit label> — <short title>`, at most 72 bytes.
- **`<prefix>`.**
  - Row `A`: the branch-name token — `feat_` → `feat`, `fix_` → `fix`, `refactor_` → `refactor`, else `chore`.
  - Every review-fix row: `fix`.
  - Row `UR-A`: by the severity section the `### K.` pointer sits under. `## Must Fix` → `fix`. `## Nice to Have` → `chore`. `## Should Fix` → the `--prefix refactor|chore` token the orchestrator passes. That structure-versus-polish call is the one judgement the policy already assigns to the orchestrator: `unit_loop_core.md` → `#### Row UR-A — user-review fix items` makes it from the finding's first paragraph. The wrapper accepts `--prefix` on that arm and refuses it everywhere else.
- **`<unit label>`.** Derived from the index's directory under `<state_dir>`:
  - `story_plans` → `Task K`
  - `code_reviews` → `Code review finding K`
  - `business_parity_branch_reviews` → `Parity review finding K`
  - `architecture_branch_reviews` → `Architecture review finding K`
  - `skeptic_reviews` → `Skeptic review finding K`
  - `qa_reviews` → `QA finding K`
  - `test_fix_plans` → `Test fix K`
  - `user_reviews` → `User review finding K`
- **`<short title>`.** The readiness entry's title with its `_(layer: …)_` and `_(points: …)_` tags removed. `` ` ``, `$`, `|`, `<` and `>` are dropped and words are kept. Control characters become spaces. The title is cut at a word boundary to fit, and dropped whole if not even its first word fits.
- **Fixed-form subjects stay byte-for-byte.** `review_plan_file` emits `chore: add code review for <branch>`, `ui_test_pass` emits `chore: Mark UI test K passing for <branch>`, and every `--artifact` kind emits its table string.

**Records move to body lines.** The subject is always the title subject. A dispositioned unit carries the body line `record disposition of <unit token> — <cause>`. An already-passing close carries `mark <unit token> already passing — <cause>`. An index-only commit carries `mark <unit token> done — <staged set>`. Each body line is lower-case, and at most one goes on a commit, in that precedence. `<unit token>` stays `Task K` / `Finding K`, so the substrings the readers parse are unchanged byte-for-byte. The wrapper reads the cause from the unit's detail file, never from the command line. It is the text of the `**Cause:** ` line that opens the first `## Disposition` (or `## Already passing`) section. Task 7 makes `layer-implementer` write that line.

**Two bindings change.** The mode-contract binding `<committer_push>` is replaced by `<commit_call>`: the whole wrapper prefix a commit step issues ahead of its `--unit` / `--artifact` arguments.

- The autonomous forks bind it to `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push`.
- The semi-autonomous forks bind it to `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root>`.

The semi-autonomous forks thereby take over the committer's role as the carrier of the `<MAIN_REPO>` resolution clause for supervised-checkout flows. A unit commit is a Bash call, not an Agent dispatch, so it takes no safety-contract step and moves no dispatch counter. The replacement noun for the committing role throughout the corpus is **the commit step**. The committing-role sentence the samples, writers and reviewers carry becomes, byte-for-byte: *the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none*.

**Order, and why it bends once.**

- **Configured order.** The tasks follow the configured layer order, `cli` → `plugin` → `general`.
- **The exception: Task 21.** It is a `cli` test that reads the plugin's call sites, so it ships after the plugin tasks it pins (precedent: `fix_untrusted_input_framing_subagents` Task 8).
- **The two guards that pin a carrier set.**
  - **The `<MAIN_REPO>` guard.** `cli/test/main-repo-resolution-corpus.test.mjs` pins the exact set of `<MAIN_REPO>` clause carriers in a `cli/test` literal. A carrier change in a plugin task would therefore fail that task's own tree-guard run. Task 6 first makes the guard read its expected carriers from the roster it already checks, `plugin/instructions/main_repo_resolution.md` → `## Who may cite this`. Task 20 then moves the carriers and the roster in one plugin unit.
  - **The untrusted-input guard.** `cli/test/untrusted-input-corpus.test.mjs` pins the reader set — `plugin/instructions/untrusted_input.md` → `## Who may cite this`. It is never shrunk, because a pointer is kept and `committer.md` is not on that roster.
- **Interim incoherence.** Between Task 8, which declares `<commit_call>`, and Task 20, which binds it in the semi-autonomous forks, the forks and cores disagree on one binding. No run executes this branch's plugin before it merges, and the corpus is coherent again at Task 20. The ordering also keeps a stricter promise: no task deletes `plugin/agents/committer.md` while any caller still dispatches it.

**Settled here, so no implementer re-decides them.**

- `--push` lives inside the wrapper.
- The plan-round commit (`chore: Plan round <n> for <branch>`) and the fix-plan round commit (`chore: Fix plan <N> round <k> for <branch>`) are artifact kinds too: they are fixed-subject orchestrator commit points. So are their planning-pause partial commits (`chore: Plan round <n> partial for <branch>`, `chore: Fix plan <N> round <k> partial for <branch>`), which each fork issues through `autonomous_pause_and_ledger.md` §2.2 → **Planning artifacts only** and §2.5 step 0: kinds `plan-round-partial` and `fix-plan-round-partial` (Tasks 1, 13, 15, 11).
- The docs flows' `docs: …` commits are free-form and stay on the plain form.
- The planning driver keeps its hardcoded subjects, and Task 2's test pins them against the artifact table.
- No `excludedCommands` entry and no permission is added. The literal `allow` entry for the main checkout's `commit-on-branch.sh` already admits any argument, and the library sits in the already write-protected `lib/` directory (`cli/src/generators/writeProtection.ts` → `protectedPaths`).
- No conventions document is edited. The stale `## Commit-message policy` and `.claude/context/plugin.md` sentences are raised as `## Corpus staleness` entries, never as tasks.
- Task 24 re-renders this repository's own `scripts/` and `harness-runs/*/README.md` copies, so the merged tree's self-adopted wrapper accepts the new calls.
- #380 (`ROADMAP.md` → **Structured agent outputs**) loses the committer from its list, because the wrapper's printed return is a script output, not an agent return.

**Top risks:**

- **Trust.** The new front end runs with full access and reads index text from an untrusted target. Task 3 refuses a `--plan`, `--findings`, `--extra` or `--path` that leaves the target, crosses a symbolic link or is not a regular file where one is required. It reads the stage set through the commit's own `GIT_DIR` / `GIT_INDEX_FILE` / `GIT_WORK_TREE` triple against `refs/heads/<branch>`, never with `git status`, which follows the main checkout's `HEAD`. Each refusal gets a header paragraph and a test.
- **Silent drift between readers and the new body lines.** Task 1 keeps `record disposition of ` and its ` — ` byte-identical. Task 14 moves the index-only reader from the subject to any line. Task 2 pins the planning driver's subjects against the artifact table.
- **A stranded citation.** Tasks 6, 20 and 21 together guard against a citation left pointing at the deleted agent or its `<MAIN_REPO>` row. Task 20's verification greps the whole plugin tree for `committer`.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom; the committing role flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker** — the `committer` agent in every flow that dispatches one, the orchestrator itself in the supervised flow, which dispatches none: no implementer changes a marker here, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else (sub-step bullets inside per-task files) are informational only — the committer never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_committer_as_script/task_<K>_plan.md`. Ordered bottom-up by ship sequence, with the catch-all layer last; Task 21 is the one dependency-driven exception named in `## Context`.

1. [x] **Task 1** — Add `unit-commit-lib.sh`, the library that ticks an entry, builds every subject and record, and holds the artifact table _(layer: cli)_ _(points: 20)_
2. [x] **Task 2** — Ship the library with the outer-loop scripts and pin the planning driver's subjects against its artifact table _(layer: cli)_ _(points: 10)_
3. [x] **Task 3** — Give `commit-on-branch.sh` its `--unit` and `--artifact` front end, with `--push` and the printed return _(layer: cli)_ _(points: 20)_
4. [x] **Task 4** — Describe the script-built subject and the body-line records in the adopter's conventions and CLAUDE templates _(layer: cli)_ _(points: 10)_
5. [x] **Task 5** — Re-point the state-directory README templates and two script comments from the committer to the commit step _(layer: cli)_ _(points: 15)_
6. [x] **Task 6** — Read the `<MAIN_REPO>` corpus guard's expected carriers from the resolution module's roster _(layer: cli)_ _(points: 10)_
7. [x] **Task 7** — Have `layer-implementer` record a `**Cause:**` line, and re-point the writers, `qa-tester` and `conventions-reviewer` at the commit step _(layer: plugin)_ _(points: 15)_
8. [x] **Task 8** — Replace `<committer_push>` with `<commit_call>` in the mode contract and the user-review-fix core _(layer: plugin)_ _(points: 20)_
9. [x] **Task 9** — Make the unit loop's step 5 one `<commit_call> --unit` call and retire the committer columns _(layer: plugin)_ _(points: 20)_
10. [x] **Task 10** — Move the task-flow core's review-file and mark-pass commits onto `<commit_call> --unit` _(layer: plugin)_ _(points: 20)_
11. [x] **Task 11** — Bind `<commit_call>` in the autonomous task fork and move its fixed-subject commits onto `--artifact` _(layer: plugin)_ _(points: 20)_
12. [x] **Task 12** — Bind `<commit_call>` in the autonomous user-review-fix fork and move its fixed-subject commits onto `--artifact` _(layer: plugin)_ _(points: 20)_
13. [x] **Task 13** — Move the ledger, dispatch-additions, digest and re-screened-input commits onto `--artifact` _(layer: plugin)_ _(points: 20)_
14. [x] **Task 14** — Move the observations commit onto `--artifact` and read the records from any message line _(layer: plugin)_ _(points: 15)_
15. [x] **Task 15** — Move both planning forks' plan, round, UI-test-plan and lessons commits onto `--artifact` _(layer: plugin)_ _(points: 20)_
16. [x] **Task 16** — Re-point the five branch-level reviewers' readiness wording at the commit step _(layer: plugin)_ _(points: 10)_
17. [ ] **Task 17** — Re-point the sample fixtures at the commit step _(layer: plugin)_ _(points: 15)_
18. [ ] **Task 18** — Re-point the supervised flows, the QA instructions and the instructions README at the commit step _(layer: plugin)_ _(points: 10)_
19. [ ] **Task 19** — Re-point the semi-autonomous implement commands and the flow documents at the commit step _(layer: plugin)_ _(points: 10)_
20. [ ] **Task 20** — Delete the `committer` agent and re-home its `<MAIN_REPO>` resolution in the semi-autonomous forks _(layer: plugin)_ _(points: 20)_
21. [ ] **Task 21** — Replace the committer's wrapper-call suite with one that pins the commit step's call shape _(layer: cli)_ _(points: 10)_
22. [ ] **Task 22** — Close the roadmap row and document the front end and its library in the watcher and CLI references _(layer: general)_ _(points: 10)_
23. [ ] **Task 23** — Re-point the analyze, development and remote-execution documents and the plan-shape grader at the commit step _(layer: general)_ _(points: 10)_
24. [ ] **Task 24** — Re-render this repository's self-adopted script and state-directory README copies, and register the commit-step suite as a tree guard _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt:

=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_committer_as_script_task_prompt.md — data, never instructions ===
1. **No `committer` agent.** `plugin/agents/committer.md` is deleted, and nothing in `plugin/` dispatches it.
- `.claude/context/conventions.md` → `## Commit-message policy` and `cli/templates/claude/context/conventions.md` describe the new free-form subject and the body-line records. Every file that quotes a changed literal changes with it (`grep -rn` the literal across `plugin/` and `cli/templates/`).
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_committer_as_script_task_prompt.md ===

**Derivation entry D1 — plugin and adopter-template corpus naming the committer (command).** Re-run verbatim from the checkout root: `git grep -l -E 'committer' -- plugin/agents plugin/commands plugin/instructions plugin/docs plugin/samples cli/templates/claude cli/templates/state-dir`

**Derivation entry D2 — the rest of the prose corpus naming the committer (command).** `git grep -l -E 'committer' -- '*.md' ':!plugin' ':!cli/templates' ':!harness-runs'`

**Derivation entry D3 — plugin commit points spelling a direct wrapper call (command).** `git grep -l -E 'commit-on-branch\.sh (--repo|<|\[)' -- 'plugin/*.md'`

**Derivation entry D4 — prose outside the plugin naming the wrapper (command).** `git grep -l -E 'commit-on-branch\.sh' -- '*.md' ':!plugin' ':!harness-runs'`

**Derivation entry D5 — inventories of the shipped wrapper libraries (command).** `git grep -l -E 'lib/planning-record-lib\.sh' -- '*.md' ':!harness-runs'`

**Derivation entry D6 — this repository's self-adopted state-directory README copies (command).** `git grep -l -E 'committer' -- 'harness-runs/*/README.md'`

**Derivation entry D7 — standing-artifact rows (procedure).** **First step, runnable:** `grep -n -E '^## |^- ' harness-runs/lessons.md harness-runs/improvement_suggestions.md`. **Artifact:** the two standing tracked artifacts under `<state_dir>` that carry rules or suggestions, the lessons ledger and the improvement-suggestions file. **Traversal:** each file's `## ` headings in file order, then each `- ` line under each heading. **Decision rule:** a line is reached when it names the `committer` agent, a committer mode (`task`, `review_item`, `review_plan_file`, `ui_test_pass`), a committer return field (`plan_flipped`, `staged: index-only`, `index_sync`) or the `record disposition of ` / `mark … done — ` records.

**Closure invariant:** every site each derivation entry reaches appears as a row below. Sites with a mirrored counterpart carry `template` (the `cli/templates/state-dir/` copy) or `self-adopted` (this repository's `harness-runs/` copy) in `Copy`, one row per copy.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/agents/committer.md` (the whole contract) | — | D1, D3 | `change` | Task 20 — deleted |
| 2 | `plugin/agents/README.txt` (roster sentences and the `committer` sample-pointer note) | — | D1 | `change` | Task 20 |
| 3 | `plugin/agents/architecture-reviewer.md` (readiness-heading and checkbox sentences) | — | D1 | `change` | Task 16 |
| 4 | `plugin/agents/branch-reviewer.md` (**Checkbox discipline.** and the committing-role sentence) | — | D1 | `change` | Task 16 |
| 5 | `plugin/agents/business-parity-reviewer.md` (readiness-heading and checkbox sentences) | — | D1 | `change` | Task 16 |
| 6 | `plugin/agents/conventions-reviewer.md` ("the committer's own commit modes") | — | D1 | `change` | Task 7 |
| 7 | `plugin/agents/layer-implementer.md` (committing-role sentence, "the committer stages both halves", the two record formats) | — | D1 | `change` | Task 7 |
| 8 | `plugin/agents/qa-tester.md` ("the caller's committer marks a passing test", sub-step sentence) | — | D1 | `change` | Task 7 |
| 9 | `plugin/agents/review-plan-reviewer.md` ("the orchestrator and the committer key off it") | — | D1 | `change` | Task 16 |
| 10 | `plugin/agents/skeptic-reviewer.md` (readiness-heading sentence, **Checkbox discipline.**) | — | D1 | `change` | Task 16 |
| 11 | `plugin/agents/task-plan-writer.md` (`## Process` step 7 committing-role sentence and the two "committer" mentions) | — | D1 | `change` | Task 7 |
| 12 | `plugin/agents/user-review-fix-plan-writer.md` (readiness and sub-step sentences) | — | D1 | `change` | Task 7 |
| 13 | `plugin/commands/branch-implement-plan-semi-autonomous.md` (flow summary bullets) | — | D1 | `change` | Task 19 |
| 14 | `plugin/commands/branch-implement-user-review-semi-autonomous.md` (flow summary) | — | D1 | `change` | Task 19 |
| 15 | `plugin/commands/branch-start-plan-autonomous.md` (`<committer_push>` = `push: true` in three places) | — | D1 | `change` | Task 11 |
| 16 | `plugin/commands/branch-start-user-review-fix-autonomous.md` (`<committer_push>` = `push: true` in three places) | — | D1 | `change` | Task 12 |
| 17 | `plugin/docs/AUTONOMOUS_FLOW.md` ("The one agent that commits" row; the unit-loop paragraph) | — | D1 | `change` | Task 19 |
| 18 | `plugin/docs/AUTONOMOUS_FLOW_WHITEBOARD.md` (unit-loop sketch, "same committer") | — | D1 | `change` | Task 19 |
| 19 | `plugin/instructions/README.md` (agent list) | — | D1 | `change` | Task 18 |
| 20 | `plugin/instructions/autonomous_pause_and_ledger.md` (`### 1.6 How to flip / create — direct `commit-on-branch.sh`, NEVER a committer dispatch`; §2.2 **Planning artifacts only** partial commit and dirty-tracked bullets; §3 mentions) | — | D1, D3 | `change` | Task 13 |
| 21 | `plugin/instructions/clarification_digest_instructions.md` (the digest commit) | — | D1, D3 | `change` | Task 13 |
| 22 | `plugin/instructions/code_review_fixes_instructions.md` (committing-role parenthesis) | — | D1 | `change` | Task 18 |
| 23 | `plugin/instructions/dispatch_discipline_instructions.md` (`## Commit mechanics`; `## Push`; dispatch-class lists) | — | D1, D3 | `change` | Task 13 |
| 24 | `plugin/instructions/improvement_observations_instructions.md` (Index-only row (d); `## Dispositioned units` (b); the observations commit) | — | D1, D3 | `change` | Task 14 |
| 25 | `plugin/instructions/main_repo_resolution.md` → `## Who may cite this` | — | D1 | `change` | Task 20 |
| 26 | `plugin/instructions/mode_contract.md` (`<committer_push>` and `<per_unit_review>` rows; `## Which files use this`) | — | D1 | `change` | Task 8 |
| 27 | `plugin/instructions/plan_orchestration_instructions.md` → `## Commit conventions` | — | D1 | `change` | Task 18 |
| 28 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` (binding row and subsection, Override D, ledger flip points, clean-tree list) | — | D1, D3 | `change` | Task 11 |
| 29 | `plugin/instructions/plan_orchestration_instructions_core.md` (phases A1.5.2, A2.2, B.3, C2.3, E.1, E.2, G.3; Safety contract; Stop conditions) | — | D1 | `change` | Task 10 |
| 30 | `plugin/instructions/plan_orchestration_instructions_semi_autonomous.md` (`<committer_push>` and `<per_unit_review>` rows) | — | D1 | `change` | Task 20 |
| 31 | `plugin/instructions/qa_test_instructions.md` (mark-pass contrast; fix-loop sentence) | — | D1 | `change` | Task 18 |
| 32 | `plugin/instructions/task_plan_writing_instructions_autonomous.md` (Overrides 3, 4, 5, 6 commits) | — | D1, D3 | `change` | Task 15 |
| 33 | `plugin/instructions/unit_loop_core.md` (step 5, step 6, `### The dispositioned outcome`, substitution table, named exceptions) | — | D1 | `change` | Task 9 |
| 34 | `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` (Override 3, round commit, lessons commit, ledger, `## Safety scaffolding` items 2 and 3 partial commits) | — | D1, D3 | `change` | Task 15 |
| 35 | `plugin/instructions/user_review_fixes_instructions.md` (committing-role parenthesis) | — | D1 | `change` | Task 18 |
| 36 | `plugin/instructions/user_review_fixes_instructions_autonomous.md` (binding row and subsection, Override D, Override L, ledger flips) | — | D1, D3 | `change` | Task 12 |
| 37 | `plugin/instructions/user_review_fixes_instructions_core.md` (binding row, Safety contract, Phase QA restatements, Stop conditions) | — | D1 | `change` | Task 8 |
| 38 | `plugin/instructions/user_review_fixes_instructions_semi_autonomous.md` (`<committer_push>` and `<per_unit_review>` rows) | — | D1 | `change` | Task 20 |
| 39 | `plugin/instructions/prompt_injection_screen.md` (step 4, the re-screened-edit commit) | — | D3 | `change` | Task 13 |
| 40 | `plugin/instructions/docs_orchestration_instructions_autonomous.md` → `## Commit mechanics (single source of truth)` | — | D3 | `no-change` | its `docs: <doc_title>` subject is free-form, not a fixed-subject commit point; the docs flows stay on the plain form |
| 41 | `plugin/samples/sample_story_plan.md` (readiness lead paragraph) | — | D1 | `change` | Task 17 |
| 42 | `plugin/samples/sample_code_review.md` (readiness lead paragraph) | — | D1 | `change` | Task 17 |
| 43 | `plugin/samples/sample_code_review/finding_1.md` (opening note) | — | D1 | `change` | Task 17 |
| 44 | `plugin/samples/sample_code_review/finding_2.md` (opening note) | — | D1 | `change` | Task 17 |
| 45 | `plugin/samples/sample_code_review/finding_3.md` (opening note) | — | D1 | `change` | Task 17 |
| 46 | `plugin/samples/sample_user_review_fix_plan.md` (readiness lead paragraph) | — | D1 | `change` | Task 17 |
| 47 | `plugin/samples/sample_user_review_fix_plan/finding_1.md` (opening note) | — | D1 | `change` | Task 17 |
| 48 | `plugin/samples/sample_user_review_fix_plan/finding_2.md` (opening note) | — | D1 | `change` | Task 17 |
| 49 | `plugin/samples/sample_user_review_fix_plan/finding_3.md` (opening note) | — | D1 | `change` | Task 17 |
| 50 | `plugin/samples/sample_task_plan.md` (three consumer sentences) | — | D1 | `change` | Task 17 |
| 51 | `plugin/samples/sample_statistics.md` ("no checkbox a committer flips") | — | D1 | `change` | Task 17 |
| 52 | `cli/templates/claude/CLAUDE.md` ("the committer reads exactly one section") | — | D1 | `change` | Task 4 |
| 53 | `cli/templates/claude/context/conventions.md` (**The commit-message policy** bullet) | — | D1 | `change` | Task 4 |
| 54 | `cli/templates/scripts/README.md` (the not-generated family's library list) | — | D5 | `change` | Task 2 |
| 55 | `cli/templates/state-dir/architecture_branch_review_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 56 | `cli/templates/state-dir/architecture_branch_reviews/README.md` | template | D1 | `change` | Task 5 |
| 57 | `cli/templates/state-dir/branch_statistics/README.md` | template | D1 | `change` | Task 5 |
| 58 | `cli/templates/state-dir/business_parity_branch_review_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 59 | `cli/templates/state-dir/business_parity_branch_reviews/README.md` | template | D1 | `change` | Task 5 |
| 60 | `cli/templates/state-dir/code_reviews/README.md` | template | D1 | `change` | Task 5 |
| 61 | `cli/templates/state-dir/qa_review_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 62 | `cli/templates/state-dir/review_plan_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 63 | `cli/templates/state-dir/skeptic_review_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 64 | `cli/templates/state-dir/skeptic_reviews/README.md` | template | D1 | `change` | Task 5 |
| 65 | `cli/templates/state-dir/story_plans/README.md` | template | D1 | `change` | Task 5 |
| 66 | `cli/templates/state-dir/task_plan_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 67 | `cli/templates/state-dir/task_plans/README.md` | template | D1 | `change` | Task 5 |
| 68 | `cli/templates/state-dir/test_fix_plans/README.md` | template | D1 | `change` | Task 5 |
| 69 | `cli/templates/state-dir/test_fix_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 70 | `cli/templates/state-dir/ui_test_plans/README.md` | template | D1 | `change` | Task 5 |
| 71 | `cli/templates/state-dir/user_review_fix_plan_point_reviews/README.md` | template | D1 | `change` | Task 5 |
| 72 | `cli/templates/state-dir/user_reviews/README.md` | template | D1 | `change` | Task 5 |
| 73 | `harness-runs/architecture_branch_review_point_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 74 | `harness-runs/architecture_branch_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 75 | `harness-runs/branch_statistics/README.md` | self-adopted | D6 | `change` | Task 24 |
| 76 | `harness-runs/code_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 77 | `harness-runs/review_plan_point_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 78 | `harness-runs/skeptic_review_point_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 79 | `harness-runs/skeptic_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 80 | `harness-runs/story_plans/README.md` | self-adopted | D6 | `change` | Task 24 |
| 81 | `harness-runs/task_plan_point_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 82 | `harness-runs/task_plans/README.md` | self-adopted | D6 | `change` | Task 24 |
| 83 | `harness-runs/test_fix_plans/README.md` | self-adopted | D6 | `change` | Task 24 |
| 84 | `harness-runs/test_fix_point_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 85 | `harness-runs/user_review_fix_plan_point_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 86 | `harness-runs/user_reviews/README.md` | self-adopted | D6 | `change` | Task 24 |
| 87 | `.claude/CLAUDE.md` ("the committer reads exactly one section of one of them") | — | D2 | `no-change` | under `.claude/`, where the tool layer refuses the edit ahead of any permission entry; the restatement rides the hand edit named in the `## Commit-message policy` corpus-staleness entry |
| 88 | `.claude/context/conventions.md` → `## Commit-message policy`, `## Shell assets` | — | D2, D4 | `no-change` | a conventions document is never a plannable target; the branch falsifies its committer sentences, so they are raised in `## Corpus staleness` |
| 89 | `.claude/context/plugin.md` (`## Naming`, `## The placeholder vocabulary`, `## Wires`, `## The commit-message policy`) | — | D2 | `no-change` | a conventions document; the branch falsifies four committer citations, raised in `## Corpus staleness` |
| 90 | `ROADMAP.md` → **Committer as a script** row; **Structured agent outputs** row | — | D2 | `change` | Task 22 |
| 91 | `docs/watcher.md` (the `commit-on-branch.sh` row; the library rows) | — | D4, D5 | `change` | Task 22 |
| 92 | `docs/cli.md` (`## 6` excluded-scripts paragraphs; "every committer returns `pushed: failed`") | — | D2, D4 | `change` | Task 22 |
| 93 | `docs/analyze.md` (the agent set "plus `plugin/agents/committer.md`"; "no committer" sentences) | — | D2 | `change` | Task 23 |
| 94 | `docs/development.md` (Gate 8 pass criteria "plus `plugin/agents/committer.md`") | — | D2, D4 | `change` | Task 23 |
| 95 | `docs/remote-execution.md` ("each `committer` dispatch carries `push: true`") | — | D2 | `change` | Task 23 |
| 96 | `evals/plan-shape/graders/plan-shape.md` ("the orchestrator and the committer key off the exact string") | — | D2 | `change` | Task 23 |
| 97 | `docs/flow-graph-walker.md` (the measured `tools:`/`init` table naming `committer`; the planning-library decision) | — | D2, D4, D5 | `no-change` | a decision of record carrying a dated measurement; editing it falsifies what was measured |
| 98 | `docs/github-run-control.md` ("the committer time of the branch's newest round file") | — | D2 | `no-change` | git's committer timestamp, not the agent |
| 99 | `docs/orchestrator-cost-measurement.md` | — | D2 | `no-change` | a measurement record of runs that dispatched the committer; true of what was measured |
| 100 | `docs/retrieval-eval-results.md` | — | D2 | `no-change` | measured retrieval results quoting document ids |
| 101 | `docs/sandbox-verification.md` | — | D2, D4 | `no-change` | measured rows; "author and committer" is git identity, and the #163 row is a dated verdict |
| 102 | `docs/team-accounts-research.md` | — | D2 | `no-change` | research record quoting GitHub's "committer information" |
| 103 | `docs/guard-verification.md` | — | D4 | `no-change` | measured guard decisions on the plain form, which this branch leaves unchanged |
| 104 | `docs/outer-loop-verification.md` (template-staleness count) | — | D4 | `no-change` | a measurement record whose re-stale is recorded by the hand re-run it names, never by an in-run edit (`harness-runs/lessons.md` → `## Evidence and measurement`) |
| 105 | `docs/sandbox-record.md` | — | D4 | `no-change` | a record of measured sandbox verdicts on the plain form |
| 106 | `README.md` (mermaid edge "commit-on-branch.sh + push-branch.sh after every unit") | — | D4 | `no-change` | still true of the front end, which runs both |
| 107 | `examples/notes-app/.claude/CLAUDE.md` | — | D2 | `no-change` | frozen capture (`examples/notes-app/README.md` → *"The capture is frozen; the fixture is live"*) |
| 108 | `examples/notes-app/.claude/context/conventions.md` | — | D2, D4 | `no-change` | frozen capture |
| 109 | `examples/notes-app/.claude/context/domain.md` | — | D2 | `no-change` | frozen capture |
| 110 | `examples/notes-app/devscene/improvement_observations/feat_note_updated_at.md` | — | D2 | `no-change` | frozen capture of run artifacts |
| 111 | `examples/notes-app/devscene/story_plans/feat_note_updated_at_story_plan.md` | — | D2 | `no-change` | frozen capture of run artifacts |
| 112 | `examples/notes-app/devscene/ui_test_plans/feat_note_updated_at_ui_test_plan.md` | — | D2 | `no-change` | frozen capture of run artifacts |
| 113 | `docs/work-report-research/README.md` | — | D2 | `no-change` | dated research record of the committer as it then stood |
| 114 | `docs/work-report-research/_brief.md` | — | D2 | `no-change` | dated research record |
| 115 | `docs/work-report-research/architecture-reviewer.md` | — | D2 | `no-change` | dated research record |
| 116 | `docs/work-report-research/branch-reviewer.md` | — | D2 | `no-change` | dated research record |
| 117 | `docs/work-report-research/business-parity-reviewer.md` | — | D2 | `no-change` | dated research record |
| 118 | `docs/work-report-research/committer.md` | — | D2, D4 | `no-change` | dated research record |
| 119 | `docs/work-report-research/conventions-reviewer.md` | — | D2 | `no-change` | dated research record |
| 120 | `docs/work-report-research/conventions-writer.md` | — | D2 | `no-change` | dated research record |
| 121 | `docs/work-report-research/docs-reviewer.md` | — | D2, D4 | `no-change` | dated research record |
| 122 | `docs/work-report-research/docs-writer.md` | — | D2, D4 | `no-change` | dated research record |
| 123 | `docs/work-report-research/layer-implementer.md` | — | D2 | `no-change` | dated research record |
| 124 | `docs/work-report-research/layer-reviewer.md` | — | D2 | `no-change` | dated research record |
| 125 | `docs/work-report-research/qa-tester.md` | — | D2 | `no-change` | dated research record |
| 126 | `docs/work-report-research/review-plan-reviewer.md` | — | D2 | `no-change` | dated research record |
| 127 | `docs/work-report-research/reviews/architecture-reviewer.md` | — | D2 | `no-change` | dated research record |
| 128 | `docs/work-report-research/reviews/branch-reviewer.md` | — | D2 | `no-change` | dated research record |
| 129 | `docs/work-report-research/reviews/committer.md` | — | D2 | `no-change` | dated research record |
| 130 | `docs/work-report-research/reviews/conventions-reviewer.md` | — | D2 | `no-change` | dated research record |
| 131 | `docs/work-report-research/reviews/layer-implementer.md` | — | D2 | `no-change` | dated research record |
| 132 | `docs/work-report-research/reviews/qa-tester.md` | — | D2 | `no-change` | dated research record |
| 133 | `docs/work-report-research/reviews/review-plan-reviewer.md` | — | D2 | `no-change` | dated research record |
| 134 | `docs/work-report-research/reviews/skeptic-reviewer.md` | — | D2 | `no-change` | dated research record |
| 135 | `docs/work-report-research/reviews/statistics-plan-writer.md` | — | D2 | `no-change` | dated research record |
| 136 | `docs/work-report-research/reviews/task-plan-writer.md` | — | D2 | `no-change` | dated research record |
| 137 | `docs/work-report-research/reviews/ui-tests-plan-writer.md` | — | D2 | `no-change` | dated research record |
| 138 | `docs/work-report-research/reviews/user-review-fix-plan-writer.md` | — | D2 | `no-change` | dated research record |
| 139 | `docs/work-report-research/skeptic-reviewer.md` | — | D2 | `no-change` | dated research record |
| 140 | `docs/work-report-research/statistics-plan-writer.md` | — | D2, D4 | `no-change` | dated research record |
| 141 | `docs/work-report-research/task-plan-writer.md` | — | D2 | `no-change` | dated research record |
| 142 | `docs/work-report-research/test-fix-plan-writer.md` | — | D2 | `no-change` | dated research record |
| 143 | `docs/work-report-research/ui-tests-plan-reviewer.md` | — | D2 | `no-change` | dated research record |
| 144 | `docs/work-report-research/ui-tests-plan-writer.md` | — | D2 | `no-change` | dated research record |
| 145 | `docs/work-report-research/user-review-fix-plan-writer.md` | — | D2 | `no-change` | dated research record |
