`fix_reviewers_should_fix_only_pass` makes Should Fix and Nice to Have findings **advisory in every plan-review loop**:

1. **The verdict keys on Must Fix alone.** A plan review with no Must Fix item returns `verdict: PASS`, never `verdict: FAIL`, as `layer-reviewer` already does (`plugin/agents/layer-reviewer.md` → `## Output contract`).
2. **The writer acts on Must Fix alone.** A plan writer re-dispatched after a failing round applies (or rejects) the round's Must Fix items and never acts on a Should Fix or Nice to Have item, whichever gate's file it sits in.
3. **Should Fix and Nice to Have stay in the review file as a human record.** Nothing in a loop reads them, and no agent is given a new duty to read them.

This branch builds on #365 (`feat_converging_plan_reviews`) and #371 (`feat_parallel_plan_reviews`) as they were merged. Read what they shipped for round files, verdicts, the writer's revision and round-close routing — `plugin/instructions/plan_review_rounds.md` is the shared contract — and apply these rules on top of it.

> ⚠️ **Find every anchor in this prompt by its quoted text or heading, never by line number.**

## Why

**What was observed (feat_gate12_sandbox_round_driver, 2026-11-04).** The task-plan loop parked at its 5-revision cap with the architecture gate still open. Its review files said `## Must Fix` → `_None._` and still returned `verdict: FAIL`, `must_fix_count: 0`. The revisions changed nothing the reviewer counted, it raised the same Should Fix items again, and the loop ran until the cap.

**What #365 changed since.** #365 made every gate of a round write its round file, `PASS` included, with its Should Fix and Nice to Have, and re-dispatches the writer once per failing round with every findings file of the round. It also added `plan_review_rounds.md` → `## The writer's revision` item 3: *"Each Should Fix of the round is applied, or recorded under `## Rejected findings` with its reason"*. Together these apply every gate's Should Fix items when any one gate raises a Must Fix, and none of them when every gate passes: whether a Should Fix is acted on depends on another gate's verdict. Rule 2 removes that coupling. The ledger line the rule came from has been retired on its own branch.

## What already holds — keep it

- `task-plan-reviewer` → `## Output contract`: *"Only **Must Fix** makes the round `FAIL`; a round whose only findings are Should Fix, Nice to Have or incidental is a `PASS`."*
- `plan_review_rounds.md` → `## The round file`: the round file is written on `PASS` too and may carry `## Should Fix` and `## Nice to Have` — that is the record rule 3 keeps.

## What changes

1. **`plan_review_rounds.md` → `## The writer's revision`** — item 3 goes. The writer acts on the round's Must Fix items only; say so in the place item 3 held, once. The revision note and `## Rejected findings` then carry Must Fix items only.
2. **`task-plan-writer` and `user-review-fix-plan-writer`** — each cites that section and paraphrases *"apply or reject each Should Fix"*; drop the paraphrase. In `user-review-fix-plan-writer` this is the **revision of its fix plan against reviewer findings** only: its own Must Fix / Should Fix / Nice to Have classification of the user's observations is a different thing and does not change.
3. **`architecture-reviewer` and `business-parity-reviewer` in plan-review mode** — neither states that a review without a Must Fix is a `PASS`, and the closing *"Only **Must Fix** triggers another upstream iteration"* reads as permitting `FAIL` with zero Must Fix. State rule 1 where the shared contract can carry it once, and point at it.
4. **`architecture-reviewer` sub-case (c)** (test fix plan, insertion point 4) — still the pre-#365 *"Clean review"*: `PASS` with no file, and the Should-Fix-only case undefined. Apply rules 1 and 3.
5. **`ui-tests-plan-reviewer`** — `## Output contract` returns `PASS` only *"If everything is clean"* and writes no file on `PASS`; the Should-Fix-only case is undefined. Apply rules 1 and 3. `ui-tests-plan-writer` already applies only Must Fix items; its *"Same shape as the `task-plan-writer`'s revision mode"* must still be true once this branch lands.

## Scope

- **In scope:** `task-plan-reviewer`, `ui-tests-plan-reviewer`, and `architecture-reviewer` / `business-parity-reviewer` in plan-review mode, in every loop that dispatches them over a plan, plus the writers those loops re-dispatch.
- **Out of scope:** every other review keeps its current contract. That includes the implemented-solution mode of the reviewers above, the end-of-branch reviewers (which keep reading only `## Incidental findings (not gating)` from the planning rounds), and `qa-tester`'s deliberate `verdict: FAIL` with `must_fix_count: 0`.
- **Unchanged:** Must Fix grading, and how a reviewer decides what is a Should Fix.
- **Wire strings:** every wire string a caller matches stays byte-identical unless the same branch changes the caller.
