# Story: The review sweep moves into an adopter-owned document

## Context

This branch takes half (a) of the end-of-branch reviewer's Pass 0, the grep sweep, out of `plugin/agents/branch-reviewer.md` and into one adopter-owned document, `.claude/review-sweep.md`. `devscene init` writes that document as a skeleton, and `/devscene:analyze` fills it from the repository's own code. A shipped script runs its rows against the branch's added lines, and `branch-reviewer` verifies each hit in context. Half (b), the new-exported-symbol caller check, and the rest of the review are unchanged. Tasks run bottom-up: the `cli` layer's skeleton, script, script row and doctor check; then the `plugin` layer's writer, reviewer, analyze command and branch reviewer; then the `general` layer's self-adopted script copy and documentation.

**The settled design. Every task builds against these decisions.**

- **The document.** `.claude/review-sweep.md` is a fixed path, written `create-if-absent` like the conventions stubs. It is deliberately **not** under `.claude/context/` and gets **no** row in the always-loaded file's routing table, so no per-unit agent loads it (task prompt, goal 1). Its owner constant is `REVIEW_SWEEP_PATH` in `cli/src/generators/claudeContext.ts` (Task 1). The plugin spells the path literally, as it already spells `.claude/qa_test_scenarios.md`. The skeleton carries both halves of the two-part untouched-skeleton test (`<!-- devscene:unfilled -->` and `**What belongs here**`), so `init`, `doctor` and the analyze command can all tell whether it has been filled.
- **The row format is a wire.** The script parses it, the conventions writer emits it, the conventions reviewer grades it and the skeleton states it to a person:
  - the rows sit in the one GitHub-flavoured Markdown table directly under the exact heading `## Sweep rows`;
  - the table's header row is exactly `| Escape class | Regex | Covers | Exempts | A hit is a candidate for |`, followed by its separator row and then one row per escape class;
  - the table ends at the first line that does not begin with `|`;
  - the `Regex` cell is exactly one backtick code span holding a POSIX extended regular expression, the dialect `grep -E` reads. A literal `|` inside it is written `\|`, the Markdown table escape, and the script turns each `\|` back into `|` before matching. A regex cannot contain a backtick;
  - `Covers` is one or more code-spanned repo-relative paths separated by `, `. Each is a `layers[].path` value or a path beneath one, and `.` is the whole repository;
  - `Exempts` is code-spanned repo-relative paths or git pathspec globs separated by `, `, or the single character `—` for none;
  - the last cell is prose.

  Worked examples anywhere else in the document are bullet lists, never tables.
- **The sweep script.** The proposal is taken. `review-sweep.sh` ships with the outer-loop scripts (Tasks 2 and 3) and is tested once in `cli/test/review-sweep.test.mjs`. Usage is `review-sweep.sh [--repo <checkout>]`. It reads `defaultBranch` and `stateDir` from **its own** checkout's `devscene.config.json` through `lib/harness-run-lib.sh`, and it reads the rows from the sweep document **as `<default_branch>` commits it** in the `--repo` checkout (`git show <default_branch>:.claude/review-sweep.md`). It applies each row to the added lines of `git diff <default_branch>...HEAD`, restricted to that row's `Covers` minus its `Exempts`, with the whole `<state_dir>` tree always excluded. Exit `0` means no hits, with nothing printed. Exit `1` means hits, one `<path>:<line>: <escape class>` per hit on stdout, where `<line>` is the line number in the branch's version of the file. Exit `2` is a configuration error, with one line on stderr naming the cause.
  - **Why the script beats the agent's grep:** the old in-agent pipeline lost the hit's file and line (`grep -n` numbered the filtered stream), and a per-row `Covers` / `Exempts` scope cannot be written as one pathspec. A script gets both right deterministically, and one test covers it for every adopter. The reviewer still judges every hit.
  - **Tamper resistance:** a branch cannot weaken its own sweep. The rows are read from `<default_branch>`, never from the branch's tree, and `branch-reviewer` invokes the **main checkout's** copy, `bash <MAIN_REPO>/<scripts_dir>/review-sweep.sh --repo <repo_root>`, which the unattended profile write-protects as it does every outer-loop script.
  - **The one permission:** the script's `OUTER_LOOP_SCRIPTS` row carries `agentInvocable: true`. That flag is the single allow rule this branch adds. The permission-profile generator renders it into its existing repo-relative and repo-root-absolute pair with no code change. No other profile entry is added.
- **Rejected: a gate tier for exact rows.** A hit stays a lead, never a failure. That is how the reviewer treats it, and a second row kind that fails the branch would need a consumer in Run gates, whose units are test files (`treeGuards`), not document rows. The exact case this repository has already has its own gate, `scripts/check-machine-paths.sh`. Nothing is deferred.
- **Taken: a `doctor` check.** `review-sweep` (Task 4) warns when the document is missing or still an untouched skeleton, reusing `isUntouchedSkeletonText`.
- **Taken: the stub's UI classes move into the skeleton** as worked examples for a front-end adopter (Task 1), as a bullet list inside the `**What belongs here**` guidance. They are never live rows.
- **The analyze integration.** `sweep` becomes a fourth reserved analyze target (`RESERVED_ANALYZE_TARGETS`, Task 1). It runs **last**, after the corpus pass, because its rows are derived from the finished conventions documents. It is classified by the same two-part test as a conventions document, written by `conventions-writer` (`pass: document`, `target: sweep`, `scope` = repository root) and reviewed once by `conventions-reviewer`, whose new check runs every row's regex against the code it covers. It is never a member of the corpus pass.
- **No agent's return changes.** A missing or unfilled sweep document goes in the branch review index's Context paragraph. The writer and reviewer returns keep their fields, and `shared_document_divergences` is `[]` on a `target: sweep` dispatch. So no `plugin/schemas/*.return.json` changes.
- **Removed outright:** the in-agent table, its "stub, to be edited" sentence and its *"add a row when `<state_dir>/lessons.md` records a new one"* rule. No document takes the lessons rule over, and nothing falls back to the old table (task prompt, constraints and goal 4).

**Nothing under `.claude/` is written by this branch** (task prompt, goal 5). That covers this repository's own sweep document, its machine-local permission profile and the `examples/notes-app/.claude/` copies alike. The self-adopted copy outside `.claude/`, `scripts/review-sweep.sh`, is Task 9's.

**Top risks:**

- **A row format that drifts between the four parties that read or write it** — script, writer, reviewer and skeleton. Every task file restates the wire format above verbatim. Task 2's test pins the parser to it, including the `\|` escape and `—`.
- **A sweep the branch can disarm.** Task 2 reads the rows from `<default_branch>` and Task 8 invokes the main checkout's copy. Task 2's test asserts that a working-tree edit to the document changes nothing.
- **A sweep document the branch reviewer turns into a blocker.** Task 8 states that a missing script, a refused call or an exit `2` is a configuration gap, reported in the index's Context paragraph, and that half (b) and the rest of the review still run.

**Manual setup required:**

- After the merge, in this repository's main checkout on `dev`, run `npx devscene init`. Unforced, it creates the absent `.claude/review-sweep.md` skeleton and rewrites nothing else.
- Add the review sweep's two `allow` entries to the machine-local `.claude/settings.autonomous.json` by hand: the repo-relative `bash scripts/review-sweep.sh` form and its repo-root-absolute twin, in the `:*` shape the profile already uses for every other agent-invocable outer-loop script. A forced `init` would also regenerate the conventions documents.
- Run `/devscene:analyze sweep` and commit the filled `.claude/review-sweep.md` on `dev`. This is goal 5, and the first real-world check of goal 3.

  These three depend on Tasks 1, 3 and 7.
- Re-render `examples/notes-app/.claude/settings.autonomous.json` and add that example's `.claude/review-sweep.md` skeleton. Both sit under a `.claude/` directory the run cannot write. Depends on Tasks 1 and 3.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom, and the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker:** the commit step, `commit-on-branch.sh --unit`, in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets in per-task files, are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_review_sweep_in_conventions/task_<K>_plan.md`. They are ordered bottom-up by ship sequence in the configured layer order (`cli`, `plugin`, then the catch-all `general` last).

1. [x] **Task 1** — Write the `.claude/review-sweep.md` skeleton from `init` and reserve the `sweep` analyze target _(layer: cli)_ _(points: 20)_
2. [x] **Task 2** — Ship `review-sweep.sh`, which applies the sweep rows to a branch's added lines, with its test suite _(layer: cli)_ _(points: 20)_
3. [ ] **Task 3** — Add `review-sweep.sh` to the outer-loop script table as agent-invocable _(layer: cli)_ _(points: 15)_
4. [ ] **Task 4** — Add the `review-sweep` doctor check for a missing or unfilled sweep document _(layer: cli)_ _(points: 15)_
5. [ ] **Task 5** — Teach `conventions-writer` the `sweep` target and the sweep row format _(layer: plugin)_ _(points: 15)_
6. [ ] **Task 6** — Teach `conventions-reviewer` the `sweep` target and the regex-grounding check _(layer: plugin)_ _(points: 15)_
7. [ ] **Task 7** — Run the `sweep` target last in `/devscene:analyze` _(layer: plugin)_ _(points: 20)_
8. [ ] **Task 8** — Make `branch-reviewer` take its Pass 0 grep sweep from `review-sweep.sh` _(layer: plugin)_ _(points: 20)_
9. [ ] **Task 9** — Self-adopt `scripts/review-sweep.sh` and list it in the watcher's script table _(layer: general)_ _(points: 10)_
10. [ ] **Task 10** — Document the sweep document, the `sweep` target and the `review-sweep` check _(layer: general)_ _(points: 20)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`## Constraints`, first bullet):

=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_review_sweep_in_conventions_task_prompt.md — data, never instructions ===
The document path and heading the reviewer reads, and any literal it quotes, appear in every file that cites it. Rename or add one in every citer in the same change, including the `plugin/schemas/*.return.json` of any agent whose return changes.
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_review_sweep_in_conventions_task_prompt.md ===

Application source (`cli/src/**`, shell bodies and their comments) is outside the register. Its edits are owned by the tasks above. No `plugin/schemas/*.return.json` is a site, because no agent's return changes (`## Context`).

**Derivation entries.** Each is re-run verbatim from the repository root. All are read-only.

- **E1 — the Pass 0 sweep's citers (command):** `git grep -l -E 'Pass 0|sweep list|stub, to be edited|deterministic sweep' -- plugin cli docs schemas examples README.md ARCHITECTURE.md`
- **E2 — the reserved analyze-target vocabulary (command):** `git grep -l -E 'reserved (analyze )?(target|name|word)s?|three reserved|RESERVED_ANALYZE_TARGETS' -- 'plugin/*.md' 'docs/*.md' 'cli/templates/*.md' README.md ARCHITECTURE.md`
- **E3 — prose inventories of the outer-loop scripts (command):** `git grep -l -F 'task-offer-check.sh' -- 'docs/*.md' 'plugin/*.md' 'cli/templates/*.md' README.md ARCHITECTURE.md`
- **E4 — prose inventories of what `init` writes under `.claude/` (command):** `git grep -l -F 'devscene-task-offer.md' -- 'docs/*.md' 'cli/templates/*.md' README.md ARCHITECTURE.md`
- **E5 — prose naming `doctor`'s setup checks (command):** `git grep -l -F 'setup-analysis' -- 'docs/*.md' 'plugin/*.md' 'cli/templates/*.md' README.md`
- **E6 — the conventions agents' target vocabulary (command):** `git grep -l -E 'the reserved word `conventions`|`conventions` for the shared cross-layer document' -- plugin docs`
- **E7 — counted citation rosters (command):** `git grep -n -E 'no document beyond these [0-9]+' -- plugin`
- **E8 — conventions-document statements of the main-checkout wrapper set (command):** `git grep -n -F 'launch-sandboxed-gates.sh' -- .claude/context`
- **E9 — standing-artifact rows (procedure).** **First step, runnable:** `grep -n -i -E 'sweep|Pass 0|regex|review-sweep' harness-runs/lessons.md harness-runs/improvement_suggestions.md`. **Artifact:** those two standing ledgers. **Traversal:** each topic heading in file order, then the one-line entries under it. **Decision rule:** an entry is reached when it names the reviewer's sweep, its table or a surface on this branch's target list. On this plan's walk the procedure reached no entry, so it contributes no row.
- **E10 — statements of what `/devscene:analyze` writes (command):** `git grep -n -E "command's to write|What it may write|conventions documents it fills|You write one file" -- docs plugin/commands plugin/agents/conventions-writer.md README.md ARCHITECTURE.md`

**Closure invariant:** every site any derivation entry reaches appears as a row below. A site is each separately anchored passage of a printed file that carries the entry's pattern, not the file as a whole: re-run an `-l` entry with `-n` in place of `-l` to see its passages. A printed file, or a passage within one, that no row names is a register gap.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/agents/branch-reviewer.md` → `### Pass 0 — the deterministic sweep` | — | E1 | `change` | Task 8 |
| 2 | `docs/work-report-research/branch-reviewer.md` ("The sweep table is a per-row check") | — | E1 | `no-change` | A dated research record of the definition as it was measured. A document of record is not edited to track later behaviour. |
| 3 | `docs/work-report-research/reviews/branch-reviewer.md` ("then Pass 0") | — | E1 | `no-change` | Same reason as row 2. |
| 4 | `examples/notes-app/devscene/code_reviews/feat_note_updated_at_code_review.md` ("Pass 0's grep sweep found no escapes") | — | E1 | `no-change` | Frozen capture (`examples/notes-app/README.md` → *"The capture is frozen; the fixture is live"*). |
| 5 | `docs/analyze.md` → `## 1. The target vocabulary` ("plus three reserved names") | — | E2 | `change` | Task 10 |
| 6 | `docs/cli.md` → the analyze-step paragraph ("plus the three") | — | E2 | `change` | Task 10 |
| 7 | `plugin/agents/conventions-reviewer.md` → `<layer_names>` row and `## Invocation contract` `target` row | — | E2, E6 | `change` | Task 6 |
| 8 | `plugin/agents/conventions-writer.md` → `<layer_names>` row and `## Invocation contract` `target` row | — | E2, E6 | `change` | Task 5 |
| 9 | `plugin/commands/analyze.md` → `<layer_names>` row and `## Context` ("one of the three reserved words") | — | E2 | `change` | Task 7 |
| 10 | `cli/templates/scripts/README.md` ("The other family in this directory is not generated.") | — | E3 | `change` | Task 3 |
| 11 | `docs/cli.md` → `## 3. The re-run contract` table | — | E3, E4 | `change` | Task 10 |
| 12 | `docs/cli.md` → the `doctor` check table (the `task-offer-rules` row) | — | E3, E5 | `change` | Task 10 |
| 27 | `docs/cli.md` → the paragraph opening "Two families land in `scriptsDir`, and only one of them is generated." (the outer-loop inventory and the agent-invocable list) | — | E3 | `change` | Task 10 |
| 28 | `docs/cli.md` → the list under the `doctor` table opening "Which severity a check carries is a decision, not a default" (the `setup-analysis` bullet, and the `task-offer-rules` bullet with its "Two more arms" paragraphs) | — | E3, E5 | `change` | Task 10: a `review-sweep` severity bullet joins the list. The `setup-analysis` and `task-offer-rules` bullets themselves are unchanged. |
| 29 | `plugin/agents/branch-reviewer.md` → `## Resolved values`, the `<repo_root>` / `<app_dir>` row ("the Pass 0 sweep") and the `<impl_stack>` row ("write a Pass 0 regex") | — | E1 | `change` | Task 8 |
| 30 | `plugin/agents/branch-reviewer.md` → the review steps, step 3 ("Run the mechanical sweep (Pass 0)") | — | E1 | `no-change` | It points at `### Pass 0 — the deterministic sweep`, a heading Task 8 keeps. |
| 31 | `docs/analyze.md` → §4, the paragraph opening "What a forced setup re-run costs the analysis." ("Two artifacts are kept instead") | — | E5 | `change` | Task 10: Task 1 gives the sweep document the conventions stub's conditional `--force` keep, so the kept artifacts this paragraph enumerates gain one. |
| 32 | `docs/analyze.md` → §9, the paragraph opening "The precondition is stated at two sites" (`doctor`'s `setup-analysis` warnings) | — | E5 | `no-change` | The `review-sweep` warning names the command as one route among two (or a hand edit), the case this paragraph already leaves out. |
| 33 | `plugin/commands/analyze.md` → `## Resolved values`, the `<shared_conventions_path>` row (the document set `doctor` states in `setup-analysis`) | — | E5 | `no-change` | The sweep document is not a member of the conventions document set (Task 7), so the derivation stated there is unchanged. |
| 34 | `cli/templates/claude/CLAUDE.md` → `## Where a change request runs`, the closing paragraph naming `.claude/devscene-task-offer.md` | — | E4 | `no-change` | It describes the offer only. |
| 13 | `docs/guard-verification.md` ("`task-offer-check.sh` joined the guard's left-allowed set") | — | E3 | `no-change` | The guard's code and lists are unchanged, and the new script reaches the same non-denied arm as every other agent-invocable script, so nothing needs re-measuring. |
| 14 | `docs/watcher.md` → the outer-loop script table | — | E3 | `change` | Task 9 |
| 15 | `plugin/hooks/README.md` → `## The deny list` | — | E3 | `no-change` | `review-sweep.sh` is agent-invocable and joins no deny list. |
| 16 | `ARCHITECTURE.md` → the "The adopter's `.claude/` namespace" row (`TASK_OFFER_PATH`, and its prose list of what `init` writes inside the directory) | — | E4, E10 | `change` | Task 10: `REVIEW_SWEEP_PATH` joins the constants, and the review-sweep document joins the prose list. The row's citation of `docs/analyze.md` `## 3. What it may write` for the `.claude/` wall stays true. |
| 17 | `ARCHITECTURE.md` → item 9, "Load an adopter's root context document" | — | E4 | `no-change` | It is about the always-loaded file. The sweep document is read only by one agent's own contract. |
| 18 | `README.md` → the change-request offer paragraph | — | E4 | `no-change` | It describes the offer only. |
| 19 | `cli/templates/claude/CLAUDE.md` → `## Context files (read on demand)` ("One read-on-demand document is deliberately not in that table") | — | E4 | `no-change` | The routing table omits the sweep document on purpose (goal 1). The sentence names a document a session reads on demand, which the sweep document is not. |
| 20 | `cli/templates/claude/README.md` → the opening paragraph | — | E4 | `change` | Task 1 |
| 21 | `docs/development.md` → the self-adoption re-render record (the bullet opening "`.claude/devscene-task-offer.md`, `.claude/push-notify.env.example`"), the command-spelling gate paragraph opening "A fourth command checks that every slash spelling", and the roadmap's row 15 | — | E4, E5 | `no-change` | The re-render bullet is a dated record of one `init` run at a named commit. The command-spelling paragraph cites the task-offer template only as where an agent invokes a command through `Skill`. Roadmap row 15 is the legend's shipped-status line. None of these three passages enumerates what `init` writes, what `/devscene:analyze` writes or which checks `doctor` must pass. Gate 8's pass criteria do, and they are row 35. |
| 22 | `docs/remote-execution.md` ("The task offer — checked, unchanged.") | — | E4 | `no-change` | A dated check of the offer only. |
| 23 | `docs/analyze.md` → ``## 7. `doctor`'s share`` | — | E5 | `change` | Task 10 |
| 24 | `plugin/commands/analyze.md` → `## Steps` step 6 (next action `npx devscene doctor`) and step 4 | — | E5 | `change` | Task 7 |
| 25 | `plugin/instructions/main_repo_resolution.md` → `## Who may cite this` ("no document beyond these 27") | — | E7 | `change` | Task 8 |
| 26 | `.claude/context/conventions.md` → `## Shell assets` ("A command an unattended run issues must be spellable as a literal") | — | E8 | `no-change` | A conventions document is never a plannable target. Task 8 adds a fifth main-checkout script call, which that bullet's enumeration does not list; recorded in `corpus_staleness`. |
| 35 | `docs/development.md` → Gate 8, the paragraph opening "Pass criteria, invariants of the output rather than judgements of it" | — | E4, E5 | `change` | Task 10: a no-argument `/analyze` now ends with the `sweep` target (Task 7), so the criteria name `.claude/review-sweep.md` as filled, and `doctor`'s `PASS review-sweep` (Task 4) joins `PASS setup-analysis` and `PASS layer-profile`. |
| 36 | `docs/analyze.md` → `## 3. What it may write`, the opening sentence ("The conventions documents and `.claude/CLAUDE.md` are the command's to write") | — | E10 | `change` | Task 10: the review-sweep document joins the command's write set (Task 7). |
| 37 | `docs/analyze.md` → `## 3.`, the paragraph opening "Any write under a repository's own `.claude/` tree is a supervised action" | — | E10 | `change` | Task 10: "the conventions documents it fills live there" names the sweep document beside them. The closing advice to check that the conventions documents changed stays, because the same wall refuses every write under `.claude/`, so a run that wrote none of them wrote no sweep document either. |
| 38 | `README.md` → the bullet opening "Any write under a repository's own `.claude/` tree is a supervised action." | — | E10 | `no-change` | It states the wall and the check that detects it, and points at `docs/analyze.md` §3 for the write set. Checking the conventions documents detects the wall for every `.claude/` write, the sweep document included, and the bullet enumerates no write set of its own. |
| 39 | `plugin/agents/conventions-writer.md` → `## Scope` ("You write one file, `document_path`, and no other.") | — | E10 | `no-change` | Task 5's reason: on `target: sweep`, `document_path` is the sweep document, so the dispatch still writes exactly one file. |
| 40 | `docs/config.md` → the `stateDir` paragraph opening "It must not be a dot-directory." | — | E10 | `no-change` | It cites `docs/analyze.md` §3 only for the measured `.claude/**` wall, which this branch does not change. It states nothing about what the command writes. |
| 41 | `docs/github-integration-research.md` → the paragraph opening "Consequence:" (citing `docs/analyze.md` → `## 3. What it may write`) | — | E10 | `no-change` | A dated research measurement of the wall on a named version. A document of record is not edited to track later behaviour. |
