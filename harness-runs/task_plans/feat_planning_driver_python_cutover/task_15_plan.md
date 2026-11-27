### Task 15 — Check findings and round files, and keep revision findings, in `host/planning_executor.py`

**Goal:** Wrap `ClaudeExecutor` in `PlanningExecutor`, an `Executor` that adds the reviewer-file rules run mode would otherwise skip. Run mode records through `Walker.next` directly, never through `host/round_gates.py` → `record_outcome` (the story index's third `Top risks:` entry). So:
- a verdict with no findings file, or a round gate's file that `round_file_problem` refuses, becomes `Failed("infra", …)`;
- a lone reviewer's `FAIL` findings file is kept in `RevisionFindingsStore`, where `CorePromptBuilder` reads it for the revision that follows.

**The two producers this task reads, as they define their values:**
- **`Completed.outcome` and `Completed.detail`.** `ClaudeExecutor.run` returns `Completed(outcome, detail)`, where `detail` is the return object's `findings_file`, or `None`. GraphScene passes `detail` to `Walker.next` only for a gate of a set (`graphscene/src/graphscene/model/execution.py` → *"The rule"*).
- **The kept findings.** `CorePromptBuilder` (`host/agent_prompts.py`) reads `RevisionFindingsStore(repo_root, state_dir, branch).read()` for a `revision` dispatch, through `host/prompt_variants.py` → `findings_files(revision_findings, closed_round)`.

**Where this task stops.**
- **Constructing the inner executor** is **Task 16's**.
- **Retrying a `Failed("infra")`** is GraphScene's `AttemptBook`: alone, three attempts, then recorded as the run's `failure_outcome`, `error`, which the round holds. That matches *"The third refusal of one gate in a round records the held outcome `error`"* (`round_gates.py`). Task 16 passes `failure_outcome="error"`.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/planning_executor.py` (new)
- `devscene-flow-host/tests/test_planning_executor.py` (new)

**Work:**

- [ ] **`PlanningExecutor(inner: Executor, *, graph: FlowGraph, repo_root: Path, state_dir: str, branch: str)`.** `run(dispatch)` awaits `inner.run(dispatch)`, and passes on unchanged every `Failed`, and every `Completed` whose outcome is not a verdict outcome of `dispatch.node`. Whether an outcome is a verdict is read off the graph's outcome declaration, as `round_gates.py` reads it.
- [ ] **The findings-file presence rule** is `record_outcome`'s, and `pnl_reap`'s `class=infra` before it. A `Completed` whose outcome has verdict `fail`, or that is any verdict outcome at a gate of a round node (`host/reviewers.py` → `round_of_gate`), and whose `detail` is `None` or blank, becomes `Failed("infra", "<outcome> carries no findings_file")`.
- [ ] **The round-file rule.** At a round gate, a `detail` for which `records/round_files.py` → `round_file_problem` returns a problem becomes `Failed("infra", "the round file was refused: <problem>")`. The path is read absolute as given, and relative under `repo_root`, as `flow-walker.sh next --findings` reads it.
- [ ] **The kept-findings rule.** At a node that is not a round gate, a `Completed` `fail` verdict with a `detail` writes `(detail,)` to `RevisionFindingsStore`, under `RefusalStore`'s lock, as `record_outcome` keeps `revision_findings`.
  - `clear_revision_findings(repo_root, state_dir, branch) -> None` clears the store under the same lock. Task 16 calls it when a round closes, as `record_outcome` clears the record on a `RoundPassage`.
  - **The module docstring** states *"The rule:"* as given above, naming `record_outcome` and `pnl_reap` as the rules it reads as, and a *"Deliberately not covered"* list: retrying a `Failed("infra")`, which is GraphScene's `AttemptBook`; constructing the inner executor, which is Task 16's `host/planning_run.py`; and closing a round, whose `clear_revision_findings` call is Task 16's too.
- [ ] **`tests/test_planning_executor.py`** drives a stand-in inner executor returning scripted `NodeResult`s over the real planning graph, loaded read-only from `cli/templates/scripts/flows/task_plan_writing.graph.json`. Its cases:
  - its header rule;
  - a non-verdict `Completed` passed through;
  - a gate `PASS` with no detail made `infra`, with exact text;
  - a `FAIL` with a blank detail made `infra`;
  - a gate `PASS` whose planted round file has no verdict line made `infra`, with `round_file_problem`'s text;
  - a valid round file passed through;
  - `ui_review`'s `FAIL` with a detail kept in the store, and `clear_revision_findings` emptying it;
  - a `Failed` passed through unchanged.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_executor.py` passes.
- `PlanningExecutor` satisfies `graphscene.Executor` structurally, and `mypy` `strict` passes on its typed assignment in the test.
