### Task 17 — Re-point the sample fixtures at the commit step

**Goal:** The sample fixtures every writer and reviewer agent grades against stop naming the `committer` agent as the committing role. They name **the commit step**, with the committing-role sentence byte-for-byte as the story index's `## Context` fixes it. The fixtures describe one coherent worked branch (`.claude/context/plugin.md` → `## Sample fixtures`), so every fixture that carries the shared sentence carries the same new one.

**Depends on:**

- **Task 3**, whose `commit-on-branch.sh --unit` flips one readiness entry by its token and never a sub-step bullet.
- **Task 7**, which puts the same committing-role sentence into `task-plan-writer.md` and `user-review-fix-plan-writer.md`, the agents that cite these fixtures.

**The committing-role sentence:** *the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none*.

### Targets

- `plugin/samples/sample_story_plan.md`
- `plugin/samples/sample_code_review.md`, plus `plugin/samples/sample_code_review/finding_1.md`, `finding_2.md`, `finding_3.md`
- `plugin/samples/sample_user_review_fix_plan.md`, plus `plugin/samples/sample_user_review_fix_plan/finding_1.md`, `finding_2.md`, `finding_3.md`
- `plugin/samples/sample_task_plan.md`
- `plugin/samples/sample_statistics.md`

**Work:**

- [ ] **The three index samples' readiness lead paragraphs** (`sample_story_plan.md`, `sample_code_review.md`, `sample_user_review_fix_plan.md`).
  - **The sentences.** "the committer flips each one to `[x]` as that task's (or fix's) commit lands" → "the commit step flips …". The parenthesis "the `committer` agent in every flow that dispatches one, the orchestrator itself in the supervised flow, which dispatches none" → the committing-role sentence above. "the committer does NOT touch them" → "the commit step does NOT touch them".
  - **What stays.** Keep each paragraph's licence pointer (`layer-implementer.md` → `## Working modes`) and every other sentence byte-for-byte.
- [ ] **The six finding files' opening notes.** "The committer flips this finding's checkbox in the index's `## Phase 2 Readiness — Ordered Fix List`, never here." → "The commit step flips …". In `sample_code_review/finding_2.md`, "the committer does not touch them either" → "the commit step does not touch them either".
- [ ] **`sample_task_plan.md`.** "(implementer, reviewer, committer)" → "(implementer and reviewer; the commit step reads only the index)". "the orchestrator and the committer key off it" → "… the commit step key off it". "the committer never touches them" → "the commit step never touches them".
- [ ] **`sample_statistics.md`.** "no checkbox a committer flips" → "no checkbox the commit step flips".
- [ ] **What must not change.** No task title, finding number, `_(points: …)_` tag or cross-fixture citation changes. The statistics arithmetic is derived from them (`plugin/samples/README.md`).

**Verification:**

- `git grep -n -w committer -- plugin/samples` prints nothing.
- `git grep -n -F 'the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none' -- plugin/samples` lists the three index samples.
- `git diff -- plugin/samples` changes no line containing `**Task `, `**Finding `, `_(points:` or a `### ` heading.
