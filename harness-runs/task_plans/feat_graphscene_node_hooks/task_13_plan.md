### Task 13 — Implement the planning graph's hooks as `PlanningHooks` and walk the planning graph in run mode with them

**Goal:** Implement the three hooks the planning graph declares as one `graphscene.HookHost`, `PlanningHooks`. Prove them by walking the real planning graph in GraphScene's run mode with these hooks over a planted repository. The hooks carry Overrides 3–6 of `plugin/instructions/task_plan_writing_instructions_autonomous.md`. The bash driver makes these commits and flips today in `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_act` and `pd_handoff`.

**Depends on:**

- **Task 1:** the planning graph declares `vocabulary.hooks` `commit_plan_round`, `flip_ledger` and `commit_convergence`; `plan_round` has `"after": ["commit_plan_round", "flip_ledger"]`; `convergence` has `"before": ["flip_ledger", "commit_convergence"]`.
- **Task 7:** `graphscene` exports `HookHost` (`provides(hook) -> bool`, `async run(hook, call) -> None`) and the calls `AfterRound(passage, step)`, `BeforeEnd(end)`, `AfterDispatch(record, step)`, `BeforeRound(dispatch_set)` and `BeforeDispatch(dispatch, seq, attempt)`. It also exports `start_run(…, hooks=…)`. Per Task 6, run mode runs a round's after-hooks for every `RoundPassage` in a step it takes, a `current` included, and a terminal's before-hooks before returning its `End`.
- **Task 10:** `records/ledger.py` → `read_planning_marks(repo_root, state_dir, branch) -> PlanningMarks(p1, p2, p3)`, each `"x" | "-" | " " | None`, and `PLANNING_ENTRIES: Final = ("P1", "P2", "P3")`, the ledger's planning entry ids, which this module imports from `records/ledger.py` and does not redeclare.
- **Task 12:** `commit_artifact(wrapper, worktree, kind, *, round_number=None, entry=None) -> bool`. It raises `CommitPointError` on a refusal. Also `flip_ledger_entry(repo_root, state_dir, branch, entry) -> bool`.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/planning_hooks.py` (new)
- `devscene-flow-host/tests/test_planning_hooks.py` (new)

**The contract this task produces.** The README (Task 16) describes it, and the run driver (#424) constructs it.

```python
HOOKS: Final = ("commit_plan_round", "flip_ledger", "commit_convergence")

class PlanningHooks:
    def __init__(self, graph: FlowGraph, *, repo_root: Path, state_dir: str, branch: str,
                 commit_wrapper: Path) -> None: ...
    def provides(self, hook: str) -> bool: ...          # hook in HOOKS
    async def run(self, hook: str, call: HookCall) -> None: ...
```

- **`commit_plan_round`** is Override 6. It takes an `AfterRound` and calls `commit_artifact(..., "plan-round", round_number=call.passage.number)`.
- **`flip_ledger`** is Override 5's flips, as `pd_act` makes them. Every call kind carries a step whose `passed` it reads: `AfterRound.step`, `AfterDispatch.step`, `BeforeEnd.end` and `BeforeRound.dispatch_set`. A `BeforeDispatch` carries none and is refused, as below. For each `LedgerPassage` in that `passed`, in order:
  - an entry in `PLANNING_ENTRIES` (imported from `records/ledger.py`) is flipped with `flip_ledger_entry`, then committed with `commit_artifact(..., "ledger-flip", entry=<id>)`. The commit is made even when the flip returned `False`. A flip whose earlier commit was lost lands now, and an already-landed one costs the wrapper's exit 3;
  - any other entry is skipped.
- **`commit_convergence`** is Overrides 3 and 4, then the `P3` flip, as `pd_handoff` → `prl_convergence_commits` then `prl_ledger_flip P3`. It takes a `BeforeEnd`.
  - **Whether a UI-test plan was written.** The `End.reports` slot `ui_test` decides when present: the plan was written exactly when its status is `passed`. With no such slot (a walk that entered at `convergence`), the ledger decides: the plan was written exactly when `P2` is `"x"` and the graph's `paths["ui_test_index"]`, rendered with `host/paths.py` → `render_path`, exists under `repo_root`.
  - **Then the commits.** If a UI-test plan was written, `commit_artifact(..., "ui-test-plan")`. Then `commit_artifact(..., "task-plan")`. Then `flip_ledger_entry(..., "P3")` and `commit_artifact(..., "ledger-flip", entry="P3")`.
- **A misused hook.** A hook given a call kind it does not take raises `ValueError(f"hook '{hook}' does not run on {call.kind}")`. An unknown hook raises `LookupError(f"PlanningHooks provides no hook '{hook}'")`. `CommitPointError` and `RecordError` propagate. GraphScene propagates them out of `start_run`, and the run driver parks on them.

**Work:**

- [ ] **`host/planning_hooks.py` — the module.** Implement `PlanningHooks` exactly as the contract spells it, with `HOOKS`, the `ui_test` slot and the `ui_test_index` path key as `Final` constants. Import `PLANNING_ENTRIES` from `records/ledger.py` and declare no entry id of its own.
  - **The docstring's *"The rule:"*** names the overrides each hook carries and the bash functions it reads as (`pd_act`, `pd_handoff`, `prl_round_commit`, `prl_convergence_commits`, `prl_ledger_flip`), and states that every hook is repeatable through the wrapper's exit 3.
  - **Its *"Deliberately not covered"*** names three things: a pause's `plan-round-partial` commit and the `<ask>` / `<escalate>` parks (the run driver's, #424, because each is a `RunExit` and not a node or round event); `P0` and the ledger's creation (the fork's Setup acts); and resolving `commit_wrapper` (the caller's).
- [ ] **`tests/test_planning_hooks.py` — each hook.** Open with the header *"The rule this file exists to enforce"*. Use a fake wrapper planted under `tmp_path`, which logs each call's arguments and exits by a scripted status, as `tests/test_commit_points.py` (Task 12) plants one, plus planted ledgers. Cover:
  - `commit_plan_round` with round 3;
  - `flip_ledger` over a step whose `passed` carries `RoundPassage`, `LedgerPassage("P1")` and `LedgerPassage("A")`: it flips and commits `P1` only;
  - `commit_convergence` for each `ui_test` status (`passed`, `no_ui`, `qa-phase-off`, `run-mode-skipped`);
  - the ledger-decided case, with and without the UI-test index on disk;
  - a misused call kind and an unknown hook, each with its exact message;
  - a refused wrapper call propagating `CommitPointError`.
- [ ] **`tests/test_planning_hooks.py` — the end-to-end walk.** Walk the real planning graph in run mode, so this case exercises the wiring end to end:
  - **The planning graph.** Load `cli/templates/scripts/flows/task_plan_writing.graph.json` read-only with `graphscene.load_graph_file`. This also loads the graph under the format-5 schema, the vocabulary check and the static checks.
  - **The walker.** Compose it over a planted repository with `host/walking.py` → `open_walker`. Plant a `devscene.config.json` with `phases` `parity` and `qa` off and a ledger whose `P1`–`P3` are `[ ]`.
  - **The run.** Drive `graphscene.start_run` with `graphscene.StubExecutor`. Its script: `plan_writer` `returned`, both unskipped gates `FAIL` with a findings detail, `plan_writer` `returned`, then both gates `PASS`. Pass `hooks=PlanningHooks(...)`, with `RunSignals`, `DispatchCounter` and `LaunchSink` doubles defined in the test and `ExecutionLimits(backoff_seconds=0)`.
  - **What to assert.** The run returns an `End` at `convergence`. The fake wrapper's log is exactly, in order:
    1. `plan-round --round 0`
    2. `plan-round --round 1`
    3. `ledger-flip --entry P1`
    4. `ledger-flip --entry P1`, the convergence step's own `LedgerPassage`, since the UI-test loop is skipped
    5. `task-plan`
    6. `ledger-flip --entry P3`

    The ledger ends with `P1` and `P3` `[x]` and `P2` untouched. Hand-write the expected sequence from the graph and the contract.
- [ ] **`tests/test_planning_hooks.py` — the refusal and the resume.** Add these cases:
  - `start_run` with `hooks=None` over the planning graph raises *"the graph names hook 'commit_plan_round' and no hook host was given"*. The first hook in node key order is `plan_round`'s, and `plan_round` sorts before `convergence` in the graph's key order. Confirm that order when writing the literal.
  - **A resume after a refused commit.** A wrapper scripted to refuse the second `plan-round` call makes `start_run` raise `CommitPointError`. A following `continue_run` over the same store, with the wrapper now accepting, re-issues `plan-round --round 1` before any later call.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_hooks.py` passes.
- The end-to-end case's wrapper log is the evidence that Overrides 3–6's commits and flips fire from the graph's declarations, in Override 6's order: the round commit before the `P1` flip.
