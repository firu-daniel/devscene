# devscene-flow-host

**Who reads this:** a contributor changing this package. It owns what the package is, what it may depend on, how its lock follows GraphScene's, and how its toolchain is run here.

## What it is

`devscene-flow-host` is the harness's GraphScene host, imported as `devscene_flow_host`. It holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it. It reads the harness's configuration, flow-progress ledger and round and reviewer files, answers the planning graph's phase and run-mode predicates, applies the reviewer-file rules when a gate's outcome is recorded, resumes a round from the files on disk, and keeps each branch's walk, for GraphScene's `Walker`. Its one command line is `devscene-flow-walker`, `flow-walker.sh`'s compatibility command (`## The command line`). Any other DevScene Python integration gets its own `devscene`-prefixed package rather than a place here. Anything useful without DevScene goes in GraphScene (`graphscene/`), not here.

It stays in this repository: it is not part of the npm package (`cli/package.json` → `files`), and adopters never import it.

## What it may depend on

- **The package imports only the standard library, itself and its declared runtime dependencies.** It reaches `graphscene` through its public surface only — `import graphscene` or `from graphscene import <name in graphscene.__all__>`, never a submodule such as `graphscene.engine` — and GraphScene never imports it.
- **`graphscene` is an editable path dependency on `../graphscene`** (`pyproject.toml` → `[tool.uv.sources]`), so one sync provisions both packages, this package's environment imports the checkout's current `graphscene/src/graphscene/`, and no release is needed.
- **The tests stay inside the same boundary, widened only by the `dev` dependency group.** A module under `tests/` imports the standard library, `devscene_flow_host`, the declared runtime dependencies through the same public surface, the `dev` group's tools, and the suite's own support modules — never another package's tests or another layer's source. Reading a tracked file of another layer as test input (the walker's graph file, GraphScene's manifest) is not an import and stays allowed.

`tests/test_boundary.py` and `tests/test_layers.py` enforce these rules for the package; `tests/` itself is not scanned, so the tests' rule is held by review.

## The layers

| Layer | Path | Holds | May import |
|---|---|---|---|
| `commands` | `src/devscene_flow_host/commands/` | The command lines over the host: `main` (`commands/flow_walker.py`), `parse` (`commands/arguments.py`), `render` (`commands/render.py`) | `host`, `records`, `graphscene`'s public surface, the standard library |
| `host` | `src/devscene_flow_host/host/` | GraphScene's protocols over the records, and the harness's rules over them: `HarnessPredicateHost` (`host/predicates.py`), `walk_store` (`host/store.py`), `open_walker` (`host/walking.py`), `render_path` (`host/paths.py`), `round_of_gate`, `round_of_writer` and `review_iteration` (`host/reviewers.py`), `RefusalStore` (`host/refusals.py`), `RevisionFindingsStore` (`host/revision_findings.py`), `read_printed` and `PrintedReadsStore` (`host/printed_reads.py`), `round_resume` (`host/resume.py`), `record_outcome` and `HostStep` (`host/round_gates.py`), `start_walk` and `current_step` (`host/re_entry.py`) | `records`, `graphscene`'s public surface, the standard library |
| `records` | `src/devscene_flow_host/records/` | The repository's records read into plain values: `read_config` (`records/config.py`), `read_run_mode` (`records/ledger.py`), `review_verdict`, `round_file_problem`, `next_review_index`, `fail_count` and `round_file_path` (`records/round_files.py`), `read_round_evidence` (`records/round_evidence.py`), `read_index_evidence` (`records/index_evidence.py`), `RecordError` (`records/errors.py`) | `records`, the standard library |

Imports point down only, and `records` never imports `graphscene`. The contracts `devscene-flow-host-layers` and `devscene-flow-host-graphscene-outside-records` in `pyproject.toml` hold this, and `tests/test_layers.py` runs them with no cache. A new module lands in the layer its work belongs to. A new layer or a changed import rule lands with its contract change, its planted cases in `tests/test_layers.py` and its row here. The package root exports nothing (`__all__ = []`), because adopters never import it.

## What it reads, answers and keeps

**Records.** `read_config` reads `devscene.config.json` for `stateDir` and `phases` only, and refuses one with no `defaultBranch` as `hr_config_load` does, into a `HarnessConfig`, as `hr_state_dir` and `hr_phase_enabled` read them (`cli/templates/scripts/lib/harness-run-lib.sh`). `read_run_mode` reads the flow-progress ledger's `## Run mode` → `- skipped:` line, as `fw_run_mode_skipped` reads it (`cli/templates/scripts/lib/flow-walker-gates.sh`). Whenever the ledger exists it wins over the skipped ids the caller gives; those are used only when there is no ledger, and with neither the result is a `RunModeUnresolved` carrying the reason.

**Predicates.** `HarnessPredicateHost` answers `phase_<parity|qa|docs>_off`, true when that phase is off in `phases`, and `run_mode_skips_<id>`, true when the run mode skips `<id>`. Any other name, an unresolvable phase or an unresolved run mode is `None`, which the walk refuses rather than guesses; `refusal_reason` gives the reason. The records are re-read on every arrival, so a ledger written mid-walk is seen at the next one.

**The walk.** `walk_store` keeps one GraphScene `FileStateStore` per branch at `<stateDir>/.flow_walker_state/<percent-encoded branch>.json`, which this repository's ignore rule for that path covers. Another branch's walk is never read. The bash walker's own state, a flat file at that same path, is not this package's.

**Round and reviewer files.** Each reader reads as the bash function it names (`cli/templates/scripts/lib/flow-walker-gates.sh`). `review_verdict` reads a reviewer file's one `verdict: PASS` or `verdict: FAIL` line, as `fw_review_verdict` does. `round_file_problem` gives the reason a round gate may not use a file — no single verdict line, a `FAIL` with no numbered entry under `## Must Fix`, a `PASS` with one, or an entry lacking `**Class:**` or `**Failure:**` — as `fw_round_file_check` does. `next_review_index` and `fail_count` read a findings folder's next free `review_<n>.md` index and its `FAIL` count, as `fw_next_review_index` and `fw_fail_count` do. `read_round_evidence` reads a round's highest round number, each gate's status at it, whether the next revision note exists and whether the plan changed after the round's files were committed, asking `git` as `fw_round_evidence` does. `read_index_evidence` reads whether a story index has a `## Rejected findings` section, the entries there still open, and whether it has a `## Scope register` section, as `fw_index_evidence` does. A missing round file or findings folder is a value (`None`, `0`), never a `RecordError`, because the walk routes on it. `render_path` renders a graph path template's `{state_dir}`, `{branch}` and `{round}`, and `review_iteration` gives a reviewer outside a round the next free index in its `findingsFolder`.

**Recording a gate.** `record_outcome` records a gate's outcome under the four reviewer-file rules, as `flow-walker.sh`'s `next` does: an outcome whose verdict is `fail` requires a findings file, and so does any verdict outcome at a gate of the open round; a round gate's file must pass `round_file_problem` before its verdict is recorded; a refused file records nothing in the walk — its gate is left out of a `wait`'s pending list, and once no other gate is out every refused gate is re-dispatched as one set in the same round; a held gate at a join whose only gates out are refused ones does not escalate there — the refused gates are re-dispatched first, and the held gate escalates at the round's next join, once every re-dispatched gate has a verdict or is held, so the escalation carries the whole round's verdicts (`host/round_gates.py` → *"The rule:"*); and the third refusal of one gate in a round records the held outcome `error`. The refusals are the host's own record, `RefusalStore`, at `<stateDir>/.flow_walker_state/round_refusals/<percent-encoded branch>.json` behind the lock `<file>.lock`; every call that records takes that lock before the walk's own and releases it after. The `HostStep` returned carries the step and the `refused:` lines it brings.

**Kept findings files.** A findings file given outside an open round set — a non-round reviewer's `FAIL`, such as `ui_review`'s, or one given with `answered` — is kept for the writer's next revision, as `flow-walker.sh` → `next` keeps its one `revision_findings` key. The record is `RevisionFindingsStore`, at `<stateDir>/.flow_walker_state/revision_findings/<percent-encoded branch>.json`. `record_outcome` writes it, under `RefusalStore`'s lock and only when the returned action is not `Refused`; a held outcome at a gate of an open set never touches it; a result that closes a round clears it, as bash's `close_round` overwrites the key; and `start_walk` clears it when the walk started. `HostStep.revision_findings` carries the record as it stands after the call, and `current_step` returns it unchanged. When it is non-empty, `render` prints it as a revision's `arg.findings_file:` lines and a cap's `findings_file:` lines in place of the closed round's files: it takes precedence, as bash's single key holds whichever was written last.

**Printed reads.** The values a step read from disk when it was printed — a non-round reviewer's next free index, a cap's `FAIL` counts and the story index's evidence — are kept as the host's record `PrintedReadsStore`, at `<stateDir>/.flow_walker_state/printed_reads/<percent-encoded branch>.json`, as bash's `next` saves its `out=` lines. `read_printed` does those reads for a step. `record_outcome` and `start_walk` write the record under `RefusalStore`'s lock, and only when the returned action is not `Refused`. `HostStep.printed` carries it, and `render` prints from it and reads no file. `current_step` returns it as kept, so a file written since the step was printed changes nothing; it reads the files only when no record exists.

**Resuming a round.** `round_resume` builds a round's `RoundResume` for GraphScene's `Walker.start` from the files on disk, as `flow-walker.sh`'s `start_round` and `start_record` do. The entry is a round's writer or a round node; any other entry has no resume, and a round with no file has none either. Entered at the writer, the round resumes at the number after its highest. Entered at the round node: a round with files missing whose evidence is consistent records the present gates and opens only the missing ones; any other incomplete round opens the whole set at that round; a complete round that is unreadable or has no `FAIL` is reviewed again; a `FAIL` with the next revision note on disk opens the next round; and a `FAIL` without the note records every verdict, so the round closes at once. Convergence is never inferred from files. `start_walk` reads as `flow-walker.sh`'s `start`: it rebuilds the round position through `round_resume` and `Walker.start`, under the same lock order as `record_outcome`, and clears the refusal record only when the walk started. `current_step` reads as its `current`: it re-reads the saved step with every gate awaiting re-dispatch left out, takes no lock and changes nothing, so a refused gate is never dispatched twice, and it returns the printed reads as kept. The counter and the prompt variants a lost walk loses are lost here too, as in bash.

## Errors

`RecordError` is the one anticipated failure: a record absent, or not readable as the harness writes it, with a one-line message naming the file. Any other `OSError` propagates. A malformed refusal record raises `ValueError` naming the file, and its lock `TimeoutError`, as the walk's store does; a round gate with no `findingsFolder` raises `ValueError`. The `commands` layer alone turns these into exit statuses: `commands/flow_walker.py` → `failure` maps a `RecordError`, a `GraphError`, a lock's `TimeoutError` and any other `OSError` or `ValueError` to exit `2` with its own message, and any other exception to exit `2` as `internal error: <type>: <message>`. `## The command line` gives the whole table.

## The command line

`devscene-flow-walker` is `flow-walker.sh`'s compatibility command, for #419 to hand every `flow-walker.sh` caller to it: the same four verbs, the same flags plus `--flows`, the same `key: value` output on stdout, and the same exit statuses with one `flow-walker: <cause>` line on stderr (`commands/flow_walker.py` module docstring). It records an outcome only through `record_outcome`, starts only through `start_walk` and re-reads only through `current_step`. Where it answers differently from `flow-walker.sh` is `## Differences from flow-walker.sh`.

Install the console script into the package environment first, outside any sandbox (this provisions every package's environment):

```
bash scripts/python-service.sh provision
```

Then run each verb from the repository root. Start a walk:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker start --flow <flow> --branch <branch> --flows <dir> [--entry <node>] [--skipped <ids|none>]
```

Record an outcome:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker next --flow <flow> --branch <branch> --flows <dir> --outcome <outcome> [--node <node>] [--findings <path>] [--skipped <ids|none>]
```

Re-read the pending step:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker current --flow <flow> --branch <branch> --flows <dir>
```

Check a round file:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker check-round-file --findings <path>
```

| Flag | Verbs | Value |
|---|---|---|
| `--flow` | `start`, `next`, `current` | The flow, `[a-z0-9_]` only; required |
| `--branch` | `start`, `next`, `current` | The branch whose walk this is; required |
| `--flows` | `start`, `next`, `current` | **The launcher's, not `flow-walker.sh`'s**: the directory holding `<flow>.v4.graph.json`, absolute as given or relative under the repository root; required, because bash finds its graph beside itself and this command cannot |
| `--entry` | `start` | The entry node |
| `--skipped` | `start`, `next` | The run mode's skipped ids, comma-separated, or `none`; read only when no flow-progress ledger exists |
| `--outcome` | `next` | The outcome, `[A-Za-z0-9_]` only; required. `FAIL` requires `--findings` |
| `--node` | `next` | The gate the outcome is for, `[a-z0-9_]` only |
| `--findings` | `next`, `check-round-file` | The reviewer's findings file, absolute as given or relative under the repository root, with no tab; required by `check-round-file` |

`parse` (`commands/arguments.py`) refuses a command line as `flow-walker.sh` → `# --- Arguments` does, with the same checks in the same order and the same words: a flag the verb does not take, a value carrying a newline, a required flag missing or given an empty value. A repeated flag keeps its last value.

| Exit | Meaning |
|---|---|
| `0` | An action was printed on stdout; for `check-round-file`, the file is valid and nothing is printed. |
| `1` | A refusal: a usage error; a step the walk refuses, whose cause is the predicate host's `last_refusal` when it has one; `next` or `current` with no saved walk; no `<flows>/<flow>.v4.graph.json`. |
| `2` | A fault: not inside a git repository; a graph that does not load or declares another flow; and every other exception, through `failure`. |
| `3` | `check-round-file` only: the file is invalid or absent. |

Every non-zero exit writes exactly one `flow-walker: <cause>` line on stderr, a newline in the cause flattened, and nothing on stdout. Only `KeyboardInterrupt` and `SystemExit` escape `main`.

`bash scripts/python-service.sh run` is not a route to the command: its `devscene-flow-host` row names no console script. How an adopter launches it is #419's.

## Differences from flow-walker.sh

**Who reads this:** #419, switching `flow-walker.sh`'s callers to `devscene-flow-walker`. Each entry names what `flow-walker.sh` does, what the command does, and the `cli/test/flow-walker*.test.mjs` suite area that pins bash's behaviour and must change with it.

**Chosen** — the host's way wins; these stay:

- **The walk's state.** Bash keeps one flat file, `<stateDir>/.flow_walker_state`, for whichever branch is walking, and refuses a `next` or `current` naming another flow or branch. The command keeps one file per branch at `<stateDir>/.flow_walker_state/<percent-encoded branch>.json` (`host/store.py` → `walk_state_path`), so another branch's walk is never read and a different branch is never refused; only a mismatched flow is, in GraphScene's words (`the saved walk is of flow '<saved>', not '<flow>'`). With no saved walk the refusal names the per-branch file: `no walk in progress at <that file>: run 'start' first`. One state directory cannot hold both bash's file and the command's directory at `.flow_walker_state`. Suites: `flow-walker-ui-and-reentry.test.mjs` → *"(11) next for a branch other than the one started is refused"*; `flow-walker-resume.test.mjs`, which deletes and inspects the saved walk.
- **The run-mode refusal.** Bash says `no run-mode record: no flow-progress ledger for '<branch>' and no --skipped`; the command says `… and no skipped ids given` (`records/ledger.py` → `read_run_mode`). No caller outside the walker parses it, and no `flow-walker*` suite asserts its text.
- **The graph.** Bash reads `<its own dir>/flows/<flow>.graph.json` and refuses a `formatVersion` other than 3 with exit `1`. The command reads format 4 at `<flows>/<flow>.v4.graph.json` (`commands/flow_walker.py` → `GRAPH_SUFFIX`), and a graph GraphScene rejects, or one declaring another flow, exits `2` as `cannot load <file>: <violation>` or `graph <file> declares flow …`. A missing graph file still exits `1` as `unknown flow '<flow>': no <file>`. Suite: `cli/test/helpers/walker.mjs` → `WALKER_GRAPH_PATH`, which every `flow-walker*` suite's fixture uses.
- **The locks.** Bash takes one `mkdir` lock directory, `<state file>.lock`, breaks one older than a minute through a `.break` sibling, and gives up after 120 s with exit `2` and an `rmdir` remedy. The command takes two `flock` locks — `RefusalStore`'s, then the walk's — each polled every 0.1 s for 120 s; a lock dies with its process, so there is no stale-lock removal and no `rmdir` remedy. A timeout exits `2` as `cannot lock <file> within 120.0 s` (`host/refusals.py`) or `<file>: not acquired within 120.0 s` (GraphScene's `FileStateStore`). Suite: `flow-walker-concurrency.test.mjs` → *"(2) a lock older than a minute is broken"*, *"(3) a fresh lock held by another call is waited for"* and *"(4) two calls waiting on a stale lock"*; *"(1) three outcomes recorded by simultaneous next calls"* holds unchanged (`tests/test_flow_walker_concurrency.py`).
- **Refusal texts no caller parses.** A refusal the walk makes is worded by GraphScene or the host rather than bash — an undeclared outcome, a gate not pending, a missing `--node`, a finished walk, an `--entry` outside the flow's entries, an unresolvable phase flag; the exit status `1` and the `flow-walker: ` prefix are kept, and `parse`'s usage refusals keep bash's words. Suites asserting only the status and prefix hold unchanged: `flow-walker.test.mjs` → *"(10) an outcome the pending node does not declare is refused"*; `flow-walker-ui-and-reentry.test.mjs` → *"(9) an --entry outside the flow's entries is refused"*. `flow-walker-fan-out.test.mjs` → `assertRefused` also matches the cause: *"(3) an outcome for a gate not pending in the round"* (`/not pending in round 0/`) still matches, but *"(5) a gate's error with two verdicts recorded"* (`/the walk finished/`, GraphScene says `the walk has finished`) and *"(6) --node is required while a set is pending"* (`/name the gate with --node/`, GraphScene says `name the gate with node`) do not.
- **An unexpected exception.** Bash has no such case. The command exits `2` with `internal error: <type>: <message>`, never Python's own exit `1` and traceback (`commands/flow_walker.py` → `failure`). No suite pins it.
- **`current` re-renders.** Bash re-prints the saved action's bytes (`out=`). The command re-reads the saved step and renders it again; every line keeps bash's form. The values bash read from disk at print time — a non-round reviewer's `arg.iteration`, a cap's `rounds:` counts and its evidence lines — come from the printed-reads record (`commands/render.py` → `HostStep.printed`), so a file written since the step was printed changes nothing on `current`. Suites that hold unchanged: `flow-walker-ui-and-reentry.test.mjs` → *"(10) current re-prints the pending set byte-identically"* and *"(4) UI reviewer FAILs until the cap"*; `flow-walker-resume.test.mjs` → *"(1) a set in flight is re-printed"*, *"(2) a revision a FAIL round queued is re-printed"* and *"(4) a UI reviewer in flight is re-dispatched"*; `flow-walker.test.mjs` → *"(3) architecture FAILs every round until the cap"*. The host's pins: `tests/test_flow_walker.py` → `test_current_reprints_a_ui_reviewers_index_after_its_file_is_written` and `test_current_reprints_the_plan_rounds_cap_after_a_fail_and_an_index_edit`.
- **A rendering fault after the save.** Bash renders before it writes, so every non-zero exit leaves its state file byte-identical. The command saves the walk inside `start_walk` or `record_outcome` and renders after, so a rendering fault exits `2` with the walk already saved (`commands/flow_walker.py` module docstring → *"Deliberately not covered"*). A fault in `read_printed` (`host/printed_reads.py`) after the save exits `2` the same way and removes the printed-reads record, so a later `current` reads the files again. No suite pins it.
- **The held-gate escalation.** At a join whose only gates out are refused, bash escalates the held gate at once (`flow-walker.sh` → `ROUNDS`, `record_in_set`); the refused gate is reviewed again only on resume: `fw_round_evidence` reads the refused file on disk as `unreadable`, so `start` at the round node reopens the round's whole set (`flow-walker.sh` → `STATE`, *"any other incomplete round opens the whole set at that round"*; `flow-walker-resume.test.mjs` → *"(9) inconsistent round evidence dispatches the whole set, and each gate replaces its file"*). The command re-dispatches the refused gates as one set in the same round and escalates at the round's next join, carrying the whole round's verdicts (`host/round_gates.py` → *"The rule:"*). GraphScene gives a host no way to set a due gate aside in an open round, and no GraphScene change is made for this. Both orders review the refused gate again; they differ in when. No `flow-walker*` suite pins this combination, so #419 moves no suite: `flow-walker-fan-out.test.mjs` → *"(5) a gate's error with two verdicts recorded"* holds an `error` with no gate refused, and *"(10) the third refusal of a gate escalates"* escalates on the gate's own refusal with nothing else held; the other refused-gate tests, *"(7)"* to *"(9)"* and *"(11)"*, hold no gate. The host's order is pinned by `tests/test_round_gates.py` → `test_a_held_error_beside_a_refused_gate_re_dispatches_first` and `test_a_held_error_waits_while_its_refused_sibling_is_refused_again`.

**Still open** — differences to be removed:

None is open. A repeated `## Rejected findings` heading was once listed here and is not a difference: `fw_index_evidence` prints one `evidence:` line however many such headings an index carries, then every open entry after it in file order, as the command does (`tests/test_index_evidence.py`, `tests/test_render.py`).

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
