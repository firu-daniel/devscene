# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_3_plan.md` — the f-string verification bullet contradicts the Work bullet.** The Work bullet for `_gate_in_round` says the writer clause *"reads `loop.writer` instead of `node.writer`"*, and the one for `_round_fan_out` says the writer clause *"read[s] `loop.writer`"*. But the current reason f-strings interpolate those attributes themselves: `graphscene/src/graphscene/engine/static_check.py` → `_gate_in_round`, *"names '{node.writer}' as its"*, and `_round_fan_out`, *"writer '{r.writer}' of round '{r.id}' routes no outcome"*. Following the Work bullets therefore changes the source text of two f-strings, which breaks the Verification bullet *"`git diff` shows no change to any reason f-string's text in `static_check.py`"*, although the rendered reason stays byte-identical. Restate that bullet as *"no change to any rendered reason"*, or allow the `{node.writer}` / `{r.writer}` → `{loop.writer}` substitution by name. This is plan structure rather than layering, so it is outside this review's lens and does not gate.

## Nice to Have

1. **`task_1_plan.md` — say why `ReviewLoop` sits in `engine`.** `.claude/context/graphscene.md` → `## The internal layers` puts *"Walk state and checker findings, as plain types"* in `model`. `ReviewLoop` is neither: it is a view the engine derives from a `RoundNode`, it is not public, and no adapter implements or stores it. So `engine/review_loop.py` is the right home. One sentence in the module's docstring saying so would stop a later reader from moving it into `model`.
