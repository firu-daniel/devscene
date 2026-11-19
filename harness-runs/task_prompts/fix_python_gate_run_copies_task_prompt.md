`fix_python_gate_run_copies` makes the Python gates run inside an unattended run's copy instead of grading BLOCKED, so GraphScene's tests gate the branches that build it. Part of #376.

## Why

Gate 13 (`scripts/python-service.sh`) can't run in a run copy today. Unprovisioned, it grades BLOCKED and the round passes with it hand-run. Provisioned with `sync`, `uv` fails on `~/.cache/uv` under the sandbox and the gate is FAIL. That's tolerable for the docs-retrieval service, but not for the engine of the outer loop. Once the walker is Python, the `flow-walker*` node suites will hit the same wall too.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- A `uv` cache location the sandbox can write, keyed per checkout like the venv.
- A way for a run copy to get its environment without the gate reaching the network (provisioned with the run copy, synced offline from the main checkout's cache, or something else).
- Let `python-service.sh` serve more than one package (today it is fixed on `docs-retrieval-service/`).
- A host with no `uv` still grades BLOCKED.
