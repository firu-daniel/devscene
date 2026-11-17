### Task 2 — Give `layer-implementer` a schema-validated return and move the unit loop and stop conditions onto it

**Goal:** `layer-implementer` ends its reply with a return object checked against `plugin/schemas/layer-implementer.return.json`. The unit loop routes on its `outcome` through `plugin/instructions/agent_return_contract.md` → `## Reading a return`, and takes the progress-line clauses from `` `layer-implementer.cause` `` and `` `layer-implementer.flags` `` rather than by position in a `blocker:` line. The returned `cause` stays the same text as the detail file's `**Cause:** ` line, which the commit step writes into the commit body.

**Depends on:** Task 1. Task 1 added `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` to `agent_return_contract.md` → `## Who may cite this`, so this task adds no roster line.

- In `unit_loop_core.md`, Task 1 owns the `<escalate>` row's `### Per-unit review step` clause, the **Fix iteration** bullet of step 3 and the whole of `### Per-unit review step`. Do not edit them.
- In the two orchestration cores and the user-review autonomous fork, Task 1 owns the *"Reviewers return"* bullets, the reviewer clauses and the review-loop stop bullets.
- Task 3 owns every Phase G sentence, and the `test-fix-plan-writer` rows of `untrusted_input.md` → `## Where a report goes`.
- **This task edits only the sections and sentences named under `**Work:**`.**

**The return this task defines.** This is the contract both the agent and the callers below are written to. Field names and outcome values are byte-stable.

- An `outcome` of `implemented`: the unit's work for this layer is done. It may carry `flags` (array of strings, each non-empty, omitted when empty): one item per thing the orchestrator should flag to the user. That covers today's `## Output contract` item 7, every `**Unactioned under a gate:**` part and every refused task-data instruction included.
- An `outcome` of `prohibited`: a standing prohibition or an unsatisfiable gate admitted the disposition route, and the `## Disposition` record is written. It carries `cause` (string, non-empty, one line).
- An `outcome` of `already passing`: row `G.4` only. The row-`G.4` check closed the unit, and the `## Already passing` record is written. It carries `cause` (string, non-empty, one line).
- An `outcome` of `blocker`: a transient stop — everything the two disposition paragraphs exclude. It carries `blocker` (string, non-empty, one line naming the cause).
- These outcome values follow `docs/structured-agent-returns.md` → *An agent's own `error:` return becomes an outcome, never `error`*. The halting form becomes `blocker`. The two non-halting marked forms keep the literal a caller matched before as their outcome value: `prohibited` and `already passing`, the latter with its space.
- Parts 1–6 of today's report stay prose above the return object. No caller routes or records on them (story index `## Context`).

### Targets

- `plugin/schemas/layer-implementer.return.json` (new)
- `plugin/agents/layer-implementer.md`
- `plugin/instructions/unit_loop_core.md` — only the sections named below
- `plugin/instructions/plan_orchestration_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_autonomous.md`, `plugin/instructions/untrusted_input.md` — only the sentences named below

**Work:**

- [ ] **`plugin/schemas/layer-implementer.return.json` (new).**
  - Write it in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`, with the four variants exactly as **The return this task defines** states them.
  - `flags` is `type: "array"` with `items: { "type": "string", "minLength": 1 }`, and appears in `implemented` only, not required.
  - `cause` and `blocker` are `string` with `minLength: 1`, each required in its variant.
  - Every variant has `additionalProperties: false`.
- [ ] **`plugin/agents/layer-implementer.md`, every section except `## Output contract`.** Turn each return reference into an outcome reference and change nothing else in those paragraphs:
  - `## Invocation contract` → **Stop condition**: *"return a blocker naming it"* becomes *"return an `outcome` of `blocker` naming it"*.
  - `## Scope`: the plan-needs-splitting stop and the missing-symbol stop each say they return an `outcome` of `blocker`.
  - `## Read first`: *"return a blocker naming the path and the refusal"* becomes *"return an `outcome` of `blocker` naming the path and the refusal"*.
  - The row-`G.4` check: *"return the `already passing — ` form"* becomes *"return an `outcome` of `already passing`"*. *"goes in item 5, not a blocker"* stays: item 5 is still prose.
  - **The already-passing record.** and **The disposition record.**: the `**Cause:** ` line is *"the same text as the return's `cause`"*, replacing each quotation of the `blocker: … — <one-line cause>; …` form. Keep *"which the commit step reads for the commit's body record"* unchanged.
  - **A sandbox refusal is the boundary working**: *"a transient `blocker:` naming the refused path or host"* becomes *"an `outcome` of `blocker` naming the refused path or host"*. Keep that paragraph's bold lead sentence byte-identical, because `test-fix-plan-writer.md` cites it by that text.
  - **Unsatisfiable-gate disposition**: *"carry it in item 7"* becomes *"carry it in `flags`"*.
  - The closing *"stop and surface the conflict in your output"* says it returns an `outcome` of `blocker`.
  - Add no pointer to `agent_return_contract.md`: agents do not point at the module.
- [ ] **`plugin/agents/layer-implementer.md` → `## Output contract`.**
  - Open it with the canonical sentence from `docs/structured-agent-returns.md` → `### The return block`, verbatim.
  - Keep items 1–6 as the numbered report written above the return object, unchanged except that item 5's wording stays as is. Delete item 7: its content moves to the `flags` bullet.
  - Replace *"If you are blocked, return one of three named forms; the caller discriminates on the string …"* and its three form bullets with `### Return fields`, per `docs/structured-agent-returns.md` → `### Return fields`:
    - `outcome` names `implemented`, `prohibited`, `already passing` and `blocker`, with when each applies. Carry over today's admission rules: `prohibited` only when a disposition paragraph admits it and the `## Disposition` record is written; `already passing` only on a row-`G.4` dispatch, after the check closed the unit and the `## Already passing` record is written; `blocker` for everything else.
    - `flags` (array of strings) carries today's item-7 text: a part left unimplemented under a gate, carried verbatim from its `**Unactioned under a gate:**` sub-bullet; a change that needs a deploy to verify; one that affects an in-flight session or a permission file the user must reload.
    - `cause` — `prohibited` / `already passing`: carry over today's rules. One line, self-contained, no newline. The same text as the detail file's `**Cause:** ` line. A `prohibited` cause names its class in plain words, keeping the two worked examples. The `already passing` default is *"already passing after an earlier fix"* plus how that was established.
    - `blocker` — `blocker`: one line naming the cause.
  - Keep *"The two … are mutually exclusive on one return: a layer both refused and already passing is dispositioned"*, reworded to outcomes (it returns `prohibited`).
  - Drop the delimiter-literal clause (*"free of … `; disposition appended to ` or `; record appended to `"*): no delimiter exists any more.
  - Keep *"Keep the return message tight."*
  - The section carries no fenced `key: value` block and no fenced `json` block.
- [ ] **`plugin/instructions/unit_loop_core.md` — these places only.**
  - (a) `## Mode contract — bindings this file uses`:
    - In the `<escalate>` row, the step-3 clause becomes *"(the implementer returns an `outcome` of `blocker`, an `outcome` of `already passing` on a row other than `G.4`, or a return that fails the routing check a third time; an `outcome` of `prohibited`, or of `already passing` on row `G.4`, takes `### The dispositioned outcome` and never reaches this binding)"*.
    - In the paragraph **"The third unit outcome adds none either."**, *"Its second marker, `already passing — `,"* becomes *"Its second outcome, `already passing`,"*.
  - (b) `## The unit loop` step 3, the paragraph opening *"Receive its return and read a blocker line in **three arms**"*. Rewrite it to read the return as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states:
    - An `outcome` of `implemented`: continue, keeping each `` `layer-implementer.flags` `` item for step 6.
    - State once, here, that `` `layer-implementer.flags` `` is **optional**: an absent or empty field means nothing to flag, never a failed return, and it is not a field the routing check reads for `implemented`. An `implemented` return that omits `flags` passes `## Reading a return` and continues. Model the wording on `plan_orchestration_instructions_autonomous.md`'s *"(an absent or empty field means no corpus debt, never "the planner did not check")"*.
    - Name the fields the check does read, per outcome: `cause` for `prohibited` and `already passing`, `blocker` for `blocker`, none beyond `outcome` for `implemented`.
    - An `outcome` of `prohibited`: takes `### The dispositioned outcome`.
    - An `outcome` of `already passing` on row `G.4` only: takes `#### The already-passing close`.
    - An `outcome` of `blocker`, an `outcome` of `already passing` on any other row, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) `<escalate>`s, quoting `` `layer-implementer.blocker` `` or naming the check that failed.
    - Keep the fail-safe sentence, reworded: an outcome the row does not admit escalates.
  - (c) Step 6:
    - *"every line an implementer of this unit returned under its `## Output contract` item 7"* becomes *"every item of `` `layer-implementer.flags` `` an implementer of this unit returned (none when the field was absent or empty, as step 3 states)"*. Point back at step 3's optional-field sentence; do not restate it.
    - Replace the **by position** sentence (*"The cause is taken from the implementer's return **by position, not by judgement**: …"*) with: the cause is `` `layer-implementer.cause` ``, carried verbatim and never re-worded.
    - Keep *"One clause, one cause"* and the clause names `dispositioned: ` / `already passing: `.
  - (d) `### The dispositioned outcome`, its opening paragraph and **What already exists on disk**: *"reached by a blocker line carrying the `prohibited — ` marker, or on row `G.4` the `already passing — ` marker"* becomes *"reached by an `outcome` of `prohibited`, or on row `G.4` an `outcome` of `already passing`"*. The parenthetical about `<one-line cause>` becomes the `cause` field. *"the marker on the return is the whole decision"* becomes *"the outcome is the whole decision"*.
  - (e) `#### The already-passing close`, first paragraph, and `### Named exceptions` → `#### Row G.4 — test-fix items`, third bullet: *"close on the `already passing — ` marker"* / *"whose return carries `already passing — ` — full form …"* become the `already passing` outcome.
  - Do **not** touch **The commit's record.** paragraph: its `mark <unit token> already passing — <cause>` is the commit-body line, which is file content and unchanged.
- [ ] **The other callers — these sentences only.**
  - `plan_orchestration_instructions_core.md`:
    - The context-discipline bullet *"Implementers return a short list (files + deviations + blockers)."* becomes *"Implementers return a short report (files + deviations) above a return object the cited unit loop's step 3 reads."*
    - `## Stop conditions` → the bullet opening *"Any implementer reports `blocker:` or returns an `error:`"* becomes *"Any implementer returns an `outcome` of `blocker`, or a return that fails the routing check a third time — halt and report it via `<escalate>`"*. Its exclusion becomes *"an `outcome` of `prohibited`, or on row `G.4` of `already passing`"*. Drop *"and an `error:` return halts either way"*.
  - `user_review_fixes_instructions_core.md`: the same two edits to its own *"Implementers return a short list"* bullet and its *"Any implementer reports `blocker:`"* stop bullet. Also, in the `<escalate>` row, change the implementer clause *"(an implementer reporting an **escalating** blocker — one whose line carries neither the `prohibited — ` marker nor, on row `G.4`, the `already passing — ` marker; …)"* to the outcome form (a) gives.
  - `user_review_fixes_instructions_autonomous.md` → the closed list: *"an implementer reporting `blocker:` or `error:`"* becomes *"an implementer returning an `outcome` of `blocker` or failing the routing check a third time"*.
  - `untrusted_input.md` → `## Where a report goes`, the `layer-implementer` row: *"a line under its `## Output contract` item 7; the unit loop appends every item-7 line to that unit's progress line, …"* becomes *"an item of its return object's `flags`; the unit loop appends every item to that unit's progress line, …"*, keeping the step-6 citation.

**Verification:**

- `jq empty plugin/schemas/layer-implementer.return.json` exits 0.
- `unit_loop_core.md` → `## The unit loop` step 3, read after the edit: the rewritten arms name `cause` as the field the routing check reads for `prohibited` / `already passing` and `blocker` for `blocker`, and state that an `implemented` return with an absent or empty `flags` passes the check and continues. Step 6 reads `flags` as optional by pointing back at that sentence. `flags` is not in the schema's `required` list for `implemented`.
- `git grep -nE 'blocker: (prohibited|already passing)|; (disposition|record) appended to |prohibited — |item-7|item 7' -- plugin` prints nothing.
- `git grep -n 'already passing — ' -- plugin`: every hit is the commit-body line form `mark <…> already passing — <cause>`.
- `git grep -nE 'reports .blocker:|reporting .blocker:|returns an .error:' -- plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/user_review_fixes_instructions_core.md plugin/instructions/user_review_fixes_instructions_autonomous.md`: no hit names an implementer.
- `git grep -noE 'layer-implementer\.[a-z_]+' -- plugin`: every hit is a file name (`layer-implementer.md`, `layer-implementer.return`) or a property the new schema declares (`flags`, `cause`, `blocker`).
- Goal 3 in `layer-implementer.md`: the `**Cause:** ` sentences of **The already-passing record.** and **The disposition record.**, and the `cause` bullet of `### Return fields`, each name the other side as the same text. `cli/templates/scripts/lib/unit-commit-lib.sh` → `ucl_record_cause` is unchanged (`git diff --stat -- cli/templates/scripts scripts` is empty).
- `git grep -n 'agent_return_contract' -- plugin/agents/layer-implementer.md` prints nothing.

- **Deviations from plan:**
  - `layer-implementer.md` → **Unsatisfiable-gate disposition.**: its *"return an ordinary blocker if the item it names has not landed"* is a return reference the `**Work:**` sub-bullets did not list. It now reads *"return an `outcome` of `blocker`"*, following that bullet's lead *"Turn each return reference into an outcome reference"*.
  - `unit_loop_core.md` → `### The dispositioned outcome` → **What it is.** still reads *"the admissibility test that let the return carry the marker"*. That bullet is outside (d)'s named places, so it was left unedited. "marker" there is now stale wording, and none of this task's verification greps match it.
  - Verification also ran the tree guards that `## The test-run rule` point 7 selects for this diff, through `npm test --workspace cli -- <test>`: `agent-return-schemas`, `main-repo-resolution-corpus`, `no-container-home-paths`, `untrusted-input-corpus` and `commit-step-calls`. Each passed (`# fail 0`).
