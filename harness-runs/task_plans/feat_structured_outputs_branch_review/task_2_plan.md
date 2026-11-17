### Task 2 — Give `branch-reviewer` a schema-validated return and move Phase B and the supervised code review onto it

**Goal:** `branch-reviewer` replaces its prose summary — the index path, the per-finding folder, the finding count, the two-pass line `Pass 2 carried over N items, skipped M (already covered) and K (stale).` and the `## Questions` section — with one fenced `json` return object declared in `plugin/schemas/branch-reviewer.return.json`. Phase B of the orchestration core, the supervised code review and the two Done-summary / observation sentences that read its questions move onto that object.

**Depends on:** Task 1, which rewrote `### B.2` step 2 of `plugin/instructions/plan_orchestration_instructions_core.md` and keeps its `branch-reviewer` re-dispatch prompt — *"Adjust the code-review index at <code_review_path> and the per-finding files in <code_review_findings_dir> per findings at <findings_file>."* — byte-identical. That re-dispatch's return is read by the `### B.1` sentence this task writes; this task does not edit `### B.2`.

**The contract this task defines** (no later task changes it):

- An `outcome` of `returned` — the split review was written.
  - `index_path` (string, non-empty): the index path the caller supplied.
  - `findings_dir` (string, non-empty): the per-finding folder, with the round suffix mirrored.
  - `finding_count` (integer, at least 0): the number of `finding_<N>.md` files written.
  - `carried_over`, `skipped_covered`, `skipped_stale` (integers, at least 0): **two-pass mode only**, where they are required. Pass 2's real-and-missed, already-covered and stale counts, replacing the prose line. A single-pass return omits all three. An `Adjust …` re-dispatch carries no `per_task_findings_root`, so it is single-pass.
  - `questions` (array of strings, items non-empty, **optional**): one item per decision a finding could not take, naming the decision owed and who owes it. Omitted when there is none.
- An `outcome` of `blocker` — `blocker` (string, non-empty): one line naming the unreadable path and the refusal. No review file is written.

In the schema, the `returned` variant's `required` is exactly `outcome`, `index_path`, `findings_dir` and `finding_count`. The three counts and `questions` are declared but not required. `questions` carries `minItems: 1`, so an empty array is never written.

**The two clause-shared sentences** (Task 3 rewrites only the `skeptic-reviewer` clause of each):

- `### D.2 Done summary`'s **Review questions** bullet, after this task: *"— taken from `` `branch-reviewer.questions` `` (optional: absent or empty means none) and from the `## Questions` section of the `skeptic-reviewer`'s return (that literal heading; the section is omitted when there is none). Say **"none raised"** when neither raised one. This is a hand-off line, never a gate: …"* (the rest unchanged).
- The autonomous fork's observation bullet, after this task: *"- **A review's questions are not an observation.** `` `branch-reviewer.questions` `` (Phase B) and a `## Questions` section returned by the `skeptic-reviewer` (Phase C2) are **never** written here: …"* (the rest unchanged).

### Targets

- `plugin/schemas/branch-reviewer.return.json` (new).
- `plugin/agents/branch-reviewer.md` — `## Read first`'s report-don't-substitute paragraph, `## Findings format`'s *"Every finding must be implementable as written …"* paragraph, and `## Output contract`'s *"When you finish …"* lead and *"Summary you return to the caller"* block.
- `plugin/instructions/plan_orchestration_instructions_core.md` — `### B.1 Generate the review plan`'s two paragraphs after the dispatch block (*"The `per_task_findings_root` argument triggers …"* and *"A **`## Questions`** section in that return …"*), and the `branch-reviewer` clause of `### D.2`'s **Review questions** bullet. **No other sentence of this file.**
- `plugin/instructions/plan_orchestration_instructions_autonomous.md` — the `branch-reviewer` clause of the *"A reviewer's `## Questions` section is not an observation."* bullet. **No other sentence of this file.**
- `plugin/instructions/code_review_instructions.md` — `## Flow` steps 3 and 4. Step 6's statistics dispatch is Task 5's.
- `plugin/instructions/agent_return_contract.md` — `## Who may cite this`: add `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_instructions.md`.

**Work:**

- [ ] **The schema.** Write `plugin/schemas/branch-reviewer.return.json` in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`.
  - Top level: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `branch-reviewer return`, `description`, `type: "object"`, and a `oneOf` of two variants: `returned` and `blocker`, exactly as the contract above states.
  - Each property carries `type` and `description`, with `minLength: 1` on the strings, `minimum: 0` on the five integers, and `minItems: 1` plus `items: { "type": "string", "minLength": 1 }` on `questions`.
  - No other keyword anywhere.
- [ ] **The definition, `plugin/agents/branch-reviewer.md`.**
  - **`## Output contract`.**
    - Keep *"When you finish, **write the split review to disk** …"* and the whole **Files you write** list unchanged, but end the lead sentence on ending your reply with the return object rather than *"then return a short summary"*.
    - Replace the **Summary you return to the caller** block — its four bullets, the reconciliation sentence among them — with the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`: *End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence.*
    - Follow it with one sentence: an optional `## Unsolicited dispatch guidance` section sits above the fenced block and changes nothing in it.
    - Then `### Return fields`, one bullet per property, the five integers annotated `(integer)` and `questions` annotated `(array of strings)`:
      - `outcome` — `returned` / `blocker`;
      - `index_path`, `findings_dir`, `finding_count`;
      - `carried_over`, `skipped_covered`, `skipped_stale` — `returned`, two-pass mode only and required there; not written into any saved file;
      - `questions` — `returned`, omitted when none; one item per decision owed under `## Findings format`, naming the decision and who owes it;
      - `blocker`.
  - **`## Findings format`.** In *"Put it in a `## Questions` section of your return, where a `## Unsolicited dispatch guidance` section sits, naming the decision owed and who owes it; write no per-finding file and no readiness entry for it, and add no return field."*, make the question an item of your return object's `questions`, naming the decision owed and who owes it. Drop *"where a `## Unsolicited dispatch guidance` section sits"* and *"and add no return field"*. Keep *"write no per-finding file and no readiness entry for it"* and the partly-decidable split sentence.
  - **`## Read first`.** Change *"return a `blocker:` line naming the path and the refusal **in place of** your summary"* to an `outcome` of `blocker` whose `blocker` names the path and the refusal. Keep *"and write no review files"*.
  - Leave `## Unsolicited dispatch guidance` byte-identical: `plugin/instructions/dispatch_discipline_instructions.md` owns it. Add no other words.
- [ ] **Phase B, `plugin/instructions/plan_orchestration_instructions_core.md` → `### B.1`.**
  - Keep the dispatch block and *"When it returns, treat the **index** at `<code_review_path>` … as the review plan."*
  - Replace the sentence *"The `branch-reviewer` returns a one-line reconciliation summary in its message; read it and pass through."* and the whole *"A **`## Questions`** section in that return …"* paragraph with:
    > Read every `branch-reviewer` return in this phase — this dispatch's and each B.2 re-dispatch's — as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:
    > - An `outcome` of `returned` → on this dispatch, continue to **B.2**, and pass through the Pass 2 reconciliation `` `branch-reviewer.carried_over` `` / `` `branch-reviewer.skipped_covered` `` / `` `branch-reviewer.skipped_stale` ``; on a B.2 re-dispatch, return to B.2's loop. `` `branch-reviewer.questions` `` is optional — absent or empty means none. Its items are **retained, not acted on**: each names a decision the review declined to take, has no per-finding file and no readiness entry, and changes nothing in this phase. Carry them verbatim to `### D.2 Done summary`.
    > - An `outcome` of `blocker`, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) → `<escalate>`, naming the origin `Phase B branch-reviewer` and quoting `` `branch-reviewer.blocker` `` or naming the check that failed.
  - Keep the paragraph's existing sentence on what `per_task_findings_root` triggers.
  - **`### D.2`.** Rewrite only the `branch-reviewer` clause of the **Review questions** bullet, to exactly the intermediate text stated above.
- [ ] **The autonomous fork, `plugin/instructions/plan_orchestration_instructions_autonomous.md`.** Rewrite the observation bullet's lead and its `branch-reviewer` clause to exactly the intermediate text stated above. Leave the rest of the bullet, from *"it names a decision owed **about this branch**"* on, byte-identical.
- [ ] **The supervised code review and the roster.**
  - **`plugin/instructions/code_review_instructions.md` → `## Flow` step 3.** Replace *"Present the review findings returned by the agent to the user."* with: read every `branch-reviewer` return in this flow — step 2's and any step-4 re-spawn's — as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states.
    - On an `outcome` of `returned`, present `` `branch-reviewer.index_path` ``, `` `branch-reviewer.findings_dir` ``, `` `branch-reviewer.finding_count` `` and each `` `branch-reviewer.questions` `` item to the user. `questions` is optional: absent or empty means none.
    - On an `outcome` of `blocker`, or the third consecutive return that fails the check (`## A return that fails the check`), report `` `branch-reviewer.blocker` `` or the check that failed, and stop.
    - The supervised dispatch is single-pass, so it reads no reconciliation field.
  - **`code_review_instructions.md` step 4.** Keep its re-spawn sentence and add nothing else to it: step 3's reading rule covers the re-spawn.
  - **The roster.** Add `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_instructions.md` to `plugin/instructions/agent_return_contract.md` → `## Who may cite this`. Add no other line to that module.

**Verification:**

- `jq -e . plugin/schemas/branch-reviewer.return.json` exits 0; the `outcome` consts are exactly `returned` and `blocker`; and the `returned` variant's `required` is exactly `outcome`, `index_path`, `findings_dir` and `finding_count`.
- `grep -rn 'Pass 2 carried over' plugin/` has no hit.
- `grep -n '## Questions' plugin/agents/branch-reviewer.md` has no hit.
- `grep -nF 'End your reply with your return object:' plugin/agents/branch-reviewer.md` has exactly one hit, inside `## Output contract`.
- `grep -n 'reconciliation summary' plugin/instructions/plan_orchestration_instructions_core.md` has no hit.
- `grep -n '## Questions' plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/plan_orchestration_instructions_autonomous.md` shows only the `skeptic-reviewer` clauses that Task 3 rewrites: one in `### C2.1`, one in `### D.2`'s **Review questions** bullet and one in the autonomous observation bullet.
- Every `` `branch-reviewer.<field>` `` citation added names a property the schema declares.
- `grep -l 'agent_return_contract.md' plugin/instructions/code_review_instructions.md` hits, and the module's `## Who may cite this` lists that file.
