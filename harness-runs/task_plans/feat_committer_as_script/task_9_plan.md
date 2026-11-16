### Task 9 — Make the unit loop's step 5 one `<commit_call> --unit` call and retire the committer columns

**Goal:** Rewrite `plugin/instructions/unit_loop_core.md` so every unit's commit is one literal Bash call of the wrapper front end, not a `committer` dispatch.

- **The orchestrator's inputs.** It passes only what it already holds from step 1: the row's readiness index and the entry's unit token `K`.
- **The wrapper's job.** The wrapper reads the entry, the detail file and the tree.
- **What is kept.** The orchestrator's rule against opening detail files stays as it stands (steps 1–2), with row `UR-A`'s narrow first-paragraph exception.

**Depends on:**

- **Task 3**, whose front end is `<commit_call> --unit task|review_item --plan <index> --id <K> [--findings <dir>] [--prefix refactor|chore]`.
  - **What it prints.** `commit_sha:`, `subject:`, `files_committed:`, `plan_flipped:` (the entry, `already-[x]: <entry> — not flipped by this call`, or `none`) and `pushed:`. It adds `staged: index-only — …` and `index_sync: failed — …` lines when they apply.
  - **Its exits.** 0 committed (a landed commit already re-synced); 1 a refusal with one `error:` line; 2 protected; 3 `error: nothing to commit`.
  - **What it reads.** The disposition and already-passing causes, from the detail file's `**Cause:** ` line.
- **Task 8**, which declares `<commit_call>` in `mode_contract.md`.
- **Task 7**, which makes `layer-implementer` write that `**Cause:** ` line.

### Targets

- `plugin/instructions/unit_loop_core.md`

**Work:**

- [ ] **Bindings and the pre-dispatch rule.**
  - **The bindings table.** In `## Mode contract — bindings this file uses`, replace the `<committer_push>` row with `<commit_call>`: used at `## The unit loop` step 5; the wrapper prefix the fork binds. Make the same replacement in `### Placeholder resolution` (i), and wherever the `## Resolved values` preamble names the three bindings.
  - **The pre-dispatch rule.** It now binds **two** dispatches, the implementer and the reviewer. Delete the "or the literal `commit` …" clause and the `[A · Task 3 · commit] → committer  (#N)` example. Add one sentence: step 5's commit is a Bash call, not a dispatch, so no safety-contract step applies to it and the dispatch counter does not move.
  - **The step-3 note.** "Step 5's committer dispatch takes that same optional line" goes: the commit call takes no `context_notes:`.
- [ ] **Steps 5 and 6.**
  - **Step 5.** Step 5 becomes: issue, as **one** Bash call, with every placeholder spelled as the literal text it resolves to and no `$` anywhere:

    ```
    <commit_call> --unit <the row's commit unit> --plan <the row's readiness index> --id <K> <the row's commit extra args>
    ```

    `K` is the unit token from step 1's entry, never the walk position `N`.
  - **The once-alone definition.** Carry the sentence byte-for-byte as `autonomous_pause_and_ledger.md` §1.6 states it: **Once, alone** means its own Bash call holding that one command and nothing else — no `cd`, `;`, `&&`, `||`, pipe, `echo "exit $?"`, `$(…)` or shell variable before or after it.
  - **Reading the call.** Exit 0 continues to step 6. Exit 3 is a unit with nothing left to commit; continue. Any `error:` line with exit 1 or 2 `<escalate>`s.
  - **Step 6.** Step 6 takes `<sha>` and `<subject>` from the printed `commit_sha:` / `subject:` lines. It appends `plan_flipped: already-[x]: <entry> — not flipped by this call`, `staged: index-only — …` and `index_sync: failed — …` verbatim, exactly as it appends the committer's lines today.
- [ ] **`### The dispositioned outcome` and `#### The already-passing close`.**
  - **The commit's record.** Replace **Step 5's commit, as this exit calls it.** and **Passing the argument is what puts the disposition on the commit's record; the committer decides only where.** with one paragraph. The loop passes nothing extra. The commit step finds the detail file's `## Disposition` (or `## Already passing`) section and writes the lower-case body line `record disposition of <unit token> — <cause>` (or `mark <unit token> already passing — <cause>`). The cause comes from the section's `**Cause:** ` line. The subject stays the title subject. Only the first section's cause goes on the commit, and every layer's diagnosis stays in the detail file.
  - **What stays.** Keep the "`[x]` means closed, no third marker" paragraph. "the committer resolves the entry and flips `[ ]`→`[x]`" becomes "the commit step resolves …".
  - **The progress clause.** Move the extraction-by-position rule to step 6, which still builds its `dispositioned: ` / `already passing: ` clause from the implementer's return line.
  - **The already-passing close.** Make the matching edit to **Its commit argument.**: no argument; the commit step reads `## Already passing` when no `## Disposition` is present.
- [ ] **The substitution table and its ⚠️ note.**
  - **The columns.** Rename `committer mode` → `commit unit` (values `task` / `review_item`). Rename `committer extra args` → `commit extra args`; its value is `--findings <the row's Per-item findings folder>` when `<per_unit_review>` is `on`, nothing when `off`, and on row `UR-A` additionally `--prefix refactor|chore` on a `## Should Fix` entry. Rename `commit_prefix rule` → `commit prefix`, now stating what the wrapper computes: row `A` the branch-name token, the fix rows `fix`, row `UR-A` its severity mapping.
  - **The ⚠️ note.** Rewrite the note under the table around `--id <K>`. Keep its "**this entry's `K`, never the walk position `N`**" argument and its pointer to `samples/sample_code_review.md`. Drop `task_heading`, `committer.md` and the `error: task_heading required …` quotation, and grep the file for any other `task_heading` citing the committer.
  - **Leave alone.** `### Per-unit review step`'s reviewer block keeps its own `task_heading:`, unchanged.
  - **Before renaming.** Grep `plugin/` for `committer mode`, `committer extra args` and `commit_prefix rule`. Every citer outside this file belongs to another task: `autonomous_pause_and_ledger.md` and `dispatch_discipline_instructions.md` to Task 13, `improvement_observations_instructions.md` to Task 14, `plan_orchestration_instructions.md` to Task 18, and `agents/committer.md` to Task 20, which deletes it. Edit none of them here.
- [ ] **`### Named exceptions`.**
  - **Row A.** **Committer staging.** becomes **Commit staging.**: the commit step stages every changed path, so the per-task file goes when the implementer changed it.
  - **Rows A1.5.3 / A2.3 / C2.4.** The heading "— the index-agnostic `review_item` committer" becomes "— the index-agnostic `review_item` commit". Rewrite its body for the commit step.
  - **Row UR-A.** **Committer staging.** and **Committer `task_heading:`.** become the commit step's staging and `--id <K>`; **`commit_prefix` by severity** maps to `--prefix` on the Should Fix arm only. None of these bold labels, nor the `####` heading above, is cited outside this file today, so renaming them strands no citer.
  - **The fix rows.** **The fix rows — `commit_prefix` by designation** is replaced by one sentence: the wrapper prefixes every fix row `fix`.
  - **The progress lines.** Each "After the committer returns `commit_sha:`" becomes "After the commit call prints `commit_sha:`".

**Verification:**

- `git grep -n -e 'committer' -e 'commit_prefix' -e 'task_heading required' -- plugin/instructions/unit_loop_core.md` prints nothing.
- `git grep -n -F '<commit_call> --unit <the row' -- plugin/instructions/unit_loop_core.md` shows step 5's call.
- `git grep -n -F '**Once, alone** means its own Bash call' -- plugin/instructions/unit_loop_core.md` shows the definition in step 5.
- `git diff -- plugin/instructions/unit_loop_core.md` changes no `##`-level heading, and in `## The test-run rule` no line at all.
- `git grep -n -e 'committer mode' -e 'committer extra args' -e 'commit_prefix rule' -- plugin` lists no file outside the set the **Before renaming** bullet names.

**Deviations from plan:**

- Step 6's sentence "This post-commit progress line is not the pre-dispatch heartbeat of step 5; both exist and neither replaces the other." was removed: step 5 no longer has a heartbeat, so the sentence pointed at nothing.
- Exit 3's "continue" is written as "continue, returning to step 1": an exit-3 call prints no `commit_sha:` / `subject:` for step 6 to report.
- `### Placeholder resolution`'s list of locally defined names was updated with the plan's other edits. It drops the `committer extra args` / ⚠️-note `task_heading` and `committer.md` `<mode>` entries, and adds `<K>` (step 5) and `<unit token>` / `<cause>` (the body-line forms).
- Row `A1.5.3` / `A2.3` / `C2.4`'s index-agnostic paragraph now names `G.4` beside `C` and `E.3`, because it also passes its own index.
