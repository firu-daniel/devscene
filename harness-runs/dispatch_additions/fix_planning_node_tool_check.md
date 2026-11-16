## [C · Item 1 · cli · iter 0] → layer-implementer  (#12)
- **added:** `context_notes:`
- **verbatim:** context_notes: this unit's readiness entry is tagged `_(layer: cli, general)_`, so the unit loop dispatches it once per layer in that order — this `cli` dispatch owns the sites under `cli/`, and a separate `general` dispatch follows for `docs/flow-graph-walker.md`, with one commit after both (harness-runs/code_reviews/fix_planning_node_tool_check_code_review.md, Finding 1 entry; plugin/instructions/unit_loop_core.md → `## Layer routing table`)
- **why the agent could not derive it:** the per-layer split of a multi-layer unit is stated only in the orchestrator's `unit_loop_core.md` and the review index's readiness tag, neither of which is in the implementer's read set; the previous dispatch (#11) returned a blocker asking for exactly this split

## [C · Item 1 · general · iter 0] → layer-implementer  (#13)
- **added:** `context_notes:`
- **verbatim:** context_notes: this unit's readiness entry is tagged `_(layer: cli, general)_`; the preceding `cli` dispatch already changed the two sites under `cli/` (uncommitted in the working tree), so this `general` dispatch owns `docs/flow-graph-walker.md`, with one commit after both (harness-runs/code_reviews/fix_planning_node_tool_check_code_review.md, Finding 1 entry; plugin/instructions/unit_loop_core.md → `## Layer routing table`)
- **why the agent could not derive it:** which sibling layer dispatch already owns the `cli/` sites is absent from the finding file and the implementer's read set
