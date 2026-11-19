# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`feat_graphscene_package_skeleton_story_plan.md` — the post-merge layer steps still run `/devscene:analyze` before the `graphscene` row exists, and step 2 still omits the row's `conventions` value.** Unchanged since round 0. `**Manual setup required:**` step 1 says `/devscene:analyze` *"writes the new layer's conventions document"*, but the row is added only in step 2: *"Add the layer with `npx devscene config set layers`, with name `graphscene` and path `graphscene`."* Every `layers[]` entry carries `name` / `path` / `conventions` (`.claude/context/conventions.md` → `## Configuration is the source of truth, and it is read at run time`, *"`name` / `path` / `conventions` inside a `layers` entry"*). The fix is to add the row first, with its `conventions` path, and then run the analyze pass, or to have step 1 accept the `layers` proposal and drop step 2. This is post-merge operator text and not a placement or dependency violation in this branch's plan, so it is a Should Fix.

## Nice to Have

1. **`task_1_plan.md` — the tree-guard exemption for `graphscene/tests/test_boundary.py` is argued only in the task file.** Unchanged since round 0. The Verification bullet argues that a `treeGuards[].test` value runs as `<test_file_cmd>`'s argument (`npm test --workspace cli -- test/<name>.test.mjs`), so it cannot carry a `pytest` file. That leaves gate 13's leg 13g as the scanner's only runner, and 13g runs in every Run gates round. The argument holds, but it would be easier to find later as one sentence in the story index's `## Context`, beside decision 3.

Placement checked and sound under the configuration as it stands. `graphscene/`, `scripts/python-service.sh`, `scripts/run-gates.sh`, `docs/development.md` and `ROADMAP.md` fall in the catch-all `general` layer (`.claude/context/conventions.md` → `## The layers`). Neither script has a `cli/templates/scripts/` counterpart. `cli/test/python-service.test.mjs` is in the `cli` layer, as an existing kebab-case suite. The library's one-way dependency, enforced by its own boundary test, matches the layering decisions 2 and 3 state, and no plan file asks for a forbidden test run.
