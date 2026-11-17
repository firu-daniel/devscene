### 1. The autonomous user-review fork's closed `<escalate>` list no longer covers an `already passing` return on a row other than `G.4`

**File:** `plugin/instructions/user_review_fixes_instructions_autonomous.md` → ``### `<escalate>` / `<ask>` — the park-and-yield clarification reroute``, first paragraph, at the quoted substring "an implementer returning an `outcome` of `blocker` or failing the routing check a third time, a review loop".

**Problem.**

That paragraph is the fork's **closed list** of the sites its `<escalate>` / `<ask>` reroute covers ("Together they cover a **closed list** of the core's — and its cited sections' — … paths, and nothing else"). The fork's own binding row points at it as "the closed list of the sites it covers".

This branch moved the cited unit loop onto outcomes. `plugin/instructions/unit_loop_core.md` → `## The unit loop` step 3 now sends **three** implementer cases to `<escalate>`:

> An `outcome` of `blocker`, an `outcome` of `already passing` on any other row, or the third consecutive return that fails the check … → stop the whole loop and `<escalate>`

The same three cases appear in `unit_loop_core.md` → `## Mode contract — bindings this file uses` (the `<escalate>` row) and in `plugin/instructions/user_review_fixes_instructions_core.md` → `## Mode contract — bindings this file uses` (the `<escalate>` row: "an implementer returning an `outcome` of `blocker`, an `outcome` of `already passing` on a row other than `G.4`, or a return that fails the routing check a third time").

The fork's closed list names only two of the three: "an implementer returning an `outcome` of `blocker` or failing the routing check a third time". It leaves out the `already passing` case.

This is a gap the branch opened, not one it inherited. Before the branch, the list read "an implementer reporting `blocker:` or `error:`". An off-row `already passing` return was then the line `blocker: already passing — …`, which "reporting `blocker:`" matched. In the outcome form, `already passing` is a different outcome from `blocker`, so the list's wording no longer reaches it.

**Why it is reachable.** This flow runs the unit loop on rows `UR-A`, `E.3` and `G.4` (`user_review_fixes_instructions_core.md`, the `<per_unit_review>` row). An implementer on row `UR-A` or `E.3` that returns `already passing` is exactly the misreturn step 3 guards against ("The fail-safe direction is escalate"). The headless orchestrator then reaches `<escalate>` and reads a closed list that says it covers "nothing else". The list gives it no park for this case, while the unit loop and the core say it must stop and escalate. The orchestrator can either park, which the list does not license, or end the session without a question file, which the watcher cannot resume as a park.

**Fix.**

In `plugin/instructions/user_review_fixes_instructions_autonomous.md` → ``### `<escalate>` / `<ask>` — the park-and-yield clarification reroute``, replace:

> an implementer returning an `outcome` of `blocker` or failing the routing check a third time, a review loop hitting `iteration >= 5` without PASS,

with:

> an implementer returning an `outcome` of `blocker`, an `outcome` of `already passing` on a row other than `G.4`, or failing the routing check a third time, a review loop hitting `iteration >= 5` without PASS,

Leave the rest of the paragraph unchanged. `cli/test/run-gates-park-answer.test.mjs` cases (c) and (g) read this section only for the `Phase G test-fix-plan-writer` origin and the Phase G no-read passage. The edit touches neither string.

No test runs for this prose-only change beyond the tree guards the unit loop selects.
