### Task 3 — Record the conventions pair's outcomes and field shapes in the decision record and update `docs/analyze.md`

**Goal:** Write the conventions pair's adoption into the decision record. That covers the outcomes chosen, why the three `prior_*` fields stay strings, and how the always-emitted `shared_document_divergences` is held. Then bring `docs/analyze.md`'s one sentence that spells a writer return field onto the new form.

**Depends on:** Tasks 1 and 2. Those tasks define the returns this task records:

- **`conventions-reviewer`:** `document_reviewed` (`document_path`, `findings`, `summary`), `corpus_reviewed` (`findings`, `summary`) and `blocker` (`blocker`). `findings` is an array of objects, omitted when none. Its items are `claim`, `evidence` and `correction`, plus `document_path` and `check_id` on `corpus_reviewed`.
- **`conventions-writer`:** `written` and `merged`, the old `action_taken:` values carried over as the outcome, plus `blocker`.
  - `conflicts`, `shared_document_divergences` and `findings_declined` are arrays of objects.
  - `not_determined_lines` is an array of strings.
  - `prior_document` is an `enum`. `prior_prompts` and `prior_rule_block` are strings that keep their `none` / `n/a` values.
  - `shared_document_divergences` is `required` with no `minItems`, `[]` meaning none. `plugin/commands/analyze.md` names it optional for the routing check.

This task changes no plugin file, and records what those tasks shipped rather than re-deciding it. Read the two schema files and `analyze.md`'s two pointer paragraphs, (4a) and (4c), before writing, and record what they say.

**How this task's implementer reads the conventions.** This is the catch-all layer, so read every configured `layers[].conventions` document. In particular, read `.claude/context/conventions.md` → `## Documents of record`: a decision record states what was decided and what it was chosen over. Lay out every edit to `docs/structured-agent-returns.md` in this tree's prose. That document's `### The return block` fenced sentence is read verbatim by the static schema check, so do not touch that subsection.

### Targets

- `docs/structured-agent-returns.md`
- `docs/analyze.md` — `## 8. How this is verified`, item 2 only.

**Work:**

- [ ] `docs/structured-agent-returns.md` → `### One discriminator, `outcome`, held to the graph`: add one paragraph. It records that neither conventions agent is dispatched by the graph, so neither is held to graph outcome keys. The writer's old `action_taken:` values became its outcomes `written` and `merged`, and the field is folded into `outcome`. The reviewer's outcomes `document_reviewed` and `corpus_reviewed` name the axis reviewed, never a verdict, because its contract carries none. An axis-named outcome lets `## Reading a return` step 3 refuse a return of the wrong axis.
- [ ] `docs/structured-agent-returns.md` → `### A list of structured items is an array of objects, one level deep`: add one paragraph. It names the conventions pair's object lists — `conventions-reviewer.findings`, and the writer's `conflicts`, `shared_document_divergences` and `findings_declined` — and states the one choice weighed and declined. The writer's `prior_prompts` and `prior_rule_block` stay strings carrying `none` / `n/a`, because they are opaque values the caller forwards byte for byte into the next dispatch. The receiving contracts already define those values, and no caller parses or routes on their lines. The alternative was an array, which would change two receiving tables and reviewer checks (1) and (2) for nothing a caller reads. State its cost: the static check cannot hold an item of a forwarded string.
- [ ] `docs/structured-agent-returns.md` → `### Validation on each path, and why no validator script`: add one paragraph about the always-emitted list. `conventions-writer.shared_document_divergences` is `required` with no `minItems`, and `[]` means none. That keeps the writer's "always emitted" property in the schema and its prose. The routing caller names it optional, because step 4 reads `[]` as empty. So on the orchestrator path an omitted field passes the routing check, which is that section's stated cost of a lighter check. Note also that the old writer sentence citing a caller stop condition on an omitted field named a stop `analyze.md` never stated.
- [ ] `docs/analyze.md` → `## 8. How this is verified`, item 2: re-spell its `shared_document_divergences:` clause to the new form. Its producers stay every document-axis writer return, and its sole consumer stays the reconciliation dispatch. The field becomes `` `conventions-writer.shared_document_divergences` ``, and *"`none` on the corpus axis"* becomes *"empty on the corpus axis"*. Leave the rest of item 2, §6's *"four sites"* sentence, and §11 and §12 untouched: they cite the dispatch tables and the wire literal, which are unchanged.

**Verification:**

- `git diff -U0 HEAD -- docs/structured-agent-returns.md` touches neither `### The return block` nor `## 3. Measured, and not yet measured`. The branch adds no measured claim (task prompt, `## Constraints`), so no §3 entry is owed.
- Every outcome and field the new paragraphs name appears in `plugin/schemas/conventions-writer.return.json` or `plugin/schemas/conventions-reviewer.return.json`. Check each with `jq -e '[.oneOf[].properties | keys[]] | unique' <schema>` against the names written.
- `grep -n 'shared_document_divergences:' docs/analyze.md` prints nothing. `grep -n 'Reviewer finding not applied' docs/analyze.md` still prints §6's and §12's sentences unchanged.
- Each new paragraph states what was chosen and what it was chosen over, or its cost, per `## Documents of record`.
