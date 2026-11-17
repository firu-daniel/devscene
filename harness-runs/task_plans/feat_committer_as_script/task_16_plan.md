### Task 16 — Re-point the five branch-level reviewers' readiness wording at the commit step

**Goal:** The five reviewer agents that author a review index each tell their author who keys off the readiness heading and who flips its checkboxes. Today that is "the committer". Make it **the commit step**, with the committing-role sentence byte-for-byte as the story index's `## Context` fixes it.

**Depends on:** Task 3, whose `commit-on-branch.sh --unit review_item` resolves a `**Finding K**` entry inside `## Phase 2 Readiness — Ordered Fix List` by its token and flips it. It never touches a `- [ ]` sub-step bullet in a finding body.

**The committing-role sentence:** *the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none*. The supervised fix flow is the one `branch-reviewer.md` already names.

### Targets

- `plugin/agents/architecture-reviewer.md`
- `plugin/agents/branch-reviewer.md`
- `plugin/agents/business-parity-reviewer.md`
- `plugin/agents/skeptic-reviewer.md`
- `plugin/agents/review-plan-reviewer.md`

**Work:**

- [ ] **`architecture-reviewer.md` and `business-parity-reviewer.md`.** Change the same three phrases in each: "the orchestrator and the committer key off it" → "the orchestrator and the commit step key off it"; "the committer flips each `[ ]` to `[x]` as that fix lands" → "the commit step flips …"; "the committer ignores them" → "the commit step ignores them".
- [ ] **`branch-reviewer.md`.** In **Checkbox discipline.**, "the committer flips checkboxes only inside the index's …" → "the commit step flips …", and "(informational; the committer ignores them)" → "(informational; the commit step ignores them)". In the readiness paragraph, "the orchestrator and the committer key off it" → "… the commit step key off it". Replace the parenthesis "(the `committer` agent in every flow that dispatches one, the orchestrator itself in the supervised fix flow, which dispatches none)" with the committing-role sentence above, keeping "supervised fix flow".
- [ ] **`skeptic-reviewer.md`.** "the orchestrator and the committer key off it" → "… the commit step key off it". In **Checkbox discipline.**, make the same two replacements as `branch-reviewer.md`.
- [ ] **`review-plan-reviewer.md`.** "the orchestrator and the committer key off it" → "the orchestrator and the commit step key off it".
- [ ] **No new words.** Each edit swaps a noun phrase and adds no sentence, so no definition's up-front word count grows (`.claude/context/plugin.md` → `## Writing agent prose`).

**Verification:**

- `git grep -n -w committer -- plugin/agents/architecture-reviewer.md plugin/agents/branch-reviewer.md plugin/agents/business-parity-reviewer.md plugin/agents/skeptic-reviewer.md plugin/agents/review-plan-reviewer.md` prints nothing.
- In each of the five files, `git diff --word-diff` shows only the noun-phrase swaps above.
