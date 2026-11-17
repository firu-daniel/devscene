# Review plan meta-review — iteration 0

## Must Fix

1. **The `general` layer was touched, and the review shows no check drawn from its conventions document** — refers to "Missed checks". File: the index, `harness-runs/code_reviews/feat_structured_outputs_branch_review_code_review.md`.
   The diff against `origin/dev` changes `docs/structured-agent-returns.md`. That path falls under the `general` layer (`path: "."`), whose rules are `.claude/context/conventions.md`. The index's `**What was checked:**` list grades the docs edit only against the story plan's Goal 3, which is about routing. Nothing in it is drawn from `.claude/context/conventions.md`. The rules that bind this edit are `### Where a new responsibility goes` (*"a measured fact or a decision of record → `docs/`, and nowhere else"*) and `## Documents of record`, which covers how a measured fact is stated and requires a deferral to cite a numbered roadmap item. No finding and no clean-pass rationale covers the `general` layer. That leaves one touched layer unreviewed against its own rules.
   **Fix:** In the index, add a bullet to `**What was checked:**` that grades the `docs/structured-agent-returns.md` edit against `.claude/context/conventions.md` → `## Documents of record` and `### Where a new responsibility goes`. If that check turns up a defect, add a new `finding_<N>.md` and its readiness entry instead.

2. **The `## Agent prose` lessons the diff exhibits have no clean-pass rationale** — refers to "Missed checks". File: the index, `harness-runs/code_reviews/feat_structured_outputs_branch_review_code_review.md`.
   The diff exhibits several `harness-runs/lessons.md` → `## Agent prose` categories that the story plan itself names as binding (scope register rows 76–79):
   - `plugin/instructions/agent_return_contract.md` → `## A return that fails the check` is amended. That is the *"A shared instruction module carries only what its runtime reader acts on"* lesson.
   - Five agent definitions change and grow. `branch-reviewer.md` goes +17/−8. That is the *"cut restatement or rationale, never a definition or edge case"* lesson, which `.claude/context/plugin.md` → `## Writing agent prose` → *"An agent's growth is paid for by behaviour"* codifies.
   - New outcome values are introduced (`returned`, `written`, `not_written`, `questions`). That is the *"one token with no space"* lesson.

   Finding 1 cites the ledger, but only its *"State a new behaviour once"* lesson. The `**What was checked:**` list confirms that the amended module takes the named `error` route. It never states that the amendment is runtime routing content rather than an authoring rule, that each definition's added words are paid for by the new return behaviour, or that every outcome is one token. A ledger category the diff exhibits needs either a finding or a clean-pass rationale.
   **Fix:** In the index, add a `**What was checked:**` bullet that grades the diff against each of these three `## Agent prose` lessons: the shared-module rule for `agent_return_contract.md`, the agent-growth rule for the five definitions, and the one-token outcome rule for every new outcome value. For any lesson the diff breaks, add a new `finding_<N>.md` with its readiness entry and index pointer instead.

## Should Fix

None. The index's structure, its readiness section, the four index↔finding pointers, the folder and suffix match, and the four finding files' site anchors and fixes are all correct. Each finding's quoted substring resolves in the tree.

## Nice to Have

None.
