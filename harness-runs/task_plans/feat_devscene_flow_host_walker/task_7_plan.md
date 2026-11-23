### Task 7 — Document the layers, the records, the predicates and the walk store in `devscene-flow-host/README.md`

**Goal:** Make the package's README describe the package as it now is. That means its three layers and what each may import, the records it reads and how, the predicates it answers, where each branch's walk is kept, and its error type. A contributor then learns the structure from the README, and the conventions pass that follows this branch has a source to read.

**Depends on:** Tasks 1–6, which build what this documents. State each fact as their files define it, re-read from the landed code rather than from this plan:

- Task 1: the layers `commands` over `host` over `records`, the contracts `devscene-flow-host-layers` and `devscene-flow-host-graphscene-outside-records` in `pyproject.toml`, and `tests/test_layers.py`. The package root exports nothing (`__all__ = []`).
- Task 2: `records/config.py` → `read_config`, `HarnessConfig` (`stateDir` and `phases` only), and `records/errors.py` → `RecordError`.
- Task 3: `records/ledger.py` → `read_run_mode`: the ledger's `## Run mode` `- skipped:` line wins, then the skipped ids given, and otherwise an unresolved reason.
- Task 4: `host/predicates.py` → `HarnessPredicateHost`, answering `phase_<parity|qa|docs>_off` and `run_mode_skips_<id>`, re-read on every arrival, with `None` for anything else.
- Task 5: `host/store.py` → `walk_store`, one `FileStateStore` per branch at `<stateDir>/.flow_walker_state/<percent-encoded branch>.json`.
- Task 6: `host/walking.py` → `open_walker`.

**Where this task stops.** It edits the README only. `.claude/context/devscene-flow-host.md` is a conventions document and is never a target: its restatement is recorded in the plan's return as a `stale-rule` entry for a supervised `/devscene:analyze` pass. `docs/development.md` and `ROADMAP.md` are **Task 8's**.

### Targets

- `devscene-flow-host/README.md`

**Work:**

- [ ] **`## What it is`**: drop "and no behaviour yet". Add one sentence saying what the package does now: it reads the harness's configuration and flow-progress ledger, answers the planning graph's phase and run-mode predicates, and keeps each branch's walk, for GraphScene's `Walker`. It has no command line yet. Keep the paragraph's other sentences and the *"It stays in this repository"* paragraph as they are.
- [ ] **A new `## The layers` section**, after `## What it may depend on`. It holds a table — `Layer`, `Path`, `Holds`, `May import` — with one row each for `commands`, `host` and `records`. Describe a layer's future contents by kind only (*"the command lines over the host"*), never by an issue number: a deferral in this tree cites a numbered roadmap row, not an issue. After the table, say that imports point down only, that `records` never imports `graphscene`, that the two contracts in `pyproject.toml` hold this and `tests/test_layers.py` runs them with no cache, and that a new module lands in the layer its work belongs to. Also say that a new layer or a changed import rule lands with its contract change, its planted cases in `tests/test_layers.py` and its row here, and that the package root exports nothing because adopters never import it.
- [ ] **A new `## What it reads, answers and keeps` section**, after `## The layers`, with three short paragraphs:
  - **Records.** `devscene.config.json`, read for `stateDir` and `phases` only. The ledger's `## Run mode` → `- skipped:` line, which wins over skipped ids the caller gives. Each reader mirrors the bash walker's reader of the same record, and names it.
  - **Predicates.** The two name patterns and their meanings. A predicate the host cannot answer is refused by the walk, never guessed. The records are re-read on every arrival.
  - **The walk.** One state file per branch under `<stateDir>/.flow_walker_state/`, which the existing ignore rule for that path covers. Another branch's walk is never read. The bash walker's own state, a flat file at the same path, is not this package's.
- [ ] **A new `## Errors` section**, or a paragraph at the end of the one above. `RecordError` is the one anticipated failure: a record absent, or not readable as the harness writes it, with a one-line message naming the file. Any other `OSError` propagates. Which exit status either becomes is the caller's, and the package has no command line yet. Keep `## The lock follows GraphScene`, `## Running the toolchain` and `## Gating` unchanged, apart from adding `tests/test_layers.py` beside `tests/test_boundary.py` where the README names what enforces its rules.

**Verification:**

- Every symbol, path, contract id and reason the README names exists under that name in the landed code. Check by `grep -rn` for each in `devscene-flow-host/src` and `devscene-flow-host/pyproject.toml`.
- `grep -nE '#[0-9]+' devscene-flow-host/README.md` prints nothing: no issue number in the README.
- `git diff --stat` shows `devscene-flow-host/README.md` as the only changed file.
