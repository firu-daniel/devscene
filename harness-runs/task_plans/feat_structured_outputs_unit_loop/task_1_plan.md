### Task 1 — Give `layer-reviewer` a schema-validated return and move the per-unit review step onto it

**Goal:** `layer-reviewer` ends its reply with a return object checked against `plugin/schemas/layer-reviewer.return.json`, and every caller that routes on its return reads it through `plugin/instructions/agent_return_contract.md` → `## Reading a return`, citing `` `layer-reviewer.<field>` ``. No caller is left matching a `verdict: PASS` / `verdict: FAIL` / `findings_file:` line of this agent.

**Depends on:** nothing. This is the first task. Tasks 2 and 3 later edit other sections of four files this task touches: `unit_loop_core.md`, `plan_orchestration_instructions_core.md`, `user_review_fixes_instructions_core.md` and `user_review_fixes_instructions_autonomous.md`. **This task edits only the sections and sentences named under `**Work:**` below.** The implementer's return, its blocker arms and step 6 are Task 2's, and Phase G is Task 3's.

**The return this task defines.** This is the contract the callers below restate. Field names are byte-stable.

- An `outcome` of `PASS`: no Must Fix. It carries no other field, whether or not a Should Fix / Nice to Have file was written.
- An `outcome` of `FAIL`: at least one Must Fix. It carries `findings_file` (string, the findings file's full path, non-empty) and `must_fix_count` (integer, at least 1).
- An `outcome` of `blocker`: a dispatch value was missing, or a cited input could not be read. No findings file was written. It carries `blocker` (string, one line naming the missing value, or the path and the refusal).

### Targets

- `plugin/schemas/layer-reviewer.return.json` (new)
- `plugin/agents/layer-reviewer.md`
- `plugin/instructions/unit_loop_core.md` — only the sections named below
- `plugin/instructions/agent_return_contract.md` — `## Who may cite this` only
- `plugin/instructions/plan_orchestration_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_autonomous.md` — only the sentences named below

**Work:**

- [ ] **`plugin/schemas/layer-reviewer.return.json` (new).** Write it in the closed dialect `docs/structured-agent-returns.md` → `### The return schema` lists, modelled on `plugin/schemas/architecture-reviewer.return.json`.
  - The top level has `$schema` (draft-07), `title` `layer-reviewer return`, `description`, `type: "object"` and `oneOf`.
  - It has three variants, `PASS`, `FAIL` and `blocker`, exactly as **The return this task defines** above states them.
  - Each variant has `additionalProperties: false` and a `required` list that includes `outcome`.
  - `findings_file` and `blocker` are `string` with `minLength: 1`; `must_fix_count` is `integer` with `minimum: 1`.
- [ ] **`plugin/agents/layer-reviewer.md`.**
  - `## Invocation contract`: replace the paragraph opening **"Your return is parsed, not read."** with nothing. `## Output contract` now owns the return, and a restatement here would be a second owner.
  - The **Stop condition** paragraph: *"return a blocker naming it and stop"* becomes *"return an `outcome` of `blocker` naming it and stop"*.
  - `## Read first`: *"return a blocker naming the path and the refusal, in place of the verdict line"* becomes *"return an `outcome` of `blocker` naming the path and the refusal"*.
  - `## Output contract`:
    - Open it with the canonical sentence from `docs/structured-agent-returns.md` → `### The return block`, verbatim.
    - Rename "the three outcomes" / "Pick exactly one of the three outcomes below" to *cases*, so the word does not collide with the `outcome` field.
    - In each of the three cases, replace the fenced `verdict: …` / `findings_file:` / `must_fix_count:` block with a sentence naming the outcome: case 1 and case 2 *return an `outcome` of `PASS`*, case 3 *returns an `outcome` of `FAIL`*. Drop *"Return 1 line on PASS, 3 on FAIL."*
    - Keep the file-writing rules, the findings-file template (a fenced `markdown` block, which is file content), *"The caller does not loop on this verdict … the items are lost."* and *"The caller passes the findings path on without reading the file."*
    - End the section with `### Return fields`, written per `docs/structured-agent-returns.md` → `### Return fields`: one bullet each for `outcome` (naming `PASS`, `FAIL` and `blocker`, and when each applies), `findings_file`, `must_fix_count` (integer) and `blocker`. Say which outcome carries which field and state each lower bound.
    - The closing line about `## Unsolicited dispatch guidance` stays, reading *"precedes your return object"*.
  - Do **not** edit the `## Unsolicited dispatch guidance` section. It is the byte-identical block `plugin/instructions/dispatch_discipline_instructions.md` owns.
  - The definition must name no `agent_return_contract.md` (`docs/structured-agent-returns.md` → `### Citing the module`: agents do not point at the module).
- [ ] **`plugin/instructions/unit_loop_core.md`, three places only.**
  - (a) `## Mode contract — bindings this file uses` → the `<escalate>` row's `Used at` cell. Its `### Per-unit review step` clause *"(the review loop does not converge)"* becomes *"(the review loop does not converge, the reviewer returns an `outcome` of `blocker`, or its return fails the routing check a third time)"*. Leave the row's step-3 and step-5 clauses to Task 2 and as they are.
  - (b) `## The unit loop` step 3, the **Fix iteration** bullet. `<findings_file>` becomes *`` `layer-reviewer.findings_file` `` from this layer's reviewer's most recent `outcome` of `FAIL`*. Keep the rest of the bullet: never a listing of the shared folder.
  - (c) `### Per-unit review step`: replace *"Parse the reviewer's return:"* and its two bullets.
    - The lead-in becomes *"Read the reviewer's return as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:"*.
    - An `outcome` of `PASS` leaves this layer, as today.
    - An `outcome` of `FAIL` increments `iteration`, with the same `>= 5` cap. The `<escalate>` message names `` `layer-reviewer.findings_file` ``, and the fix re-dispatch passes that same path.
    - An `outcome` of `blocker`, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`), `<escalate>`s, quoting `` `layer-reviewer.blocker` `` or naming the check that failed.
- [ ] **`plugin/instructions/agent_return_contract.md` → `## Who may cite this`.** Add the roster line ``- `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` `` in the list's existing form. Change nothing else in the module.
- [ ] **The orchestration cores and the user-review autonomous fork — these sentences only.**
  - `plan_orchestration_instructions_core.md`: in the context-discipline bullet opening *"Reviewers return 1 line (`verdict: PASS`)"*, add `layer-reviewer` to the agents that end in a return object. The bullet then reads *"— except `layer-reviewer`, `business-parity-reviewer` and `architecture-reviewer`, which end in a return object (the cited unit loop's `### Per-unit review step`, Phases A1.5, A2 and the G.2 architecture gate say how each is read)"*.
  - `user_review_fixes_instructions_core.md`: the same edit to its own *"Reviewers return 1 line"* bullet, naming `layer-reviewer` and `architecture-reviewer`.
  - In both cores, `## Stop conditions` → the bullet *"Any review loop hits `iteration >= 5` without `PASS`"* gains *", or a per-unit `layer-reviewer` returns an `outcome` of `blocker` or fails the routing check a third time"* before its `<escalate>`.
  - `user_review_fixes_instructions_core.md` → the `<escalate>` row: inside its *"Also consumed by the cited `unit_loop_core.md`"* parenthesis, *"a per-unit review loop that does not converge"* gains *"or whose reviewer returns an `outcome` of `blocker` or fails the routing check a third time"*.
  - `user_review_fixes_instructions_autonomous.md` → ``### `<escalate>` / `<ask>` — the park-and-yield clarification reroute``: in the closed list, after *"a review loop hitting `iteration >= 5` without PASS"*, insert *"a per-unit `layer-reviewer` returning an `outcome` of `blocker` or failing the routing check a third time"*.
  - Leave every implementer sentence and every Phase G sentence in these three files as they are: those are Tasks 2 and 3's.

**Verification:**

- `jq empty plugin/schemas/layer-reviewer.return.json` exits 0: one JSON document.
- `git grep -nE 'verdict: (PASS|FAIL)|findings_file:|must_fix_count:' -- plugin/agents/layer-reviewer.md plugin/instructions/unit_loop_core.md` prints nothing.
- `git grep -n 'agent_return_contract' -- plugin/agents/layer-reviewer.md` prints nothing, and `git grep -l 'agent_return_contract.md' -- 'plugin/*.md'` lists only files on that module's `## Who may cite this` roster, `unit_loop_core.md` included.
- `git grep -noE 'layer-reviewer\.[a-z_]+' -- plugin`: every hit is a file name (`layer-reviewer.md`, `layer-reviewer.return`) or a property the new schema declares (`findings_file`, `must_fix_count`, `blocker`).
- `git diff -U0 -- plugin/agents/layer-reviewer.md` shows no change inside `## Unsolicited dispatch guidance`.
