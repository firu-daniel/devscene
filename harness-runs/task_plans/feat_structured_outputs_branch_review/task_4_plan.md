### Task 4 — Give `user-review-fix-plan-writer` a schema-validated return and move the user-review fix-plan flow onto it

**Goal:** `user-review-fix-plan-writer` replaces its fenced `fix_plan_file:` … `invalid:` block, its `## Questions` section, the `fix_plan_file: (pending — questions for user)` sentinel and its `blocker:` line with one fenced `json` return object declared in `plugin/schemas/user-review-fix-plan-writer.return.json`. Every caller moves onto that object: the fix-plan core, its two forks, the supervised command's summary, the untrusted-input module's report table and the task-flow fork's closed list.

**Depends on:** Task 3. That task is the last before this one to edit `plugin/instructions/plan_orchestration_instructions_autonomous.md`; this task edits one other sentence of it, its closed list's entry 13. No file this task edits is otherwise shared with Tasks 1–3.

**The contract this task defines** (no later task changes it):

- An `outcome` of `returned` — the fix plan was written or revised.
  - `fix_plan_file` (string, non-empty): the index path.
  - `fix_plan_dir` (string, non-empty): the per-finding folder, with the round suffix mirrored.
  - `valid_must_fix`, `valid_should_fix`, `valid_nice_to_have`, `invalid` (integers, at least 0).
- An `outcome` of `questions` — an observation needs clarification, or an untrusted-input report is owed. Nothing was written.
  - `questions` (array of strings, `minItems: 1`, items non-empty): routed to the user verbatim and answerable without the plan.
- An `outcome` of `blocker` — `blocker` (string, non-empty): one line naming the unreadable path and the refusal. Neither the index nor any per-finding file was written.

The fix plan's **files** are unchanged: the index, its readiness list, its `## Out of scope / verified-OK` bullets with their ` **Review comments:** ` suffix, the per-finding `**Review comments:** ` line, and `## Source observations`. The lessons-ledger append in `## Process` step 6 is unchanged too.

**How the fix-plan core routes the return** (written by this task, in `## Flow` step 6; steps 8 and 11 already route back through step 6, so step 6 reads every writer return):

- `returned` → go on to the round's gates (steps 7–8).
- `questions` → `<ask>`, with each `` `user-review-fix-plan-writer.questions` `` item verbatim.
- `blocker`, or the third consecutive return that fails the check → `<escalate>`, quoting `` `user-review-fix-plan-writer.blocker` `` or naming the check that failed.

### Targets

- `plugin/schemas/user-review-fix-plan-writer.return.json` (new).
- `plugin/agents/user-review-fix-plan-writer.md` — `## Resolved values`' lead paragraph, `## Invocation contract`'s *"How the caller consumes your return."* paragraph, `## Read on demand`'s report-don't-substitute paragraph, `## Process` step 3's **Needs clarification** bullet and step 5's pull-request-id bullet, and `## Output contract`.
- `plugin/instructions/user_review_fix_plan_writing_instructions_core.md` — the `<escalate>` and `<ask>` rows of `## Mode contract — bindings this file uses`; `## Flow` step 6; the *"no outstanding `## Questions`"* phrases of steps 7 and 8; the *"re-check for `## Questions`"* phrases of steps 8 and 11; and `## Convergence`'s `fix_plan_file` / `fix_plan_dir` / counts bullets.
- `plugin/instructions/user_review_fix_plan_writing_instructions.md` (the supervised fork) — the `<ask>` binding row, step 9's contract-summary sentence, and the *"`## Flow` steps 5 and 6 — … the `## Questions` handling body"* line of its not-redefined list.
- `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` — the opening paragraph's not-restated clause *"the `## Questions` handling (step 6)"*; the `<ask>` binding row; the *"Both bindings resolve to the **same** file-based channel …"* paragraph; the **Headless / watcher entry point** bullet's trigger clause; the convergence-summary bullet's counts; Override 5's **Trigger** paragraph.
- `plugin/commands/branch-start-user-review-fix-plan.md` — step 4's *"the live `## Questions` surface"*.
- `plugin/instructions/plan_orchestration_instructions_autonomous.md` — the closed list's entry 13 (*"… before any `## Questions` park …"*). **No other sentence of this file.**
- `plugin/instructions/untrusted_input.md` → `## Where a report goes` — the `user-review-fix-plan-writer` row and the `statistics-plan-writer`, `qa-tester` row. This task owns both rows; Task 5 does not edit this file.

**Work:**

- [ ] **The schema.** Write `plugin/schemas/user-review-fix-plan-writer.return.json` in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`, shaped like `plugin/schemas/test-fix-plan-writer.return.json`.
  - Top level: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `user-review-fix-plan-writer return`, `description`, `type: "object"`, and a `oneOf` of the three variants above.
  - Every listed field is required on its variant.
  - `minLength: 1` on the strings, `minimum: 0` on the four counts, and `minItems: 1` with `items: { "type": "string", "minLength": 1 }` on `questions`.
  - No other keyword anywhere.
- [ ] **The definition, `plugin/agents/user-review-fix-plan-writer.md`.**
  - **`## Output contract`.**
    - Replace the whole section above *"Do not paste the fix plan content back to the orchestrator"*: the fenced block, the `fix_plan_file` / `fix_plan_dir` explanation and the `## Questions` / pending paragraph. In its place put the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`: *End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence.*
    - Keep *"Do not paste the fix plan content back to the orchestrator — it will not read it."*
    - Add `### Return fields`, the four counts annotated `(integer)` and `questions` annotated `(array of strings)`:
      - `outcome` — `returned` after writing or revising, `questions` when a clarification or an untrusted-input report stops the work (nothing written), `blocker` when a cited path cannot be read (nothing written);
      - `fix_plan_file` — the index path;
      - `fix_plan_dir` — the per-finding folder, with the round suffix mirrored (`<branch>_fix_plan_2/` on a re-run);
      - the four counts;
      - `questions` — at least 1 item, each self-contained;
      - `blocker` — one line naming the path and the refusal.
  - **`## Process` step 3.** The **Needs clarification** bullet becomes: list it as an item of your return object's `questions`, return an `outcome` of `questions`, and stop without writing.
  - **`## Process` step 5.** The pull-request bullet's *"unless its observation is under `## Questions`"* becomes *"unless its observation is one of your `questions`"*.
  - **`## Invocation contract`.** *"How the caller consumes your return."* becomes: the caller reads `fix_plan_file`, `fix_plan_dir` and the four counts without opening the fix-plan files; an `outcome` of `questions` stops the loop and each item is routed to the user **verbatim**, so write questions the user can answer without the plan in front of them.
  - **`## Read on demand`.** *"return a `blocker:` line naming the path and the refusal in place of the `## Output contract` block"* becomes an `outcome` of `blocker` whose `blocker` names the path and the refusal. Keep *"and write neither the index nor any per-finding file"*.
  - **`## Resolved values`.** In the lead paragraph, drop `<full_path_to_index>` and *"and the return block"* from the placeholder list.
  - The one `${CLAUDE_PLUGIN_ROOT}/instructions/untrusted_input.md` → `## The markers` citation in this file stays exactly one. Add no other words.
- [ ] **The fix-plan core, `plugin/instructions/user_review_fix_plan_writing_instructions_core.md`.**
  - **`## Flow` step 6.** Replace *"**If the writer returns a `## Questions` section** above its output contract: …"* with: read every writer return — step 5's, and the revisions of steps 8 and 11, which route back here — as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states, routing it as **How the fix-plan core routes the return** above states. Keep the existing answer handling of the `questions` arm byte-for-byte: redispatch with each answer appended between the markers of `${CLAUDE_PLUGIN_ROOT}/instructions/untrusted_input.md` → `## The markers`, go back to step 6, and do not invent answers or paraphrase the questions. That keeps the file's two `## The markers` citations at two.
  - **Steps 7 and 8.** *"Once the writer has returned a real plan with no outstanding `## Questions`"* becomes *"Once the writer has returned an `outcome` of `returned`"*.
  - **Steps 8 and 11.** *"re-check for `## Questions` on the revised plan"* becomes *"read the revised plan's return as step 6 states"*.
  - **`## Mode contract — bindings this file uses`.** In the `<ask>` row's `Used at` cell, change *"the writer returns a `## Questions` section"* to *"the writer returns an `outcome` of `questions`"*. Add to the `<escalate>` row's `Used at` cell *"`## Flow` step 6 (the writer returns an `outcome` of `blocker`, or fails the check a third time)"*.
  - **`## Convergence`.** The first three bullets name `` `user-review-fix-plan-writer.fix_plan_file` `` (`<fix_plan_path>`), `` `user-review-fix-plan-writer.fix_plan_dir` `` (`<fix_finding_dir>`) and the four counts `` `user-review-fix-plan-writer.valid_must_fix` ``, `` `user-review-fix-plan-writer.valid_should_fix` ``, `` `user-review-fix-plan-writer.valid_nice_to_have` `` and `` `user-review-fix-plan-writer.invalid` ``.
  - The file is already on the module's `## Who may cite this` roster.
- [ ] **The forks, the command and the task-flow fork's closed list.** Each of these names the case and points at the core's step 6; none restates its routing.
  - **Supervised fork, `user_review_fix_plan_writing_instructions.md`.**
    - Its `<ask>` row surfaces each `` `user-review-fix-plan-writer.questions` `` item to the user, in place of *"the writer's `## Questions` section"*.
    - Step 9 presents `` `user-review-fix-plan-writer.fix_plan_file` ``, `` `user-review-fix-plan-writer.fix_plan_dir` `` and the four counts in citation form.
    - Its not-redefined line says *"the writer's return handling"* in place of *"the `## Questions` handling body"*.
  - **Autonomous fork, `user_review_fix_plan_writing_instructions_autonomous.md`.**
    - Its opening paragraph's *"the `## Questions` handling (step 6)"* becomes *"the writer's return handling (step 6)"*, matching the supervised fork's not-redefined line.
    - Its `<ask>` row, the *"Both bindings resolve …"* paragraph and the **Headless / watcher entry point** bullet say *"when the writer returns an `outcome` of `questions`"*.
    - The *"Both bindings resolve …"* paragraph's list of `<escalate>` triggers adds the writer's `blocker` or third failing return (the core's step 6).
    - The convergence summary names the fields in citation form.
    - Override 5's **Trigger** says *"before step 6 routes any `` `user-review-fix-plan-writer.questions` `` through `<ask>`"*.
  - **The command, `plugin/commands/branch-start-user-review-fix-plan.md`.** Step 4 reads *"the live surface for the writer's `questions`"*.
  - **The task-flow fork, `plugin/instructions/plan_orchestration_instructions_autonomous.md`.** Entry 13 reads *"before any `questions` park"*.
- [ ] **The untrusted-input report table, `plugin/instructions/untrusted_input.md` → `## Where a report goes`.**
  - Move `user-review-fix-plan-writer` into the first row's reader list, beside `task-plan-writer`, `ui-tests-plan-writer` and `test-fix-plan-writer`, whose cell already reads *"one item of its return object's `questions`, then stop as for any question; …"*. Delete its own row.
  - In the `statistics-plan-writer`, `qa-tester` row, change *"whose return has no free-text field"* to *"whose return has no field a report can go in"*. That wording is true both before and after Task 5 gives the statistics writer a `cause` field, which names an unreadable input and never a report.
  - Leave `## Who may cite this` unchanged: no reader is added.

**Verification:**

- `jq -e . plugin/schemas/user-review-fix-plan-writer.return.json` exits 0, and the `outcome` consts are exactly `returned`, `questions` and `blocker`.
- `grep -rn 'pending — questions for user' plugin/` has no hit.
- `grep -n '## Questions' plugin/agents/user-review-fix-plan-writer.md plugin/instructions/user_review_fix_plan_writing_instructions_core.md plugin/instructions/user_review_fix_plan_writing_instructions.md plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md plugin/commands/branch-start-user-review-fix-plan.md plugin/instructions/untrusted_input.md` has no hit.
- `grep -n '## Questions' plugin/instructions/plan_orchestration_instructions_autonomous.md` has exactly one expected hit, the closed list's entry 14 (*"… on a writer return that also carries `## Questions` it fires before the `<ask>` park."*): it is `ui-tests-plan-writer`'s, outside this branch's five agents, and no task edits it. Entry 13 reads *"before any `questions` park"*.
- `grep -nE '^(fix_plan_file|fix_plan_dir|valid_[a-z_]+|invalid):' plugin/agents/user-review-fix-plan-writer.md` has no hit.
- `grep -nF 'End your reply with your return object:' plugin/agents/user-review-fix-plan-writer.md` has exactly one hit.
- `grep -c 'instructions/untrusted_input.md` → `## The markers`' plugin/instructions/user_review_fix_plan_writing_instructions_core.md` is unchanged from before the edit.
- `grep -c 'instructions/untrusted_input.md` → `## The markers`' plugin/agents/user-review-fix-plan-writer.md` is unchanged from before the edit.
- Every `` `user-review-fix-plan-writer.<field>` `` citation added names a property the schema declares.

**Deviations from plan:**
- Autonomous fork, `## Mode contract — bindings` table: the `<escalate>` row's list of core sites it covers also gains the writer's `outcome` of `blocker` or third failing return at step 6. The Targets list omits that row, but the row enumerates the `<escalate>` sites and would otherwise contradict the *"Both bindings resolve …"* paragraph and the core's new `<escalate>` site.
- Autonomous fork convergence summary: the old text named `fix_plan_path`, which is not a return field; the citation-form edit names `` `user-review-fix-plan-writer.fix_plan_file` `` in its place.
