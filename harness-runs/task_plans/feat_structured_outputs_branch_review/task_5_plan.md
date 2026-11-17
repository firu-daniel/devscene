### Task 5 — Give `statistics-plan-writer` a schema-validated return with a non-halting `not_written` outcome and move every statistics dispatch onto it

**Goal:** `statistics-plan-writer` replaces its fenced seven-line count block and its `error:` line with one fenced `json` return object declared in `plugin/schemas/statistics-plan-writer.return.json`. Every one of its five dispatch sites moves onto that object and keeps a failed write **non-halting** — the task prompt's goal 3. That covers the plan and user-review orchestration cores' `### D.1`, the supervised code review's clean-pass step, and the two supervised fix flows' Phase 3. So do every sentence that compares another skipped write with the old `error:` route.

**Depends on:** Task 4, and through it Tasks 1–3. This task shares files with them and edits only the sentences listed under `### Targets`.

- Task 2 added `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_instructions.md` to `plugin/instructions/agent_return_contract.md` → `## Who may cite this`, and gave that file its module pointer in `## Flow` step 3. This task adds only the step-6.2 reading rule to it.
- Task 4 reworded `plugin/instructions/untrusted_input.md`'s `statistics-plan-writer` row to *"whose return has no field a report can go in"*, which this task's `cause` field keeps true. This task does not edit that file.

**The contract this task defines:**

- An `outcome` of `written` — `statistics.md` was written. Every field below is required:
  - `statistics_file` (string, non-empty): the full path written.
  - `story_points_total`, `issue_cost_total`, `story_plan_tasks`, `user_review_issues` (integers, at least 0).
  - `success_rate` (string, non-empty): the headline rate as a percentage, such as `54.5%`, or `n/a`.
  - `status` (string, `enum` `pre-user-review` / `post-user-review`).
- An `outcome` of `not_written` — a required input was missing or unreadable, and no file was written.
  - `cause` (string, non-empty): one line naming the reason and the missing or unreadable path.

This is the former `error:` return. Per `docs/structured-agent-returns.md` → *An agent's own `error:` return becomes an outcome, never `error`*, a return the caller treats as non-halting becomes *"an outcome of its own, named for the result it reports and never `error` or `blocker`, with its cause in a field"*. This schema has no `blocker` variant, because nothing this agent reports halts a caller.

**How every dispatch site routes the return.** State it at each site, reading as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:

- An `outcome` of `written` → keep or relay `` `statistics-plan-writer.success_rate` `` and `` `statistics-plan-writer.statistics_file` ``. Never open the file to verify.
- An `outcome` of `not_written`, **or** the third consecutive return that fails the check → report `` `statistics-plan-writer.cause` ``, or the check that failed. Omit the statistics line, invent no numbers, and continue. **This is the site's `error` route.** Name it so at each site.

**Why a named route holds.** As the module stands, `## A return that fails the check` defines the `error` route as `--outcome error` where the section passes outcomes to `flow-walker.sh`, otherwise the flow's blocker route. Neither orchestration core runs on `flow-walker.sh` and both bind `<escalate>`, so a site's own sentence alone would be overridden. This task therefore amends that section so a dispatching section that **names** its own `error` route has that route taken, ahead of the `flow-walker.sh` and blocker-route fallbacks. The non-halting outcome then follows from the module's wording, at every site including both cores' `### D.1`. The orchestrating session acts on that sentence at run time, so the amendment is runtime content under `harness-runs/lessons.md`'s shared-module rule.

### Targets

- `plugin/schemas/statistics-plan-writer.return.json` (new).
- `plugin/agents/statistics-plan-writer.md` — the opening paragraph's *"return a terse count block"*, `## Resolved values`' lead paragraph, `## Read first`'s report-don't-substitute paragraph, `## Invocation contract`'s *"How the caller consumes your return."* paragraph, and `## Output contract`.
- `plugin/instructions/plan_orchestration_instructions_core.md` — the `<escalate>` row's sentence *"D.1's `statistics-plan-writer` `error:` is **not** a site …"*, `### D.1`'s *"Parse the agent's contract return …"* paragraph, and `### D.2`'s **Branch statistics** bullet's parenthesis. **No other sentence of this file.**
- `plugin/instructions/user_review_fixes_instructions_core.md` — `### D.1`'s *"Parse the agent's contract return …"* paragraph and `### D.2`'s **Branch statistics** bullet's parenthesis.
- `plugin/instructions/improvement_observations_instructions.md` — the clause *"This mirrors the statistics override's `error:` gate"* and the clause *"Same discipline the statistics bullet uses when D.1 returns `error:`"*.
- `plugin/instructions/plan_orchestration_instructions_autonomous.md`:
  - `### Override D` — its **Trigger / ordering**, **`error:` gate (skip on failed write)** and **Commit mechanism** paragraphs;
  - Override I's *"This mirrors Override D's `error:` gate"* clause;
  - the closed list's entry 5 clause *"the analogue of Override D's `error:` gate"*.

  **No other sentence of this file.**
- `plugin/instructions/user_review_fixes_instructions_autonomous.md` — `### Override D`'s **Trigger / ordering**, **`error:` gate** and **Commit mechanism** paragraphs, and its observations step's *"This mirrors Override D's `error:` gate"* clause.
- `plugin/instructions/code_review_instructions.md` — `## Flow` step 6.2's *"Relay the returned `success_rate` / `statistics_file` to the user."*
- `plugin/instructions/code_review_fixes_instructions.md` — `## Phase 3` step 2's relay sentence.
- `plugin/instructions/user_review_fixes_instructions.md` — `## Phase 3` step 2's relay sentence.
- `plugin/instructions/agent_return_contract.md`:
  - `## A return that fails the check` — its second paragraph's sentence *"After the **third** consecutive failing return for the same dispatch, take the dispatching section's `error` route: …"*;
  - `## Who may cite this` — add `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_fixes_instructions.md` and `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions.md`.

  **No other sentence of this file.** Task 2's roster line for `code_review_instructions.md` stays as Task 2 left it.

**Work:**

- [ ] **The schema.** Write `plugin/schemas/statistics-plan-writer.return.json` in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`.
  - Top level: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `statistics-plan-writer return`, `description`, `type: "object"`, and a `oneOf` of the two variants above, `written` and `not_written`.
  - Every listed field is required on its variant.
  - `minLength: 1` on `statistics_file`, `success_rate` and `cause`; `minimum: 0` on the four integers; `enum: ["pre-user-review", "post-user-review"]` on `status`.
  - No other keyword anywhere.
- [ ] **The definition, `plugin/agents/statistics-plan-writer.md`.**
  - **`## Output contract`.**
    - Replace the two fenced blocks, the seven-line count block and the `error:` line, with the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`: *End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence.*
    - Keep *"and write no file"* for `not_written` and *"Do not paste the file body back."*
    - Add `### Return fields`, the four counts annotated `(integer)`:
      - `outcome` — `written` after writing the file; `not_written` when the story index or any required input is missing or unreadable, and no file was written;
      - `statistics_file` — the full path written;
      - the four counts;
      - `success_rate` — the headline rate as a percentage, or `n/a`;
      - `status` — `pre-user-review` or `post-user-review`, per the invocation;
      - `cause` — `not_written`: one line naming the reason and the missing or unreadable path.
  - **`## Read first`.** *"return the `error:` line of `## Output contract` naming the path and the refusal"* becomes an `outcome` of `not_written` whose `cause` names the path and the refusal. Keep *"and write no file"*.
  - **`## Invocation contract`.** *"How the caller consumes your return."* becomes: the caller routes on your `outcome` and reads your fields without opening the file you wrote. *"**Do not rename a return line.**"* becomes *"**Do not rename a return field.**"*. A `not_written` return is **non-halting**: the caller reports it and continues.
  - **The opening paragraph.** *"return a terse count block"* becomes *"return a short return object"*.
  - **`## Resolved values`.** In the lead paragraph, drop `<full_path>` / `<pct or n/a>` and *"and the return block"* from the placeholder list.
  - Add no other words.
- [ ] **The two orchestration cores' Phase D, and the observations module's two comparisons.**
  - **`plan_orchestration_instructions_core.md` → `### D.1`.** Replace *"Parse the agent's contract return (`statistics_file:` / … / `status:`). Keep … If it returns `error:` … This one is **not** a halt … Do **not** open the written file to verify; the contract line is enough."* with the two routes above, ending on *"This is **not** a halt: the flow continues into D.2 without that bullet."*
  - **That file's `<escalate>` row.** The sentence becomes *"D.1's `statistics-plan-writer` route — an `outcome` of `not_written`, or a third failing return — is **not** a site: it is a non-halting report the flow continues past."*
  - **That file's `### D.2`.** The **Branch statistics** bullet reads *"(omit this bullet if D.1 took its `not_written` route)"*.
  - **`user_review_fixes_instructions_core.md`.** Make the same `### D.1` replacement, ending *"This is **not** a halt: the flow continues into D.2 without that bullet."*, and the same `### D.2` parenthesis.
  - **`improvement_observations_instructions.md`.** *"the statistics override's `error:` gate"* becomes *"the statistics override's `not_written` gate"*; *"when D.1 returns `error:`"* becomes *"when D.1 takes its `not_written` route"*.
  - Both cores are already on the module's roster.
- [ ] **The two autonomous forks' Override D, and every citation of its gate.**
  - In `plan_orchestration_instructions_autonomous.md` and `user_review_fixes_instructions_autonomous.md` alike:
    - **Trigger / ordering:** *"returns its contract (`statistics_file:` / `success_rate:` / `status:` …)"* becomes *"returns its return object"*.
    - **The gate:** the paragraph label *"**`error:` gate (skip on failed write).**"* becomes *"**`not_written` gate (skip on failed write).**"*, and *"If D.1 returned `error:`"* becomes *"If D.1 took its `not_written` route (an `outcome` of `not_written`, or a third failing return — the core's `### D.1`)"*. The rest of the paragraph is unchanged.
    - **Commit mechanism:** *"the path the writer reports as `statistics_file:`"* becomes *"the path the writer reports as `` `statistics-plan-writer.statistics_file` ``"*.
  - Rename the three citations of the gate label to *"`not_written` gate"*: Override I's clause and the closed list's entry 5 in `plan_orchestration_instructions_autonomous.md`, and the observations step's clause in `user_review_fixes_instructions_autonomous.md`.
  - Neither fork names the module: the core's `### D.1` does the check.
- [ ] **The three supervised dispatch sites, and the module's `error`-route sentence and roster.**
  - In `code_review_instructions.md` step 6.2, `code_review_fixes_instructions.md` `## Phase 3` step 2 and `user_review_fixes_instructions.md` `## Phase 3` step 2, replace *"Relay the returned `success_rate` / `statistics_file` to the user."* with the two routes above. Relay on `written`. On `not_written` or a third failing return, tell the user the statistics were not written and why, and stop — the write is the step's last act.
  - **`plugin/instructions/agent_return_contract.md` → `## A return that fails the check`.** The sentence becomes: *"After the **third** consecutive failing return for the same dispatch, take the dispatching section's `error` route: the route that section names as its `error` route, where it names one; otherwise `--outcome error` where that section passes outcomes to `flow-walker.sh`; otherwise the flow's blocker route — `<escalate>` where the flow binds it, else stop and report."* Keep *"Name the agent and the check that failed."* and the section's first paragraph unchanged. The new clause applies to any section that names its own route, and names no agent.
  - **That module's `## Who may cite this`.** `code_review_instructions.md` is already on it (Task 2). Add `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_fixes_instructions.md` and `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions.md`. Add no other line to that module.

**Verification:**

- `jq -e . plugin/schemas/statistics-plan-writer.return.json` exits 0; the `outcome` consts are exactly `written` and `not_written`; and no variant declares `blocker` or `error`.
- `grep -rnE 'statistics_file:|success_rate:|story_plan_tasks:|user_review_issues:' plugin/` has no hit.
- `grep -rnE 'returns? `error:`|returned `error:`|`error:` gate|statistics-plan-writer` `error:`' plugin/` has no hit. Every site it hits before this task is a statistics site; the `qa-tester` sites spell theirs *"an unmarked `error:`"* and *"`error: blocked — `"*, which it does not match.
- `grep -n 'not_written' plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/user_review_fixes_instructions_core.md plugin/instructions/code_review_instructions.md plugin/instructions/code_review_fixes_instructions.md plugin/instructions/user_review_fixes_instructions.md` hits each of the five files. Each hit sits in its statistics dispatch site, which also names that route as the site's `error` route and never `<escalate>`.
- Read `plugin/instructions/agent_return_contract.md` → `## A return that fails the check`: its `error`-route sentence lists, in this order, the route the dispatching section names as its own `error` route, then `--outcome error` for a `flow-walker.sh` section, then the flow's blocker route. `git diff -- plugin/instructions/agent_return_contract.md` shows that sentence and the two roster lines as this task's only changes to the file.
- `grep -l 'agent_return_contract.md' plugin/instructions/code_review_fixes_instructions.md plugin/instructions/user_review_fixes_instructions.md` lists both files, and the module's `## Who may cite this` lists both.
- Every `` `statistics-plan-writer.<field>` `` citation added names a property the schema declares.
