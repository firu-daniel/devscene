### Task 4 — Point `architecture-reviewer` and `business-parity-reviewer` at `## The verdict`, and define sub-case (c)'s advisory PASS

**Goal:** In plan-review mode, make both reviewers state the task prompt's rule 1 by pointing at the shared contract, instead of the closing *"Only **Must Fix** triggers another upstream iteration"*, which reads as permitting `FAIL` with zero Must Fix. Also give `architecture-reviewer` sub-case (c), the test fix plan at insertion point 4, the rule-1 and rule-3 behaviour it lacks: a review with Should Fix or Nice to Have but no Must Fix writes its file and returns `verdict: PASS`.

**Depends on:** Task 2. It adds `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md` → `## The verdict`, which states that a plan review returns `verdict: FAIL` only when it raises at least one Must Fix, and that the Should Fix and Nice to Have items stay in the review file as a record no loop reads. Both agents are already on that file's `## Who may cite this` roster. Cite the heading byte-for-byte, and point at it without paraphrasing it.

**Wires that must not move** (`.claude/context/plugin.md` → `## Wires: dispatch in, return out`):
- **Every return block stays byte-identical.** Sub-case (c)'s advisory PASS returns exactly `verdict: PASS`, with no `findings_file:` line: its caller, `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_core.md` → `### G.2 Write and review the test fix plan`, routes `verdict: PASS` straight to G.3 and parses nothing else.
- **The sentence "Nothing else. Do not write any file when PASS." stays verbatim** in `architecture-reviewer`'s `### Clean review (both modes)`. `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_autonomous.md` (the **Zero-finding rounds** paragraph) quotes *"Do not write any file when PASS"* for implemented-solution mode.
- The heading `### Clean review (both modes)` keeps its text.

**Out of scope here:** implemented-solution mode's semantics, in both agents, and `business-parity-reviewer`'s `### Clean review (both modes)`, which covers only implemented-solution mode and the disabled-phase no-op. Sub-cases (a) and (b) already write a round file on `PASS`, per `## The round file`; nothing about their file changes.

### Targets

- `plugin/agents/architecture-reviewer.md`
- `plugin/agents/business-parity-reviewer.md`
- `plugin/instructions/plan_orchestration_instructions_core.md`

**Work:**

- [ ] `architecture-reviewer.md` and `business-parity-reviewer.md` → `## Output contract`.
  - Directly under the intro line "Both modes share the return lines; they differ in **what file they write**.", add one sentence: in plan-review mode the verdict follows `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md` → `## The verdict`.
  - In `### Return lines (both modes on FAIL)`, replace "Only **Must Fix** triggers another upstream iteration." so that it no longer reads as a plan-review verdict rule. Either delete it (the new pointer covers plan-review mode) or scope it explicitly to implemented-solution mode. Either way, implemented-solution mode's return behaviour must not change.
  - Make the edit identical in both files, since the paragraphs are parallel.
- [ ] `architecture-reviewer.md` → `### Clean review (both modes)`. Its opening "Sub-case (c) and implemented-solution mode." becomes sub-case (c) **with no finding at all**, and implemented-solution mode. Keep "Nothing else. Do not write any file when PASS." verbatim.
- [ ] `architecture-reviewer.md` → `## Output contract`. Add a section for **sub-case (c) with no Must Fix but at least one Should Fix or Nice to Have**, placed after `### Clean review (both modes)`. It must say:
  - Run `mkdir -p <findings_folder>`.
  - Write `<findings_folder>/review_{iteration}.md` in sub-case (c)'s existing shape: heading `# Architecture review — iteration {iteration}`, no `verdict:` / `review_mode:` lines, carrying only `## Should Fix` and/or `## Nice to Have`, with no `## Must Fix`.
  - Return exactly `verdict: PASS`, nothing else.

  The existing `## Invocation contract` sentence "In sub-case (c) and implemented-solution mode you create it only when you have findings to write" already covers this. Leave that sentence unchanged.
- [ ] `plan_orchestration_instructions_core.md` → `### G.3 Commit the test fix plan`, the existence-guard sentence. "a gate that passed on iteration 0 created none" becomes a gate that passed on iteration 0 **with no finding at all** created none. A passing gate that raised a Should Fix or Nice to Have now leaves a file there, and the guard already commits it. Change nothing else in G.2 or G.3. G.2's "(The `architecture-reviewer` creates `<test_fix_review_folder>` itself only when it has findings to write — do NOT `mkdir -p` here.)" stays true.

**Verification:**

- `git grep -n "Only \*\*Must Fix\*\* triggers another upstream iteration" -- plugin/agents/architecture-reviewer.md plugin/agents/business-parity-reviewer.md` prints no line, or only lines scoped explicitly to implemented-solution mode.
- `git grep -n "## The verdict" -- plugin/agents/architecture-reviewer.md plugin/agents/business-parity-reviewer.md` prints at least one pointer in each file. Neither file restates the rule in its own words.
- `git grep -n "Do not write any file when PASS" -- plugin` still prints the `architecture-reviewer.md` and `business-parity-reviewer.md` clean-review lines and the `plan_orchestration_instructions_autonomous.md` quote, so the quoter still resolves.
- `git grep -n "passed on iteration 0 created none" -- plugin` prints no line.
- Walk G.2 → G.3 for the three sub-case (c) outcomes and check that each lands correctly:
  - no finding: `verdict: PASS`, no folder, `meta_findings_folder` omitted;
  - advisory only: `verdict: PASS`, a file, `meta_findings_folder` included;
  - Must Fix: unchanged `FAIL` path.
