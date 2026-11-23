### Task 2 — Read a round's evidence from its reviewer files, revision note and plan commits

**Goal:** Add `devscene-flow-host/src/devscene_flow_host/records/round_evidence.py`. It reads a round's evidence exactly as `fw_round_evidence` does: the round's highest number, each gate's status at that number, whether the next revision note exists, and whether the plan changed after the round's files were committed.

**Depends on:** Task 1. It uses `devscene_flow_host.records.round_files`:
- `next_review_index(folder: Path) -> int`;
- `review_verdict(path: Path) -> Literal["PASS", "FAIL"] | None`;
- `round_file_problem(path: Path) -> str | None`.

Its tests use `tests/round_fixtures.py` (`plant_review`, `init_repo`, `commit`, `git`, `PASS_BODY`, `FAIL_BODY`) without editing it.

**Source:** `cli/templates/scripts/lib/flow-walker-gates.sh` (`fw_round_evidence`).

**Where this layer stops.** This returns the evidence and decides nothing. It does not decide which round a resume enters or which records it carries. That is Task 6's `round_resume`. It renders no graph path either: the caller passes absolute paths and a note template that still carries `{round}`.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/round_evidence.py` (new)
- `devscene-flow-host/tests/test_round_evidence.py` (new)

**Work:**

- [ ] **The values.** Declare two frozen dataclasses. Task 6 consumes both exactly as written here:
  - `GateEvidence`, with `gate: str`, `status: Literal["PASS", "FAIL", "missing", "unreadable"]` and `file: Path` (absolute: `<folder>/review_<R>.md`).
  - `RoundEvidence`, with:
    - `round: int | None` (`None` is bash's `round: none`);
    - `gates: tuple[GateEvidence, ...]`, in the order given and empty when `round` is `None`;
    - `note_present: bool`;
    - `plan: Literal["not-newer", "newer", "unknown"]`.
- [ ] **The reader, up to git.** `read_round_evidence(repo_root: Path, note_template: str | None, plan_paths: Sequence[Path], gates: Sequence[tuple[str, Path]]) -> RoundEvidence`:
  - `R` is the highest `next_review_index(folder) - 1` over the gate folders. If every folder gives `-1`, return `RoundEvidence(None, (), False, "unknown")`.
  - A gate is `missing` when its round-`R` file does not exist (`exists()`). Otherwise it is its `review_verdict`, or `unreadable` when that is `None` or `round_file_problem` returns a reason.
  - The note is `note_template` with its **first** `{round}` replaced by `R + 1`. `note_present` is whether that path exists. A `None` template is absent.
  - With no gate's file present, `plan` is `"unknown"` and no git command runs.
- [ ] **The plan freshness, as `fw_round_evidence` asks git.** Each call is a fixed argument vector through `subprocess.run(["git", "-C", str(repo_root), …], capture_output=True)`, in this order:
  1. `rev-parse --is-inside-work-tree` fails → `RecordError(f"git cannot answer in {repo_root}")`.
  2. `rev-parse --verify -q HEAD` fails → `"unknown"`.
  3. For each present file, `rev-list -1 HEAD -- <file>`. A failure is the same `RecordError`; an empty answer is `"unknown"`.
  4. No plan paths → `"not-newer"`.
  5. Otherwise, for each present file's commit `c` until one answers non-empty, `rev-list <c>..HEAD -- <plan paths>`. If all are empty, `--no-optional-locks status --porcelain -- <plan paths>`. Either failing is the `RecordError`.
  6. A non-empty answer is `"newer"`, otherwise `"not-newer"`.

  A `FileNotFoundError` for the `git` binary is that `RecordError` too. Add the constant `ROUND_PLACEHOLDER: Final = "{round}"`.
- [ ] **The module docstring.**
  - **"The rule:"** names `fw_round_evidence`, and says `plan` is judged against the earliest-committed present file, as bash's header says.
  - **"Deliberately not covered"** names: deciding what the evidence means for the walk (`host`'s); and that git's own stderr is not carried into the message.
- [ ] **`tests/test_round_evidence.py`.** It opens with *"The rule this file exists to enforce"*. Each case plants a git repository under `tmp_path` through `round_fixtures`, with literal expectations taken from `fw_round_evidence`'s `REPRO` lines:
  - no review file → `round: none`;
  - round 0 with one gate FAIL and one missing → note absent, plan not-newer;
  - the next note planted, plus an uncommitted plan edit → note present, plan newer;
  - a plan commit after the round's files → newer;
  - a present, uncommitted review file → unknown;
  - a present file the check refuses → `unreadable`;
  - a gate whose round-`R` file is a valid PASS while another gate reached `R` → that gate PASS;
  - the `RecordError` message for a `repo_root` that is not a git repository but holds a present file.

**Verification:**

- `tests/test_round_evidence.py` passes, with the `RecordError` message asserted byte-exactly as `git cannot answer in <root>`.
- No case writes outside `tmp_path`: every repository is created there by `init_repo`.
- `round_evidence.py` runs `git` only through fixed argument vectors, with no shell string.
