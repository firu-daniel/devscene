### Task 4 — Give `docs-reviewer` a schema-validated return and move the docs phase and the docs catalog onto it

**Goal:** `docs-reviewer` replaces its `verdict:` · `findings_file:` · `missed_docs:` · `summary:` lines, its disabled-phase `verdict: PASS` plus a reason line, and its `blocker:` line with one fenced `json` return object declared in `plugin/schemas/docs-reviewer.return.json`. Its two callers move every `docs-reviewer` dispatch's reading onto that object in the same change.

**Depends on:** Task 3, which owns every `docs-writer` sentence in the two files this task shares with it and has already:

- pointed both `plugin/instructions/docs_phase_instructions.md` and `plugin/instructions/docs_orchestration_instructions_autonomous.md` at `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` and added both to its `## Who may cite this` — this task adds no roster line;
- routed every `docs-writer` return, including a writer re-dispatched in a fix loop: in the docs phase, an `outcome` of `written` carries `` `docs-writer.doc_path` `` and a writer `error` route logs and skips the target; in the catalog, a writer `error` route leaves the box `[ ]` and ends the session;
- rewritten `plugin/instructions/untrusted_input.md`'s `docs-writer` row. This task edits that file's `docs-reviewer` row only.

This task edits only the sentences `### Targets` lists, and no sentence Task 3 wrote.

**The contract this task defines** (every outcome one token):

- An `outcome` of `PASS` — accurate, adequately researched and, in update mode, faithful to the diff.
- An `outcome` of `FAIL` — a factual error, a shallow document, a material omission, an unclassified line coordinate, or (update mode) a stale or missing change.

  `PASS` and `FAIL` carry the same fields:
  - `findings_file` (string, non-empty, required): the `findings_path` written.
  - `summary` (string, non-empty, required): one line. An untrusted-input report the document does not act on is one clause of it, carrying the report literal.
  - `missed_docs` (array of strings, optional, at least 1, each non-empty): update mode only — the slug of every other document the diff should have touched. Omitted when none.
- An `outcome` of `phase_disabled` — `phases.docs` is `false`; nothing was read and no findings file was written.
  - `reason` (string, non-empty, required).
- An `outcome` of `blocker` — the writer's contract, a conventions document or an input the dispatch names could not be read; no findings file was written.
  - `blocker` (string, non-empty, required): the path and the refusal.

The disabled-phase return was *"`verdict: PASS` plus one line … and no `findings_file:`"*. It becomes `phase_disabled` because the consts must be distinct across variants and `PASS` carries a required `findings_file`; Task 3 gave `docs-writer` the same outcome, and Task 6 records the choice.

**How each caller routes the return.** State it at each dispatch site, reading as `agent_return_contract.md` → `## Reading a return` states, and name each site's `error` route:

- An `outcome` of `PASS` → commit, as today.
- An `outcome` of `FAIL` → the fix loop, re-dispatching the writer with `` `docs-reviewer.findings_file` ``.
- In the docs phase only, `` `docs-reviewer.missed_docs` `` — optional, absent meaning none, on `PASS` and `FAIL` alike → append those slugs to the working target list as `update` targets.
- An `outcome` of `phase_disabled` or `blocker`, or the third consecutive return that fails the check — each review site's `error` route → treat it as the fix cap does: record `<slug>` and `` `docs-reviewer.blocker` ``, `` `docs-reviewer.reason` `` or the check that failed in `<state_dir>/docs_catalog/needs_review.md`, and commit the doc as-is. Neither flow halts on a review.

### Targets

- `plugin/schemas/docs-reviewer.return.json` (new).
- `plugin/agents/docs-reviewer.md` — the phase-gate paragraph; `## Invocation contract`'s two *"Returns `verdict:` + …"* lines and its report-don't-substitute paragraph; and `## Output contract`.
- `plugin/instructions/docs_phase_instructions.md` — `## Loop` step 2's **Review.**, **Fix loop (cap 3).** and **Missed-doc ripple.** bullets. **No other sentence of this file.**
- `plugin/instructions/docs_orchestration_instructions_autonomous.md` — `## Per-entry loop` step 2's *"It returns `verdict:` PASS|FAIL + `findings_file:` + `summary:`."*; step 3's opening clause *"On `FAIL`, re-dispatch `docs-writer` with the same fields **plus** the reviewer's `findings_file` …"* and its *"If still `FAIL` after the cap"* clause; and, in `## Final entry — INDEX`, one added sentence routing the INDEX review's return. **No other sentence of this file.**
- `plugin/instructions/untrusted_input.md` → `## Where a report goes` — the `docs-reviewer` row only.
- `plugin/instructions/improvement_observations_instructions.md` → `## What the orchestrator may log — rules` item 6 — the clause *"every sub-agent's `notes:` / `summary:` contract field"*.

**Work:**

- [ ] **The schema.** Write `plugin/schemas/docs-reviewer.return.json` in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `docs-reviewer return`, `description`, `type: "object"`, a `oneOf` of four variants — `PASS`, `FAIL`, `phase_disabled`, `blocker` — each `additionalProperties: false`, `required` naming `outcome` and exactly the fields marked required above. `minLength: 1` on every string and on `missed_docs`' `items`; `minItems: 1` on `missed_docs`. No other keyword.
- [ ] **The definition, `plugin/agents/docs-reviewer.md`.**
  - **`## Output contract`.** Keep *"Write `findings_path` (each finding: the claim, the file that contradicts it, the correction)."* and *"Do not paste the document back."* Add the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`. Keep the **PASS** and **FAIL** criteria as the two outcomes' meanings, `PASS` and `FAIL` backticked. Replace the `findings_file:`, `missed_docs:`, `summary:` and disabled-phase bullets with `### Return fields`: `outcome` with its four values; `findings_file`; `summary`; `missed_docs` (array of strings) — update mode only, omitted when none; `reason` — `phase_disabled`; `blocker` — `blocker`. Each bullet names its outcomes and states its lower bound. No fenced `key: value` or `json` block in the section.
  - **The phase gate.** *"return `verdict: PASS` followed by one line naming the disabled phase as the reason. The verdict line stays byte-exact so the caller's parse is unaffected, and a stray dispatch is a clean no-op …"* becomes *"return an `outcome` of `phase_disabled` whose `reason` names the disabled phase, so a stray dispatch is a clean no-op …"*; keep the rest of the sentence.
  - **`## Invocation contract`.** *"Returns `verdict:` + `findings_file:` + `summary:`."* becomes *"Returns an `outcome` of `PASS` or `FAIL` with `findings_file` and `summary`."*; the update-mode line adds *"and `missed_docs` where any"*. The report-don't-substitute paragraph's *"return a `blocker:` line naming the path and the refusal **in place of** the verdict line"* becomes *"return an `outcome` of `blocker` whose `blocker` names the path and the refusal"*.
  - Keep `## Unsolicited dispatch guidance` byte-identical, and this file's single `untrusted_input.md` pointer. Add no other words.
- [ ] **`docs_phase_instructions.md` — the reviewer's three bullets.**
  - **Review.** *"It returns `verdict:` + `findings_file:` + `missed_docs:` + `summary:`."* becomes: read its return as `agent_return_contract.md` → `## Reading a return` states; an `outcome` of `PASS` → commit; an `outcome` of `FAIL` → the fix loop; an `outcome` of `phase_disabled` or `blocker`, or the third consecutive return that fails the check — this bullet's `error` route → append `<slug>` and `` `docs-reviewer.blocker` ``, `` `docs-reviewer.reason` `` or the check that failed to `<state_dir>/docs_catalog/needs_review.md` and commit the doc as-is. Keep the next-free `<i>` sub-bullet byte-identical.
  - **Fix loop (cap 3).** *"On `FAIL`, re-dispatch the writer with the findings"* becomes *"On an `outcome` of `FAIL`, re-dispatch the writer with `` `docs-reviewer.findings_file` ``"*. Keep the rest.
  - **Missed-doc ripple.** *"If the reviewer returns `missed_docs:`"* becomes *"If the review's return carries `` `docs-reviewer.missed_docs` `` — optional, absent meaning none —"*. Keep the rest.
- [ ] **`docs_orchestration_instructions_autonomous.md` — the reviewer's dispatch sites.**
  - **Step 2.** *"It returns `verdict:` PASS|FAIL + `findings_file:` + `summary:`."* becomes: read its return as `agent_return_contract.md` → `## Reading a return` states; an `outcome` of `PASS` → step 4; an `outcome` of `FAIL` → step 3; an `outcome` of `phase_disabled` or `blocker`, or the third consecutive return that fails the check — the `error` route of this step, of step 3's re-reviews and of the INDEX review → treat it as step 3's exhausted cap: record `<slug>` and `` `docs-reviewer.blocker` ``, `` `docs-reviewer.reason` `` or the check that failed in `<state_dir>/docs_catalog/needs_review.md` and proceed to commit the doc as-is.
  - **Step 3.** *"On `FAIL`, re-dispatch `docs-writer` with the same fields **plus** the reviewer's `findings_file`"* becomes *"On an `outcome` of `FAIL`, re-dispatch `docs-writer` with the same fields **plus** `` `docs-reviewer.findings_file` ``"*; *"If still `FAIL` after the cap"* becomes *"If the outcome is still `FAIL` after the cap"*. Keep the rest, and leave Task 3's writer routing untouched.
  - **`## Final entry — INDEX`.** After the review sentence, add: its return routes as step 2's.
- [ ] **The report row and the observations clause.**
  - `untrusted_input.md`, the `docs-reviewer` row: *"and verdict `FAIL`"* becomes *"and an `outcome` of `FAIL`"*; *"otherwise one clause of its `summary:` line carrying the literal, the verdict decided on the document alone"* becomes *"otherwise one clause of `` `docs-reviewer.summary` `` carrying the literal, the outcome decided on the document alone"*.
  - `improvement_observations_instructions.md` item 6: *"every sub-agent's `notes:` / `summary:` contract field"* becomes *"every sub-agent's return object — `` `docs-writer.notes` `` and `` `docs-reviewer.summary` `` among its fields"*. Keep the rest of the item.

**Verification:**

- `jq -e . plugin/schemas/docs-reviewer.return.json` exits 0; the `outcome` consts are exactly `PASS`, `FAIL`, `phase_disabled` and `blocker`; no variant declares `error`.
- `grep -nE 'verdict:|findings_file:|missed_docs:|`summary:`|`blocker:`' plugin/agents/docs-reviewer.md plugin/instructions/docs_phase_instructions.md plugin/instructions/docs_orchestration_instructions_autonomous.md` has no hit.
- `grep -nE '`notes:`|`summary:`' plugin/instructions/untrusted_input.md plugin/instructions/improvement_observations_instructions.md` has no hit.
- `grep -c 'Untrusted instruction not followed — ' plugin/instructions/docs_orchestration_instructions_autonomous.md` still prints `1`.
- `agent_return_contract.md` is unchanged by this task (`git diff --stat` on it is empty).
- Every review site in the two docs instruction files names its `error` route, and none halts the flow.
- Every `` `docs-reviewer.<field>` `` citation added names a property the schema declares, and every `` `docs-writer.<field>` `` citation added names one Task 3's schema declares.
