# Task plan review — round 1

verdict: PASS
review_mode: full

## Should Fix
1. **Task 3 (`task_3_plan.md`): two Verification bullets cannot both hold as written**
   Two reason f-strings in `graphscene/src/graphscene/engine/static_check.py` interpolate the attribute that Task 3 has to stop reading:
   - `_gate_in_round`: `f"gate-in-round: round '{node_id}' names '{node.writer}' as its "`
   - `_round_fan_out`: `f"round-fan-out: writer '{r.writer}' of round '{r.id}' routes no outcome "`

   The first Verification bullet requires `git grep -nE "r\.writer|node\.writer|…"` to print nothing in `static_check.py`, so both interpolations must become `{loop.writer}`. The third bullet then fails as written: *"`git diff` shows no change to any reason f-string's text in `static_check.py`"*. The rendered reasons stay byte-identical, so the code that gets built is correct; only the check is self-contradictory. Restate the third bullet so it holds the **rendered** reason text unchanged, for example: *"the literal parts of every reason f-string are unchanged; only the two writer interpolations move from `node.writer` / `r.writer` to `loop.writer`"*.
2. **Scope register (`feat_graphscene_review_loop_pattern_story_plan.md`): the lessons-ledger procedure still reaches a rule with no row. This is disposition (i), first raised in round 0 and still unaddressed.**
   I re-walked the standing-artifact procedure over `harness-runs/lessons.md` (*"a rule is reached when it names a flow graph, …"*). It reaches `## Agent prose` → *"A value a script or graph may route on (an outcome, a key, an id) is one token with no space; when it is carried over from an old literal, keep the literal's words and drop its spacing."*, and the register has no row for that rule. The plan complies: every id in `valid_plain_round.json` (`release_checks`, `intake`, `lint`, `license`, `checks`, `accepted`, `rejected`, `crashed`, `published`, `discarded`) is one token. So the missing row is `no-change` with that reason.
   I re-ran the command entry verbatim. Every site it reached is a row already (rows 1–7), and no further site turned up: `docs/flow-graph-walker.md` → *Format 4* and `.claude/context/graphscene.md` state nothing this branch falsifies.

## Nice to Have
1. **Task 5 (`task_5_plan.md`), `test_transitions.py`:** the file's `_round(gates, outcomes)` helper always writes `"writer": "draft"`, `"counter"` and `"convergingFrom"`. *"Build the planted graph through the file's own helpers"* therefore does not give you a writer-less round. Say how to get one: drop the three keys from the helper's result, or give the helper an option to leave them out.
2. **Task 6 (`task_6_plan.md`):** `Wait` has three fields: `round`, `recorded` and `pending`. To keep the expected value fully hand-written, spell it out in full: `Wait("checks", recorded=GateRecord("lint", "accepted", None), pending=("license",))`.
3. **Task 8 (`task_8_plan.md`), `ROADMAP.md` (repeated from round 0):** once *"the review loop's rules on the engine"* comes out of **Left:**, *"the walker's port onto it"* has no antecedent for `it`. Name it: *"the walker's port onto the engine"*.
