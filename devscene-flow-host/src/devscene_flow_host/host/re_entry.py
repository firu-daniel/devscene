"""A re-entry's two calls: the host's `start` and `current`.

The rule: `start_walk` reads as `flow-walker.sh`'s `start` — the round position is rebuilt from
the round files through `round_resume` and GraphScene's `Walker.start` — and `current_step` as
its `current`, which re-prints the saved step with every gate marked `round.redo.<gate>` left
out (`render_set`):
- `start_walk` is the only call here that clears the refusal record and the kept findings record
  (`RevisionFindingsStore`, bash's `revision_findings`), and only when the walk started; a
  `Refused` start leaves both as they were.
- `current_step` takes no lock and changes nothing; it returns the kept findings record as it
  stands.
- A refused gate is never dispatched twice: it stays out of the re-read set until
  `record_outcome` re-dispatches it.
`start_walk` takes the `RefusalStore` lock before the walk's lock and releases it after, as
`record_outcome` does. A `RecordError`, and the `ValueError` for a round gate with no
`findingsFolder`, propagate.

Deliberately not covered:
- The counter and the prompt variants a lost walk loses: every `start` sets the counter to 0,
  as in bash.
- Choosing the entry: the caller's, from the ledger.
"""

from pathlib import Path

from graphscene import DispatchSet, Refused, Walker

from devscene_flow_host.host.refusals import RefusalStore
from devscene_flow_host.host.resume import round_resume
from devscene_flow_host.host.revision_findings import RevisionFindingsStore
from devscene_flow_host.host.round_gates import HostStep
from devscene_flow_host.records.config import read_config


def start_walk(walker: Walker, repo_root: Path, branch: str, entry: str | None = None) -> HostStep:
    state_dir = read_config(repo_root).state_dir
    store = RefusalStore(repo_root, state_dir, branch)
    with store.lock():
        resume = round_resume(walker.graph, walker.host, repo_root, state_dir, branch, entry)
        step = walker.start(entry, resume=resume)
        if not isinstance(step, Refused):
            store.clear()
            RevisionFindingsStore(repo_root, state_dir, branch).clear()
    return HostStep(step)


def current_step(walker: Walker, repo_root: Path, branch: str) -> HostStep:
    step = walker.current()
    if isinstance(step, Refused):
        return HostStep(step)
    state_dir = read_config(repo_root).state_dir
    store = RefusalStore(repo_root, state_dir, branch)
    if isinstance(step, DispatchSet):
        refusals = store.read(step.round, step.number)
        step = DispatchSet(
            step.round,
            step.number,
            tuple(
                dispatch
                for dispatch in step.dispatches
                if dispatch.node not in refusals.gates or not refusals.gates[dispatch.node].redo
            ),
            step.passed,
        )
    return HostStep(
        step, store.read_announced(), RevisionFindingsStore(repo_root, state_dir, branch).read()
    )
