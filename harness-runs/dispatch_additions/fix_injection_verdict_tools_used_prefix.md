## Step 11 → user-review-fix-plan-writer (iter 1)
- **added:** `context_notes:`
- **verbatim:** context_notes: "suggestions 1 and 2" are Should Fix items 1 and 2 of harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/user_review_1/review_0.md, both about finding_4.md.
context_notes: "the other-agents parsing gap" is the item your previous return listed as outside the plan: plugin/instructions/agent_return_contract.md → `## Reading a return` step 2 requires the reply's JSON to parse, and any other agent's return holding `<\s…` would fail that check and be re-dispatched.
- **why the agent could not derive it:** the user's feedback used the numbering and the phrase from the orchestrator's hand-off message, which exists only in the session transcript; the writer's earlier return is absent from every file a fresh dispatch reads.

## [A · Item 4 · plugin · iter 0] → layer-implementer  (#19)
- **added:** `context_notes:`
- **verbatim:** context_notes: this unit's cli layer, uncommitted, changed pis_unwrap_vlines in cli/templates/scripts/prompt-injection-screen.sh so that after the `agentId: ` line only blank lines and at most one closed `<usage>` block are accepted; source: that file and the deviation note appended to finding_4.md.
- **why the agent could not derive it:** the change was made by the cli layer's review-fix iteration and is absent from finding_4.md's Fix steps, which describe the plugin edit without it.

## [A · Item 4 · general · iter 0] → layer-implementer  (#21)
- **added:** `context_notes:`
- **verbatim:** context_notes: this unit's cli layer, uncommitted, changed pis_unwrap_vlines in cli/templates/scripts/prompt-injection-screen.sh so that after the `agentId: ` line only blank lines and at most one closed `<usage>` block are accepted; scripts/prompt-injection-screen.sh does not carry that change yet (`git diff --no-index --numstat` reports 8 24); source: the deviation note appended to finding_4.md.
context_notes: the live prompt-injection-reviewer probe that delivered the notice inside the frame ran on 2026-11-18 in the Claude Code session whose transcript is /Users/daniel/.claude/projects/-Users-daniel-Work-devscene-fix-injection-verdict-tools-used-prefix/bdb25286-e7fa-4093-b186-fd27908bb706.jsonl; every `"version"` field in that transcript reads 2.1.327.
- **why the agent could not derive it:** finding_4.md's Fix steps say the script copies are untouched and that the live run's version is unrecorded; the cli change and the session transcript's path are in no file the dispatch reads.
