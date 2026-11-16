### 2. The return-contract module and this branch's agent prose spend tokens on authoring rules and restatement their runtime readers never act on

**File:** `plugin/instructions/agent_return_contract.md` → `## The return block` / `## The return schema` / `## Return fields` / `## Citing a field` / `## Adopting it for another agent` / `## Who may cite this` (the authoring sections), beside `## Reading a return` and `## A return that fails the check` (the runtime sections). Second site: the `## Output contract` of each of the six planning agents, for example `plugin/agents/ui-tests-plan-writer.md` → `## Output contract`: "An augment that wrote or revised files before stopping carries `ui_test_index`, `ui_test_files_dir` and `tests_count` as well."

**Depends on:** Finding 1. Apply it first, because it rewrites the same module sections and the same `### Return fields` subsections.

**Problem.** Verified in the current tree, and measured as the user asked: word and character counts per file and per section, taken with `wc -w -c` on the file or on a `sed -n '<a>,<b>p'` range of it. Branch base `d953d476` is `git merge-base HEAD origin/dev`.

**The branch's growth.** The six agent definitions measured 27,221 words at the base and 29,073 now, so **+1,852**, and 1,391 of those are the `## Return schema` blocks Finding 1 removes. The orchestrator-side files grew as follows:

| File | Base words | Now | Delta |
|---|---|---|---|
| `plugin/instructions/agent_return_contract.md` (new) | 0 | 847 (5,666 chars) | +847 |
| `plugin/instructions/plan_orchestration_instructions_core.md` | 18,649 | 18,860 | +211 |
| `plugin/instructions/task_plan_writing_instructions_core.md` | 6,422 | 6,543 | +121 |
| `plugin/instructions/task_plan_writing_instructions_autonomous.md` | 10,320 | 10,403 | +83 |
| `plugin/instructions/user_review_fixes_instructions_core.md` | 8,766 | 8,833 | +67 |
| `plugin/instructions/plan_review_rounds.md` (read by the agents) | 1,296 | 1,302 | +6 |

**Who reads `agent_return_contract.md`.** No agent does. The six agents carry the canonical sentence and do not point at the module. Its runtime reader is the orchestrating session, through 15 citations: `plan_orchestration_instructions_core.md` (6), `user_review_fix_plan_writing_instructions_core.md` (3), `task_plan_writing_instructions_core.md` (2), `user_review_fixes_instructions_core.md` (2) and `qa_test_instructions.md` (2). Every citation names `## Reading a return` or `## A return that fails the check`, and nothing else. Its sections measure:

| Section | Words / chars | Who acts on it |
|---|---|---|
| title + `## Resolved values` | 53 / 303 | orchestrator (header) |
| `## The return block`, `## The return schema`, `## Return fields`, `## Citing a field` | 393 / 2,584 | agent authors and the static suite only |
| `## Reading a return` + `## A return that fails the check` | 201 / 1,289 | orchestrator |
| … of which the two driver sentences ("The driver applies the agent's full …"; "The driver's bound is the same three attempts …") | ~44 | nobody at run time: rationale |
| `## Adopting it for another agent` | 102 / 585 | agent authors only |
| `## Who may cite this` | 98 / 905 | the suite's roster check; its closing paragraph (67 words) is an authoring rule |

**The options, measured.**
- **Thin module (chosen).** Keep the header, the two runtime sections without the driver sentences, and the roster list with a one-sentence rule. Projected about **255 words / ~1,900 chars**, down from 847 / 5,666. That saves about 590 words on every orchestrator session that follows a citation.
- **Inline at call sites.** About 160 words of runtime rule copied into each of the five citing files: about 800 words across the tree, and about 320 on an autonomous planning session, which reads both `task_plan_writing_instructions_core.md` and `plan_orchestration_instructions_core.md`. That is larger than the thin module on that session. It also makes five owners of one rule, which `.claude/context/plugin.md` → `## Cores, forks and the single-owner rule` (rule 5) forbids.

**Agent prose.** On top of the schema, the six agents' `## Output contract` sections state which outcome carries which field twice: once in sentences and once in `### Return fields` (778 words in total, 385 of them in `task-plan-writer`). Examples verified in the tree:
- `task-plan-writer`: "Return `returned` after writing or revising the plan." / "Return `questions` when …" / "Return `blocker` …", beside "`outcome` — `returned`, `questions` or `blocker`."
- `ui-tests-plan-writer`: "An augment that wrote or revised files before stopping carries `ui_test_index`, `ui_test_files_dir` and `tests_count` as well.", beside three bullets that each say "and `questions` after an augment wrote files".
- `architecture-reviewer` `### Plan-review mode (a) and (b) PASS` / `### Clean review (both modes)` / `### Sub-case (c) advisory PASS`, and `business-parity-reviewer` `### Plan-review mode PASS` / `### Clean review (both modes)`: each ends "return `PASS` with `findings_file`" or "with no `findings_file`", which the `findings_file` bullet already states.
- `ui-tests-plan-reviewer`: "then return `PASS` — still with no other field.", beside "`PASS` carries no other field, whether or not you saved a findings file."
- Four of the six (`task-plan-reviewer`, `architecture-reviewer`, `business-parity-reviewer`, `ui-tests-plan-reviewer`) carry "An optional `## Unsolicited dispatch guidance` section may sit above the return object …". Their byte-identical `## Unsolicited dispatch guidance` block already says to report "above the fenced block".

**Fix.** Apply in this order. Before each edit, re-measure the files it touches with the same commands, because Finding 1 will have moved the agent figures. Then check that the after-figure is lower.

- [ ] **Thin the module.** Trim `plugin/instructions/agent_return_contract.md` to:
  - `## Resolved values`. Drop the `<scripts_dir>` row if no remaining text uses it. A file that declares no token says so in one sentence, because `.claude/context/plugin.md` → `## The sections an asset carries` requires the section.
  - `## Reading a return` and `## A return that fails the check`. Keep both headings byte-for-byte, because 15 plugin citations and `docs/flow-graph-walker.md` cite them. Move "The driver applies the agent's full … run no validator." and "The driver's bound is the same three attempts, taken as its infrastructure class." out to `docs/structured-agent-returns.md`.
  - `## Who may cite this`. Keep the list unchanged, because `checkRoster` reads it. Cut the closing paragraph to the one rule the citers follow ("A citer points and never restates; a new citer joins this list."). Move the remainder (heading-rename duty, the agents not pointing here, outside-plugin citation) to the maintainer document.
- [ ] **Move the authoring rules to the maintainer document.** Move `## The return block` (with its fenced canonical sentence), `## The return schema` (the dialect), `## Return fields`, `## Citing a field` and `## Adopting it for another agent` into `docs/structured-agent-returns.md`. Put them in one new section such as `## 2. Authoring an agent's return`, with `###` subsections carrying those five names, and fold the current `## 2. Adopting it for another agent` into it. In the same document:
  - Rewrite the `**What it owns.**` paragraph. The document now owns the authoring rules, and the plugin module owns only the routing check and the failed-return route.
  - Update every `agent_return_contract.md` → `## …` citation in the document that points at a moved section.
- [ ] **Repoint the suite and the driver comments.** In `cli/test/agent-return-schemas.test.mjs`:
  - `canonicalSentence` reads the first fenced block of `docs/structured-agent-returns.md` → `### The return block`.
  - `roster` still reads `plugin/instructions/agent_return_contract.md` → `## Who may cite this`.
  - Update the header comment ("The dialect, the sentence and the roster are read from `plugin/instructions/agent_return_contract.md`").
  - Add a `devscene.config.json` → `treeGuards` entry `{ "test": "test/agent-return-schemas.test.mjs", "covers": "docs/structured-agent-returns.md" }`, so an edit to the sentence's new home triggers the suite.

  Then repoint the `cli/templates/scripts/lib/planning-node-lib.sh` comment naming `agent_return_contract.md` → `## The return schema` to the dialect's new home. Update the `plugin/docs/AUTONOMOUS_FLOW.md` row "What an agent's return object is, its schema dialect, and how a caller checks it" to describe only what the module still holds.
- [ ] **Make the six agents' `## Output contract` say each thing once.** For each of the six:
  - Fold the "Return `<outcome>` when …" sentences into the `outcome` bullet of `### Return fields` as one `<outcome>` — `<when>` clause each.
  - Delete a field-presence clause from an outcome sentence or a mode subsection when the field's own bullet states it. This covers the `ui-tests-plan-writer` augment sentence, the `findings_file` tails in the two reviewers' mode subsections, and the `ui-tests-plan-reviewer` "still with no other field".
  - Drop the "An optional `## Unsolicited dispatch guidance` section may sit above the return object …" sentence where the agent's `## Unsolicited dispatch guidance` block already places the report above the fenced block. Never edit that block itself: it is copied byte-for-byte across the graded agents and owned by `plugin/instructions/dispatch_discipline_instructions.md`.

  Keep every outcome backticked somewhere in `## Output contract`, because the suite checks this. Keep every definition and edge case the agent acts on, per the lesson ledger's `## Agent prose` rule and `.claude/context/plugin.md` → `## Writing agent prose`. Keep the mode-specific file formats (round-file templates, the split-index spec) unchanged: they are behaviour, not restatement.
- [ ] **Light orchestrator pass, optional.** Per the user's own priority, the orchestrator files need no more than the thin module. Where a citing section repeats the same two citations in consecutive bullets, a shorter wording that keeps the file-and-heading citation is welcome. Do no other rewrite of `plan_orchestration_instructions_core.md`, `task_plan_writing_instructions_core.md`, `user_review_fix_plan_writing_instructions_core.md`, `user_review_fixes_instructions_core.md` or `qa_test_instructions.md`.

**Verification:**
- Run `bash scripts/typecheck.sh`.
- Run the test file this fix edits, through the configured single-file command: `cli/test/agent-return-schemas.test.mjs`.
- `wc -w -c plugin/instructions/agent_return_contract.md` is at or below about 300 words.
- `grep -rn -o -E 'agent_return_contract\.md` → `## [^`]+`' plugin docs cli/templates` names only `## Reading a return`, `## A return that fails the check` or `## Who may cite this`.
- For each of the six agents, `wc -w -c plugin/agents/<agent>.md` is lower than its figure after Finding 1, and no definition grows.
