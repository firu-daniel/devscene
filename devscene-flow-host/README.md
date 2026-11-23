# devscene-flow-host

**Who reads this:** a contributor changing this package. It owns what the package is, what it may depend on, how its lock follows GraphScene's, and how its toolchain is run here.

## What it is

`devscene-flow-host` is the harness's GraphScene host, imported as `devscene_flow_host`. It holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it. It reads the harness's configuration, flow-progress ledger and round and reviewer files, answers the planning graph's phase and run-mode predicates, applies the reviewer-file rules when a gate's outcome is recorded, resumes a round from the files on disk, and keeps each branch's walk, for GraphScene's `Walker`; it has no command line yet. Any other DevScene Python integration gets its own `devscene`-prefixed package rather than a place here. Anything useful without DevScene goes in GraphScene (`graphscene/`), not here.

It stays in this repository: it is not part of the npm package (`cli/package.json` → `files`), and adopters never import it.

## What it may depend on

- **The package imports only the standard library, itself and its declared runtime dependencies.** It reaches `graphscene` through its public surface only — `import graphscene` or `from graphscene import <name in graphscene.__all__>`, never a submodule such as `graphscene.engine` — and GraphScene never imports it.
- **`graphscene` is an editable path dependency on `../graphscene`** (`pyproject.toml` → `[tool.uv.sources]`), so one sync provisions both packages, this package's environment imports the checkout's current `graphscene/src/graphscene/`, and no release is needed.
- **The tests stay inside the same boundary, widened only by the `dev` dependency group.** A module under `tests/` imports the standard library, `devscene_flow_host`, the declared runtime dependencies through the same public surface, the `dev` group's tools, and the suite's own support modules — never another package's tests or another layer's source. Reading a tracked file of another layer as test input (the walker's graph file, GraphScene's manifest) is not an import and stays allowed.

`tests/test_boundary.py` and `tests/test_layers.py` enforce these rules for the package; `tests/` itself is not scanned, so the tests' rule is held by review.

## The layers

| Layer | Path | Holds | May import |
|---|---|---|---|
| `commands` | `src/devscene_flow_host/commands/` | The command lines over the host | `host`, `records`, `graphscene`'s public surface, the standard library |
| `host` | `src/devscene_flow_host/host/` | GraphScene's protocols over the records, and the harness's rules over them: `HarnessPredicateHost` (`host/predicates.py`), `walk_store` (`host/store.py`), `open_walker` (`host/walking.py`), `render_path` (`host/paths.py`), `round_of_gate`, `round_of_writer` and `review_iteration` (`host/reviewers.py`), `RefusalStore` (`host/refusals.py`), `round_resume` (`host/resume.py`), `record_outcome` and `HostStep` (`host/round_gates.py`), `start_walk` and `current_step` (`host/re_entry.py`) | `records`, `graphscene`'s public surface, the standard library |
| `records` | `src/devscene_flow_host/records/` | The repository's records read into plain values: `read_config` (`records/config.py`), `read_run_mode` (`records/ledger.py`), `review_verdict`, `round_file_problem`, `next_review_index`, `fail_count` and `round_file_path` (`records/round_files.py`), `read_round_evidence` (`records/round_evidence.py`), `read_index_evidence` (`records/index_evidence.py`), `RecordError` (`records/errors.py`) | `records`, the standard library |

Imports point down only, and `records` never imports `graphscene`. The contracts `devscene-flow-host-layers` and `devscene-flow-host-graphscene-outside-records` in `pyproject.toml` hold this, and `tests/test_layers.py` runs them with no cache. A new module lands in the layer its work belongs to. A new layer or a changed import rule lands with its contract change, its planted cases in `tests/test_layers.py` and its row here. The package root exports nothing (`__all__ = []`), because adopters never import it.

## What it reads, answers and keeps

**Records.** `read_config` reads `devscene.config.json` for `stateDir` and `phases` only, and refuses one with no `defaultBranch` as `hr_config_load` does, into a `HarnessConfig`, as `hr_state_dir` and `hr_phase_enabled` read them (`cli/templates/scripts/lib/harness-run-lib.sh`). `read_run_mode` reads the flow-progress ledger's `## Run mode` → `- skipped:` line, as `fw_run_mode_skipped` reads it (`cli/templates/scripts/lib/flow-walker-gates.sh`). Whenever the ledger exists it wins over the skipped ids the caller gives; those are used only when there is no ledger, and with neither the result is a `RunModeUnresolved` carrying the reason.

**Predicates.** `HarnessPredicateHost` answers `phase_<parity|qa|docs>_off`, true when that phase is off in `phases`, and `run_mode_skips_<id>`, true when the run mode skips `<id>`. Any other name, an unresolvable phase or an unresolved run mode is `None`, which the walk refuses rather than guesses; `refusal_reason` gives the reason. The records are re-read on every arrival, so a ledger written mid-walk is seen at the next one.

**The walk.** `walk_store` keeps one GraphScene `FileStateStore` per branch at `<stateDir>/.flow_walker_state/<percent-encoded branch>.json`, which this repository's ignore rule for that path covers. Another branch's walk is never read. The bash walker's own state, a flat file at that same path, is not this package's.

**Round and reviewer files.** Each reader reads as the bash function it names (`cli/templates/scripts/lib/flow-walker-gates.sh`). `review_verdict` reads a reviewer file's one `verdict: PASS` or `verdict: FAIL` line, as `fw_review_verdict` does. `round_file_problem` gives the reason a round gate may not use a file — no single verdict line, a `FAIL` with no numbered entry under `## Must Fix`, a `PASS` with one, or an entry lacking `**Class:**` or `**Failure:**` — as `fw_round_file_check` does. `next_review_index` and `fail_count` read a findings folder's next free `review_<n>.md` index and its `FAIL` count, as `fw_next_review_index` and `fw_fail_count` do. `read_round_evidence` reads a round's highest round number, each gate's status at it, whether the next revision note exists and whether the plan changed after the round's files were committed, asking `git` as `fw_round_evidence` does. `read_index_evidence` reads whether a story index has a `## Rejected findings` section, the entries there still open, and whether it has a `## Scope register` section, as `fw_index_evidence` does. A missing round file or findings folder is a value (`None`, `0`), never a `RecordError`, because the walk routes on it. `render_path` renders a graph path template's `{state_dir}`, `{branch}` and `{round}`, and `review_iteration` gives a reviewer outside a round the next free index in its `findingsFolder`.

**Recording a gate.** `record_outcome` records a gate's outcome under the four reviewer-file rules, as `flow-walker.sh`'s `next` does: an outcome whose verdict is `fail` requires a findings file, and so does any verdict outcome at a gate of the open round; a round gate's file must pass `round_file_problem` before its verdict is recorded; a refused file records nothing in the walk — its gate is left out of a `wait`'s pending list, and once no other gate is out every refused gate is re-dispatched as one set in the same round; and the third refusal of one gate in a round records the held outcome `error`. The refusals are the host's own record, `RefusalStore`, at `<stateDir>/.flow_walker_state/round_refusals/<percent-encoded branch>.json` behind the lock `<file>.lock`; every call that records takes that lock before the walk's own and releases it after. The `HostStep` returned carries the step and the `refused:` lines it brings. Two departures from the bash walker are each marked by a `TODO: @claude` in `host/round_gates.py`:

- **The held-gate escalation.** The host does not yet escalate a held gate at a join whose only gates out are refused ones, as `flow-walker.sh` → `record_in_set` does ("With none out: a held gate escalates"); that needs a GraphScene way for a host to set a due gate aside in an open round. It re-dispatches the refused gates first instead, and escalates at the join that follows.
- **The non-round findings file.** The host does not yet keep a findings file given outside a round gate (a non-round reviewer's `FAIL`, or `answered`) as `flow-walker.sh` → `next` keeps `revision_findings`, so the writer's revision dispatch carries it as `arg.findings_file`; that needs a host-side record of `revision_findings` for a non-round reviewer and for `answered`, cleared as bash clears it on `start`. Instead, a findings file given at a non-gate call is required on `FAIL` but not kept, and neither is one given with `answered`, so `ui_review`'s `FAIL` reaches `ui_writer`'s revision with no findings file on it.

**Resuming a round.** `round_resume` builds a round's `RoundResume` for GraphScene's `Walker.start` from the files on disk, as `flow-walker.sh`'s `start_round` and `start_record` do. The entry is a round's writer or a round node; any other entry has no resume, and a round with no file has none either. Entered at the writer, the round resumes at the number after its highest. Entered at the round node: a round with files missing whose evidence is consistent records the present gates and opens only the missing ones; any other incomplete round opens the whole set at that round; a complete round that is unreadable or has no `FAIL` is reviewed again; a `FAIL` with the next revision note on disk opens the next round; and a `FAIL` without the note records every verdict, so the round closes at once. Convergence is never inferred from files. `start_walk` reads as `flow-walker.sh`'s `start`: it rebuilds the round position through `round_resume` and `Walker.start`, under the same lock order as `record_outcome`, and clears the refusal record only when the walk started. `current_step` reads as its `current`: it re-reads the saved step with every gate awaiting re-dispatch left out, takes no lock and changes nothing, so a refused gate is never dispatched twice. The counter and the prompt variants a lost walk loses are lost here too, as in bash.

## Errors

`RecordError` is the one anticipated failure: a record absent, or not readable as the harness writes it, with a one-line message naming the file. Any other `OSError` propagates. A malformed refusal record raises `ValueError` naming the file, and its lock `TimeoutError`, as the walk's store does; a round gate with no `findingsFolder` raises `ValueError`. Which exit status either becomes is the caller's; the package has no command line yet.

## The lock follows GraphScene

This package's `uv.lock` pins GraphScene's own runtime dependencies as resolved through the path source. A change to `graphscene/pyproject.toml` → `[project] dependencies` re-locks this package too:

```
bash scripts/python-service.sh --package devscene-flow-host lock
```

`tests/test_graphscene_dependency.py` fails until it is done.

## Running the toolchain

Every command goes through `scripts/python-service.sh`, run from the repository root.

Lint:

```
bash scripts/python-service.sh --package devscene-flow-host lint
```

Typecheck:

```
bash scripts/python-service.sh --package devscene-flow-host typecheck
```

Test:

```
bash scripts/python-service.sh --package devscene-flow-host test
```

`test` forwards paths to `pytest`, relative to `devscene-flow-host/`:

```
bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py
```

Provision every package's environment, outside any sandbox:

```
bash scripts/python-service.sh provision
```

## Gating

The package is gated by gate 13's legs 13h–13j ([`docs/development.md`](../docs/development.md) → `## 5. Verifying a change`).
