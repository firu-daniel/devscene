# Story: Structured returns for the conventions writer and reviewer, and `/devscene:analyze` moved onto them

## Context

This branch is the fourth of five that give every plugin agent a declared, schema-validated return. It covers the two agents `/devscene:analyze` dispatches, `conventions-writer` and `conventions-reviewer`. Each gets:

- a schema file `plugin/schemas/<agent>.return.json` in the closed dialect `docs/structured-agent-returns.md` → `### The return schema` lists;
- a `### Return fields` subsection;
- the canonical return-block sentence in its `## Output contract`.

Every caller that reads one of these returns moves onto the citation form `` `<agent>.<field>` `` / `` `<agent>.<field>.<property>` `` and the outcome form "an `outcome` of `written`". The only routing caller is `plugin/commands/analyze.md`. It points at `plugin/instructions/agent_return_contract.md` → `## Reading a return` and `## A return that fails the check`, and joins that module's `## Who may cite this`. The writer's own `## Invocation contract` also reads the reviewer's findings, because `analyze.md` forwards them to it verbatim. That paragraph moves onto the new form too. The mechanism is not re-decided here. The static schema check that `docs/structured-agent-returns.md` → `### Adopting it for another agent` describes picks up each new schema file with no change to the suite.

**The preconditions hold.**

- `docs/structured-agent-returns.md` records all three of `feat_structured_outputs_mechanism`'s decisions:
  - how a session reads an `Agent` result: `## Reading a return` step 1, plus the 2026-11-17 measurement in §3;
  - how a list of multi-part items is represented: `### A list of structured items is an array of objects, one level deep`;
  - what an agent's `error:` return becomes: *An agent's own `error:` return becomes an outcome, never `error`*.
- `agent_return_contract.md` → `## Reading a return` step 4 carries the optional-field rule.
- `harness-runs/lessons.md` carries the rule that an outcome value is one token with no space.

The plan found no point where the record and the task prompt disagree. One reading is stated here. The prompt says `Reviewer finding not applied — ` appears in the writer's *"`findings_declined:` / `not_determined_lines:` return"*. In today's text, only `not_determined_lines` carries the literal: it quotes the document's `## Not determined` lines verbatim. `findings_declined` carries the finding and the reason without the literal. The plan keeps that split.

**The outcomes and fields.** The planning graph dispatches neither agent, so neither is held to graph outcome keys. Every name below is one token. Neither agent returned `error:` before, so no `error` route is renamed. Each agent's existing stop condition becomes outcome `blocker`. On the reviewer, that includes its "caller bug — say so, and stop".

- **`conventions-writer`** (Task 2):
  - `written` and `merged`. These are the old `action_taken:` values, carried over as the outcome, so `action_taken` is folded into `outcome` and is no longer a field. Both outcomes carry the same fields:
    - `document_path`;
    - `not_determined` (integer, at least 0);
    - `not_determined_lines` (array of strings, at least 1, omitted when none);
    - `conflicts` (array of objects, at least 1, omitted when none). Items: `prose` and `code`;
    - `shared_document_divergences` (array of objects, **required**, `[]` when none). Items: `shared_document_says`, `code_shows` and `source`;
    - `findings_applied` (integer, at least 0). Fix dispatches only, omitted on a write dispatch. That replaces `n/a`;
    - `findings_declined` (array of objects, at least 1, omitted when none). Items: `finding` and `reason`;
    - `evidence`;
    - `prior_document` (`enum` `skeleton` / `filled` / `absent`);
    - `prior_prompts`;
    - `prior_rule_block`;
    - `notes` (optional).
  - `blocker`, with `blocker`.
- **`conventions-reviewer`** (Task 1):
  - `document_reviewed`, with `document_path`, `findings` and `summary`;
  - `corpus_reviewed`, with `findings` and `summary`;
  - `blocker`, with `blocker`.

  The outcome names the axis that was reviewed, not a judgement, so the reviewer's *"No severity band and no verdict field"* rule still holds. An axis-named outcome also lets the routing check's step 3 refuse a corpus return to a document dispatch. `findings` is an array of objects, at least 1, omitted when none. That replaces `findings: none`. Its items differ by axis:
  - on `document_reviewed`: `claim`, `evidence` and `correction`;
  - on `corpus_reviewed`: `document_path` and `check_id` (`C1`–`C6`, or a document-pass check number), then `claim`, `evidence` and `correction`.

**Three representation choices, each written into the decision record by Task 3.**

- **The three `prior_*` fields stay strings.** `prior_prompts` and `prior_rule_block` keep their verbatim text and their `none` / `n/a` values, and `prior_document` becomes an `enum`. These three are opaque values. The writer returns them, `analyze.md` forwards them unchanged into the review and fix dispatches, and the writer re-emits them *"exactly as the dispatch handed them"*. The receiving tables already define their `none` and `n/a` values (`conventions-reviewer.md` → `## Invocation contract`; `conventions-writer.md` → the fix-dispatch paragraphs). No caller parses or routes on their lines. A string round-trips byte for byte. Re-shaping one into an array would change both receiving tables and reviewer checks (1) and (2) for nothing a caller reads.
- **The multi-part lists become arrays of objects**, per the record's rule. These are the reviewer's `findings`, and the writer's `conflicts`, `shared_document_divergences` and `findings_declined`. `not_determined_lines` is a list of verbatim one-part lines, so it is an array of strings.
- **`shared_document_divergences` is the one list that is always emitted.** Its schema `required`s it with no `minItems`, and `[]` means none. The writer's prose says so, and the static check holds that prose to the schema. `analyze.md` names it as optional for the routing check: under `## Reading a return` step 4, `[]` would otherwise fail as empty. Today's writer sentence *"an omitted field is what the caller's stop condition fires on"* names a caller stop that `analyze.md` does not state. A grep of `analyze.md` for "omitted" finds the dispatch-side `shared_document` rule and step 5's rationale rule, and no rule about an omitted return field. Task 2 rewords that sentence to the schema fact, and Task 3 records the choice.

**How the work is split, and who owns which sentences.** The constraint *"No caller is left reading a field its agent no longer returns, at the end of any task"* means each agent's schema, its definition and every reader of its return change in one task. That follows the precedent of `feat_structured_outputs_branch_review`. The reviewer goes first, because the writer reads the reviewer's findings. Two files are shared, sentence by sentence. Each task file names its own sentences, and no task edits a sentence another task owns.

- **`plugin/agents/conventions-writer.md`:**
  - Task 1 owns `## Invocation contract`'s two corpus-axis `findings` origin bullets (*"**Corpus review findings** — …"*, *"**Forwarded layer-writer divergences** — …"*) and the paragraph *"**The prefix is the discriminator.** …"*.
  - Task 2 owns every other sentence that changes.
- **`plugin/commands/analyze.md`:**
  - Task 1 owns the module pointer for the reviewer's returns, added to (4c) and covering both axes. It also owns (4c)'s *"Take the reviewer's `findings:` return. …"* sentence, (4d) iteration 1's *"Take its `findings:` and group them by the `document_path` each names:"*, and iteration 2's *"when iteration 1 returned `findings: none`"* clause.
  - Task 2 owns the writer-return pointer and every sentence that reads a writer field: (4a)'s *"Keep every `shared_document_divergences:` line …"* paragraph; (4c)'s *"… taken verbatim from that document's write return …"* clause; (4d.0); iteration 1's corpus-fix-return clause; iteration 2's *"… whose fix return reports at least one finding applied"* clause; step 2's *"`evidence:` clause"* spelling; and step 6.
- `agent_return_contract.md` → `## Who may cite this` is Task 1's alone, because `analyze.md` first names the module in Task 1.

**What stays as it is.**

- The documents the writer writes are file content. That includes their `## Not determined` lines and every `Reviewer finding not applied — ` line in them.
- The dispatch argument tables of both agents are unchanged. That covers the `prior_*` rows and the `Layer-writer divergence — ` prefix.
- `plugin/instructions/mention_reading.md` quotes *"Field names byte-stable"* from the writer's `## Output contract`, and so does `.claude/context/plugin.md`. Task 2 keeps that phrase, so both quotes stay true.
- No script reads either return, so no script changes.
- No permission, configuration key or measured fact is added. The change relies on nothing about an `Agent` result that `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` does not already record.
- Per the ledger's breaking-rename rule, no caller keeps a fallback that reads the old `key: value` form.

**Top risks:**

- **A read site in `analyze.md` left on the old prose form.** That 513-line command quotes the writer's fields across steps 2, 4 and 6. Tasks 1 and 2 each re-derive their agent's old field spellings by grep across `plugin/`. Each requires no hit outside the agent's own dispatch tables, and the `## Scope register` below closes the site set.
- **`Reviewer finding not applied — ` drifting between its three carriers.** Task 2 rewrites the writer's return prose around it, and its `Verification:` checks the literal byte-identical in all three files, in the same roles.
- **An object finding the writer cannot tell from a forwarded divergence.** Task 1 restates the discriminator as *an object carrying `check_id`* versus *a line carrying the `Layer-writer divergence — ` prefix*. Task 2's (4d.0) rendering of each divergence is held to the prefix rule that paragraph states.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom. The commit step flips each one to `[x]` as that task's commit lands.

- **Only the committing role flips a marker.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. No implementer changes a marker here, or edits any other line of this section, while a run is iterating this index.
- `[ ]` markers anywhere else, such as sub-step bullets in the per-task files, are informational only. The commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_structured_outputs_setup/task_<K>_plan.md`. They are ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Give `conventions-reviewer` a schema-validated return and move its readers in `analyze.md` and the writer's invocation contract onto it _(layer: plugin)_ _(points: 20)_
2. [ ] **Task 2** — Give `conventions-writer` a schema-validated return and move every read of it in `analyze.md` onto it _(layer: plugin)_ _(points: 20)_
3. [ ] **Task 3** — Record the conventions pair's outcomes and field shapes in the decision record and update `docs/analyze.md` _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`harness-runs/task_prompts/feat_structured_outputs_setup_task_prompt.md` → `## The goal`, item 2): *"`analyze.md` and every other caller read the new objects. No caller parses these returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`."*

**Derivation entry C1 — corpus files naming either agent (command).** Re-run verbatim from the checkout root:
`git grep -lE 'conventions-(writer|reviewer)' -- '*.md' '*.txt' ':(exclude)harness-runs/*'`

**Derivation entry C2 — corpus files carrying one of the two agents' old return spellings, or the writer's quoted wire phrase (command).** Re-run verbatim from the checkout root:
`git grep -lE 'action_taken|not_determined_lines|shared_document_divergences|findings_applied|findings_declined|prior_document|prior_prompts|prior_rule_block|findings: none|Field names byte-stable' -- '*.md' '*.txt' ':(exclude)harness-runs/*'`

**Derivation entry C3 — corpus files carrying the cross-file wire literal (command).** Re-run verbatim from the checkout root:
`git grep -lF 'Reviewer finding not applied' -- '*.md' '*.txt' ':(exclude)harness-runs/*'`

**What the three command entries cover.**

- They cover every Markdown and text file in the tree: the plugin, `docs/`, the root prose documents, the conventions documents and `examples/`.
- They leave out `harness-runs/`. That tree holds past runs' artifacts. Its one standing artifact a rule could bind this plan through, the lessons ledger, is reached by P2.
- They leave out shell and TypeScript source and its comments, which are not corpus text. `git grep -lE 'conventions-(writer|reviewer)' -- cli/src cli/templates/scripts` finds only `cli/src/generators/claudeContext.ts`, whose doc comment names the writer composing a document. Nothing in it reads a return.

**Derivation entry P1 — the files the task prompt names (procedure).**

- **Artifact:** the task prompt `harness-runs/task_prompts/feat_structured_outputs_setup_task_prompt.md`.
- **Traversal:** its sections in file order — the opening paragraphs, `## Why`, `## Scope: the agents and their current returns`, `## The goal`, `## Constraints` — and, within each, every backticked repository path in order of appearance. The pattern `plugin/schemas/<agent>.return.json` is expanded once for each of the two agents the opening paragraph names.
- **Decision rule:** a path is reached when it names durable corpus text: a plugin file, a document under `docs/`, a root prose document or a schema file. A path to a script or a test is not reached.

**Derivation entry P2 — standing-artifact rows (procedure).**

- **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`.
- **Artifact:** the lessons ledger.
- **Traversal:** its topic headings in file order, then the one-line rules under each.
- **Decision rule:** a rule is reached when it sits under `## Agent prose`, or names a rename, an agent's return, an outcome or a shared instruction module.

**Closure invariant:** every site any of the five entries reaches appears as a row below. A site two entries reach is one row, and its `Evidence` cell names every entry that reached it.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/schemas/conventions-reviewer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 1 |
| 2 | `plugin/agents/conventions-reviewer.md` | — | C1, C2 (`prior_prompts`, `prior_rule_block`, `prior_document`, `findings: none`), C3, P1 | `change` | Task 1 (`## Invocation contract`'s stop condition and dispatch-count paragraph; `## The corpus pass — what to verify` (c) and its closing `findings: none` paragraph; `## Output contract`). Its `prior_*` dispatch rows and check (11)'s literal are unchanged |
| 3 | `plugin/agents/conventions-writer.md` | — | C1, C2 (every writer field, `Field names byte-stable`), C3, P1 | `change` | Task 1 (`## Invocation contract`'s corpus-axis `findings` origin bullets and *"The prefix is the discriminator"* paragraph), Task 2 (every other changed sentence: the stop condition, `## Scope`'s `evidence:` reference, `## The document`'s count bullet and divergence paragraph, the absent-document paragraph, `## The fix dispatch`, `## Output contract`) |
| 4 | `plugin/commands/analyze.md` | — | C1, C2, C3, P1 | `change` | Task 1 ((4c)'s reviewer-return pointer and *"Take the reviewer's `findings:` return"* sentence; (4d) iteration 1's grouping sentence; iteration 2's `findings: none` clause), Task 2 ((4a)'s writer-return pointer and *"Keep every `shared_document_divergences:` line"* paragraph; (4c)'s `prior_*` clause; (4d.0); iteration 1's corpus-fix-return clause; iteration 2's findings-applied clause; step 2's `evidence:` spelling; step 6) |
| 5 | `plugin/instructions/agent_return_contract.md` → `## Who may cite this` | — | P1, `## Why` | `change` | Task 1 adds `${CLAUDE_PLUGIN_ROOT}/commands/analyze.md` |
| 6 | `docs/structured-agent-returns.md` | — | P1, `## Why` and `## Constraints` | `change` | Task 3 records the pair's outcomes, the `prior_*` string choice and the always-emitted list. It adds no `## 3.` entry: the change relies on no unrecorded measurement |
| 7 | `docs/analyze.md` → `## 8. How this is verified`, item 2 | — | C1, C2 (`shared_document_divergences:`), C3 | `change` | Task 3 re-spells item 2's `shared_document_divergences:` / `none` clause in the new form, and rewrites its *"whose omission the caller's stop condition is what catches"* clause, which this branch makes false: the schema `required`s the field and `analyze.md`'s routing check reads it as optional, so no caller stop catches an omission. §6's *"four sites"* sentence, §11 and §12 cite dispatch tables and the literal, which are unchanged |
| 8 | `plugin/instructions/mention_reading.md` → *"The return-wire rules this return answers to."* | — | C1, C2 (`Field names byte-stable`) | `no-change` | It quotes *"Field names byte-stable"* from the writer's `## Output contract`. Task 2 keeps that phrase verbatim, and its `Verification:` checks it |
| 9 | `plugin/instructions/dispatch_discipline_instructions.md` → the receiving-side exclusions paragraph | — | C1 | `no-change` | It explains why `conventions-reviewer` is off the backstop roster. It reads no return |
| 10 | `.claude/context/plugin.md` | — | C1, C2 (`Field names byte-stable`) | `no-change` | A conventions document, never a plannable target. Its quotes of the writer's *"Field names byte-stable"* and of the reviewer's *"that omission is deliberate …"* stay true after Tasks 1 and 2. Its `## Wires` statement of the declared-object return already describes the new form, so no `stale-rule` entry is owed |
| 11 | `.claude/CLAUDE.md` | — | C1, C3 | `no-change` | It names the literal and the three files that carry it. Goal 3 keeps that true. It sits under `.claude/`, which no run may write |
| 12 | `ARCHITECTURE.md` → item 9 | — | C1 | `no-change` | It names the writer while discussing the root context document. It reads no return |
| 13 | `docs/development.md` → Gate 8 | — | C1, C3 | `no-change` | It counts the literal in written documents, which are file content. Its `C1`–`C6` check ids survive as `conventions-reviewer.findings.check_id` values |
| 14 | `docs/retrieval-eval-results.md` | — | C1 | `no-change` | A measured record. It names research documents' paths |
| 15 | `docs/work-report-research/README.md` | — | C1 | `no-change` | A research record of a past study. It names these agents as subjects and routes nothing |
| 16 | `docs/work-report-research/_brief.md` | — | C3 | `no-change` | as row 15 |
| 17 | `docs/work-report-research/conventions-reviewer.md` | — | C1, C2, C3 | `no-change` | as row 15 |
| 18 | `docs/work-report-research/conventions-writer.md` | — | C1, C2, C3 | `no-change` | as row 15 |
| 19 | `docs/work-report-research/layer-implementer.md` | — | C1 | `no-change` | as row 15 |
| 20 | `docs/work-report-research/task-plan-writer.md` | — | C1 | `no-change` | as row 15 |
| 21 | `docs/work-report-research/reviews/conventions-reviewer.md` | — | C1 | `no-change` | as row 15 |
| 22 | `docs/work-report-research/reviews/conventions-writer.md` | — | C1, C2, C3 | `no-change` | as row 15 |
| 23 | `docs/work-report-research/reviews/layer-implementer.md` | — | C1 | `no-change` | as row 15 |
| 24 | `docs/work-report-research/reviews/task-plan-writer.md` | — | C1 | `no-change` | as row 15 |
| 25 | `examples/notes-app/README.md` | — | C3 | `no-change` | It greps the literal in the frozen capture's documents. Those are file content, and the capture is frozen |
| 26 | `ROADMAP.md` → the `Structured agent outputs` row | — | P1, `## Why` | `no-change` | The row stays open until the fifth branch of the series lands |
| 27 | `harness-runs/lessons.md` → *"A rename declared breaking ships no compatibility path …"* | — | P2, names a rename | `no-change` | It binds Tasks 1 and 2: no caller keeps a fallback that reads the old `key: value` form or `action_taken` |
| 28 | `harness-runs/lessons.md` → *"State a new behaviour once, in the section that decides it, and cite it from everywhere else …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan. Each agent's return is read under one pointer in `analyze.md` — the reviewer's in (4c), the writer's in (4a) — and every other read site cites a field without restating the check |
| 29 | `harness-runs/lessons.md` → *"When an agent definition has to give back words to hold its word count, cut restatement or rationale …"* | — | P2, `## Agent prose` | `no-change` | It binds Tasks 1 and 2's agent edits: no definition or edge case is dropped |
| 30 | `harness-runs/lessons.md` → *"Keep a machine-read contract the model never acts on … in a plugin file outside the agent definition …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan: each schema lives in `plugin/schemas/`, never in a definition |
| 31 | `harness-runs/lessons.md` → *"A shared instruction module carries only what its runtime reader acts on …"* | — | P2, `## Agent prose` | `no-change` | Task 1 adds one roster line to `agent_return_contract.md` and nothing else |
| 32 | `harness-runs/lessons.md` → *"A value a script or graph may route on (an outcome, a key, an id) is one token with no space …"* | — | P2, `## Agent prose`, names an outcome | `no-change` | It binds every outcome this plan names: `written`, `merged`, `document_reviewed`, `corpus_reviewed`, `blocker` |
| 33 | `harness-runs/lessons.md` → `## Adopter-facing documentation` → *"Name an adopter-facing surface with the term adopters already arrive with …"* | — | P2, names a rename | `no-change` | This branch renames no adopter-facing surface. Both returns are read by the plugin's own command session |
| 34 | `harness-runs/lessons.md` → `## Evidence and measurement` → *"A decision rule's outcome is a proposal to the maintainer, not a settled future …"* | — | P2, names an outcome | `no-change` | This branch makes no measurement and records no verdict. Task 3 records decisions of record the task prompt asks for |
| 35 | `harness-runs/lessons.md` → `## Evidence and measurement` → *"Grade a write probe on what reached the disk … an outcome of its own …"* | — | P2, names an outcome | `no-change` | This branch writes and grades no probe |
| 36 | `plugin/schemas/conventions-writer.return.json` (new) | — | P1, `## Why` / `## The goal` item 1 | `change` | Task 2 |
