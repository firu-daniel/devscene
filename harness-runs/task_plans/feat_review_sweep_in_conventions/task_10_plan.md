### Task 10 — Document the sweep document, the `sweep` target and the `review-sweep` check

**Goal:** Bring the documents of record in line with what Tasks 1–8 shipped:
- the analyze command's decisions (`docs/analyze.md`);
- the CLI's re-run contract, analyze-step vocabulary and `doctor` check table (`docs/cli.md`);
- the `.claude/` namespace inventory in `ARCHITECTURE.md`.

**Depends on:**
- **Task 1:** `.claude/review-sweep.md`, `create-if-absent`, with the same `--force` keep as a conventions stub; `REVIEW_SWEEP_PATH` in `cli/src/generators/claudeContext.ts`; `sweep` as the fourth entry of `RESERVED_ANALYZE_TARGETS`.
- **Task 4:** the `doctor` check `review-sweep`. It warns when the document is absent (remedy `npx devscene init`) or still an untouched skeleton (remedy `/devscene:analyze sweep` or a hand edit, committed on the default branch), and passes otherwise.
- **Task 7:** the `sweep` target runs last, after the corpus pass, and goes through one write → review → fix chain; it is never a corpus member.
- **Tasks 2, 3 and 8:** the script reads its rows from the default branch and applies them to the branch's added lines; the reviewer calls the main checkout's copy and reports an exit `2` as a configuration gap.

**How this task's implementer reads the conventions.** This is the catch-all layer, so its implementer reads every configured layer's conventions document. Each added sentence states what the code does, citing the module or the section that owns it, rather than restating a rule another file owns (`.claude/context/conventions.md` → `## Documents of record`).

### Targets

- `docs/analyze.md`
- `docs/cli.md`
- `ARCHITECTURE.md`

**Work:**

- [ ] `docs/analyze.md` → `## 1. The target vocabulary`:
  - add a `sweep` row: the review-sweep document `.claude/review-sweep.md`;
  - change "plus three reserved names" to four;
  - extend the no-argument order sentence with `sweep` last, and the reason: its rows are derived from the finished conventions documents;
  - make **The collision rule** paragraph name all four reserved words.
- [ ] `docs/analyze.md`:
  - in ``## 7. `doctor`'s share``, add one sentence naming the `review-sweep` check and the two states it warns on, and keep the paragraph opening "Two further checks are this command's share without being `setup-analysis`" true: either the new sentence stands in its own paragraph, or that count becomes three;
  - in §4's paragraph opening "What a forced setup re-run costs the analysis.", add the sweep document to the artifacts a forced run keeps ("Two artifacts are kept instead" becomes three): an already-skeleton `.claude/review-sweep.md` whose `.bak` holds the filled one is kept, as a conventions document is (Task 1);
  - add **`## 13. The review-sweep document`**, recording the decisions with what each was chosen over:
    - its own document rather than rows in a conventions document, so no per-unit agent loads them;
    - its place in the run, last and outside the corpus pass;
    - the row format and the `\|` escape, over a TSV block;
    - the regex-grounding check;
    - the sweep script, over the reviewer's own grep;
    - rows read from the default branch, so a branch cannot weaken its own sweep;
    - the rejected gate tier and its reason: a hit stays a lead, and Run gates' units are test files;
    - the stub's UI classes kept as skeleton examples;
    - lessons never becoming rows.
- [ ] `docs/cli.md`:
  - in the analyze-step paragraph ("takes **this repository's configured layer names** plus the three"), name the four reserved targets;
  - in `## 3. The re-run contract`'s table, add a `.claude/review-sweep.md` row after `.claude/devscene-task-offer.md`: `create-if-absent`, filled by `/devscene:analyze sweep` and maintained by the adopter, with the same two-part filled test and the same conditional `--force` keep as a conventions stub;
  - in the bullet under that table that counts the artifacts kept conditionally, add the review-sweep document beside the conventions documents if that bullet enumerates them;
  - in the paragraph opening **"Two families land in `scriptsDir`, and only one of them is generated."**, name the review sweep's script `review-sweep.sh` in the outer-loop inventory (after the prompt-injection screen's script), and add it to the agent-invocable list: the end-of-branch reviewer runs the main checkout's copy against its run copy (`--repo`) to apply the default branch's sweep rows to the branch's added lines; it stays sandboxed and carries no deny-list entry (Task 3's row: `agentInvocable: true`, no `runsUnsandboxed`).
- [ ] `docs/cli.md` → the `doctor` check table and the severity list under it:
  - add a `review-sweep` row immediately after the `task-offer-rules` row, in the same column shape, stating what it grades and that it only ever warns;
  - in the list opening "Which severity a check carries is a decision, not a default", add a **`review-sweep` is a warning in every state it can report** bullet after the `task-offer-rules` bullet and its arms: a missing or unfilled sweep document disables the reviewer's grep half only, which the reviewer reports as a configuration gap, so the run still works; name both remedies, `npx devscene init` for an absent document and `/devscene:analyze sweep` or a hand edit for an unfilled one, each committed on the default branch.
- [ ] `ARCHITECTURE.md` → the "The adopter's `.claude/` namespace" row: add `REVIEW_SWEEP_PATH` to the `claudeContext.ts` constants it lists.

**Verification:**

- `git grep -n -E 'three reserved|plus the three' -- docs` prints nothing.
- `git grep -n -F 'review-sweep' -- docs/analyze.md docs/cli.md ARCHITECTURE.md` prints the new rows and the new section.
- `git grep -n -F 'review-sweep.sh' -- docs/cli.md` includes the "Two families land in `scriptsDir`" paragraph.
- `git grep -n -F 'Two artifacts are kept instead' -- docs/analyze.md` prints nothing.
- `git grep -n -F '**`review-sweep` is a warning' -- docs/cli.md` prints the new severity bullet.
- Every module, constant and heading a new sentence cites resolves: `git grep -n -F 'REVIEW_SWEEP_PATH' -- cli/src` and `git grep -n -F "id: 'review-sweep'" -- cli/src/doctor/checks.ts` each resolve.
