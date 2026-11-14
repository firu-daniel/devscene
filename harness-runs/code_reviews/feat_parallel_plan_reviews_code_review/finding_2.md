### 2. The semi-autonomous plan command still says the architecture gate runs ahead of the plan review

**File:** `plugin/commands/branch-start-plan-semi-autonomous.md` (`## Context`, first paragraph) — "The architecture gate runs ahead of the structural"

**Problem.** The branch rewrote the next paragraph of this section: the business-parity gate now "reviews each round's draft at the same time as the architecture gate and the plan review". The sentence just before it was left as it was, and it still states an execution order between two gates of the same round. That is now false. `plugin/instructions/task_plan_writing_instructions_core.md` → `## Safety contract — applies before EVERY Agent dispatch` → **A set.** sends a round's three gates in one message, and the walker prints them as one set. So the two paragraphs of this command now disagree with each other and with the core.

The task prompt's scope predicate asks for every such sentence to be corrected on this branch: *"Verify every other place that says a gate runs "then" or "before" another gate in plan-review mode"*. The story index's `## Scope register` row 5 assigns this file to Task 14, and derivation E1's own pattern `ahead of the (architecture|structural|…` matches this sentence through `ahead of the structural`. Only the parity sentence was changed.

**Fix.** Replace this text:

```
The architecture gate runs ahead of the structural `task-plan-reviewer`; the loop runs without user input
```

with this text:

```
The architecture gate and the structural `task-plan-reviewer` review each round's draft together; the loop runs without user input
```

Leave the rest of the sentence ("(up to 5 iterations) unless the writer surfaces a clarification question.") unchanged. This fix runs no test: it is a prose edit in a `plugin/` command, and it creates or edits no test file.
