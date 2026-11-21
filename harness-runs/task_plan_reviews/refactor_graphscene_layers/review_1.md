# Task plan review — round 1

verdict: PASS
review_mode: full

## Should Fix
- **`task_2_plan.md` — three planted cases cannot tell the `layers` contract from the `forbidden` one.** The clean plant's single `adapters` module imports `jsonschema`. The `forbidden` contract checks indirect chains, so these cases also break it through `adapters`: *"`engine` importing `adapters` (sibling)"*, *"`model` importing `adapters` (upward)"* and *"`engine` importing `facade` (upward)"*. Both reports then print the same `<importer> -> <imported>` chain line, and that line is the only thing each case asserts. So the `engine` → `adapters` case would still pass if the `layers` contract were rewritten as two stacked entries with `engine` above `adapters`. That is exactly the form the task prompt rules out (*"never as two stacked entries"*), and it is the story index's second top risk. The `adapters` → `engine` case does catch the opposite stacking, so this is a weaker guard, not a missing one. Fix: point each upward or sibling case at a planted `adapters` (or `facade`) module that does not import `jsonschema`, or also assert the contract's own heading line (`graphscene.engine is not allowed to import graphscene.adapters:`).
- **`\b` is inert under this checkout's `git grep -E`** (measured in round 0). Two commands still rely on it, and each check passes without testing anything:
  - In `task_1_plan.md`, the "No old module path survives" check, `graphscene\.(loader|vocabulary|errors)\b`.
  - In `task_4_plan.md`, the first Verification check, `graphscene\.vocabulary\b`.

  The story index's `## Scope register` entry A also starts with a `\b` alternative. Re-running it portably reaches no missing site. Task 4's last Verification check already uses the portable `([^A-Za-z0-9_]|$)` form. Use that form in the other commands too.
- **Story index → `## Scope register`: entry C reaches sites that have no row (disposition (i)).** Entry C was re-run this round and still prints these lines. None of them has a row:
  - `.claude/context/conventions.md` → the closing `_Written by …_` provenance paragraph, which cites `graphscene/tests/test_boundary.py`.
  - `.claude/context/graphscene.md` → `## Not determined`, the mocking bullet.
  - `.claude/context/graphscene.md` → the closing `_Written by …_` paragraph.

  All three are conventions-document sites, so each takes `no-change`. No site that needs a change is missed. Add them to rows 12 and 10 so the closure invariant holds.
- **`task_3_plan.md` keeps a sentence the new layout makes misleading.** The `## What it is` bullet keeps the opening paragraph, *"reworded only where it says 'a loader'"*. That paragraph also says *"It has no engine code yet"*, and after this branch the package has a `graphscene.engine` layer holding the vocabulary check. Reword that clause too, for example to say that nothing runs or walks a graph yet.
- **`task_1_plan.md`: two moved test docstrings name old paths that no rule covers.** `tests/test_vocabulary.py`'s second docstring paragraph names `graphscene.errors.Violation`. `tests/test_model.py`'s rule sentence names `graphscene.model.build_flow_graph`. The tests bullet only requires the rule sentence to name the new module path, and the leftover-path check does not match `graphscene.model.build_flow_graph`. State that every module path in a moved docstring is rewritten.
- **`task_1_plan.md` granularity** (carried from round 0). The task sits at the 20-point cap and makes about 25 file creations, edits and deletions. The story index's argument for keeping the move as one unit still holds. It remains the task most likely to overrun a unit.

## Nice to Have
- **Story index → `## Context`** has a Markdown table, where the sample keeps Context to prose. Task 3 writes the same table into the README.

## Incidental findings (not gating)
- Carried from round 0: `devscene.config.json` → `treeGuards` has `{ "test": "test/no-container-home-paths.test.mjs", "covers": "**/*.md" }`, whose path is relative to `cli/`. Task 3, a `graphscene`-layer unit that edits `graphscene/README.md`, selects that guard. Point 7 then runs it through `bash scripts/python-service.sh --package graphscene test …`, which cannot run a `.mjs` file. This configuration issue predates this plan.
