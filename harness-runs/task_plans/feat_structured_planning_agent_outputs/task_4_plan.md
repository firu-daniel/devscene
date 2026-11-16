### Task 4 — Give `task-plan-reviewer` and `ui-tests-plan-reviewer` a `## Return schema`, and restate the plan gates' return in `plan_review_rounds.md`

**Goal:** Make the two structural plan reviewers return one JSON object each, declared once in a `## Return schema` section, and make the shared round-file module describe the plan gates' return by outcome and field instead of quoting the retired `verdict:` lines.

**Depends on:** Task 1 — the dialect, the canonical sentence (`plugin/instructions/agent_return_contract.md` → `## The return block`) and the `### Return fields` rule.

**The returns this task declares** (the story index `## Context` field table — Tasks 6, 7, 10 and 11 read exactly these names):

- `task-plan-reviewer`: `outcome` `PASS` with required `findings_file` (string; it writes a round file on every outcome); `outcome` `FAIL` with required `findings_file` and `must_fix_count` (integer, `minimum` 1); `outcome` `blocker` with required `blocker` (string).
- `ui-tests-plan-reviewer`: `outcome` `PASS` with no other property (it returns no path, advisory file or not); `outcome` `FAIL` with required `findings_file` and `must_fix_count` (integer, `minimum` 1); `outcome` `blocker` with required `blocker`.

**Where this task stops.** The round file and the findings file keep their own `verdict:` / `review_mode:` lines and formats: they are files, not returns, and the walker and the convergence rules read them as they do today. `## Unsolicited dispatch guidance` is a block copied byte-for-byte across the graded agents and owned by `plugin/instructions/dispatch_discipline_instructions.md`: do not edit it — "above your fixed return — above the fenced block" stays true. `architecture-reviewer` and `business-parity-reviewer`, which also cite `plan_review_rounds.md` → `## The round file`, are Task 5's.

### Targets

- `plugin/agents/task-plan-reviewer.md`
- `plugin/agents/ui-tests-plan-reviewer.md`
- `plugin/instructions/plan_review_rounds.md` → `## The round file`

**Work:**

- [ ] `task-plan-reviewer.md`: in `## Output contract`, replace the two fenced return blocks with the canonical sentence, a paragraph per outcome (keep the round-file format block, which is file content, and keep "Only **Must Fix** makes the round `FAIL`"), and a `### Return fields` subsection — `outcome`, `findings_file`, `must_fix_count`, `blocker`. Add `## Return schema` directly after `## Output contract` (its three variants, `additionalProperties: false`). Rewrite `## Invocation contract` → **Your return is parsed, not read.** to say the caller routes on the `outcome` value, which must be exactly one of the schema's, passing `findings_file` on both verdicts; and `## Read first` → **A cited path you cannot read is a finding, not a fallback.** to return the `blocker` outcome in place of any verdict.
- [ ] `ui-tests-plan-reviewer.md`: the same rewrite for its three outcomes and `### Return fields` — `outcome`, `findings_file`, `must_fix_count`, `blocker` — keeping its findings-file format block and its two `PASS` cases (no finding: no file; advisory only: a file but still a bare `PASS`). Add `## Return schema` after `## Output contract`. Rewrite `## Invocation contract` → **Your return is parsed, not read.**, `## Read first`'s unreadable-path rule (the `blocker` outcome) and `## Process` step 0, the no-plan guard (return the `PASS` outcome at once, write no file).
- [ ] `plan_review_rounds.md` → `## The round file`: replace the fenced `verdict: PASS` / `findings_file:` block and the "Return on `FAIL`" sentence with the plan gates' return stated by outcome and field: on `PASS`, an `outcome` of `PASS` carrying `findings_file`; on `FAIL`, an `outcome` of `FAIL` carrying `findings_file` and `must_fix_count`; the reviewer's own `## Return schema` owns the shape. Leave the round file's own line rules (`verdict:` and `review_mode:` lines inside the file) and every other section untouched, and keep `## Who may cite this` as it is.
- [ ] Hold each definition's word budget (`.claude/context/plugin.md` → `## Writing agent prose`): the schema replaces the retired blocks; no grading rule or edge case is cut.

**Verification:**

- `git grep -nE '^verdict: |^findings_file: |^must_fix_count: ' -- plugin/agents/task-plan-reviewer.md plugin/agents/ui-tests-plan-reviewer.md plugin/instructions/plan_review_rounds.md` prints only the `verdict:` line inside each round-file / findings-file format block, and no return block.
- In each reviewer, every `## Return schema` property has exactly one `### Return fields` bullet and the reverse, the three `outcome` values appear in `## Output contract`, and the canonical sentence is byte-identical to Task 1's.
- Each schema matches its rows of the story index `## Context` field table, variant by variant.
- The `## Unsolicited dispatch guidance` section of both reviewers is byte-identical to its state before this task: `git diff -- plugin/agents/task-plan-reviewer.md plugin/agents/ui-tests-plan-reviewer.md` shows no hunk inside it.
