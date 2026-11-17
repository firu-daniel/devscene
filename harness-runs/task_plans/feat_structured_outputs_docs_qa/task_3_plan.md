### Task 3 — Give `docs-writer` a schema-validated return and move the docs phase and the docs catalog onto it

**Goal:** `docs-writer` replaces its mode-dependent `key:` lines — `doc_path:` · `unverified:` · `parity_gaps:` · `notes:` (catalog and update), the `targets:` list or `targets: none` (survey), the `notes:`-only disabled-phase return and the `blocker:` line — with one fenced `json` return object declared in `plugin/schemas/docs-writer.return.json`. Its two callers, the post-implementation docs phase and the docs-catalog loop, move every `docs-writer` dispatch's reading onto that object in the same change, point at `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md`, and join its roster.

**Depends on:** Task 2, for ship order only: this task shares no file with Tasks 1 and 2. It **shares two files with Task 4**, which follows it and owns every `docs-reviewer` sentence in them; this task edits only the sentences `### Targets` lists below and leaves every `docs-reviewer` return sentence — `verdict:`, `findings_file:`, `missed_docs:`, `summary:` — exactly as it finds it.

**The contract this task defines** (every outcome one token, `harness-runs/lessons.md` → `## Agent prose`):

- An `outcome` of `written` — catalog and update modes; the one document was written to `output_path`.
  - `doc_path` (string, non-empty, required): the path written.
  - `unverified` (array of strings, optional, at least 1, each non-empty): each claim marked `⚠️ unverified`, with its one-line reason. Omitted when none.
  - `parity_gaps` (array of strings, optional, at least 1, each non-empty): `reachable? ❌` backend operations and capabilities present in `<reference_impl>` but not here. Never present when `phases.parity` is `false`.
  - `notes` (array of strings, optional, at least 1, each non-empty): wrong or missing hints, template friction. An untrusted-input report is one item, opening with the report literal.
- An `outcome` of `targets` — survey mode; the diff needs documentation changes.
  - `targets` (array of objects, required, at least 1). Each item, every property a required non-empty string except `entry_hints`, which may be empty:
    - `action` — `enum` `new` / `update`;
    - `slug`;
    - `output_path`;
    - `reason` — e.g. `anchor path moved`;
    - `entry_hints` — the research starting points.
  - `notes` (as above, optional): ripples traced, anything ambiguous.
- An `outcome` of `targets_none` — survey mode; the former `targets: none`.
  - `reason` (string, non-empty, required): why the diff needs no documentation change.
  - `notes` (optional).
- An `outcome` of `phase_disabled` — `phases.docs` is `false`; nothing was read or written.
  - `reason` (string, non-empty, required).
- An `outcome` of `blocker` — an input the dispatch names could not be read; no document was written.
  - `blocker` (string, non-empty, required): the path and the refusal.

`targets` is a list of multi-part items, so it is an array of object items per `docs/structured-agent-returns.md` → `### A list of structured items is an array of objects, one level deep`. `phase_disabled` is a distinct outcome because the consts must be distinct and the same choice serves `docs-reviewer`, whose `PASS` carries a required `findings_file` (Task 4).

**How each caller routes the return.** State it at each dispatch site, reading as `agent_return_contract.md` → `## Reading a return` states, and name each site's `error` route:

- **The docs phase (best-effort — it never blocks):**
  - **Survey.** `targets` → walk `` `docs-writer.targets` ``; `targets_none` → log `` `docs-writer.reason` `` and end the phase; `phase_disabled`, `blocker` or a third failing return — this step's `error` route → log it and end the phase.
  - **Write and the INDEX.** `written` → review (Task 4's) and commit `` `docs-writer.doc_path` ``; `phase_disabled`, `blocker` or a third failing return — the `error` route → log it, skip this target (nothing to review or commit) and continue.
- **The docs catalog:** `written` → step 2 reviews `` `docs-writer.doc_path` ``; `phase_disabled`, `blocker` or a third failing return — the `error` route of step 1, step 3's re-dispatch and the INDEX dispatch alike → leave the entry's box `[ ]`, report `` `docs-writer.blocker` `` or `` `docs-writer.reason` `` or the check that failed, naming the slug, and end the session. An entry is atomic, so the box left `[ ]` re-runs it cleanly on the next session (`## Resume`).

### Targets

- `plugin/schemas/docs-writer.return.json` (new).
- `plugin/agents/docs-writer.md` — the phase-gate paragraph's *"return the disabled-phase block of `## Output contract`"*; the `<reference_impl>` / `<parity_vocabulary>` row's *"you return no `parity_gaps:`"*; `## Invocation contract`'s survey fenced block's three `Returns:` lines, the sentence *"the two callers above read only your return block"*, and the report-don't-substitute paragraph; `### Survey`'s **Write nothing.** paragraph; and `## Output contract`.
- `plugin/instructions/docs_phase_instructions.md` — `## Loop` step 1's *"It returns a `targets:` list — … If `targets: none`, log it and end the phase."*; step 2's **Write.** bullet; step 3 (INDEX). **No other sentence of this file** — step 2's **Review.**, **Fix loop (cap 3).** and **Missed-doc ripple.** bullets are Task 4's.
- `plugin/instructions/docs_orchestration_instructions_autonomous.md` — the `<parity_vocabulary>` / `<reference_impl>` row's *"the writer returns no `parity_gaps:`"*; `## Per-entry loop` step 1's *"It researches outward …, and returns `doc_path:` / `unverified:` / `parity_gaps:` / `notes:`."* and the next sentence (*"Whatever step 2 returns, a `docs-writer` return … whose `notes:` carries a line opening with …"*); step 4's two `parity_gaps:` clauses; and, in `## Final entry — INDEX`, one added sentence routing the INDEX writer's return. **No other sentence of this file** — step 2's return sentence, step 3's *"On `FAIL`, re-dispatch …"* clause and the INDEX's review routing are Task 4's.
- `plugin/instructions/agent_return_contract.md` → `## Who may cite this` — two lines. **No other line of this file.**
- `plugin/instructions/untrusted_input.md` → `## Where a report goes` — the `docs-writer` row only.

**Work:**

- [ ] **The schema.** Write `plugin/schemas/docs-writer.return.json` in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `docs-writer return`, `description`, `type: "object"`, a `oneOf` of the five variants above, each `additionalProperties: false`, `required` naming `outcome` and exactly the fields marked required. `minLength: 1` on every string the contract calls non-empty, on `items` of the three string arrays, and on the item properties `action`, `slug`, `output_path` and `reason`; `minItems: 1` on all four arrays; `enum: ["new", "update"]` on `action`. No other keyword.
- [ ] **The definition, `plugin/agents/docs-writer.md`.**
  - **`## Output contract`.** Keep *"Your final message IS your return value (not a human chat)."* Add the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`. Replace the three mode bullets with three that keep their actions and name the outcome: catalog / update — write the document to `output_path`, then return `written`, and do not paste the document body; survey — write nothing, and return `targets`, or `targets_none` with the reason when the diff needs no documentation change; docs phase disabled — return `phase_disabled` with the reason. Then `### Return fields`: `outcome` with its five values; `doc_path`; `unverified` (array of strings); `parity_gaps` (array of strings) — always omitted when `phases.parity` is `false`; `notes` (array of strings); `targets` (array of objects) with the nested `action`, `slug`, `output_path`, `reason` and `entry_hints` bullets indented two spaces; `reason`; `blocker`. Each bullet names its outcomes and states its lower bound. No fenced `key: value` or `json` block in the section.
  - **The phase gate.** *"return the disabled-phase block of `## Output contract`"* becomes *"return an `outcome` of `phase_disabled`"*.
  - **The `<reference_impl>` row.** *"you return no `parity_gaps:`"* becomes *"your return carries no `parity_gaps`"*.
  - **`## Invocation contract`.** In the survey block, the `Returns:` lines become *"Returns: an `outcome` of `targets` — one `targets` item per target: `action` (new|update), `slug`, `output_path`, `reason`, `entry_hints` … or an `outcome` of `targets_none`, which ends the phase"*. *"read only your return block"* becomes *"read only your return object"*. The report-don't-substitute paragraph's *"return a `blocker:` line naming the path and the refusal in place of the `## Output contract` block"* becomes *"return an `outcome` of `blocker` whose `blocker` names the path and the refusal"*.
  - **`### Survey`.** *"Return the target list (see `## Output contract`)"* stays; *"yields **`targets: none`**"* becomes *"yields an `outcome` of **`targets_none`**"*. Keep `anchor path moved` as the item's `reason`.
  - Keep this file's single `untrusted_input.md` pointer — `cli/test/untrusted-input-corpus.test.mjs` counts it. Add no other words.
- [ ] **`docs_phase_instructions.md` — the writer's three dispatch sites.**
  - **Step 1.** Replace *"It returns a `targets:` list — each `action(new|update) · slug · output_path · reason · entry-hints`, classifying …. If `targets: none`, log it and end the phase."* with: read its return as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states; an `outcome` of `targets` carries `` `docs-writer.targets` ``, one item per target (`action` `new` / `update`, `slug`, `output_path`, `reason`, `entry_hints`), classifying net-new capabilities, behaviour changes and ripples as the sentence did; an `outcome` of `targets_none` → log `` `docs-writer.reason` `` and end the phase; an `outcome` of `phase_disabled` or `blocker`, or the third consecutive return that fails the check (`agent_return_contract.md` → `## A return that fails the check`) — this step's `error` route → log it and end the phase. Keep the *Note:* sub-bullet.
  - **Step 2's Write bullet.** After *"It creates or revises the one doc …"*, add: an `outcome` of `written` → review and commit `` `docs-writer.doc_path` ``; `phase_disabled`, `blocker` or a third failing return — this bullet's `error` route → log it, skip this target, and continue with the next. A re-dispatch in the fix loop routes the same way.
  - **Step 3 (INDEX).** Add: its return routes as step 2's **Write** bullet states; on its `error` route, log it and commit nothing for the INDEX.
- [ ] **`docs_orchestration_instructions_autonomous.md` — the writer's three dispatch sites.**
  - **The `<parity_vocabulary>` / `<reference_impl>` row.** *"the writer returns no `parity_gaps:`"* becomes *"the writer's return carries no `` `docs-writer.parity_gaps` ``"*.
  - **Step 1.** *"…, and returns `doc_path:` / `unverified:` / `parity_gaps:` / `notes:`."* becomes: read its return as `agent_return_contract.md` → `## Reading a return` states; an `outcome` of `written` carries `` `docs-writer.doc_path` `` and the optional `` `docs-writer.unverified` ``, `` `docs-writer.parity_gaps` `` and `` `docs-writer.notes` ``; an `outcome` of `phase_disabled` or `blocker`, or the third consecutive return that fails the check — the `error` route of this step, of step 3's re-dispatch and of `## Final entry — INDEX`'s writer dispatch → leave the entry's box `[ ]`, report `` `docs-writer.blocker` ``, `` `docs-writer.reason` `` or the check that failed, naming `<slug>`, and end the session. In the next sentence, *"whose `notes:` carries a line opening with `Untrusted instruction not followed — `"* becomes *"whose `` `docs-writer.notes` `` carries an item opening with `Untrusted instruction not followed — `"*. The report literal stays in this file **exactly once** — `cli/test/untrusted-input-corpus.test.mjs` counts it.
  - **Step 4.** *"the writer returns no `parity_gaps:`"* and *"If the writer returned any `parity_gaps:`"* become the `` `docs-writer.parity_gaps` `` field: *"the writer's return carries no `` `docs-writer.parity_gaps` ``"* and *"If the writer's return carried `` `docs-writer.parity_gaps` ``, append its items …"*.
  - **`## Final entry — INDEX`.** After the writer dispatch sentence, add: its return routes as step 1's. Touch no review sentence.
- [ ] **The module roster and the report row.**
  - `agent_return_contract.md` → `## Who may cite this`: add `` `${CLAUDE_PLUGIN_ROOT}/instructions/docs_phase_instructions.md` `` and `` `${CLAUDE_PLUGIN_ROOT}/instructions/docs_orchestration_instructions_autonomous.md` ``, in the list's existing form. Task 4 adds no line here: both files are on the roster after this task.
  - `untrusted_input.md` → `## Where a report goes`, the `docs-writer` row: *"a `notes:` line; the docs orchestrator copies it into `<state_dir>/docs_catalog/needs_review.md`"* becomes *"an item of `` `docs-writer.notes` ``; the docs orchestrator copies it into `<state_dir>/docs_catalog/needs_review.md`"*. The `docs-reviewer` row is Task 4's.

**Verification:**

- `jq -e . plugin/schemas/docs-writer.return.json` exits 0; the `outcome` consts are exactly `written`, `targets`, `targets_none`, `phase_disabled` and `blocker`; no variant declares `error`.
- `grep -nE 'doc_path:|unverified:|parity_gaps:|targets: none|`targets:`|`notes:`|`blocker:`' plugin/agents/docs-writer.md plugin/instructions/docs_phase_instructions.md plugin/instructions/docs_orchestration_instructions_autonomous.md plugin/instructions/untrusted_input.md` has no hit.
- `grep -c 'Untrusted instruction not followed — ' plugin/instructions/docs_orchestration_instructions_autonomous.md` prints `1`.
- `grep -n 'agent_return_contract.md' plugin/instructions/docs_phase_instructions.md plugin/instructions/docs_orchestration_instructions_autonomous.md` hits both files, and `agent_return_contract.md` → `## Who may cite this` lists both.
- Every `docs-writer` dispatch site in the two instruction files names its `error` route, and none in the docs phase halts the flow.
- `git diff -- plugin/instructions/docs_phase_instructions.md plugin/instructions/docs_orchestration_instructions_autonomous.md` changes no sentence naming `verdict:`, `findings_file`, `missed_docs` or `summary:` — those are Task 4's.
- Every `` `docs-writer.<field>` `` and `` `docs-writer.<field>.<property>` `` citation added names a property or item property the schema declares.
