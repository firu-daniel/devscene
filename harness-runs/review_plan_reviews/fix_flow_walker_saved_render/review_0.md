# Review plan meta-review — iteration 0

## Must Fix
1. **Finding 1's fix names two tree guards the fix neither creates nor edits** — refers to review finding #1. Offending file: `harness-runs/code_reviews/fix_flow_walker_saved_render_code_review/finding_1.md`.
   Step 5 of the fix ends with: *"Because this touches `devscene-flow-host/src/devscene_flow_host/**`, also run the tree guards `tests/test_boundary.py` and `tests/test_layers.py` the same way."* The fix creates and edits neither file. `plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 4 says that no finding fix or sub-step names a test file the unit neither creates nor edits, and that *"No plan names a tree guard the task neither creates nor edits … the guard run is the loop's, never the plan's."* Point 7 already selects and runs both guards, because the fix edits paths that match their `covers` globs. A breach of point 4 is a Must Fix for every reviewer. The sentence also restates, inside a finding, a rule that belongs to the loop. (Every other claim in `finding_1.md` was checked: its anchors resolve in `round_gates.py` → `record_outcome` and `re_entry.py` → `start_walk`, `render.py` → `_block` / `_cap_lines` carry the cited lookups, `RevisionFindingsStore.clear` exists as cited, the test helpers it uses all exist in `tests/test_flow_walker.py`, and the probe script is present under `harness-runs/scratch/`.)
   **Class:** Wrong build
   **Failure:** If the implementer of Finding 1 follows step 5 of `finding_1.md` as written, then it runs `tests/test_boundary.py` and `tests/test_layers.py` because the finding told it to. Both are test files the fix neither creates nor edits, and the test-run rule's point 4 forbids a finding to name them.
   **Fix:** In `finding_1.md` step 5, delete the sentence *"Because this touches `devscene-flow-host/src/devscene_flow_host/**`, also run the tree guards `tests/test_boundary.py` and `tests/test_layers.py` the same way."* Keep *"Run only that file: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_flow_walker.py`."* or reword it so it names only that file, without saying that no other test runs. Do not substitute another mention of the guards: selecting them is the loop's job under point 7. No change to the index or to `finding_2.md`.

## Should Fix
None.

## Nice to Have
None.
