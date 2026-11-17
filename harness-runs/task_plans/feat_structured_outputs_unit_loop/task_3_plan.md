### Task 3 — Give `test-fix-plan-writer` a schema-validated return and move Phase G onto it

**Goal:** `test-fix-plan-writer` ends its reply with a return object checked against `plugin/schemas/test-fix-plan-writer.return.json`, and Phase G routes on it through `plugin/instructions/agent_return_contract.md` → `## Reading a return`, citing `` `test-fix-plan-writer.<field>` ``. The former `## Questions` section becomes a `questions` field, following the `task-plan-writer` precedent. No caller is left matching a `fix_plan_file:` / `fixable:` line or a `## Questions` heading of this agent.

**Depends on:** Task 2, which last edited three of this task's files.

- In `untrusted_input.md` → `## Where a report goes`, Task 2 rewrote the `layer-implementer` row; leave it as Task 2 left it.
- In `user_review_fixes_instructions_autonomous.md`'s closed list, Tasks 1 and 2 own the reviewer and implementer paths.
- In `plan_orchestration_instructions_core.md`, Tasks 1 and 2 own the context-discipline bullets and the implementer and review-loop stop bullets.
- `plan_orchestration_instructions_core.md` is already on `agent_return_contract.md` → `## Who may cite this`, so this task adds no roster line.
- **This task edits only the sections and sentences named under `**Work:**`.**

**The return this task defines.** This is the contract both the agent and Phase G are written to. Field names are byte-stable.

- An `outcome` of `returned`: the plan was written, revised or answer-mode reconciled. It carries:
  - `fix_plan_file` (string, the index path, non-empty);
  - `fix_plan_dir` (string, the per-finding folder, non-empty);
  - `fixable` (integer, at least 0);
  - `not_fixable` (integer, at least 0).
- An `outcome` of `questions`: only the user can settle a failure, or answer mode met an answer it cannot act on. Nothing was written. It carries `questions` (array of strings, at least 1 item, each non-empty, each routed to the user verbatim and answerable without the plan).
- An `outcome` of `blocker`: a cited input could not be read, and nothing was written. It carries `blocker` (string, one line naming the path and the refusal).
- `fix_plan_file: (pending — questions for user)` has no successor: the `questions` outcome carries no path.

### Targets

- `plugin/schemas/test-fix-plan-writer.return.json` (new)
- `plugin/agents/test-fix-plan-writer.md`
- `plugin/instructions/plan_orchestration_instructions_core.md` — `### G.0 Resolve the round`, `### G.2 Write and review the test fix plan`, `### G.3 Commit the test fix plan`, and the two `test-fix-plan-writer` bullets of `## Stop conditions` only
- `plugin/instructions/user_review_fixes_instructions_autonomous.md` — the G.2 phrase of the closed list only
- `plugin/instructions/untrusted_input.md` — `## Where a report goes`, the two rows named below only

**Work:**

- [ ] **`plugin/schemas/test-fix-plan-writer.return.json` (new).** Write it in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`, with the three variants exactly as **The return this task defines** states them, modelled on `plugin/schemas/task-plan-writer.return.json`.
  - `fixable` and `not_fixable` are `integer` with `minimum: 0`.
  - `questions` is `array` with `minItems: 1` and string items with `minLength: 1`.
  - `blocker` and the two path fields are `string` with `minLength: 1`.
  - Every variant has `additionalProperties: false`.
- [ ] **`plugin/agents/test-fix-plan-writer.md`.**
  - `## Resolved values`' placeholder sentence: *"… in the plan templates and the return block"* becomes *"… in the plan templates and the return object"*.
  - `## Read on demand` → **A cited path you cannot read**: *"return a `blocker:` line naming the path and the refusal in place of the `## Output contract` block"* becomes *"return an `outcome` of `blocker` naming the path and the refusal"*.
  - `## Process` step 7:
    - *"write the marker and return `fixable: 0`"* becomes *"write the marker and return an `outcome` of `returned` with `fixable` `0`"*.
    - *"return `## Questions` and write nothing"* becomes *"return an `outcome` of `questions` and write nothing"*.
    - Keep the `Park answer consumed: ` text byte-identical: `cli/test/run-gates-park-answer.test.mjs` case (b) reads it in `## Process`.
  - `## Output contract`:
    - Replace the fenced `fix_plan_file:` … `not_fixable:` block and its `## Questions` paragraph with the canonical sentence from `docs/structured-agent-returns.md` → `### The return block`, verbatim.
    - Follow it with `### Return fields`, per `docs/structured-agent-returns.md` → `### Return fields`. It has bullets for `outcome` (naming `returned`, `questions` and `blocker`, with when each applies), `fix_plan_file`, `fix_plan_dir`, `fixable` (integer), `not_fixable` (integer), `questions` (array of strings) and `blocker`.
    - Carry over: questions are routed to the user verbatim, each answerable without the plan, and nothing is written on `questions`; *"Do not paste the plan content back."*
  - Do **not** edit `## Invocation contract`: `cli/test/run-gates-park-answer.test.mjs` case (a) pins both prompt forms there.
  - Add no pointer to `agent_return_contract.md`.
- [ ] **`plan_orchestration_instructions_core.md` → `### G.2 Write and review the test fix plan`.** Replace *"Parse the return — on this dispatch and on every revision dispatch below alike."* and its five bullets.
  - The lead-in becomes *"Read the return — on this dispatch and on every revision dispatch below alike — as `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` states."* Keep *"Every escalation below names the origin `Phase G test-fix-plan-writer`"* byte-identical: case (c) of the same suite pins the origin in G.2.
  - The arms, in order:
    1. An `outcome` of `questions` or `blocker`, **without** the clause → `<escalate>`, carrying each `` `test-fix-plan-writer.questions` `` item verbatim or `` `test-fix-plan-writer.blocker` ``. It does not name the index.
    2. The same **under** the clause → also naming the index by its repo-relative `<test_fix_plan_path>`.
    3. An `outcome` of `returned` with `` `test-fix-plan-writer.fixable` `` `0`, **without** the clause → **G.3**, then `<escalate>`, as today.
    4. The same **under** the clause → **G.3**, then **G.5**, as today.
    5. The third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) → `<escalate>`, naming the check that failed and, under the clause, the index.
    6. Otherwise → the architecture gate.
  - Keep both prompt forms, the **`Park answer:` clause** paragraph and the architecture-gate block byte-identical. Cases (a) and (f) pin them.
- [ ] **The rest of `plan_orchestration_instructions_core.md` — these sentences only.**
  - `### G.0 Resolve the round` → the **Pending an answer** arm: *"an answered `fixable: 0` park"* gains its definition once, *"— the park G.2 raises on an `outcome` of `returned` whose `` `test-fix-plan-writer.fixable` `` is `0`"*. The name *`fixable: 0` park* stays. Leave the rest of G.0 as it is, including **Which Phase G answers G.0 consumes.**, which uses the same name.
  - `### G.3 Commit the test fix plan`, last paragraph: *"`<escalate>` on a `fixable: 0` returned without the `Park answer:` clause; or go to **G.5** on a `fixable: 0` returned under it"* becomes *"`<escalate>` on a `` `test-fix-plan-writer.fixable` `` of `0` returned without the `Park answer:` clause; or go to **G.5** on one returned under it"*. *"a `fixable: 0` plan may never have reached the gate"* becomes *"a plan returned with `fixable` `0` …"*.
  - `## Stop conditions`:
    - *"**`test-fix-plan-writer` returns a `## Questions` section** (G.2) — `<escalate>`, carrying the questions verbatim; a `blocker:` from it — `<escalate>`."* becomes *"**`test-fix-plan-writer` returns an `outcome` of `questions` or `blocker`, or fails the routing check a third time** (G.2) — `<escalate>`, carrying each `` `test-fix-plan-writer.questions` `` item verbatim or `` `test-fix-plan-writer.blocker` ``."*
    - *"**`test-fix-plan-writer` returns `fixable: 0`** (G.2)"* becomes *"**`test-fix-plan-writer` returns a `` `test-fix-plan-writer.fixable` `` of `0`** (G.2)"*, with the rest of that bullet unchanged.
  - Do **not** edit `### G.5 Re-run, and the round cap`: case (e) of the same suite requires its **An answered park never buys a fresh cap.** paragraph to keep the literal `fixable: 0` and `G.2`.
- [ ] **The fork and the report table.**
  - `user_review_fixes_instructions_autonomous.md` → ``### `<escalate>` / `<ask>` — the park-and-yield clarification reroute``, the closed list: *"G.2's `test-fix-plan-writer` returning a `## Questions` section, a `blocker:`, or `fixable: 0` after G.3"* becomes *"G.2's `test-fix-plan-writer` returning an `outcome` of `questions` or `blocker`, failing the routing check a third time, or a `` `test-fix-plan-writer.fixable` `` of `0` after G.3"*.
    - Keep the origin string `Phase G test-fix-plan-writer` and the name *the `fixable: 0` park* in the following bullet as they are: case (c) pins the origin in this section, and G.0 defines the name.
  - `untrusted_input.md` → `## Where a report goes`:
    - Remove `test-fix-plan-writer` from the row *"`user-review-fix-plan-writer`, `test-fix-plan-writer` | one entry of its `## Questions` return section …"*, leaving that row as `user-review-fix-plan-writer`'s alone.
    - Add `test-fix-plan-writer` to the row *"`task-plan-writer`, `ui-tests-plan-writer` | one item of its return object's `questions` …"*.
    - Change no other row.

**Verification:**

- `jq empty plugin/schemas/test-fix-plan-writer.return.json` exits 0.
- `git grep -nE 'fix_plan_file:|fix_plan_dir:|not_fixable:|pending — questions for user' -- plugin/agents/test-fix-plan-writer.md plugin/instructions/plan_orchestration_instructions_core.md` prints nothing.
- `git grep -n 'fixable: 0' -- plugin`: every hit uses it as the name *the `fixable: 0` park* or sits in G.5's **An answered park never buys a fresh cap.** paragraph. None reads a `fixable:` line of a return.
- `git grep -nE 'Questions. (section|return)' -- plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/user_review_fixes_instructions_autonomous.md plugin/instructions/untrusted_input.md`: no hit names `test-fix-plan-writer`.
- `git grep -noE 'test-fix-plan-writer\.[a-z_]+' -- plugin`: every hit is a file name (`test-fix-plan-writer.md`, `test-fix-plan-writer.return`) or a property the new schema declares.
- `git diff -U0 -- plugin/agents/test-fix-plan-writer.md` shows no change inside `## Invocation contract`, and `git diff -U0 -- plugin/instructions/plan_orchestration_instructions_core.md` shows no change inside `### G.5 Re-run, and the round cap`.
- `git grep -n 'agent_return_contract' -- plugin/agents/test-fix-plan-writer.md` prints nothing.
