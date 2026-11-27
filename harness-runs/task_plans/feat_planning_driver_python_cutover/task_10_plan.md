### Task 10 — Write the driver's park and pause files in `host/run_records.py`

**Goal:** Port the two run-control writes the bash driver made through `planning-record-lib.sh`: the clarification park (`prl_park`) and the pause files (`prl_pause`). The files keep the same names, contents and placement, so the watcher's park and pause classification reads a Python-written park exactly as a bash-written one.

**Depends on:** Task 9, which adds `records/clarifications.py` → `max_question_index(repo_root, state_dir, branch) -> int`, `0` when no question exists.

**Where this task stops.**
- **It decides nothing.** When to park or pause, a park's title, and its body are **Task 17's** decisions.
- **Partial commits** are **Task 17's**. They are made through the existing `host/commit_points.py` → `commit_artifact(wrapper, worktree, "plan-round-partial", round_number=n)`.
- **Commits.** Neither write commits; the bash pilot did not either.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/run_records.py` (new)
- `devscene-flow-host/tests/test_run_records.py` (new)

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
- [ ] **Module docstring.** *"The rule:"* names `prl_park` and `prl_pause` in `cli/templates/scripts/lib/planning-record-lib.sh`, which Task 3 deletes. Like the `fw_*` citations, they are readable in that file's history (`devscene-flow-host/README.md` → the retired-code note). *"Deliberately not covered"*: committing either file; deciding when; the partial commit.
- [ ] **`tests/test_run_records.py`:**
  - its header rule;
  - a park into an empty directory gives `question_1.md` with the exact bytes, written as a literal;
  - a second park after `question_2.md` exists gives `question_3.md`;
  - a body carrying `## Q1 — …` gets no added Q section;
  - the file mode is `0o644`;
  - a pause appends to an existing `PAUSE_PROGRESS.md` and writes `PAUSE_ACK`, both with exact bytes for a fixed `now`.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_run_records.py` passes.
- Every file the module writes stays under `<state_dir>`. One case asserts nothing else appears under `tmp_path`.
