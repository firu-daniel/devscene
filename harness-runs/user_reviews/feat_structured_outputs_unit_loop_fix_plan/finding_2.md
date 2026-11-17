### 2. `agent_return_contract.md` → `## Reading a return` has no rule for an optional field

**File:** `plugin/instructions/agent_return_contract.md` → `## Reading a return`, step 4 — "Every field that section reads for that outcome is present and not empty."

**Problem.** Step 4 of the routing check requires every field the citing section reads for an outcome to be present and not empty. The module has no rule for a field that is legitimately absent. `` `layer-implementer.flags` `` is read by the unit loop (`plugin/instructions/unit_loop_core.md` → `## The unit loop` steps 3 and 6), and its schema (`plugin/schemas/layer-implementer.return.json`) leaves it out of every variant's `required` list, so it is absent on most clean units. Read literally, step 4 fails every ordinary `implemented` return. That return is re-dispatched, and on the third failure it escalates (`## A return that fails the check`). This branch works around the gap with local sentences in each caller:

- `plugin/instructions/unit_loop_core.md` → `## The unit loop` step 3: "`` `layer-implementer.flags` `` is **optional** and is not a field the check reads: an absent or empty field means nothing to flag, never a failed return, so an `implemented` return that omits it, or carries it empty, passes the check and continues."
- `plugin/instructions/plan_orchestration_instructions_autonomous.md`, the bullet "**The plan's corpus staleness is one of the observations.**": "(an absent or empty field means no corpus debt, never "the planner did not check")" for `` `task-plan-writer.corpus_staleness` ``.
- Found during verification, and the same pattern: `plugin/instructions/task_plan_writing_instructions_core.md`. Its routing check is read "against the fields the section for `node:` reads for that outcome". On an `outcome` of `returned` that section reads `` `task-plan-writer.parity_exclusions` `` and covers absence with its own clause: "its absence means none was reported".

Every caller of an optional field has to remember to write its own exception, and a caller that forgets escalates on valid returns. The agents still to adopt the mechanism will bring more optional fields.

**Fix.** State the rule once in the module, then reduce the local exceptions to it.

- [ ] `plugin/instructions/agent_return_contract.md` → `## Reading a return`: rewrite step 4 so the module owns the optional-field rule, for example:

  `4. Every field that section reads for that outcome is present and not empty — except a field that section names as optional, which is not part of the check: absent or empty means none.`

  Keep steps 1–3 and `## A return that fails the check` byte-identical.
- [ ] `plugin/instructions/unit_loop_core.md` → `## The unit loop` step 3: reduce the local exception to naming the field as optional, and let the module's wording do the rest. For example, replace everything from "`` `layer-implementer.flags` `` is **optional** and is not a field the check reads" through "passes the check and continues." with "`` `layer-implementer.flags` `` is **optional**." Then repoint step 6's parenthetical "(none when the field was absent or empty, as step 3 states)": step 3 no longer states it, so either drop "as step 3 states" or point at `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return`. That file is already a member of the module's `## Who may cite this` roster.
- [ ] `plugin/instructions/plan_orchestration_instructions_autonomous.md`, the bullet "**The plan's corpus staleness is one of the observations.**": reduce the parenthetical to the module's wording, for example "(the field is optional: absent or empty means none)". **Do not add a `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` citation here.** This fork is not in that module's `## Who may cite this` roster, and the roster is held equal to its citers by `cli/test/agent-return-schemas.test.mjs`. If the implementer prefers a pointer, the same change must add this file to the roster.
- [ ] `plugin/instructions/task_plan_writing_instructions_core.md`, the paragraph "On an `outcome` of `returned`, note `` `task-plan-writer.story_file` ``": name `` `task-plan-writer.parity_exclusions` `` as **optional**, and replace "its absence means none was reported" with the module's wording. This file is already a roster member.

**Leave alone.** Display-side lines that say what to *print* when a field is absent are not routing-check exceptions. These are: `plan_orchestration_instructions_core.md` → `### D.2 Done summary`, the corpus-staleness bullet ("Say **"none reported"**"); `task_plan_writing_instructions_semi_autonomous.md` ("If that field is absent, state that no …"); and `task_plan_writing_instructions_autonomous.md` ("`none` if that field is absent").
