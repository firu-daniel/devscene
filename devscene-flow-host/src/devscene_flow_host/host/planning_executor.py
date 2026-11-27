"""`PlanningExecutor`, a `graphscene.Executor` over an inner one that adds the reviewer-file rules
GraphScene's run mode records without: it calls `Walker.next` directly, never
`devscene_flow_host.host.round_gates.record_outcome`.

The rule: reads as `record_outcome`'s findings-file, round-file and kept-findings rules, and as
the retired pilot's `pnl_reap` (`cli/templates/scripts/lib/planning-node-lib.sh`, read in its
history), which reaped a
reviewer return without a `findings_file` as `class=infra` before `record_outcome` saw it:
- Every `Failed`, and every `Completed` whose outcome is not a verdict outcome of
  `dispatch.node` — one the node declares and the graph's vocabulary gives a `verdict` — is
  passed on unchanged.
- A verdict `Completed` whose verdict is `fail`, or that is at a gate of a round node
  (`host/reviewers.py` → `round_of_gate`), and whose `detail` is `None` or blank, becomes
  `Failed("infra", "<outcome> carries no findings_file")`.
- At a round gate, a `detail` that `round_file_problem` refuses becomes
  `Failed("infra", "the round file was refused: <problem>")`; the path is resolved by
  `round_file_path`, absolute as given and relative under `repo_root`.
- At a node that is not a round gate, a `fail` verdict with a `detail` writes `(detail,)` to
  `RevisionFindingsStore` under `RefusalStore`'s lock; `clear_revision_findings` clears it under
  the same lock.
The file reads and the lock run in a worker thread, so a set's other runs keep the event loop.

Deliberately not covered:
- Retrying a `Failed("infra")`: GraphScene's `AttemptBook`.
- Constructing the inner executor: `host/planning_run.py`'s.
- Closing a round: its `clear_revision_findings` call is `host/planning_run.py`'s.
"""

import asyncio
from pathlib import Path

from graphscene import Completed, Dispatch, DispatchNode, Executor, Failed, FlowGraph, NodeResult

from devscene_flow_host.host.refusals import RefusalStore
from devscene_flow_host.host.reviewers import round_of_gate
from devscene_flow_host.host.revision_findings import RevisionFindingsStore
from devscene_flow_host.records.round_files import round_file_path, round_file_problem


class PlanningExecutor:
    def __init__(
        self,
        inner: Executor,
        *,
        graph: FlowGraph,
        repo_root: Path,
        state_dir: str,
        branch: str,
    ) -> None:
        self._inner = inner
        self._graph = graph
        self._repo_root = repo_root
        self._state_dir = state_dir
        self._branch = branch

    async def run(self, dispatch: Dispatch) -> NodeResult:
        result = await self._inner.run(dispatch)
        if not isinstance(result, Completed):
            return result
        return await asyncio.to_thread(self._check, dispatch.node, result)

    def _check(self, node: str, result: Completed) -> NodeResult:
        found = self._graph.nodes.get(node)
        if not isinstance(found, DispatchNode) or result.outcome not in found.outcomes:
            return result
        declared = self._graph.vocabulary.outcomes.get(result.outcome)
        if declared is None or declared.verdict is None:
            return result
        at_gate = round_of_gate(self._graph, node) is not None
        detail = result.detail
        if detail is None or not detail.strip():
            if declared.verdict == "fail" or at_gate:
                return Failed("infra", f"{result.outcome} carries no findings_file")
            return result
        if at_gate:
            problem = round_file_problem(round_file_path(self._repo_root, detail))
            if problem is not None:
                return Failed("infra", f"the round file was refused: {problem}")
            return result
        if declared.verdict == "fail":
            with RefusalStore(self._repo_root, self._state_dir, self._branch).lock():
                RevisionFindingsStore(self._repo_root, self._state_dir, self._branch).write(
                    (detail,)
                )
        return result


def clear_revision_findings(repo_root: Path, state_dir: str, branch: str) -> None:
    with RefusalStore(repo_root, state_dir, branch).lock():
        RevisionFindingsStore(repo_root, state_dir, branch).clear()
