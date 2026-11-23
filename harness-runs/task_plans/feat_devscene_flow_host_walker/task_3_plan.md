### Task 3 — Read the run mode from the flow-progress ledger, or the skipped ids given, in `records`

**Goal:** Read the run mode's skipped ids the way the bash walker does (`cli/templates/scripts/lib/flow-walker-gates.sh` → `fw_run_mode_skipped`, `fw_id_in_list`). The flow-progress ledger's `## Run mode` block wins. Only when no ledger exists are the skipped ids the caller gives used. When neither answers, the result is an unresolved value carrying the bash walker's reason. It is never a guess.

**Depends on:** Task 2, which creates `devscene-flow-host/src/devscene_flow_host/records/errors.py` → `RecordError(Exception)`, whose message is one line naming the file and the cause. This task raises it for a ledger that is not UTF-8 text. It takes `state_dir` as an argument, the repo-relative `HarnessConfig.state_dir` Task 2 produces, and reads no configuration itself.

**Where this layer stops.** This task returns the skipped-id set and decides nothing with it. That `run_mode_skips_<id>` is `True` when `<id>` is in the set is **Task 4's** (`HarnessPredicateHost`). The ledger's `P1`–`P3` entries and its other blocks are not read here.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/ledger.py` (new)
- `devscene-flow-host/tests/test_ledger.py` (new)

**Work:**

- [ ] **The path and the values.** `LEDGER_DIRECTORY: Final = "flow_progress"`. `ledger_path(repo_root: Path, state_dir: str, branch: str) -> Path` returns `repo_root / state_dir / LEDGER_DIRECTORY / f"{branch}_progress.md"`. `@dataclass(frozen=True) class RunMode` with `skipped: frozenset[str]` and `source: Literal["ledger", "argument"]`, and `@dataclass(frozen=True) class RunModeUnresolved` with `reason: str`.
- [ ] **`parse_skipped(value: str) -> frozenset[str]`**, as `fw_id_in_list` reads a list: split on `,`, strip surrounding whitespace from each member, and drop empty members and every `none`. So `"none"` → `frozenset()` and `" parity, qa "` → `{"parity", "qa"}`.
- [ ] **`read_run_mode(repo_root: Path, state_dir: str, branch: str, skipped: str | None) -> RunMode | RunModeUnresolved`**, as `fw_run_mode_skipped` reads it:
  - **The ledger exists:** read it as UTF-8. Bytes that are not UTF-8 raise `RecordError(f"{path}: not UTF-8 text")`. Split on `"\n"` only. Any line starting `## ` begins a block, and the block is the run-mode block when the line, with trailing spaces, tabs and `\r` stripped, equals `## Run mode`. In that block, the first line starting `- skipped: ` gives the value after that prefix, with trailing spaces, tabs and `\r` stripped. A non-empty value → `RunMode(parse_skipped(value), "ledger")`. No such line, or an empty value → `RunModeUnresolved("the flow-progress ledger for '<branch>' has no '- skipped:' line under '## Run mode'")`. The ledger wins whatever `skipped` is.
  - **No ledger:** a non-empty `skipped` → `RunMode(parse_skipped(skipped), "argument")`. `None` or `""` → `RunModeUnresolved("no run-mode record: no flow-progress ledger for '<branch>' and no skipped ids given")`.
  - Any other `OSError` reading the ledger propagates unchanged.

  The module docstring states the rule, citing `fw_run_mode_skipped` as the reader this mirrors. Its *"Deliberately not covered:"* list names the ledger's other blocks and entries, and whether an id is in the run mode's closed directive set, which the run-mode instructions own and the reader does not check.
- [ ] **`tests/test_ledger.py`.** Its docstring opens *"The rule this file exists to enforce"*. Every ledger is planted under `tmp_path` at `ledger_path(tmp_path, "state", "feat_x")`. One case per rule, each expected value a literal:
  - the ledger's form as the harness writes it — `## Run mode`, a `Source:` line, `- skipped: none`, `- phases: …`, then `## Planning` — → `RunMode(frozenset(), "ledger")`
  - `- skipped: parity, qa` → `{"parity", "qa"}` from the ledger, even with `skipped="architecture"` given
  - `## Run mode \r` as the heading and `- skipped: qa\r` → `{"qa"}` (the trailing whitespace and CR tolerated)
  - a `- skipped: qa` line under `## Planning` only, and a ledger whose `## Run mode` block has no such line → the "has no '- skipped:' line" reason, exact text
  - `- skipped: ` with an empty value → the same reason
  - no ledger, `skipped="architecture"` → `RunMode({"architecture"}, "argument")`; no ledger, `skipped=None` and `skipped=""` → the "no run-mode record" reason, exact text
  - a non-UTF-8 ledger → `RecordError` with its exact message
  - `parse_skipped` on `"none"`, `" a , none, b "` and `""`

**Verification:**

- Run this task's own test file from the repository root, as one foreground command: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_ledger.py`. Every case passes.
- `commands.typecheck` exits zero.
- The two reason strings in `records/ledger.py` read exactly as written above, read against `tests/test_ledger.py`'s literals. Task 4 passes them through to its callers unchanged.
