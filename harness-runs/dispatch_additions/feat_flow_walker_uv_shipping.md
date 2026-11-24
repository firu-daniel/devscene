## [A · Task 12 · general · iter 0] → layer-implementer  (#1)
- **added:** `context_notes:`
- **verbatim:** `context_notes: The clarification answer to this task's earlier blocker states the person performed option 1 in this run copy — scripts/flow-host-provision.sh copied at mode 0755, scripts/lib/harness-run-lib.sh and scripts/setup-worktree.sh copied, and the relative symlinks scripts/python/graphscene and scripts/python/devscene-flow-host created, all left uncommitted (source: harness-runs/clarifications/feat_flow_walker_uv_shipping/answer_1.md, answering question_1.md).`
- **why the agent could not derive it:** the park's answer lives only in the machine-local `harness-runs/clarifications/feat_flow_walker_uv_shipping/answer_1.md`, outside the implementer's read set; its detail file's `**Deviations from plan:**` note still recorded the operations as refused

## [C · Item 2 · cli · iter 0] → layer-implementer  (#8)
- **added:** `context_notes:`
- **verbatim:** `context_notes: The self-adopted copy scripts/lib/harness-run-lib.sh (general layer, path ".") is owned by a general-layer dispatch that runs after this one within the same unit and mirrors the template's MIRRORS edit byte-for-byte; the cli dispatch owns every path under cli/ (source: this unit's earlier cli dispatch returned blocker "Finding 2 step 2 requires the byte-identical edit to scripts/lib/harness-run-lib.sh, which is outside the cli layer's path").`
- **why the agent could not derive it:** the finding's readiness entry is tagged `_(layer: cli)_` only; the orchestrator's decision to split the unit across `cli` then `general` after dispatch #7's blocker exists in no artifact the implementer reads

## [C · Item 2 · general · iter 0] → layer-implementer  (#9)
- **added:** `context_notes:`
- **verbatim:** `context_notes: A cli-layer dispatch of this same unit already landed (uncommitted) every path under cli/ — the provision.ts header, the template cli/templates/scripts/lib/harness-run-lib.sh MIRRORS line and the new test case; this general-layer dispatch owns only the self-adopted copy scripts/lib/harness-run-lib.sh (source: the Deviations from plan note now appended to harness-runs/code_reviews/feat_flow_walker_uv_shipping_code_review/finding_2.md).`
- **why the agent could not derive it:** which sibling dispatch owns the `cli/` sites of a unit whose readiness tag names `cli` alone is recorded nowhere but in this session
