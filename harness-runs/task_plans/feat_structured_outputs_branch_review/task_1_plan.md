### Task 1 — Give `review-plan-reviewer` a schema-validated return and move the B.2 and C2.2 meta-review loops onto it

**Goal:** `review-plan-reviewer` ends its reply with one fenced `json` return object declared in `plugin/schemas/review-plan-reviewer.return.json`. Its two callers, the B.2 and C2.2 loops of the orchestration core and the autonomous fork's `Bm` flip, read that object instead of matching `verdict:` lines.

**The contract this task defines** (no later task changes it):

- An `outcome` of `PASS` — the review under meta-review is clean and no file was written. No other field.
- An `outcome` of `FAIL` — `findings_file` (string, non-empty: the full path of `<findings_folder>/review_{iteration}.md`) and `must_fix_count` (integer, at least 1).
- An `outcome` of `blocker` — `blocker` (string, non-empty: one line naming the unreadable path and the refusal), in place of any verdict when `## Read first`'s report-don't-substitute rule fires. No findings file is written.

The findings **file** this agent writes — its `# Review plan meta-review — iteration {iteration}` template, with `## Must Fix` / `## Should Fix` / `## Nice to Have` — is file content and is unchanged.

**What this task does not touch.** `branch-reviewer`'s and `skeptic-reviewer`'s own returns, including the returns of the B.2 and C2.2 **re-dispatches** of those two authors, are Tasks 2 and 3's. Those tasks add, in `### B.1` and `### C2.1`, the sentence that reads every return of the author, the re-dispatches included. This task's B.2 / C2.2 bullets keep the re-dispatch prompt text byte-identical and say nothing about the author's return.

### Targets

- `plugin/schemas/review-plan-reviewer.return.json` (new).
- `plugin/agents/review-plan-reviewer.md` — `## Resolved values`' lead paragraph, `## Invocation contract`'s *"Your return is parsed, not read."* paragraph, `## Read first`'s report-don't-substitute paragraph, and `## Output contract`.
- `plugin/instructions/plan_orchestration_instructions_core.md` — the opening *"Reviewers return 1 line …"* bullet, `### B.2 Meta-review the review plan` step 2 and `### C2.2 Meta-review the skeptic review` step 2. **No other sentence of this file**: `### B.1`, `### C2.1`, `### D.1` and `### D.2` belong to Tasks 2, 3 and 5.
- `plugin/instructions/plan_orchestration_instructions_autonomous.md` — the `Bm` clause of the `Bg` / `Bm` flip bullet. **No other sentence of this file.**

**Work:**

- [ ] **The schema.** Write `plugin/schemas/review-plan-reviewer.return.json` in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`, shaped like `plugin/schemas/task-plan-reviewer.return.json`.
  - Top level: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `review-plan-reviewer return`, `description`, `type: "object"`, and a `oneOf` of three variants.
  - Each variant: `type: "object"`, `description`, `properties`, `required` (always including `outcome`) and `additionalProperties: false`.
  - The variants: `PASS` with `required: ["outcome"]`; `FAIL` with `findings_file` (`type: "string"`, `minLength: 1`) and `must_fix_count` (`type: "integer"`, `minimum: 1`), both required; `blocker` with `blocker` (`type: "string"`, `minLength: 1`), required.
  - No other keyword anywhere.
- [ ] **The definition, `plugin/agents/review-plan-reviewer.md`.**
  - **`## Output contract`.**
    - Open it with the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`: *End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence.*
    - Keep the optional `## Unsolicited dispatch guidance` placement, now *above the fenced block*.
    - Keep *"Do not save a file when PASS"*, the `mkdir -p <findings_folder>` step, the findings-file template block and *"Only **Must Fix** triggers another iteration of the review's author."*
    - Delete the two fenced `verdict: …` return blocks, the *"Nothing else."* / *"Keep the return to those 3 lines."* sentences that describe them, and the reference to *"those 3 lines"* in the section's lead paragraph.
    - End the section with `### Return fields`, one bullet per schema property, each opening with the backticked name and a non-string one carrying its annotation:
      - `outcome` — `PASS` when the review is clean, `FAIL` when there is a Must Fix, `blocker` in place of any verdict when a cited path cannot be read (`## Read first`);
      - `findings_file` — `FAIL`: the full path of the findings file you wrote;
      - `must_fix_count` (integer) — `FAIL`: the number of Must Fix entries in it, at least 1;
      - `blocker` — `blocker`: one line naming the path and the refusal.
  - **`## Invocation contract`.** Rewrite *"Your return is parsed, not read."* so the caller routes on your `outcome`: `PASS` breaks the loop and moves the flow on to committing the review; `FAIL` increments `iteration` and re-dispatches the author of the index you just read with `Adjust the … index … per findings at <findings_file>.`, where `<findings_file>` is your `findings_file`; at `iteration >= 5` the loop stops and escalates. Keep the last sentence, *"Because the author fixes the files rather than regenerating them, every Must Fix you write must name **which file** to change — the index or a specific `finding_<N>.md`."* Drop *"So the verdict line must be **exactly** one of those two strings …"*: the outcome value carries that now.
  - **`## Read first`.** Change *"return a `blocker:` line naming the path and the refusal **in place of** the verdict line"* to return an `outcome` of `blocker`, its `blocker` naming the path and the refusal. Keep *"and write no findings file"* and the rest.
  - **`## Resolved values`.** In the lead paragraph, drop `<full_path>` from *"`<title>` / `<full_path>` / `<optional>` in the findings template"*: it named the deleted return line.
  - Add no other words: `.claude/context/plugin.md` → `## Writing agent prose`, *"An agent's growth is paid for by behaviour."*
- [ ] **The orchestration core, `plugin/instructions/plan_orchestration_instructions_core.md`.**
  - **The opening bullet.** Replace *"Reviewers return 1 line (`verdict: PASS`) or 3 lines (`verdict: FAIL` + `findings_file:` + `must_fix_count:`) — except `layer-reviewer`, `business-parity-reviewer` and `architecture-reviewer`, which end in a return object (…)."* with a form that names no agent, so it stays true while Tasks 2–5 land: *"Reviewers end in a return object, read as the section that dispatches each states — except where that section reads `verdict:` lines, where the reviewer returns 1 line (`verdict: PASS`) or 3 lines (`verdict: FAIL`, a path line and `must_fix_count:`)."* Keep the bullet's closing *"Read that, **do not open the findings file** — pass its path to the next implementer."*
  - **`### B.2` step 2.** Replace *"Parse return:"* and its two bullets with:
    > Parse the return — read it as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:
    > - An `outcome` of `PASS` → break.
    > - An `outcome` of `FAIL` → increment `iteration`. If `>= 5`, `<escalate>`, naming `` `review-plan-reviewer.findings_file` ``. Else spawn `branch-reviewer` again with *(the existing `Adjust the code-review index …` prompt, byte-identical)*, where `<findings_file>` is `` `review-plan-reviewer.findings_file` ``. Then loop.
    > - An `outcome` of `blocker`, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) → `<escalate>`, naming the origin `Phase B.2 review-plan-reviewer` and quoting `` `review-plan-reviewer.blocker` `` or naming the check that failed.
  - **`### C2.2` step 2.** Make the same replacement. Use the existing `Adjust the skeptic-review index …` prompt byte-identical, and the origin `Phase C2.2 review-plan-reviewer`.
  - The file is already on the module's `## Who may cite this` roster, so no roster edit is owed.
- [ ] **The autonomous fork, `plugin/instructions/plan_orchestration_instructions_autonomous.md`.** In the flip bullet, change *"`Bm` — after the **B.2** `review-plan-reviewer` meta-review returns `verdict: PASS`."* to *"… returns an `outcome` of `PASS`."* The `C2m` clause (*"returns PASS"*) already names no line form and stays.

**Verification:**

- `jq -e . plugin/schemas/review-plan-reviewer.return.json` exits 0, and the three `oneOf[].properties.outcome.const` values are exactly `PASS`, `FAIL` and `blocker`.
- `grep -nE 'verdict: (PASS|FAIL)|findings_file:|must_fix_count:' plugin/agents/review-plan-reviewer.md` has no hit inside `## Output contract`. Its only `verdict` mentions elsewhere describe the findings file or the review under meta-review.
- `grep -nF 'End your reply with your return object: one fenced code block whose info string is `json`' plugin/agents/review-plan-reviewer.md` has exactly one hit, inside `## Output contract`, above `### Return fields`.
- In `plan_orchestration_instructions_core.md`, `grep -nE 'verdict: (PASS|FAIL)' plugin/instructions/plan_orchestration_instructions_core.md` has no hit inside `### B.2` or `### C2.2`, and every hit left is one of these:
  - the opening bullet's generic form;
  - `### C2.1`'s skeptic lines, which are Task 3's;
  - Phase E's `qa-tester` lines;
  - `### D.2`'s skeptic bullet, which is Task 3's.
- Every `` `review-plan-reviewer.<field>` `` citation added names one of `findings_file` and `blocker`.
- `grep -n 'Bm' plugin/instructions/plan_orchestration_instructions_autonomous.md` shows the flip on *"an `outcome` of `PASS`"*.
