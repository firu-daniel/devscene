# devscene-flow-host

**Who reads this:** a contributor changing this package. It owns what the package is, what it may depend on, how its lock follows GraphScene's, and how its toolchain is run here.

## What it is

`devscene-flow-host` is the harness's GraphScene host, imported as `devscene_flow_host`. It holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it. It reads the harness's configuration and flow-progress ledger, answers the planning graph's phase and run-mode predicates, and keeps each branch's walk, for GraphScene's `Walker`; it has no command line yet. Any other DevScene Python integration gets its own `devscene`-prefixed package rather than a place here. Anything useful without DevScene goes in GraphScene (`graphscene/`), not here.

It stays in this repository: it is not part of the npm package (`cli/package.json` → `files`), and adopters never import it.

## What it may depend on

- **The package imports only the standard library, itself and its declared runtime dependencies.** It reaches `graphscene` through its public surface only — `import graphscene` or `from graphscene import <name in graphscene.__all__>`, never a submodule such as `graphscene.engine` — and GraphScene never imports it.
- **`graphscene` is an editable path dependency on `../graphscene`** (`pyproject.toml` → `[tool.uv.sources]`), so one sync provisions both packages, this package's environment imports the checkout's current `graphscene/src/graphscene/`, and no release is needed.

`tests/test_boundary.py` and `tests/test_layers.py` enforce these rules.

## The layers

| Layer | Path | Holds | May import |
|---|---|---|---|
| `commands` | `src/devscene_flow_host/commands/` | The command lines over the host | `host`, `records`, `graphscene`'s public surface, the standard library |
| `host` | `src/devscene_flow_host/host/` | GraphScene's protocols over the records: `HarnessPredicateHost` (`host/predicates.py`), `walk_store` (`host/store.py`), `open_walker` (`host/walking.py`) | `records`, `graphscene`'s public surface, the standard library |
| `records` | `src/devscene_flow_host/records/` | The repository's records read into plain values: `read_config` (`records/config.py`), `read_run_mode` (`records/ledger.py`), `RecordError` (`records/errors.py`) | `records`, the standard library |

Imports point down only, and `records` never imports `graphscene`. The contracts `devscene-flow-host-layers` and `devscene-flow-host-graphscene-outside-records` in `pyproject.toml` hold this, and `tests/test_layers.py` runs them with no cache. A new module lands in the layer its work belongs to. A new layer or a changed import rule lands with its contract change, its planted cases in `tests/test_layers.py` and its row here. The package root exports nothing (`__all__ = []`), because adopters never import it.

## What it reads, answers and keeps

**Records.** `read_config` reads `devscene.config.json` for `stateDir` and `phases` only, and refuses one with no `defaultBranch` as `hr_config_load` does, into a `HarnessConfig`, as `hr_state_dir` and `hr_phase_enabled` read them (`cli/templates/scripts/lib/harness-run-lib.sh`). `read_run_mode` reads the flow-progress ledger's `## Run mode` → `- skipped:` line, as `fw_run_mode_skipped` reads it (`cli/templates/scripts/lib/flow-walker-gates.sh`). Whenever the ledger exists it wins over the skipped ids the caller gives; those are used only when there is no ledger, and with neither the result is a `RunModeUnresolved` carrying the reason.

**Predicates.** `HarnessPredicateHost` answers `phase_<parity|qa|docs>_off`, true when that phase is off in `phases`, and `run_mode_skips_<id>`, true when the run mode skips `<id>`. Any other name, an unresolvable phase or an unresolved run mode is `None`, which the walk refuses rather than guesses; `refusal_reason` gives the reason. The records are re-read on every arrival, so a ledger written mid-walk is seen at the next one.

**The walk.** `walk_store` keeps one GraphScene `FileStateStore` per branch at `<stateDir>/.flow_walker_state/<percent-encoded branch>.json`, which this repository's ignore rule for that path covers. Another branch's walk is never read. The bash walker's own state, a flat file at that same path, is not this package's.

## Errors

`RecordError` is the one anticipated failure: a record absent, or not readable as the harness writes it, with a one-line message naming the file. Any other `OSError` propagates. Which exit status either becomes is the caller's; the package has no command line yet.

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
