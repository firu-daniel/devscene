### Task 6 — Read the six returns through the routing check in `task_plan_writing_instructions_core.md`

**Goal:** Make the planning core — the orchestrator path of the planning graph, in every mode that runs it — read each of the six agents' return objects through `plugin/instructions/agent_return_contract.md` → `## Reading a return`, pass the walker the object's `outcome`, and name every field it reads in the citation form `` `<agent>.<field>` ``.

**Depends on:** Task 1 (`## Reading a return`, `## A return that fails the check`, `## Citing a field`), and Tasks 2–5, which declare the fields this file reads. The exact contract this task consumes:

- **Every planning node's `outcome` value is its walker outcome.** `task-plan-writer`: `returned`, `questions`, `blocker`. `ui-tests-plan-writer`: `returned`, `no_ui`, `questions`, `blocker`. `business-parity-reviewer`, `architecture-reviewer`, `task-plan-reviewer`, `ui-tests-plan-reviewer`: `PASS`, `FAIL`, `blocker`. `error` is never returned by an agent: the core passes it after a third failed check.
- **Fields read here:** `` `task-plan-writer.questions` ``, `` `task-plan-writer.story_file` ``, `` `task-plan-writer.task_files_dir` ``, `` `task-plan-writer.tasks_count` ``, `` `task-plan-writer.parity_exclusions` `` (optional, parity on only); `` `ui-tests-plan-writer.questions` ``, `` `ui-tests-plan-writer.ui_test_index` ``, `` `ui-tests-plan-writer.ui_test_files_dir` ``, `` `ui-tests-plan-writer.tests_count` ``, `` `ui-tests-plan-writer.reason` ``; `` `business-parity-reviewer.findings_file` ``, `` `architecture-reviewer.findings_file` ``, `` `task-plan-reviewer.findings_file` `` (on `PASS` and `FAIL`); `` `ui-tests-plan-reviewer.findings_file` `` (on `FAIL`); the `blocker` field of whichever agent returned that outcome.

**Where this task stops.** The forks' binding values that name these returns (`<ask>`, `<escalate>`, `<terminal_handoff>`) are Task 7's. The driver reads the same returns on the script-driven path (Tasks 10–11); this file's opening note on what `planning-node-lib.sh` keys on stays true and unchanged.

### Targets

- `plugin/instructions/task_plan_writing_instructions_core.md`

**Work:**

- [ ] `## The walker — routing is its, judgement is yours` → **`<outcome>`, from the agent's return:** replace the table with: read the return as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states; `--outcome` is the return object's `outcome`, and `answered` for an answer that came back through `<ask>`; a return that fails the check takes **A dispatch that did not return** below and, on its third consecutive failure for the same node, is passed as `--outcome error` (`## A return that fails the check`). Drop the "first row whose left cell the return matches" sentence — a writer with questions now returns the `questions` outcome. Rewrite the `--findings` sentence to name the three plan gates' `findings_file` and `` `ui-tests-plan-reviewer.findings_file` `` in the citation form. In **A dispatch that did not return**, add that a return failing the check is handled the same way, bounded as above.
- [ ] `## Loop` → `### 1. Spawn \`task-plan-writer\``: the prose after the two dispatch blocks — the writer's return fields to note for the hand-off, `` `task-plan-writer.parity_exclusions` `` in place of the `## Parity exclusions / deferrals` section, and the questions routed verbatim through `<ask>` as `` `task-plan-writer.questions` `` items, with the answers appended between the markers as today. `### 5. Parse the reviewer's return`: each gate's `outcome` with its `findings_file`.
- [ ] `## UI-test-plan write loop`: `### 1. Spawn \`ui-tests-plan-writer\`` — the return fields noted for the hand-off, the **No-UI short-circuit** on an `outcome` of `no_ui` (with `` `ui-tests-plan-writer.reason` ``), and the questions; `### 3. Parse the reviewer's return`. Leave the run-mode-skip paragraph's provenance rule as it is.
- [ ] `## Convergence` (each fact taken from the writer's return field, in the citation form) and `## Stop conditions` (entry 3: a writer's `questions` outcome; entries 5 and 6: a `blocker` outcome — a writer's escalates at once, a gate's is passed to the walker as today — and a return failing the check three times, passed as `error`).
- [ ] Keep the wire text `<scripts_dir>/lib/planning-node-lib.sh` keys on byte-stable: the `## Setup (once per session)` heading and its `MAX_TOTAL_DISPATCHES = ` line, the `## Loop` and `## UI-test-plan write loop` headings, each `###` heading under them that carries a dispatch block, and the **fence count** under each of those headings — add no fenced block under any of them and remove none (the file's own opening note). Add no field name outside the citation form.

**Verification:**

- `git grep -nE 'verdict: (PASS|FAIL)|no_ui: true|## Questions|## Parity exclusions|error:' -- plugin/instructions/task_plan_writing_instructions_core.md` prints no line that routes on or reads a retired form of the six returns.
- Every `` `<agent>.<field>` `` citation in the file names a property the story index `## Context` field table lists for that agent.
- `git grep -n 'agent_return_contract' -- plugin/instructions/task_plan_writing_instructions_core.md` shows the pointer at `## Reading a return`, and the core is a roster member of that module's `## Who may cite this`.
- Under each of the six `###` dispatch headings in `## Loop` and `## UI-test-plan write loop`, the count of lines opening with three backticks is what it was before this task (`git diff` adds or removes no fence line there).
