# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`feat_graphscene_package_skeleton_story_plan.md` — the post-merge layer steps are in an order that does not produce what step 1 claims, and step 2 omits the `conventions` value a `layers[]` entry requires.** In `**Manual setup required:**`, step 1 says that running `/devscene:analyze` *"writes the new layer's conventions document"*, and step 2 adds the layer only afterwards: *"Add the layer with `npx devscene config set layers`, with name `graphscene` and path `graphscene`."* `plugin/commands/analyze.md` → `## Steps` step 1 derives the run's document set from *"every `layers[].conventions` value the target set reaches"*. Before step 2 there is no `graphscene` row, so the run writes no `graphscene` document unless the adopter accepts a `layers` proposal at that same run, which the step does not say to do. Every `layers[]` entry also carries `conventions` (`devscene.config.json` → `layers`; `.claude/context/conventions.md` → `## Configuration is the source of truth…`, *"`name` / `path` / `conventions` inside a `layers` entry"*). Either add the row first, with its `conventions` path, and then run `/devscene:analyze graphscene`, or have step 1 accept the `layers` proposal and drop step 2. This is a Should Fix, not a Must Fix, because it is post-merge operator text outside this reviewer's Must Fix triggers. The plan's placement of `graphscene/` in the catch-all `general` layer is correct under the configuration as it stands (`.claude/context/conventions.md` → `## The layers`).

## Nice to Have

1. **`task_1_plan.md` — the boundary test is a tree-reading test, and its exemption from `## The test-run rule` point 8 is argued only in the task file.** The Verification bullet argues correctly that a `treeGuards[].test` value runs through the `cli` workspace's `npm test` and cannot carry a `pytest` file. That leaves gate 13's leg 13g as the only runner. The decision would be easier to find later if it were one sentence in the story index's `## Context`, beside decision 3.
