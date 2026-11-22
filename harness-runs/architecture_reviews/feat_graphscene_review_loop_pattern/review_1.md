# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`task_3_plan.md` — the f-string verification bullet still contradicts the Work bullets.** The Work bullets say the writer clauses "read `loop.writer`" in place of `node.writer` / `r.writer`. The current reason f-strings interpolate those attributes directly: `graphscene/src/graphscene/engine/static_check.py` → `_gate_in_round` (*"names '{node.writer}' as its"*) and `_round_fan_out` (*"writer '{r.writer}' of round '{r.id}' routes no outcome"*). Following the Work bullets therefore changes the source text of two f-strings, which breaks the Verification bullet *"`git diff` shows no change to any reason f-string's text in `static_check.py`"*, even though the rendered reason stays byte-identical. Restate the bullet as "no change to any rendered reason", or allow the `{node.writer}` / `{r.writer}` → `{loop.writer}` substitution by name. This is plan structure, not layering, so it is outside this review's lens and does not gate. Carried over from round 0, where it was also non-gating.

## Nice to Have

1. **`task_1_plan.md` — say in the module docstring why `ReviewLoop` sits in `engine`.** `.claude/context/graphscene.md` → `## The internal layers` puts *"Walk state and checker findings, as plain types"* in `model`. `ReviewLoop` is neither. It is a view the engine derives from a `RoundNode`, it is not public, and no adapter implements or stores it, so `engine/review_loop.py` is the right home (*"A check or a walk over the model, and its rounds, goes in `engine`"*). One sentence saying so in the module docstring would keep a later reader from moving it into `model`.
