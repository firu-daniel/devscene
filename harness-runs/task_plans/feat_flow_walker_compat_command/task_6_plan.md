### Task 6 — Pin the command's concurrency in `tests/test_flow_walker_concurrency.py`

**Goal:** Prove, at the process level, the property `flow-walker.sh` → `CONCURRENCY` states and `cli/test/flow-walker-concurrency.test.mjs` pins for bash: `start` and `next` hold a lock from before the state is read until after it is replaced, so several calls can record a round's gates at once and **exactly one** of them prints the round's result; `current` takes no lock.

**Depends on:** Task 5, which provides the command as `python -m devscene_flow_host.commands.flow_walker` with bash's verbs and flags plus `--flows <dir>`, exit `0` with the rendered action on stdout, and exit `2` with one `flow-walker: <message>` line for a lock's `TimeoutError`. The locks themselves are the host's and are not changed here: `host/refusals.py` → `RefusalStore.lock()` (`<stateDir>/.flow_walker_state/round_refusals/<branch file>.lock`) taken first by `record_outcome` and `start_walk`, then the walk store's own (`host/store.py` → `walk_store`, `<branch file>.lock`); `current_step` takes neither. Each lock gives up after 120 s; because every caller that takes the walk store's lock already holds `RefusalStore`'s, the walk store's lock is never contended among the command's callers, so a call waits at most the one 120 s bound bash has. This suite does not wait out a timeout — Task 5's `failure` case covers the `TimeoutError` → exit `2` mapping.

### Targets

- `devscene-flow-host/tests/test_flow_walker_concurrency.py` (new)

**Work:**

- [ ] A planted git repository under `tmp_path` (`round_fixtures.init_repo`, `plant_review`, a `devscene.config.json`, git's environment isolated as `tests/test_re_entry.py` → `_isolated_git` does), `--flows` naming the checkout's `cli/templates/scripts/flows` read-only, and a walk started and advanced to `plan_round`'s three-gate set through the command.
- [ ] **One join**: launch the three gates' `next --node <gate> --outcome PASS --findings <its valid file>` as three simultaneous subprocesses of `sys.executable -m devscene_flow_host.commands.flow_walker`; all three exit `0`; exactly one stdout carries `round: 0 PASS`; each of the other two opens `action: wait`; and a following `current` prints `ui_writer`'s dispatch.
- [ ] **`current` takes no lock**: while the test process holds `RefusalStore(root, state_dir, branch).lock()`, a `current` subprocess exits `0` with the pending set, well inside the 120 s bound; released, a `next` goes on to record.
- [ ] The module docstring opens *"The rule this file exists to enforce"*, cites `flow-walker.sh` → `CONCURRENCY` and `cli/test/flow-walker-concurrency.test.mjs`, and states under what it deliberately does not cover: waiting out the 120 s timeout, and the bash lock's stale-lock breaking, which a `flock` released by the kernel when its process exits has no use for. No duration is asserted beyond the subprocess timeout that keeps a hang from stalling the suite.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_flow_walker_concurrency.py` passes, run as one foreground command from the repository root.
- Run twice in a row, the one-join case passes both times: which call prints the join may differ, the count of joins may not.
