### Task 4 — Answer the harness graph's phase and run-mode predicates with `HarnessPredicateHost`

**Goal:** Give the harness its `PredicateHost`, which answers the five predicates the format-4 planning graph declares (`cli/templates/scripts/flows/task_plan_writing.v4.graph.json` → `vocabulary.predicates`). It answers `phase_parity_off` and `phase_qa_off` from `phases.*`, and `run_mode_skips_parity`, `run_mode_skips_architecture` and `run_mode_skips_qa` from the run mode. It answers by the two name patterns `scripts/generate-flow-graph-v3.mjs` → `V3_PREDICATES` accepts, so `phase_docs_off` and any `run_mode_skips_<id>` are answered too. Whatever it cannot answer is `None`, which GraphScene refuses rather than guesses (`graphscene/src/graphscene/model/walk_state.py` → `PredicateHost`). This matches the bash walker's refusal in `flow-walker.sh` → `eval_skip`.

**Depends on:** Task 2 and Task 3. It calls exactly these contracts, all in `devscene_flow_host.records`:

- `records.config.read_config(repo_root: Path) -> HarnessConfig`, raising `RecordError`. `HarnessConfig.state_dir: str` is repo-relative. `HarnessConfig.phases: Mapping[str, bool | None]` holds exactly the keys of `records.config.PHASES = ("parity", "qa", "docs")`: `True` on, `False` off, `None` unresolvable.
- `records.ledger.read_run_mode(repo_root: Path, state_dir: str, branch: str, skipped: str | None) -> RunMode | RunModeUnresolved`. `RunMode.skipped` is a `frozenset[str]`, and `RunModeUnresolved.reason` is the exact reason string.

**Where this layer stops.** This task answers predicates and stores nothing. The walk's store is **Task 5's**, and composing host, store and graph into a `Walker` is **Task 6's** (`open_walker`). Rendering a refusal for `flow-walker.sh`'s output belongs to the `commands` layer, which has no module on this branch. `refusal_reason` below is what such a renderer will read.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/predicates.py` (new)
- `devscene-flow-host/tests/test_predicates.py` (new)

**Work:**

- [ ] **The name patterns.** Build `PHASE_PREDICATE` from `PHASES`, imported from `records.config` rather than retyped: `^phase_(parity|qa|docs)_off$`. `RUN_MODE_PREDICATE` is `^run_mode_skips_([a-z][a-z0-9_-]*)$`. The module docstring names `scripts/generate-flow-graph-v3.mjs` → `V3_PREDICATES` as the source of both patterns. It names `hr_phase_enabled` / `fw_phase_on`, `fw_run_mode_skipped` and `fw_id_in_list` as the readers this mirrors, and opens its rule with *"The rule:"*.
- [ ] **`class HarnessPredicateHost`**, with `__init__(self, repo_root: Path, branch: str, *, skipped: str | None = None)`. It satisfies `graphscene.PredicateHost` structurally, with no subclassing. Its `answer(self, predicate: str, node: str) -> bool | None` reads the records again on **every** call and caches nothing, so a ledger written mid-walk is seen at the next arrival. `node` does not change any answer.
  - `phase_<p>_off` → `read_config(repo_root).phases[p]`: `False` (phase off) → `True`; `True` → `False`; `None` → `None`.
  - `run_mode_skips_<id>` → `read_run_mode(repo_root, config.state_dir, branch, skipped)`: a `RunMode` → `id in run_mode.skipped`; a `RunModeUnresolved` → `None`.
  - any other name → `None`.
  - A `RecordError` from either reader propagates. `Walker` lets it through, and the store is left unwritten.
- [ ] **`refusal_reason(self, predicate: str) -> str | None`**: `None` when `answer` would return a boolean, otherwise the reason, re-read the same way:
  - an unresolvable phase: `cannot resolve phases.<p> in <repo_root>/devscene.config.json` (`flow-walker.sh` → `eval_skip`'s text, with `<repo_root>` as `str(repo_root)`)
  - an unresolved run mode: `RunModeUnresolved.reason`, unchanged
  - an unknown name: `'<predicate>' is not a predicate the harness answers`

  Share one private resolution between `answer` and `refusal_reason`, so the two cannot disagree.
- [ ] **`tests/test_predicates.py`.** Its docstring opens *"The rule this file exists to enforce"*. Each case plants `devscene.config.json`, and where needed the ledger at `<tmp_path>/<stateDir>/flow_progress/<branch>_progress.md`, under `tmp_path`. Expected values are literals. One case per rule:
  - `phases` `{"parity": false, "qa": true}` → `phase_parity_off` `True`, `phase_qa_off` `False`, and `phase_docs_off` `True` (absent is off)
  - `phases` `{"parity": "on"}` → `phase_parity_off` `None`, with `refusal_reason` the exact `cannot resolve phases.parity in …` text
  - a ledger with `- skipped: parity` and `skipped="qa"` → `run_mode_skips_parity` `True`, `run_mode_skips_qa` `False` (the ledger wins), `run_mode_skips_architecture` `False`
  - no ledger, `skipped="none"` → all three `run_mode_skips_*` `False`; no ledger, no `skipped` → `None`, with `refusal_reason` the exact "no run-mode record" text
  - `stage_disabled` and `phase_lint_off` → `None`, with the "is not a predicate the harness answers" text
  - re-read, not cached: answer `run_mode_skips_qa` (`False`), write a ledger with `- skipped: qa`, and ask the same host again → `True`
  - no `devscene.config.json` → `pytest.raises(RecordError)` from `answer("phase_qa_off", "ui_writer")`
  - `refusal_reason` is `None` for every predicate the host answered with a boolean in the cases above

**Verification:**

- Run this task's own test file from the repository root, as one foreground command: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_predicates.py`. Every case passes.
- `commands.typecheck` exits zero. In particular `mypy` accepts a `HarnessPredicateHost` where a `graphscene.PredicateHost` is expected: add one annotated assignment in the test file, `host: PredicateHost = HarnessPredicateHost(...)`, importing `PredicateHost` from `graphscene`.
- `host/predicates.py` imports `graphscene` names, if any, only as `from graphscene import <name>` with the name in `graphscene.__all__`, and never names a `graphscene` submodule.
