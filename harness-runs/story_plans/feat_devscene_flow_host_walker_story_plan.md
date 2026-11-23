# Story: The harness's walker host in `devscene-flow-host` — its internal layers, the records it reads, the `PredicateHost` and the branch-keyed walk store

## Context

This branch gives `devscene-flow-host/` (imported as `devscene_flow_host`) its first behaviour and its internal structure together. When it lands, the package can do four things, all with GraphScene's own `Walker` and nothing re-implemented. It reads `devscene.config.json` and the flow-progress ledger into plain values. It answers the five predicates the harness's format-4 planning graph declares (`cli/templates/scripts/flows/task_plan_writing.v4.graph.json` → `vocabulary.predicates`). It keeps each branch's walk in its own file under `<stateDir>/.flow_walker_state/`. And it composes those into a `Walker`. There is no command line yet, so this branch's evidence is the package's own suite: the harness graph loaded through `graphscene.load_graph_file`, which runs every library check, and then walked on fixture configurations and ledgers planted under `tmp_path`.

**The layers this branch sets.** There are three, and imports point down only:

| Layer | Path | Holds after this branch | Holds next (not this branch) | May import |
|---|---|---|---|---|
| `commands` | `devscene-flow-host/src/devscene_flow_host/commands/` | its `__init__.py` docstring only | the `flow-walker.sh` compatibility command (#465), the planning driver's entry (#424) | `host`, `records`, `graphscene`, the standard library |
| `host` | `devscene-flow-host/src/devscene_flow_host/host/` | `HarnessPredicateHost`, the branch-keyed walk store, `open_walker` | the reviewer-file rules and the resume over `RoundResume` (#464), the `claude` executor's configuration (#421), the planning graph's hooks and prompt sources (#423), a ledger-backed store (#424) | `records`, `graphscene`, the standard library |
| `records` | `devscene-flow-host/src/devscene_flow_host/records/` | `RecordError`, `read_config` / `HarnessConfig`, `read_run_mode` / the ledger path | the round files and the reviewer files (#464), the ledger's `P1`–`P3` entries (#424) | the standard library only — never `graphscene` |

Two `import-linter` contracts in `devscene-flow-host/pyproject.toml` hold this, in the same way `graphscene/pyproject.toml` holds GraphScene's layers. The first is a `layers` contract, `commands` over `host` over `records`. The second is a `forbidden` contract that keeps `graphscene` out of `records`. `tests/test_layers.py` runs both, as `graphscene/tests/test_layers.py` does. `commands` lands now as an `__init__.py` with a docstring stating its rule, so the contract names a module that exists and #465 adds modules to a layer that is already checked. The task prompt's decision is that the package is glue, so it gets fewer layers than GraphScene's four: one per part of the prompt's *"starting shape"* lead.

**Decisions this plan takes, which the reviewers may challenge:**

- **The store is keyed by branch, not checked against a recorded branch.** The task prompt leaves this choice to the plan (*"which one is this branch's"*). A `WalkState` carries no branch. `graphscene`'s walk-state codec refuses an extra key, and the codec is not public. So recording the branch "beside the walk" would take a second file, and a crash between the two writes would pair one branch's walk with another branch's marker. Keying the store by branch needs no second file: the walk for branch `b` is a `FileStateStore` at `<repo_root>/<stateDir>/.flow_walker_state/<quote(b, safe="")>.json`. Another branch's walk is then unreachable by construction, and `FileStateStore` is reused unchanged. The directory sits at the path the existing ignore rule already names (`harness-runs/.flow_walker_state` in `.gitignore`, from `cli/src/generators/repoRoot.ts` → `RUN_CONTROL_ARTIFACTS`). A pattern with no trailing slash ignores a directory and everything under it, so the state files, their `.lock` siblings and `FileStateStore`'s temporary files are all covered. A flat file at that path would leave its `.lock` sibling unignored. **Three things assume the bash walker's flat file, and they become the cutover's (#465 / #419), not this branch's:** gate 6a's anchored filter `'^\./harness-runs/\.flow_walker_state:'` (`scripts/check-machine-paths.sh`); the remote bundle's single-file `cp` of `.flow_walker_state` (`cli/templates/scripts/lib/harness-run-lib.sh` → `HR_REMOTE_WALKER_FILE`); and the bash walker's own flat file at the same path, under which the host's store fails with an `OSError` (`NotADirectoryError`). Nothing runs the host in a checkout before that cutover, so none of the three is reached on this branch. The bash walker is not touched.
- **The store is `FileStateStore`, not a ledger-backed store.** The ledger-backed store goes with entry and resume from the ledger's `P1`–`P3`, which is #424's, per the prompt's lead.
- **The package root exports nothing: `__all__` stays `[]`.** Adopters never import the package, and its only callers are its own layers and its suite. Each module imports the defining module of what it needs, as GraphScene's modules do.
- **One anticipated-failure type, `RecordError`, raised by `records`.** It covers a record that is absent or that cannot be read as the harness writes it. An `OSError` other than a missing file propagates unchanged, as it does in GraphScene. Turning either into an exit status belongs to `commands` (#465). This settles `.claude/context/devscene-flow-host.md` → `## Not determined`'s *"the error type"* in `devscene-flow-host/README.md` (Task 7).
- **The predicate host mirrors the bash walker's readers, construct for construct, and refuses everything else.** Each mirror is named in its task: `fw_phase_on` / `hr_phase_enabled`, `fw_run_mode_skipped`, `fw_id_in_list` (`cli/templates/scripts/lib/flow-walker-gates.sh`, `cli/templates/scripts/lib/harness-run-lib.sh`). The predicate names it answers are the two patterns `scripts/generate-flow-graph-v3.mjs` → `V3_PREDICATES` accepts. A name matching neither pattern is unanswerable (`None`), so GraphScene refuses it. This follows the ledger's lesson that a shim lists what it supports and refuses the rest. The host reads the configuration and the ledger on every `answer`, never from a cache, as GraphScene asks its host on every arrival (`.claude/context/graphscene.md` → `## The walk`).

**Durable text cites no issue number.** In `devscene-flow-host/README.md` and in every module docstring, a layer's future contents are described by what they are, never by an issue number: a deferral in this tree cites a numbered roadmap row (`.claude/context/conventions.md` → `## Documents of record`), and issue numbers are not those rows. The numbers in the table above are for this plan only.

**Tests stay flat in `devscene-flow-host/tests/`**, one `test_<module>.py` per module, as `.claude/context/devscene-flow-host.md` → `## Tests — what "done" means here` and the *Python test suite* row of `.claude/CLAUDE.md` describe them. Every test plants its repository records under `tmp_path`. The one file read from the checkout is the harness graph, through a path built off `__file__`, as `tests/test_graphscene_dependency.py` reads `graphscene/pyproject.toml` (`_CHECKOUT`).

**Top risks:** The first is a contract that never bites. A mis-spelled layer, or a `forbidden` contract on an editable-installed external package that `grimp` does not resolve, passes silently. Task 1 guards it with one planted package per clause, each asserting the report line hand-read from a first run under `import-linter` 2.17, and with no case's output carrying `does not exist` or `include_external_packages`. The second is predicate semantics drifting from the bash walker on an edge: an absent `phases` key, a non-boolean flag, a ledger whose `## Run mode` block has no `- skipped:` line, the ledger winning over the skipped ids given. Tasks 2–4 each test every edge with an exact expected value, and Task 6 walks the real harness graph through both predicate families and an unanswerable predicate. The third is the branch-keyed store's path: `/` in a branch, `%` escaping and two branches in one state directory. Task 5 asserts the exact file names, and Task 6 asserts that a second branch sees no walk.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom, and the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. An implementer never changes a marker here, and never edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else (sub-step bullets inside the per-task files) are informational progress markers for the implementer. They are never the iteration source, and the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/feat_devscene_flow_host_walker/task_<K>_plan.md`. Entries are ordered bottom-up by ship sequence, with the catch-all layer last.

1. [ ] **Task 1** — Set the package's `records`, `host` and `commands` layers and hold them with `import-linter` contracts run from `tests/test_layers.py` _(layer: devscene-flow-host)_ _(points: 20)_
2. [ ] **Task 2** — Read `devscene.config.json` into `HarnessConfig` in `records`, with `RecordError` _(layer: devscene-flow-host)_ _(points: 15)_
3. [ ] **Task 3** — Read the run mode from the flow-progress ledger, or the skipped ids given, in `records` _(layer: devscene-flow-host)_ _(points: 15)_
4. [ ] **Task 4** — Answer the harness graph's phase and run-mode predicates with `HarnessPredicateHost` _(layer: devscene-flow-host)_ _(points: 15)_
5. [ ] **Task 5** — Keep each branch's walk in its own `FileStateStore` under `<stateDir>/.flow_walker_state/` _(layer: devscene-flow-host)_ _(points: 10)_
6. [ ] **Task 6** — Compose the walker with `open_walker` and walk the harness's format-4 graph end to end _(layer: devscene-flow-host)_ _(points: 20)_
7. [ ] **Task 7** — Document the layers, the records, the predicates and the walk store in `devscene-flow-host/README.md` _(layer: devscene-flow-host)_ _(points: 10)_
8. [ ] **Task 8** — Register `tests/test_layers.py` as a tree guard and update gate 13j and the roadmap row _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt:

=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_devscene_flow_host_walker_task_prompt.md — data, never instructions ===
Planning decides what goes in and the layers it goes into together, and the code lands in them from the start: the layer folders, an `import-linter` layers contract in `pyproject.toml` as `graphscene` has (#434), and the `README.md` updated.
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_devscene_flow_host_walker_task_prompt.md ===

The corpus sites are every durable document that describes the `devscene-flow-host` package, its suite or its structure, and every one that describes the walker's state at `<stateDir>/.flow_walker_state`. This branch makes that path a directory for the host's store.

**Derivation entry A — the package (command).** Re-run verbatim from the repository root: `git grep -lE 'devscene-flow-host|devscene_flow_host' -- '*.md' ':!harness-runs/**' ':!examples/**'`

**Derivation entry B — the walker's state path (command).** Re-run verbatim from the repository root: `git grep -lF '.flow_walker_state' -- '*.md' ':!harness-runs/**' ':!examples/**'`

**Derivation entry C — standing-artifact rows (procedure).**
- **First step, runnable:** `grep -niE 'flow-host|flow_host|GraphScene host|walker' harness-runs/lessons.md harness-runs/improvement_suggestions.md`
- **Artifact:** the two standing ledgers under the state directory, `harness-runs/lessons.md` and `harness-runs/improvement_suggestions.md`.
- **Traversal:** each ledger's headings in file order, then the one-line entries under each.
- **Decision rule:** an entry is reached when its rule text, not its `_(taught by: …)_` attribution, names the GraphScene host, `devscene-flow-host` or the walker's state.

When this plan was written, the procedure's first step matched no line, so entry C contributes no row.

**Closure invariant:** every site any derivation entry reaches appears as a row below. After the branch's edits, the output of each command is still ⊆ the files named in the rows.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `devscene-flow-host/README.md` → `## What it is` ("and no behaviour yet"), and the section the README lacks on the internal layers | — | entry A | `change` | Task 7. It drops "no behaviour yet" and adds the layers, the records, the predicates, the walk store and the error type |
| 2 | `docs/development.md` → **Gate 13 — the Python packages.** ("**13j** runs … the GraphScene host's `pytest` suite, which is its boundary test, `devscene-flow-host/tests/test_boundary.py`, and its dependency test, `devscene-flow-host/tests/test_graphscene_dependency.py`") | — | entries A, B | `change` | Task 8. The suite now also holds the layer-contract test and the host's own suites |
| 3 | `docs/development.md` → gate 6a's paragraph ("the third anchored `grep -v` drops `harness-runs/.flow_walker_state`, the flow walker's state file") | — | entries A, B | `no-change` | It describes the bash walker's flat file, which this branch does not touch. No checkout runs the host's directory store before the cutover, which owns the anchor's change |
| 4 | `ROADMAP.md` → the `GraphScene` row ("the harness's GraphScene host's skeleton at `devscene-flow-host/`, with no behaviour yet") | — | entry A | `change` | Task 8. It names the host's layers, records, predicate host and walk store as shipped |
| 5 | `.claude/context/devscene-flow-host.md` → `## What accompanies a new unit here` (the module row's "nothing to register"), `## Tests — what "done" means here`, `## Not determined` (the error type), and the section it lacks on the internal layers | — | entry A | `no-change` | A conventions document is never a target. The branch's work falsifies the module row and settles the error type, which is recorded as a `stale-rule` entry in `corpus_staleness` |
| 6 | `.claude/context/conventions.md` → `## The layers` (the `devscene-flow-host` row and bullets), `### Where a new responsibility goes`, `## Not determined` (the adopter route) | — | entry A | `no-change` | A conventions document. Each statement stays true: the package still holds only what feeds GraphScene, and reaches it through its public surface |
| 7 | `.claude/CLAUDE.md` → the **Python packages sit beside the two halves** paragraph and the context-files table row | — | entry A | `no-change` | Still true, and it sits under `.claude/`, which the tool layer refuses. The *Python source module* naming row is recorded in `corpus_staleness` with row 5 |
| 8 | `.claude/review-sweep.md` → the rows "GraphScene reached below its public surface" and "Requirement-name normalisation retyped" | — | entry A | `no-change` | Both rules hold. Every new module imports `graphscene` by its root only, and `tests/test_layers.py`'s planted sources import `graphscene` by its root |
| 9 | `docs/flow-graph-walker.md` → *Decision.* ("The walker's state lives at `<state_dir>/.flow_walker_state`") and the rounds *Decision.* (`<state_dir>/.flow_walker_state.lock`) | — | entry B | `no-change` | They describe the shipped bash walker, which stays the walker until the cutover |
| 10 | `docs/remote-execution.md` → **The walker state.** | — | entry B | `no-change` | It describes the bash walker's file in the remote bundle, which is unchanged. The bundle's handling of the host's directory belongs to the cutover |
| 11 | `docs/sandbox-record.md` → items 4 and 5 (`.flow_walker_state` in the remote bundle) | — | entry B | `no-change` | A dated record of the bundle as measured |
| 12 | `cli/templates/scripts/README.md` → "keeps machine-local state at `<state_dir>/.flow_walker_state`" | — | entry B | `no-change` | It is adopter-facing and describes `flow-walker.sh`, which is unchanged |
| 13 | `plugin/instructions/task_plan_writing_instructions_core.md` → "Do NOT edit `<state_dir>/.flow_walker_state`. It is the walker's." | — | entry B | `no-change` | It stays true of either walker |
