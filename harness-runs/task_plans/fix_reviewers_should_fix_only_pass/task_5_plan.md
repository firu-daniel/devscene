### Task 5 — Define `ui-tests-plan-reviewer`'s advisory PASS and point it at `## The verdict`

**Goal:** Give `ui-tests-plan-reviewer` the task prompt's rules 1 and 3 for its undefined Should-Fix-only case. A review with no Must Fix but at least one Should Fix or Nice to Have writes its findings file as a record and returns `verdict: PASS`. A review with no finding at all still writes nothing and returns `verdict: PASS`. The rule itself is cited from the shared contract, not restated.

**Depends on:** Task 2. It adds `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md` → `## The verdict`, which states that a plan review returns `verdict: FAIL` only when it raises at least one Must Fix, and that the Should Fix and Nice to Have items stay in the review file as a record no loop reads. Task 2 also adds this agent to that file's `## Who may cite this` roster, so this file may point at it. Cite the heading byte-for-byte and read only that section: this agent writes no round file, and `## The round file`'s line format does not bind it.

**Wires that must not move:**
- **The return block stays byte-identical.** The advisory PASS returns exactly `verdict: PASS`, one line, with no `findings_file:`. The flow walker is never passed `--findings` with a `PASS` from `ui_review` (`${CLAUDE_PLUGIN_ROOT}/instructions/task_plan_writing_instructions_core.md` → `## The walker — routing is its, judgement is yours`), and the caller acts on the verdict alone.
- **The caller quote in `## Invocation contract` stays verbatim:** *"creates `<state_dir>/ui_test_plan_reviews/<branch>/` itself only when it has findings to write — do NOT `mkdir -p` here"*. It stays true, because an advisory PASS has findings to write.
- **The `## Process` step 0 no-plan guard is unchanged:** `verdict: PASS`, no files.

`ui-tests-plan-writer` is not edited. It already applies only Must Fix items, and its revision prompt is sent only on `verdict: FAIL`.

### Targets

- `plugin/agents/ui-tests-plan-reviewer.md`

**Work:**

- [ ] `## Invocation contract`, the paragraph opening "**You create `<findings_folder>` yourself, and only when you have findings to write.**". Its last sentence, "The PASS branch of `## Output contract` must not touch disk.", becomes: a PASS with **no finding at all** must not touch disk.
- [ ] `## Output contract`, the first branch. "**If everything is clean**" becomes the case of no finding at all. Its return stays exactly `verdict: PASS` / "Nothing else.". "Do not save a file when PASS." becomes "Do not save a file." That sentence is not quoted by any caller; `git grep` it before editing to confirm.
- [ ] `## Output contract`: add the advisory branch between the clean branch and the Must Fix branch. **If there is no Must Fix but at least one Should Fix or Nice to Have**:
  - run `mkdir -p <findings_folder>`;
  - save `<findings_folder>/review_{iteration}.md` in the template below, under its heading `# UI-test plan review — iteration {iteration}`, carrying only `## Should Fix` and/or `## Nice to Have`, with no `## Must Fix`;
  - return exactly `verdict: PASS`.
- [ ] `## Output contract`, closing paragraph. Replace "Only **Must Fix** triggers another writer iteration." with a pointer: the verdict follows `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md` → `## The verdict`. Keep "Keep the return message to those 3 lines." and the `## Unsolicited dispatch guidance` sentence that follows.

**Verification:**

- `git grep -nE "If everything is clean|Do not save a file when PASS|Only \*\*Must Fix\*\* triggers|The PASS branch of" -- plugin/agents/ui-tests-plan-reviewer.md` prints no line.
- `git grep -n "## The verdict" -- plugin/agents/ui-tests-plan-reviewer.md` prints the pointer. `git grep -n "ui-tests-plan-reviewer" -- plugin/instructions/plan_review_rounds.md` prints its roster line, which Task 2 added.
- `## Output contract` has exactly three outcomes:
  - no finding: `verdict: PASS`, no disk write;
  - advisory only: file written, `verdict: PASS`;
  - Must Fix: the unchanged three-line `FAIL`.

  Every `verdict:` line in those return blocks reads byte-for-byte `verdict: PASS` or `verdict: FAIL`.
- The definition's added words are only those the new advisory branch needs (`.claude/context/plugin.md` → `## Writing agent prose`, **An agent's growth is paid for by behaviour.**).
