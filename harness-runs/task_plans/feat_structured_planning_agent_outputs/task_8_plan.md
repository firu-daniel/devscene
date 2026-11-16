### Task 8 — Read the parity, architecture and plan-writer returns in the implementation core and its autonomous fork

**Goal:** Make every site of the implementation flow that routes on, or records, a return of `business-parity-reviewer`, `architecture-reviewer` or `task-plan-writer` read the return object — through `plugin/instructions/agent_return_contract.md` → `## Reading a return` where it routes — and name each field in the citation form.

**Depends on:** Task 1 (`## Reading a return`, `## A return that fails the check`, `## Citing a field`) and Tasks 2 and 5, which declare the fields read here:

- `business-parity-reviewer` and `architecture-reviewer`, implemented-solution mode (Phases A1.5 and A2): an `outcome` of `PASS` with no `findings_file` (no file written); `FAIL` with `` `business-parity-reviewer.findings_file` `` / `` `architecture-reviewer.findings_file` `` — the review **index** path — and `must_fix_count`; `blocker` with `blocker`.
- `architecture-reviewer`, plan-review sub-case (c) (Phase G.2's architecture gate): `PASS` with no `findings_file` (clean or advisory); `FAIL` with `` `architecture-reviewer.findings_file` `` (the flat `review_{iteration}.md`) and `must_fix_count`; `blocker`.
- `task-plan-writer`: `` `task-plan-writer.corpus_staleness` `` — an optional array whose entries each open with `stale-rule` or `undescribed-layer`; absent or empty means no corpus debt.

**Where this task stops.** The unit loop's own parse of `layer-reviewer`'s `verdict:` / `findings_file:` lines (`plugin/instructions/unit_loop_core.md`) is another agent's return and is #380's. `skeptic-reviewer`'s and `branch-reviewer`'s returns, read in Phases B and C2 and in the D.2 **Review questions** bullet, are not this branch's either. The user-review flows are Task 9's.

### Targets

- `plugin/instructions/plan_orchestration_instructions_core.md`
- `plugin/instructions/plan_orchestration_instructions_autonomous.md`

**Work:**

- [ ] Core, `### A1.5.1 Generate the parity review` and `### A2.1 Generate the architecture review` → **Parse the return:** read the return per `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return`; an `outcome` of `PASS` skips to the next phase as today; `FAIL` continues to the commit step with the index named by the reviewer's `findings_file` (citation form); a `blocker` outcome, or the module's third failed check, goes to `<escalate>` naming the phase — the route `## A return that fails the check` gives a flow with no walker.
- [ ] Core, `### G.2 Write and review the test fix plan` → **The architecture gate.**: the `verdict: PASS` / `verdict: FAIL` bullets become `outcome` bullets; the `FAIL` arm's "the latest `findings_file:`" and the revision prompt's `<findings_file>` take `` `architecture-reviewer.findings_file` ``; add the `blocker` and failed-check arm, escalating with the origin `Phase G architecture-reviewer gate` as the cap arm does. Leave `test-fix-plan-writer`'s return arms (its `## Questions`, `fixable:`) untouched — that agent is #380's.
- [ ] Core, `### D.2 Done summary`: the **Business-parity review (Phase A1.5)** and **Architecture review (Phase A2)** bullets' "returned `verdict: PASS`" → an `outcome` of `PASS`; the **Corpus staleness** bullet takes its entries from `` `task-plan-writer.corpus_staleness` `` (absent or empty is "none reported"), keeping its earlier-session rule.
- [ ] Autonomous fork: the `*g` / `*f` flip paragraphs (the clean-`PASS` arm — "the reviewer's `verdict: PASS` with no file written" — and **Zero-finding rounds**) name the `PASS` outcome; **The plan's corpus staleness is one of the observations.** reads `` `task-plan-writer.corpus_staleness` `` (an absent or empty field means no corpus debt, never "the planner did not check"), keeping the one-`tooling-gap`-entry rule and its keying on each entry's type. Leave **A reviewer's `## Questions` section is not an observation.** as it is: it is `branch-reviewer`'s and `skeptic-reviewer`'s.
- [ ] Add the core to the module's roster by the pointer above (Task 1 lists it), and add no field name outside the citation form.

**Verification:**

- `git grep -nE 'verdict: (PASS|FAIL)|## Corpus staleness' -- plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/plan_orchestration_instructions_autonomous.md` prints only lines about `layer-reviewer`, `branch-reviewer`, `skeptic-reviewer`, `review-plan-reviewer` or `test-fix-plan-writer`, none about the parity or architecture reviewer or the plan writer.
- Every `` `<agent>.<field>` `` citation in the two files names a property the story index `## Context` field table lists for that agent.
- Phases A1.5, A2 and the G.2 architecture gate each have an arm for `PASS`, `FAIL`, `blocker` and the failed check.
