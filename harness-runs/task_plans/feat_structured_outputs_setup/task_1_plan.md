### Task 1 — Give `conventions-reviewer` a schema-validated return and move its readers in `analyze.md` and the writer's invocation contract onto it

**Goal:** `conventions-reviewer` returns one declared JSON object on both axes, held by `plugin/schemas/conventions-reviewer.return.json`. Every reader of that return — `plugin/commands/analyze.md`'s review routing, and the corpus-axis `findings` description in `plugin/agents/conventions-writer.md` → `## Invocation contract` — reads the object form and nothing else.

**Where this task stops.** This task changes only the reviewer's return and the sentences that read it. Every sentence that reads a `conventions-writer` return field is **Task 2's**, including `analyze.md`'s `shared_document_divergences:`, `prior_*`, `findings_applied:`, `findings_declined:` and step-6 report sentences, and the writer's own `## Output contract`. Leave those byte-identical: at the end of this task the writer still returns its old `key: value` block, and those sentences still read it correctly. The sentences this task owns in the two shared files are listed under **Work:** and in the story index's `## Context`. Edit no other sentence in those files.

### Targets

- `plugin/schemas/conventions-reviewer.return.json` (new)
- `plugin/agents/conventions-reviewer.md`
- `plugin/agents/conventions-writer.md` — `## Invocation contract`'s corpus-axis `findings` origin bullets and the *"**The prefix is the discriminator.**"* paragraph only.
- `plugin/commands/analyze.md` — (4c) and (4d) review-routing sentences only.
- `plugin/instructions/agent_return_contract.md` — `## Who may cite this` only.

**The return this task defines** (Task 2's writer prose and Task 3's record both restate it):

| `outcome` | Fields |
|---|---|
| `document_reviewed` | `document_path` (string, minLength 1, required); `findings` (array of objects, `minItems` 1, **omitted when there is no finding**), each item `claim`, `evidence`, `correction` (all strings, minLength 1, all required); `summary` (string, minLength 1, required) |
| `corpus_reviewed` | `findings` (array of objects, `minItems` 1, omitted when none), each item `document_path`, `check_id` (`C1`–`C6`, or a document-pass check number for a `target: project` finding), `claim`, `evidence`, `correction` (all strings, minLength 1, all required); `summary` (string, minLength 1, required) |
| `blocker` | `blocker` (string, minLength 1, required) — a missing dispatch value, a re-dispatch for an already-reviewed document, or a corpus dispatch with an out-of-range `iteration` |

**Work:**

- [ ] `plugin/schemas/conventions-reviewer.return.json`: write the three variants in the table above, in the closed dialect `docs/structured-agent-returns.md` → `### The return schema` lists. Follow `plugin/schemas/prompt-injection-reviewer.return.json` → `findings` for the object-item shape. The top-level `description` says the reviewer writes no file, so this object is the only carrier of its findings.
- [ ] `plugin/agents/conventions-reviewer.md` → `## Output contract`:
  - Replace the two `**On pass: …**` bullet lists with the canonical return-block sentence, copied verbatim from `docs/structured-agent-returns.md` → `### The return block`.
  - Add a `### Return fields` subsection per that document's `### Return fields`:
    - one bullet each for `outcome`, `document_path`, `findings` (array of objects), `summary` and `blocker`;
    - the five item properties as two-space-indented bullets under `findings`, with `document_path` and `check_id` marked `corpus_reviewed` only.
  - Carry over into those bullets every rule the old lists held:
    - each `evidence` names the file and the symbol or quoted substring, and on the corpus axis the sibling document and a quoted anchor, never a line coordinate;
    - each `correction` is concrete;
    - a finding landing in a `role: context` member is returned the same way, and the caller decides dispatchability;
    - `document_path` as a top-level field is `document_reviewed` only.
  - Keep *"Field names byte-stable"* and *"you write no file, on either axis"*. Keep the closing sentence *"A finding you cannot state as a concrete correction …"*.
- [ ] `plugin/agents/conventions-reviewer.md`, outside `## Output contract`:
  - **Stop condition** and **Dispatch counts** in `## Invocation contract`: the "return a blocker naming which value is missing" and each "caller bug — say so, and stop" become *"return outcome `blocker`, naming …"*.
  - **`## The corpus pass — what to verify`**:
    - (c)'s *"say so in `summary:`"* becomes *"say so in `summary`"*;
    - *"A coherent corpus returns `findings: none`"* becomes *"omits `findings`"*.
  - **`## What you do not do`**: add one clause to *"No severity band and no verdict field"* stating that `outcome` names the axis reviewed, never a judgement.
  - Leave the `prior_*` rows of the dispatch tables and check (11)'s `Reviewer finding not applied — ` literal byte-identical.
- [ ] `plugin/agents/conventions-writer.md` → `## Invocation contract`, Task 1's sentences only:
  - Rewrite the **Corpus review findings** bullet. Its findings are the reviewer's finding objects, verbatim. Each names this document in `` `conventions-reviewer.findings.document_path` `` and its check in `` `conventions-reviewer.findings.check_id` ``, and carries `claim`, `evidence` and `correction`.
  - Leave the **Forwarded layer-writer divergences** bullet's content as it is: a line carrying the exact literal prefix `Layer-writer divergence — ` and no check id.
  - Rewrite *"**The prefix is the discriminator.**"* so it reads: an object carrying `check_id` is a corpus review finding, and a line carrying the prefix is a forwarded divergence. Anything else is a malformed dispatch, not a third origin.
- [ ] `plugin/commands/analyze.md` and the module roster:
  - **(4c), the pointer.** After the review dispatch's field list, add one paragraph. It says to read every `conventions-reviewer` return in this step and in (4d) as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:
    - an `outcome` of `document_reviewed` routes a document-axis review, and an `outcome` of `corpus_reviewed` routes a corpus review;
    - `` `conventions-reviewer.findings` `` is optional: absent means none;
    - an `outcome` of `blocker`, or the third consecutive return that fails the check (`## A return that fails the check`), stops the run and reports `` `conventions-reviewer.blocker` `` or the check that failed, naming the document.
  - **(4c), the findings sentence.** Rewrite *"Take the reviewer's `findings:` return. If it is `none`, that document is done. Otherwise …"* to read `` `conventions-reviewer.findings` ``: absent, the document is done; otherwise re-dispatch the writer once, with those finding objects forwarded verbatim as `findings`. The rest of that sentence stays as it is.
  - **(4d) iteration 1.** *"Take its `findings:` and group them by the `document_path` each names"* becomes a grouping by `` `conventions-reviewer.findings.document_path` ``.
  - **(4d) iteration 2.** *"when iteration 1 returned `findings: none`"* becomes *"when iteration 1's return carried no `` `conventions-reviewer.findings` ``"*.
  - **The roster.** Add `` `${CLAUDE_PLUGIN_ROOT}/commands/analyze.md` `` to `agent_return_contract.md` → `## Who may cite this`, in the existing bullet form.

**Verification:**

- `jq -e '.oneOf | map(.properties.outcome.const)' plugin/schemas/conventions-reviewer.return.json` prints exactly the three outcomes in the table: `document_reviewed`, `corpus_reviewed`, `blocker`.
- ``grep -nE 'findings: none|`summary:`|`findings:`|`document_path:`' plugin/agents/conventions-reviewer.md`` prints nothing. The dispatch tables spell `document_path` with no colon, so they do not match.
- `grep -nE "reviewer's .findings:. return|Take its .findings:|returned .findings: none" plugin/commands/analyze.md` prints nothing.
- `grep -n 'agent_return_contract.md' plugin/commands/analyze.md` is non-empty, and `grep -n 'commands/analyze.md' plugin/instructions/agent_return_contract.md` prints the new roster line.
- `grep -n 'conventions-reviewer\.' plugin/commands/analyze.md plugin/agents/conventions-writer.md`: every `` `conventions-reviewer.<field>` `` / `` `conventions-reviewer.findings.<property>` `` it prints names a field or item property of the new schema.
- `git diff -U0 HEAD -- plugin/agents/conventions-writer.md plugin/commands/analyze.md` changes only the sentences **Work:** names. In particular:
  - nothing in the writer's `## Output contract` changes;
  - no `analyze.md` sentence naming `shared_document_divergences:`, `prior_*`, `findings_applied:`, `findings_declined:` or `action_taken:` changes.
