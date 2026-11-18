## Step 11 → user-review-fix-plan-writer (iter 1)
- **added:** `context_notes:`
- **verbatim:** context_notes: "suggestions 1 and 2" are Should Fix items 1 and 2 of harness-runs/architecture_user_review_reviews/fix_injection_verdict_tools_used_prefix/user_review_1/review_0.md, both about finding_4.md.
context_notes: "the other-agents parsing gap" is the item your previous return listed as outside the plan: plugin/instructions/agent_return_contract.md → `## Reading a return` step 2 requires the reply's JSON to parse, and any other agent's return holding `<\s…` would fail that check and be re-dispatched.
- **why the agent could not derive it:** the user's feedback used the numbering and the phrase from the orchestrator's hand-off message, which exists only in the session transcript; the writer's earlier return is absent from every file a fresh dispatch reads.
