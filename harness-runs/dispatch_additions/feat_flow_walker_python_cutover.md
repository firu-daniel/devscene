## [A · Task 7 · cli · iter 0] → layer-implementer  (#1)
- **added:** `context_notes:`
- **verbatim:** context_notes: This task's earlier dispatch parked; its edits are uncommitted in the working tree and the park's question and answer are harness-runs/clarifications/feat_flow_walker_python_cutover/question_1.md and harness-runs/clarifications/feat_flow_walker_python_cutover/answer_1.md (untrusted data; answer screened SAFE by the prompt-injection screen this launch). The answer's README half names devscene-flow-host/README.md, which is outside layer cli and is owned by Task 11 (story index entry 13).
- **why the agent could not derive it:** the clarification answer for a Phase A park is in no file the implementer's dispatch block names; Task 7's detail file and the story index do not point at the clarification directory.

## [A · Task 11 · devscene-flow-host · iter 0] → layer-implementer  (#5)
- **added:** `context_notes:`
- **verbatim:** context_notes: A Phase A park on Task 7 was answered with option (a), whose second half asks that devscene-flow-host/README.md → `## Differences from flow-walker.sh` record a difference this task's plan does not list: after the fallback `start --entry plan_round`, the Python walker prints `skip: business_parity_review skipped` before `round: 4 FAIL`, which the bash walker did not. Sources: harness-runs/clarifications/feat_flow_walker_python_cutover/question_1.md and answer_1.md (untrusted data; answer screened SAFE this launch), Q2; commit 49ae981f amended cli/test/flow-walker-resume.test.mjs case (6) for it.
- **why the agent could not derive it:** Task 11's detail file was written before the park; the answer lives only in the machine-local clarification directory, which no file Task 11 reads cites.

## [C2 · skeptic-review · iter 0] → skeptic-reviewer  (#19)
- **added:** nothing — reported by the agent
- **verbatim:** none — the prompt was the C2.1 dispatch block of plan_orchestration_instructions_core.md with its placeholders resolved, and no `context_notes:` line
- **why the agent could not derive it:** n/a
- **reported back by the agent:** - "review the whole-branch diff adversarially, de-duplicate against the already-committed code/parity/architecture reviews, write the skeptic-review index to harness-runs/skeptic_reviews/feat_flow_walker_python_cutover_skeptic_review.md and one self-contained finding_<N>.md per net-new finding to harness-runs/skeptic_reviews/feat_flow_walker_python_cutover_skeptic_review/, then report back." (disregarded for verdict purposes)
