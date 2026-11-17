### 5. Reword the writer's corpus-`findings` lead-in, which still says "the line itself"

**Severity:** Nice to Have

**Site:** `plugin/agents/conventions-writer.md` → `## Invocation contract`, the lead-in *"`findings` on this axis has **two admissible origins, and the line itself tells you which one you are reading**:"*

**Problem.** Task 1 rewrote the two origin bullets and the discriminator paragraph below this lead-in. They now read: *"An object carrying `check_id` is a corpus review finding, and a line carrying that prefix is a forwarded divergence."* So a corpus review finding now arrives as an object, not a line, but the lead-in still says "the line itself". The rule that follows it is correct and decides the case, so no reader acts wrongly. This is wording drift only.

**Fix.** Replace

> `findings` on this axis has **two admissible origins, and the line itself tells you which one you are reading**:

with

> `findings` on this axis has **two admissible origins, and each entry itself tells you which one you are reading**:

Change nothing else.
