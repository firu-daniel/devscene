### Task 11 — Collect, flush and commit the driver's improvement observations in `host/observations.py`

**Goal:** Port `prl_observe` and `prl_observe_flush`. The driver collects observation blocks during a drive. On every exit it flushes them into `<state_dir>/improvement_observations/<branch>.md`, with every machine path rewritten, and commits that file as the `observations` artifact. The file keeps the shape `plugin/instructions/improvement_observations_instructions.md` and `cli/templates/state-dir/improvement_observations/README.md` describe (scope register rows 7, 8 and 18).

**Where this task stops.**
- **Which events become observations** is **Tasks 13 and 17's**. They call `Observations.add`.
- **Flushing on every exit** is **Task 16's**.
- **The commit** goes through the existing `host/commit_points.py` → `commit_artifact(wrapper, worktree, "observations")`, which returns `True` / `False` or raises `CommitPointError`.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/observations.py` (new)
- `devscene-flow-host/tests/test_observations.py` (new)

**Work:**

- [ ] **`Observations.add`.** `Observations.add(category: str, problem: str, evidence: str, cost: str) -> None`.
  - `category` must be one of `CATEGORIES`, a `Final` tuple: `tooling-gap`, `silent-failure`, `flow-efficiency`, `optimization`, `agent-contract`, `shared-state`, `convention`. Any other category raises `ValueError`.
  - Each text is flattened to one line, `\r` and `\n` becoming spaces. An empty `problem` raises `ValueError`.
  - Each block is `## <problem>\n- **category:** <category>\n- **evidence:** <evidence>\n- **cost this run:** <cost>\n\n`, held in memory.
- [ ] **`Observations.flush`.** `async Observations.flush(*, repo_root: Path, main_repo: Path, state_dir: str, branch: str, wrapper: Path, home: str | None, now: datetime, log: Callable[[str], None]) -> None`. It is best-effort and never raises: every failure is one `log` line. With no blocks it does nothing. Otherwise, as `prl_observe_flush` did:
  - **Keep the existing file.** Keep its text up to its last non-blank line. Drop that line when it is exactly `# Task run (Phase D)`, the `CLOSING_LABEL` constant. Then drop trailing blank lines.
  - **Append, in order:**
    - a blank line;
    - `# Script-driven planning — <ts>` and a blank line;
    - the blocks;
    - `# Task run (Phase D)`.
- [ ] **The machine-path rewrite**, as `PRL_REWRITE_AWK` did.
  - **The needles.** The worktree, the main checkout and the home directory are the needles.
    - A needle that is empty, `/`, a single path segment, or carries `'` is dropped, with a log line.
    - The main checkout is dropped when it equals the worktree.
    - The longer needle is rewritten first.
  - **Where a match counts.** A match counts only where the path ends, or continues with `/`, or is followed by one of the delimiter characters `` ` ``, space, tab, `'`, `"`, `)`, `,`, `;`, `]`, `>`.
  - **The rewrite.**
    - The worktree becomes the repo-relative remainder, or `.`.
    - The main checkout becomes the repo-relative remainder followed by ` (main checkout)`.
    - The home directory becomes `~`.
  - **After the rewrite.** When any needle still occurs in the file, restore the previous file and do not commit, logging why. Otherwise commit with `commit_artifact(wrapper, repo_root, "observations")`. When that raises, restore the previous file and log the cause.
- [ ] **Module docstring.** *"The rule:"* names `prl_observe` / `prl_observe_flush`. *"Deliberately not covered"*: which events are observed; pushing, which the wrapper's `--push` does.
- [ ] **`tests/test_observations.py`:**
  - its header rule;
  - an unknown category refused;
  - a multi-line problem flattened;
  - a flush into no file;
  - a flush after an existing file ending in `# Task run (Phase D)`, whose label moves to the end;
  - each needle's rewrite, as exact bytes written as literals;
  - a needle followed by a non-delimiter left alone;
  - a residual needle restoring the file with no wrapper call;
  - a wrapper exiting `1` restoring the file and logging, without raising.
  - The wrapper is a fake planted under `tmp_path` that logs its argv, as `tests/test_planning_hooks.py` → `_plant_wrapper` does.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_observations.py` passes.
- The planted wrapper's log shows exactly `--repo <root> --artifact observations --push` for a committed flush, and no call for a restored one.
