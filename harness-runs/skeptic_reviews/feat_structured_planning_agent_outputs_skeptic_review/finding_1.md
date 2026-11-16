### 1. The autonomous user-review-fix fork's closed `<escalate>` list omits the new G.2 architecture-gate `blocker` / routing-check escalation

**Site:** `plugin/instructions/user_review_fixes_instructions_autonomous.md` → ``### `<escalate>` / `<ask>` — the park-and-yield clarification reroute``. The anchor is the closed-list paragraph that opens "Both bindings resolve to the **same** file-based channel", at the clause "G.2's architecture gate hitting `iteration >= 5`)". The second anchor is the **Headless / watcher entry point:** bullet below it, at the clause "`Phase G architecture-reviewer gate` for G.2's gate cap".

**The problem.**

This branch adds a new escalation site to the shared Phase G. `plugin/instructions/plan_orchestration_instructions_core.md` → `### G.2 Write and review the test fix plan` → **The architecture gate.** now reads:

> - An `outcome` of `blocker`, or the third consecutive return that fails the check (`${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## A return that fails the check`) → `<escalate>`, naming the origin `Phase G architecture-reviewer gate`, quoting `` `architecture-reviewer.blocker` `` or naming the check that failed — and, **under** the clause, the index by its repo-relative `<test_fix_plan_path>`.

On `origin/dev` this gate had only the `verdict: PASS` and `verdict: FAIL` arms, and no blocker arm at all. So the route is new in this branch.

The autonomous user-review-fix flow runs that same Phase G by citation. Its fork binds `<escalate>` to the park-and-yield reroute, and states that the reroute covers:

> a **closed list** of the core's — and its cited sections' — "a supervised flow would stop and surface here" paths, and nothing else

That list names Phase G's escalation points one by one: "G.1's `MAX_GATE_ROUNDS` round cap and its no-verdict-line case; G.2's `test-fix-plan-writer` returning a `## Questions` section, a `blocker:`, or `fixable: 0` after G.3; G.2's architecture gate hitting `iteration >= 5`". It does not name the new arm.

This branch did maintain this same list for its other new route in this flow. It added "the same writer returning an `outcome` of `blocker` or failing the routing check a third time" for `ui-tests-plan-writer` at QA.0, but did not add the G.2 architecture gate's equivalent. The planning fork was updated the same way: `task_plan_writing_instructions_autonomous.md` now lists "an agent's `outcome` of `blocker`, or a return the core passed as `error` after its third failed check".

**Runtime symptom, and why it is reachable.**

In an autonomous user-review-fix run (`/devscene:branch-start-user-review-fix-autonomous`), a test fix plan reaches the G.2 architecture gate. That gate's `architecture-reviewer` either returns an `outcome` of `blocker` (for example, `prompt_path`, the gate log, cannot be read) or ends three consecutive replies with no valid return block. The core then routes to `<escalate>`. But the fork's binding covers a closed list "and nothing else", and this site is not on it. Under `plugin/instructions/mode_contract.md` rule (1), a binding with no value for a site halts the flow.

So the headless run stops without writing the `question_<n>.md` park that the watcher resumes from, and without the `Phase G architecture-reviewer gate` origin and the `<test_fix_plan_path>` that `### G.0 Resolve the round` keys on. The fork's own origin sentence also attaches `Phase G architecture-reviewer gate` only to "G.2's gate cap", so even an orchestrator that does park has no stated origin for this arm.

**Proof.**

- `git show origin/dev:plugin/instructions/plan_orchestration_instructions_core.md` → G.2's gate arms are `` - `verdict: PASS` → **G.3**. `` and `` - `verdict: FAIL` → increment `iteration`. … ``, with no blocker arm.
- `grep -n "gate cap\|Phase G architecture-reviewer gate" plugin/instructions/user_review_fixes_instructions_autonomous.md` → the only origin mapping for this gate is "`Phase G architecture-reviewer gate` for G.2's gate cap".

**Fix.** Two edits, both in `plugin/instructions/user_review_fixes_instructions_autonomous.md`:

1. In the closed-list paragraph under ``### `<escalate>` / `<ask>` — the park-and-yield clarification reroute``, change

   > G.2's architecture gate hitting `iteration >= 5`)

   to

   > G.2's architecture gate hitting `iteration >= 5`, returning an `outcome` of `blocker`, or failing the routing check a third time)

2. In the **Headless / watcher entry point:** bullet of the same subsection, change

   > `Phase G architecture-reviewer gate` for G.2's gate cap

   to

   > `Phase G architecture-reviewer gate` for G.2's gate cap, blocker or third failed routing check

Change no other text. Both edits are prose-only in a plugin instruction fork, so no test is owed. Before committing, re-run `grep -n "Phase G architecture-reviewer gate" plugin/instructions/*.md` and confirm that the origin string is unchanged byte-for-byte everywhere it appears.
