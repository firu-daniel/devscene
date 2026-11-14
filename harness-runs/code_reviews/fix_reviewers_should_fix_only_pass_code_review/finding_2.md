### 2. Two writers paraphrase `## The writer's revision` item 1 in words it no longer uses ("every finding")

**Files:**
- `plugin/agents/task-plan-writer.md` (`## Revision mode`, the `Follow … ## The writer's revision` sentence) — "read every finding on a file against its unchanged text"
- `plugin/agents/user-review-fix-plan-writer.md` (`## Revision mode`, the `Follow … ## The writer's revision` sentence) — "group the round's findings by target file across every findings file and read every finding on a file"

**Problem.** Task 2 rewrote `plugin/instructions/plan_review_rounds.md` → `## The writer's revision` item 1 to: *"Group the round's Must Fix items by target file across every findings file. Read every Must Fix on a file against that file's **unchanged** text before the first edit to it."*

Task 3 removed the "apply or reject each Should Fix" paraphrase from both writers. It left their paraphrase of item 1 in the old wording:

- `task-plan-writer` says "group the Must Fix items by target file and read every **finding** on a file".
- `user-review-fix-plan-writer` says "group the round's **findings** by target file … and read every **finding** on a file".

Both writers point at the section, and the module's own rule is *"A citer **points and never restates**"*. Their restatements now differ from the owner. `user-review-fix-plan-writer`'s version tells the writer to group and read every finding of the round, Should Fix included, right after its first paragraph's "apply only the requested changes". That runs against the Must-Fix-only scope this branch sets. Item 3 still decides the outcome, so this is not a behaviour break, but the citer and the owner disagree in wording.

**Fix.** Make each paraphrase use the owner's words:

1. `plugin/agents/task-plan-writer.md`: replace
   `group the Must Fix items by target file and read every finding on a file against its unchanged text before the first edit`
   with
   `group the Must Fix items by target file and read every Must Fix on a file against its unchanged text before the first edit`

2. `plugin/agents/user-review-fix-plan-writer.md`: replace
   `group the round's findings by target file across every findings file and read every finding on a file against its unchanged text before the first edit`
   with
   `group the round's Must Fix items by target file across every findings file and read every Must Fix on a file against its unchanged text before the first edit`

Leave the rest of both sentences unchanged, including the user-feedback clause in `user-review-fix-plan-writer`. Both edits are prose and need no test run.
