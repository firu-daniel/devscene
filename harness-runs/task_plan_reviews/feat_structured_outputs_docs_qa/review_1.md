# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_1_plan.md` — the `qa-tester.md` driver gate keeps an `error:` return that no Work bullet rewrites and no Verification grep catches**
   Round 0's Must Fix 1 asked that Task 1 name every sentence in its files that states `qa-tester`'s old return form, an `error:` line in any wording included. One sentence is still missed. The driver-gate paragraph of `plugin/agents/qa-tester.md` ends: *"…and that both are **declared but not implemented in this release**, so the `error:` is the terminal outcome, not a routing hop."* `### Targets` names *"the phase-gate and driver-gate paragraphs"*, but the Work rewrites only the phrase *"the run-level `error:` line of `## Output contract` → `### 4. The run cannot proceed`"* and then says *"Keep each sentence's other words; add none."* An implementer following that leaves *"so the `error:` is the terminal outcome"* in place. The definition would then tell the agent its terminal return is an `error:`, which contradicts its new `## Output contract` (an `outcome` of `blocker`).
   None of Task 1's Verification greps catch it:
   - `'error: blocked|unmarked [^.]*error|run-level [^.]*error'` needs `blocked`, `unmarked` or `run-level` in front of `error`.
   - `'verdict: (PASS|FAIL)|must_fix_count:|findings_file:'` does not match it.
   - The line-count grep does not match it.

   Task 1 has no general `` `error:` `` grep over `qa-tester.md`. Task 2 has one, over the two stubs and `README.txt`.
   **Raised against:** "**Every other mention.** *"the run-level `error:` line of `## Output contract` → `### 4. The run cannot proceed`"* becomes *"an `outcome` of `blocker` (`## Output contract` → `### 4. The run cannot proceed`)"* … Keep each sentence's other words; add none."
   **Must hold:** After Task 1, no sentence of `plugin/agents/qa-tester.md` outside the byte-kept `### n.` headings calls any of its returns an `error:` or an `error:` line. Task 1's Work schedules each such rewrite. Its Verification includes a grep that fails while any such wording is left.
   **Fix:** In `task_1_plan.md`:
   - Add a Work rewrite for the driver gate's *"so the `error:` is the terminal outcome, not a routing hop"*, for example *"so the `blocker` is the terminal outcome, not a routing hop"*.
   - Add a Verification bullet that ``grep -n '`error:`\|error: ' plugin/agents/qa-tester.md`` has no hit.
   - The same pass should also reach the namespace paragraph's *"return the run-level `error:` line (`## Output contract` → …)"*. That wording has no *"of"*, so the Work's quoted pattern does not match it word for word.

## Should Fix
- **`task_1_plan.md` — two more old-form phrases in `qa-tester.md`.** `## Resolved values` says *"`<title>` in the templates and the return blocks"*, and `## What you must NOT do` says *"never restate a credential value in a finding, a return line or a commit message"*. After Task 1, the return is one return object, not "return blocks" or a "return line". Neither phrase is in `### Targets`.
- **`task_1_plan.md` — routes stated twice.** The `### E.1` rewrite (*"the four routes above; an `outcome` of `blocker` or a third failing return stops the loop at once (E.2)"*) and `qa_test_instructions.md` step 3 invite the implementer to list the four routes in the collect paragraph and again in E.2 / step 4. `harness-runs/lessons.md` → `## Agent prose`: *"State a new behaviour once, in the section that decides it, and cite it from everywhere else; never re-walk in prose the cases that other arms or sections already route."* Have E.1 and step 3 point at E.2 and step 4 for the routes instead of listing them.
- **Story index — derivation entry P1 still does not say how a glob is handled.** The prompt's `plugin/agents/*.md` and `plugin/schemas/*.return.json` are patterns. State that a glob is not a path, or name the sites it reaches.

## Nice to Have
- Story index: the `cli` task ships after the four `plugin` tasks, against the configured order `cli`, `plugin`, `general`. The order is forced by Task 5's dependency on Tasks 1–4, and `## Context` and Task 5 both say so. Not a finding.
