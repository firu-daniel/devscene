### Task 7 — Have `layer-implementer` record a `**Cause:**` line, and re-point the writers, `qa-tester` and `conventions-reviewer` at the commit step

**Goal:** Make the producer of every disposition and already-passing record write the one line the wrapper reads its cause from. Then re-point the five agent definitions that describe the committer as the committing role at **the commit step**.

**Depends on:** Task 1. `lib/unit-commit-lib.sh` → `ucl_record_cause` reads the cause as the text after `**Cause:** ` on the first such line inside the first `## Disposition` (or `## Already passing`) section of the unit's detail file. When that line is absent, it falls back to `cause not recorded — see <detail file>`. Task 3 calls it only when the detail file is in the unit's stage set.

**The committing-role sentence, byte-for-byte as `## Context` fixes it:** *the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none*.

### Targets

- `plugin/agents/layer-implementer.md`
- `plugin/agents/qa-tester.md`
- `plugin/agents/task-plan-writer.md`
- `plugin/agents/user-review-fix-plan-writer.md`
- `plugin/agents/conventions-reviewer.md`

**Work:**

- [ ] **`layer-implementer.md` — the two record formats.**
  - **The disposition record.** In **The disposition record.**, state that the `## Disposition` section opens with the line `**Cause:** <one-line cause>`, carrying the same text as the return's `blocker: prohibited — <one-line cause>; …`. The four lettered parts follow it.
  - **The already-passing record.** In **The already-passing record.**, state the same for `## Already passing` and the `already passing — ` return.
  - **Why.** Name the reader in one clause: the commit step reads that line for the commit's body record (`<scripts_dir>/commit-on-branch.sh` → **THE SUBJECT AND ITS RECORD**).
  - **Word budget.** Add no other words (`.claude/context/plugin.md` → `## Writing agent prose`, an agent's growth is paid for by behaviour).
- [ ] **`layer-implementer.md` — the committer mentions.** Replace "the `committer` agent in every flow that dispatches one, the orchestrator itself in the supervised flow" with the committing-role sentence above. Replace "the committer stages both halves" with "the commit step stages both halves".
- [ ] **`qa-tester.md`.** "the caller's committer marks a passing test `[x]`" becomes "the caller's commit step marks a passing test `[x]`". "(informational; the committer ignores them)" becomes "(informational; the commit step ignores them)".
- [ ] **`task-plan-writer.md` and `user-review-fix-plan-writer.md`.**
  - **The committing-role sentence.** In `task-plan-writer.md` → `## Process` step 7's readiness bullet, replace the parenthetical committing-role sentence with the one above. Make the same replacement in `user-review-fix-plan-writer.md`.
  - **Other mentions.** "the committer never touches them" / "the committer ignores them" → "the commit step …". In step 7(b), "an implementer, reviewer or committer does the task" → "an implementer or reviewer does the task, and the commit step commits it". "the orchestrator and the committer ignore them" → "the orchestrator and the commit step ignore them".
  - **Deviations from plan:** `user-review-fix-plan-writer.md` carried no parenthetical committing-role sentence to replace, only "that transition belongs to the committing role". The sentence was appended there after a colon, so the second Verification grep lists that file as the plan requires.
- [ ] **`conventions-reviewer.md`.** "a list reaching past the committer's own commit modes is correct" becomes "a list reaching past the commit step's own fixed subjects is correct". Change nothing else there.

**Verification:**

- `git grep -n -w committer -- plugin/agents/layer-implementer.md plugin/agents/qa-tester.md plugin/agents/task-plan-writer.md plugin/agents/user-review-fix-plan-writer.md plugin/agents/conventions-reviewer.md` prints nothing.
- `git grep -n -F 'the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none' -- plugin/agents` lists `layer-implementer.md`, `task-plan-writer.md` and `user-review-fix-plan-writer.md`.
- `git grep -n -F '**Cause:** ' -- plugin/agents/layer-implementer.md` shows the line stated once for each of the two records.
- The return forms `blocker: prohibited — <one-line cause>; disposition appended to <detail_file>` and `blocker: already passing — <one-line cause>; record appended to <detail_file>` are byte-identical to `git show HEAD:plugin/agents/layer-implementer.md`.
