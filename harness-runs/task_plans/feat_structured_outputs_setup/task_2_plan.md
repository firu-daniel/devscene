### Task 2 — Give `conventions-writer` a schema-validated return and move every read of it in `analyze.md` onto it

**Goal:** `conventions-writer` returns one declared JSON object on both axes and on every action, held by `plugin/schemas/conventions-writer.return.json`. Every sentence in `plugin/commands/analyze.md` that reads a writer return field reads the object form, and `Reviewer finding not applied — ` still agrees across the three files that carry it.

**Depends on:** Task 1. Task 1 makes `conventions-reviewer` return an object whose `findings` items carry `claim`, `evidence` and `correction`, plus `document_path` and `check_id` on `corpus_reviewed`. It rewrites the writer's `## Invocation contract` corpus-axis `findings` bullets and *"The prefix is the discriminator"* paragraph to that form. It adds `analyze.md`'s reviewer-return pointer in (4c), its (4c) findings sentence, its (4d) grouping sentence and iteration 2's no-findings clause. It also puts `analyze.md` on `agent_return_contract.md` → `## Who may cite this`. **Do not edit any of those sentences.** This task owns every other changed sentence in both files.

### Targets

- `plugin/schemas/conventions-writer.return.json` (new)
- `plugin/agents/conventions-writer.md` — every changed sentence except Task 1's.
- `plugin/commands/analyze.md` — every sentence that reads a writer return field, plus the writer-return pointer.

**The return this task defines:**

| `outcome` | Fields |
|---|---|
| `written`, `merged` (two variants, identical properties; the old `action_taken:` values carried over as the outcome, so `action_taken` is no longer a field) | **Required:** `document_path` (string, minLength 1); `not_determined` (integer, minimum 0); `shared_document_divergences` (array of objects, **no `minItems`**, `[]` when none); `evidence` (string, minLength 1); `prior_document` (string, `enum` `skeleton`/`filled`/`absent`); `prior_prompts` (string, minLength 1 — the verbatim items one per line, or `none`, or `n/a`); `prior_rule_block` (string, minLength 1 — the verbatim block, or `none`, or `n/a`). **Optional:** `not_determined_lines` (array of strings, minItems 1); `conflicts` (array of objects, minItems 1); `findings_applied` (integer, minimum 0 — fix dispatches only, omitted on a write dispatch); `findings_declined` (array of objects, minItems 1); `notes` (string, minLength 1) |
| `blocker` | `blocker` (string, minLength 1, required) — a missing dispatch value, or a corpus-axis `findings` entry that is neither origin |

Object items, every property a required string with minLength 1:

- `conflicts`: `prose` (what the adopter's harvested prose says, naming its source) and `code` (what the code does, naming the file and the symbol or quoted substring).
- `shared_document_divergences`: `shared_document_says`, `code_shows` and `source` (the file plus the symbol or quoted substring it was read off).
- `findings_declined`: `finding` and `reason`. `finding` is a forwarded divergence's line verbatim, its `Layer-writer divergence — ` prefix intact, or a reviewer finding's `check_id` where it has one followed by its `claim`.

**Work:**

- [ ] `plugin/schemas/conventions-writer.return.json`: write the three variants above in the closed dialect `docs/structured-agent-returns.md` → `### The return schema` lists. The `prior_*` stay strings because they are forwarded opaque values, as the story index's `## Context` states.
- [ ] `plugin/agents/conventions-writer.md` → `## Output contract`:
  - Keep the opening *"Your final message IS your return value (not a human chat). Field names byte-stable"*. `plugin/instructions/mention_reading.md` and `.claude/context/plugin.md` both quote *"Field names byte-stable"* from here.
  - Replace the `- `<field>:`` list with the canonical return-block sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`.
  - Add `### Return fields`: one bullet per property, each non-string property annotated, and the item properties nested two spaces under their `(array of objects)` field.
  - Carry over every rule the old bullets held:
    - declining a document is not an outcome;
    - `not_determined_lines` quotes each `## Not determined` line verbatim, every `Reviewer finding not applied — ` line included;
    - `conflicts` and `shared_document_divergences` do not overlap and neither absorbs the other;
    - `shared_document_divergences` is **always emitted**, `[]` on every `pass: corpus` dispatch, on `shared_document: none`, and when nothing was found. That replaces *"an omitted field is what the caller's stop condition fires on"*;
    - the three `prior_*` descriptions, unchanged in content.
  - Keep the two closing paragraphs, *"The three `prior_*` fields are the pre-write state …"* and *"The caller builds its report from this return alone …"*. Change only their colon spellings: *"re-emit the whole block"* becomes *"re-emit the whole return object"*.
- [ ] `plugin/agents/conventions-writer.md`, outside `## Output contract` and outside Task 1's sentences:
  - **Stop condition** (`## Invocation contract`): *"return a blocker naming which value is missing"* becomes *"return outcome `blocker`, naming …"*.
  - **Colon spellings in `## Scope`, `## The document` and `## The fix dispatch`:**
    - `## Scope`: *"your return's `evidence:` field"* becomes `` `evidence` ``;
    - the count bullet's `` `evidence:`, `not_determined_lines:` `` loses its colons;
    - the divergence paragraph's *"go to `shared_document_divergences:` in your return"* and *"the field is `none`"* become the field name and *"`[]`"*.
  - **The absent-document paragraph:** *"Report it as `prior_document: absent` with `prior_prompts: n/a` and `prior_rule_block: n/a`"* is re-spelled as field values: `prior_document` `absent`, `prior_prompts` and `prior_rule_block` `n/a`.
  - Leave both `Reviewer finding not applied — ` sentences byte-identical: `## The document`'s `## Not determined` bullet and `## The fix dispatch`'s corpus paragraph.
- [ ] `plugin/commands/analyze.md`, (4a) and (4c):
  - **(4a), the pointer.** Before *"Keep every `shared_document_divergences:` line …"*, add one paragraph. It says to read every `conventions-writer` return this command receives — write, document fix, reconciliation and corpus fix — as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:
    - an `outcome` of `written` or `merged` routes;
    - `` `conventions-writer.not_determined_lines` ``, `` `conventions-writer.conflicts` ``, `` `conventions-writer.findings_declined` `` and `` `conventions-writer.shared_document_divergences` `` are optional for the check, absent or empty meaning none;
    - `` `conventions-writer.findings_applied` `` is read on fix returns only;
    - an `outcome` of `blocker`, or the third consecutive failing return (`## A return that fails the check`), stops the run and reports `` `conventions-writer.blocker` `` or the check that failed, naming the document.
  - **(4a), the divergences paragraph.** Rewrite it to keep every `` `conventions-writer.shared_document_divergences` `` item from the write and document-fix returns; `[]` contributes nothing.
  - **(4c).** Re-spell *"taken verbatim from that document's write return: `prior_document` (…), `prior_prompts` and `prior_rule_block`"* as `` `conventions-writer.prior_document` ``, `` `conventions-writer.prior_prompts` `` and `` `conventions-writer.prior_rule_block` ``, forwarded verbatim.
- [ ] `plugin/commands/analyze.md`, (4d.0), (4d), step 2's survey bullet and step 6:
  - **(4d.0) gate.** The non-empty test reads the collected items.
  - **(4d.0) rendering.** Each collected item is sent as **one line**: the exact literal `Layer-writer divergence — `, then its `shared_document_says`, `code_shows` and `source`. That prefix is the discriminator Task 1's writer paragraph names.
  - **(4d.0) declines.** *"in its `findings_declined:` return"* becomes `` `conventions-writer.findings_declined` ``. Keep the sentence's `Reviewer finding not applied — ` literal byte-identical.
  - **(4d) iteration 1.** *"carries `shared_document_divergences: none`"* becomes *"carries an empty `` `conventions-writer.shared_document_divergences` ``"*.
  - **(4d) iteration 2.** *"whose fix return reports at least one finding applied"* becomes *"whose fix return's `` `conventions-writer.findings_applied` `` is at least 1"*.
  - **Step 2's survey bullet.** Its *"that record is the `evidence:` clause step 6 prints for the `project` rows"* drops the colon spelling and becomes *"the evidence clause"*. The `project` target has no writer, so that clause never read a return field.
  - **Step 6.** Each read of the old fields moves onto the citation form, and the report's content is unchanged:
    - the action taken is the writer's outcome, `written` or `merged`;
    - `evidence`, `not_determined_lines`, `conflicts`, `findings_applied` and `findings_declined` are each cited as `` `conventions-writer.<field>` ``;
    - a conflict prints its `prose` and `code`;
    - a declined finding prints its `finding` and `reason`, with the `Layer-writer divergence — ` prefix intact where `finding` carries it.

**Verification:**

- `jq -e '.oneOf | map(.properties.outcome.const)' plugin/schemas/conventions-writer.return.json` prints exactly `written`, `merged`, `blocker`. `jq -e '.oneOf[0].required' plugin/schemas/conventions-writer.return.json` includes `shared_document_divergences`.
- ``grep -nE 'action_taken|`(not_determined_lines|shared_document_divergences|findings_applied|findings_declined|prior_document|prior_prompts|prior_rule_block|evidence|conflicts|notes):' plugin/agents/conventions-writer.md plugin/commands/analyze.md`` prints nothing. The leading backtick keeps `` `context_notes:` ``, a dispatch-discipline term, out of the match.
- `grep -n 'Field names byte-stable' plugin/agents/conventions-writer.md` is non-empty. That is the phrase `plugin/instructions/mention_reading.md` quotes from `## Output contract`.
- `grep -n 'Reviewer finding not applied — ' plugin/agents/conventions-writer.md plugin/agents/conventions-reviewer.md plugin/commands/analyze.md` prints a hit in every one of the three files. Every hit spells the literal byte-identically, an em dash followed by one space. In each file the hit sits in the same role as before: the writer's `## Not determined` duty and corpus-decline paragraph, the reviewer's check (11), and `analyze.md`'s (4d.0) and step-6 sentences.
- `grep -n 'Layer-writer divergence — ' plugin/commands/analyze.md plugin/agents/conventions-writer.md` still prints the (4d.0) rendering sentence and the writer's discriminator paragraph.
- `grep -n 'conventions-writer\.' plugin/commands/analyze.md`: every `` `conventions-writer.<field>` `` / `` `conventions-writer.<field>.<property>` `` it prints names a field or item property of the new schema.
- `git diff -U0 HEAD -- plugin/agents/conventions-writer.md plugin/commands/analyze.md` leaves Task 1's sentences, listed under **Depends on:**, untouched.
