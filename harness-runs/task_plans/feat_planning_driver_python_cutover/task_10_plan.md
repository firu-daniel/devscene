### Task 10 — Write the driver's park and pause files in `host/run_records.py`, and read the ledger's run-mode entries

**Goal:** Port the two run-control writes the bash driver made through `planning-record-lib.sh`: the clarification park (`prl_park`) and the pause files (`prl_pause`). The files keep the same names, contents and placement, so the watcher's park and pause classification reads a Python-written park exactly as a bash-written one. Also add the `records/ledger.py` reader of the flow-progress ledger's `## Run mode` entries — its `- skipped:` value and its `- ignored:` entries — read as `pd_run_mode_line` read them, so the hand-off narration (Task 17) takes them from `records` and parses no ledger line itself.

**Depends on:** Task 9, which adds `records/clarifications.py` → `max_question_index(repo_root, state_dir, branch) -> int`, `0` when no question exists.

**Where this task stops.**
- **It decides nothing.** When to park or pause, a park's title, and its body are **Task 17's** decisions.
- **Partial commits** are **Task 17's**. They are made through the existing `host/commit_points.py` → `commit_artifact(wrapper, worktree, "plan-round-partial", round_number=n)`.
- **Commits.** Neither write commits; the bash pilot did not either.
- **The `📌 Run mode:` line.** The ledger reader returns values and decides nothing. Formatting them into the narrated line — `none` versus `skipped … — authority …`, and the ` | ignored: "…"` suffixes — is **Task 17's**.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/run_records.py` (new)
- `devscene-flow-host/tests/test_run_records.py` (new)
- `devscene-flow-host/src/devscene_flow_host/records/ledger.py` — `RunModeEntries`, `IgnoredEntry`, `IGNORED_PREFIX` and `read_run_mode_entries`
- `devscene-flow-host/tests/test_ledger.py` — the new reader's cases

**Work:**

- [ ] **`write_park`.** Signature: `write_park(repo_root: Path, state_dir: str, branch: str, *, raised_by: str, title: str, body: str) -> str`. It returns the repo-relative path it wrote.
  - **Path.** The file is `<state_dir>/clarifications/<branch>/question_<max_question_index + 1>.md`. The directory is created when absent. A file already at that path is a `RecordError` naming it.
  - **Content, in order:**
    - `# <title>`, a blank line;
    - `Raised by: <raised_by> (script-driven planning)`, a blank line;
    - a `## Q1 — <title>` section and a blank line, only when no line of `body` starts with `## Q` followed by a digit;
    - then `body`.
  - **Writing.** The file is written through a temporary file in the same directory and `os.replace`, with mode `0o644`.
  - **Constants.** `RAISED_BY_SUFFIX = " (script-driven planning)"` is a `Final` constant. The `Raised by: ` prefix is imported from `records/clarifications.py` → `RAISED_BY_PREFIX`.
- [ ] **`write_pause`.** Signature: `write_pause(repo_root: Path, state_dir: str, branch: str, *, phase: str, next_step: str, now: datetime) -> None`. It writes as `prl_pause` did:
  - It appends `\n## <ts> — <branch> paused (script-driven planning)\n- phase: <phase>\n- next step: <next_step>\n` to `<state_dir>/PAUSE_PROGRESS.md`.
  - It writes `<ts>\n` to `<state_dir>/PAUSE_ACK`.
  - `<ts>` is `now` in UTC as `%Y-%m-%dT%H:%M:%SZ`.
  - `PAUSE_PROGRESS_FILE` and `PAUSE_ACK_FILE` are `Final` constants.
- [ ] **Module docstring.** *"The rule:"* names `prl_park` and `prl_pause` in `cli/templates/scripts/lib/planning-record-lib.sh`, which Task 4 deletes. Like the `fw_*` citations, they are readable in that file's history (`devscene-flow-host/README.md` → the retired-code note). *"Deliberately not covered"*: committing either file; deciding when; the partial commit.
- [ ] **`tests/test_run_records.py`:**
  - its header rule;
  - a park into an empty directory gives `question_1.md` with the exact bytes, written as a literal;
  - a second park after `question_2.md` exists gives `question_3.md`;
  - a body carrying `## Q1 — …` gets no added Q section;
  - the file mode is `0o644`;
  - a pause appends to an existing `PAUSE_PROGRESS.md` and writes `PAUSE_ACK`, both with exact bytes for a fixed `now`.
- [ ] **`records/ledger.py` → `read_run_mode_entries(repo_root: Path, state_dir: str, branch: str) -> RunModeEntries`**, and its cases in `tests/test_ledger.py`.
  - **The values.** `RunModeEntries` is a frozen dataclass of `skipped: str` and `ignored: tuple[IgnoredEntry, ...]`. `IgnoredEntry` is a frozen dataclass of `text: str` and `reason: str | None`.
  - **The reading**, as `pd_run_mode_line` (`cli/templates/scripts/lib/planning-driver-lib.sh`) read the ledger at `ledger_path(…)`:
    - each line has one trailing `\r` removed;
    - the section opens at the line equal to `_RUN_MODE_HEADING` and closes at the next line starting `## `; no other line is read;
    - a line starting `_SKIPPED_PREFIX` sets `skipped` to the rest, cut at the first `"   ("` (three spaces and a parenthesis); a later such line overwrites an earlier one; no such line leaves `skipped` `""`;
    - a line starting `IGNORED_PREFIX` — a new `Final` `"- ignored: "` — appends an `IgnoredEntry`, in ledger order: when the rest contains `" ("`, `text` is what precedes its **last** occurrence and `reason` is what follows it, verbatim with its closing parenthesis; otherwise `text` is the whole rest and `reason` is `None`.
  - **Unreadable shapes.** A missing ledger is `RecordError(f"the flow-progress ledger '{path}' does not exist")`; non-UTF-8 bytes are `RecordError(f"{path}: not UTF-8 text")`, the module's existing spelling.
  - **The docstring.** The module's rule gains *"`read_run_mode_entries` reads the `## Run mode` section's `- skipped:` value and `- ignored:` entries as `pd_run_mode_line` did"*, keeping the existing `_RUN_MODE_HEADING` / `_SKIPPED_PREFIX` constants as the one spelling. *"Deliberately not covered"*'s *"The ledger's other blocks"* stays, and gains *"Formatting the `📌 Run mode:` line, which is the host's"*. `read_run_mode` is not changed.
  - **The cases**, each against literals: a section with a skipped value carrying a `   (…)` comment cut before it; `none`; no `- skipped:` line giving `""`; two `- ignored:` entries, one with a reason containing an inner `(` (split at the last `" ("`) and one without; a `- skipped:` line under a later heading not read; a `\r\n` ledger; the two `RecordError` texts.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_run_records.py` passes.
- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_ledger.py` passes, every existing case unchanged.
- Every file the module writes stays under `<state_dir>`. One case asserts nothing else appears under `tmp_path`.
