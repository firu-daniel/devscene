### Task 3 — Give `skeptic-reviewer` a schema-validated return and move Phase C2 and its Done-summary lines onto it

**Goal:** `skeptic-reviewer` replaces its `verdict: PASS` / `verdict: FAIL` + `index_path:` + `must_fix_count:` block and its `## Questions` section with one fenced `json` return object declared in `plugin/schemas/skeptic-reviewer.return.json`. Phase C2 of the orchestration core, its Done-summary lines and the autonomous fork's C2 flips move onto that object.

**Depends on:** Task 2, which left the two clause-shared sentences in this exact intermediate form. This task replaces only their `skeptic-reviewer` clause.

- `plugin/instructions/plan_orchestration_instructions_core.md` → `### D.2`'s **Review questions** bullet: *"— taken from `` `branch-reviewer.questions` `` (optional: absent or empty means none) and from the `## Questions` section of the `skeptic-reviewer`'s return (that literal heading; the section is omitted when there is none). Say **"none raised"** when neither raised one. …"*
- `plugin/instructions/plan_orchestration_instructions_autonomous.md`'s observation bullet: *"- **A review's questions are not an observation.** `` `branch-reviewer.questions` `` (Phase B) and a `## Questions` section returned by the `skeptic-reviewer` (Phase C2) are **never** written here: …"*

Task 1 rewrote `### C2.2` step 2 and keeps its `skeptic-reviewer` re-dispatch prompt — *"Adjust the skeptic-review index at <skeptic_review_path> and the per-finding files in <skeptic_review_findings_dir> per findings at <findings_file>."* — byte-identical. That re-dispatch's return is read by the `### C2.1` sentence this task writes; this task does not edit `### C2.2`.

**The contract this task defines** (no later task changes it):

- An `outcome` of `PASS` — no net-new finding, and no file was written.
  - `questions` (array of strings, items non-empty, `minItems: 1`, **optional**).
- An `outcome` of `FAIL` — net-new findings were written.
  - `index_path` (string, non-empty): the index path the caller supplied.
  - `must_fix_count` (integer, **at least 0**): a FAIL may carry only Should Fix findings, as the old contract's `<integer>` allowed.
  - `questions` (optional, as above).
- An `outcome` of `blocker` — `blocker` (string, non-empty): one line naming the unreadable path and the refusal. No file is written.

`questions` is declared on `PASS` and `FAIL` and required on neither. The final text of the two shared sentences, after this task:

- **Review questions:** *"— taken from `` `branch-reviewer.questions` `` and `` `skeptic-reviewer.questions` `` (both optional: absent or empty means none). Say **"none raised"** when neither raised one. …"* (the rest unchanged).
- **Observation bullet:** *"- **A review's questions are not an observation.** `` `branch-reviewer.questions` `` (Phase B) and `` `skeptic-reviewer.questions` `` (Phase C2) are **never** written here: …"* (the rest unchanged).

### Targets

- `plugin/schemas/skeptic-reviewer.return.json` (new).
- `plugin/agents/skeptic-reviewer.md` — `## Invocation contract`'s *"Your return is parsed, not read."* paragraph, `## Read first`'s report-don't-substitute paragraph, `## Confidence bar`'s *"`verdict: PASS` with no net-new findings is a correct outcome here …"* sentence, `## Findings format`'s *"Every finding must be implementable as written …"* paragraph, and `## Output contract`.
- `plugin/instructions/plan_orchestration_instructions_core.md` — `### C2.1 Generate the skeptic review`'s *"Parse the return:"* list and its *"On **either** verdict, a **`## Questions`** section …"* paragraph; `### D.2`'s **Skeptic review (Phase C2)** bullet; the `skeptic-reviewer` clause of `### D.2`'s **Review questions** bullet. **No other sentence of this file.**
- `plugin/instructions/plan_orchestration_instructions_autonomous.md` — the `C2g` clause of the `C2g` / `C2m` / `C2f` flip bullet; the `skeptic-reviewer` clause of the *"Each `*g` flip fires once its phase reached a **recorded outcome**"* paragraph; the `skeptic-reviewer` clause of the observation bullet. **No other sentence of this file.**

**Work:**

- [ ] **The schema.** Write `plugin/schemas/skeptic-reviewer.return.json` in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`.
  - Top level: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `skeptic-reviewer return`, `description`, `type: "object"`, and a `oneOf` of three variants: `PASS`, `FAIL` and `blocker`, exactly as the contract above states.
  - `PASS` requires only `outcome`. `FAIL` requires `outcome`, `index_path` and `must_fix_count`. `blocker` requires `outcome` and `blocker`.
  - `minLength: 1` on the strings, `minimum: 0` on `must_fix_count`, and `minItems: 1` with `items: { "type": "string", "minLength": 1 }` on `questions`.
  - No other keyword anywhere.
- [ ] **The definition, `plugin/agents/skeptic-reviewer.md`.**
  - **`## Output contract`.**
    - Keep the two numbered outcome subsections and their file rules: *"do not write any file"* on PASS; `mkdir -p` the findings folder, then write the index and one `finding_<N>.md` per finding, and *"Do not paste the bodies back"* on FAIL.
    - Delete both fenced return blocks (`verdict: PASS`; `verdict: FAIL` / `index_path:` / `must_fix_count:`) and the *"Return exactly"* / *"Then return exactly three lines"* lead-ins.
    - Name the outcome in each subsection's heading text: `PASS`, `FAIL`.
    - Rewrite the section's lead to: there are three outcomes, `PASS`, `FAIL` and `blocker`; pick exactly one; an optional `## Unsolicited dispatch guidance` section sits above the fenced block and changes neither the block nor any file.
    - Add the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`: *End your reply with your return object: one fenced code block whose info string is `json`, holding one JSON object with exactly the fields `### Return fields` below lists for your outcome, with nothing after its closing fence.*
    - End with `### Return fields`:
      - `outcome` — `PASS` when you have no net-new finding, `FAIL` when you wrote findings, `blocker` in place of either when a cited path cannot be read (`## Read first`);
      - `index_path` — `FAIL`: the index path you wrote;
      - `must_fix_count` (integer) — `FAIL`: the number of Must Fix findings in it, at least 0;
      - `questions` (array of strings) — `PASS` and `FAIL`, omitted when none: one item per decision owed under `## Findings format`;
      - `blocker` — `blocker`: one line naming the path and the refusal.
  - **`## Findings format`.** Make the same change Task 2 made in `branch-reviewer.md`: the question becomes an item of your return object's `questions`, naming the decision owed and who owes it. Drop *"where a `## Unsolicited dispatch guidance` section sits"* and *"and add no return field"*; keep *"write no per-finding file and no readiness entry for it"* and the split sentence.
  - **`## Invocation contract`.** Rewrite *"Your return is parsed, not read."* so the caller routes on your `outcome`: `PASS` skips the meta-review and the fix loop, and `FAIL` opens both with your `index_path` and `must_fix_count`. Drop *"So the verdict line must be **exactly** one of those two strings …"*.
  - **`## Read first`.** *"return a `blocker:` line … **in place of** the verdict line"* becomes an `outcome` of `blocker` whose `blocker` names the path and the refusal. Keep *"and write no files"*.
  - **`## Confidence bar`.** *"**`verdict: PASS` with no net-new findings is a correct outcome here …**"* becomes *"**An `outcome` of `PASS` with no net-new findings is a correct outcome here …**"*, the rest unchanged.
  - Leave `## Unsolicited dispatch guidance` byte-identical. Add no other words.
- [ ] **Phase C2, `plugin/instructions/plan_orchestration_instructions_core.md` → `### C2.1`.** Replace *"Parse the return:"*, its two `verdict:` bullets and the *"On **either** verdict, a **`## Questions`** section …"* paragraph with:
  > Read every `skeptic-reviewer` return in this phase — this dispatch's and each C2.2 re-dispatch's — as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:
  > - An `outcome` of `PASS` (no net-new findings — the agent wrote no file) → on this dispatch, skip straight to **Phase E**; on a C2.2 re-dispatch, return to C2.2's loop.
  > - An `outcome` of `FAIL` (findings exist at `` `skeptic-reviewer.index_path` ``, with `` `skeptic-reviewer.must_fix_count` `` Must Fix among them) → on this dispatch, continue to **C2.2**; on a C2.2 re-dispatch, return to C2.2's loop.
  > - An `outcome` of `blocker`, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) → `<escalate>`, naming the origin `Phase C2 skeptic-reviewer` and quoting `` `skeptic-reviewer.blocker` `` or naming the check that failed.
  >
  > On `PASS` and `FAIL`, `` `skeptic-reviewer.questions` `` is optional — absent or empty means none — and its items are **retained, not acted on**, exactly as in Phase B.1: no per-finding file, no readiness entry, no change to the route above. Carry them verbatim to `### D.2 Done summary`.
- [ ] **The Done summary, `### D.2`.**
  - In the **Skeptic review (Phase C2)** bullet, change *"if `skeptic-reviewer` returned `verdict: PASS`"* to *"if `skeptic-reviewer` returned an `outcome` of `PASS`"*.
  - In the **Review questions** bullet, replace the `skeptic-reviewer` clause, turning Task 2's intermediate text into exactly the final text stated above.
- [ ] **The autonomous fork, `plugin/instructions/plan_orchestration_instructions_autonomous.md`.**
  - In the `C2g` clause, change *"when the reviewer returned `verdict: PASS` with no net-new findings"* to *"when the reviewer returned an `outcome` of `PASS` with no net-new findings"*.
  - In the `*g` paragraph, change *"(an `outcome` of `PASS` from `business-parity-reviewer` or `architecture-reviewer`; `skeptic-reviewer`'s `verdict: PASS`)"* to *"(an `outcome` of `PASS` from `business-parity-reviewer`, `architecture-reviewer` or `skeptic-reviewer`)"*.
  - In the observation bullet, replace the `skeptic-reviewer` clause, turning Task 2's intermediate text into exactly the final text stated above.

**Verification:**

- `jq -e . plugin/schemas/skeptic-reviewer.return.json` exits 0; the `outcome` consts are exactly `PASS`, `FAIL` and `blocker`; and no variant lists `questions` in `required`.
- `grep -nE 'verdict: (PASS|FAIL)|index_path:|must_fix_count:|## Questions' plugin/agents/skeptic-reviewer.md` has no hit, except `index_path:` inside the `## Invocation contract` dispatch block, which is the caller's dispatch key and unchanged.
- `grep -nF 'End your reply with your return object:' plugin/agents/skeptic-reviewer.md` has exactly one hit, inside `## Output contract`.
- `grep -n '## Questions' plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/plan_orchestration_instructions_autonomous.md` has no hit.
- `grep -nE "skeptic-reviewer.{0,40}verdict: PASS|verdict: PASS.{0,40}skeptic" plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/plan_orchestration_instructions_autonomous.md` has no hit.
- Every `` `skeptic-reviewer.<field>` `` citation added names `index_path`, `must_fix_count`, `questions` or `blocker`.
