# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_2_plan.md` — the Bash bullet gives the wrong reason why a refused gate is reviewed again on resume** (the story index `## Context` makes the same claim, *"bash's `start` reopens a round's missing gates when the evidence is consistent"*).
   **Raised against:** "The refused gate is reviewed again only on resume, because `start` reopens a round's missing gates when the evidence is consistent (`flow-walker.sh` → `STATE`; `cli/test/flow-walker-resume.test.mjs`). Open that suite and cite the case by its quoted title."
   At the escalation in question, the refused gate's file is still on disk: it is the file `fw_round_file_check` refused. `cli/templates/scripts/lib/flow-walker-gates.sh` → `fw_round_evidence` grades that file `unreadable` (*"`unreadable` = present, and `fw_round_file_check` refuses it"*), not `missing`. `flow-walker.sh` → `STATE` treats a round with an `unreadable` gate as inconsistent evidence (*"no present gate reads `unreadable`"*), so `start` reopens the **whole set** at that round. It does not reopen only the missing gates. The conclusion still holds: the refused gate is reviewed again in either order. But the mechanism the README entry would cite is wrong. The suite cases that a literal reading of *"cite the case by its quoted title"* points to are `flow-walker-resume.test.mjs` → *"(8) with the saved walk deleted and two of three round files committed, start dispatches only the third gate at counter 0"* and *"(11) a partial return: one gate's error escalates after the set, and a start dispatches only the missing gate"*. Both exercise the missing-gate path. The case that matches this combination is *"(9) inconsistent round evidence dispatches the whole set, and each gate replaces its file"*.
   This is a Should Fix because it is descriptive prose in the **Chosen** entry, and no step fails because of it.
   **Fix:** In Task 2's **Bash:** sub-bullet, say that `start` reopens the whole set, because the refused file reads `unreadable`. Cite `STATE`'s inconsistent-evidence clause and, if a case is cited, the whole-set case (9). Correct the story index `## Context` sentence to match.

## Nice to Have

1. **Story index `## Context`** — the Context carries a bulleted task list and a block quote. They are prose-adjacent and break no parse. The sample index keeps Context to paragraphs only.
