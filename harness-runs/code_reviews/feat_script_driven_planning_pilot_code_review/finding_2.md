### 2. The engine command's `## Context` sentence on step 4a does not parse

**File:** `plugin/commands/branch-start-plan-autonomous.md` (`## Context`, first paragraph) — "in one uninterrupted session, except on a launch step 4a ends, ending at"

**The problem.** The branch inserted the clause *"except on a launch step 4a ends"* into the sentence that states what the command chains. The phrase is missing its relative pronoun, so it reads as two noun phrases run together ("a launch step", "4a ends"). Followed by the comma and *"ending at 'branch ready for review'"*, it is hard to tell which launch the exception covers. The behaviour itself is stated correctly in step 4a. This is wording only.

**Fix.** Replace the clause so that it names the launch step 4a ends:

```markdown
This is the **one** autonomous engine command. It is the **execution-context-agnostic** entry point that chains autonomous **planning** straight into autonomous **implementation** in one uninterrupted session — except on a launch that step 4a ends after setup — ending at "branch ready for review" — **no** approval gate between planning and implementation, and **no** merge into a branch in `<protected_branches>`, no push to one, and no PR at the end.
```

No test covers this prose, so the fix runs no test.
