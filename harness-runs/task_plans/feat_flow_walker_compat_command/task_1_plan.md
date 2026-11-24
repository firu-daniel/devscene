### Task 1 — Keep a non-round findings file for the writer's revision in `host/revision_findings.py`

**Goal:** Close #464's non-round findings-file gap in the `host` layer: keep the findings file given at a non-gate call — a non-round reviewer's `FAIL` (`ui_review`), or `answered` — as `flow-walker.sh` keeps `revision_findings`, so the writer's revision and a cap escalation carry it, and remove the `TODO: @claude` marker in `record_outcome`'s non-gate branch.

**The bash rule this ports** (`cli/templates/scripts/flow-walker.sh`): `revision_findings` is one state key with four writers, and the last one wins. `next`'s `dispatch` branch sets it to `--findings` for any outcome that is not a round gate's verdict (*"`elif [ -n "$A_FINDINGS" ]; then st_set revision_findings "$A_FINDINGS"`"*); `next`'s `answer` branch sets it to `--findings` when one is given with `answered`; `close_round` overwrites it with the closed round's files; `start` clears it. A held outcome recorded in an open set (`record_in_set`'s `*)` branch) never touches it. `render_block` prints it as `arg.findings_file:` lines on a `prompt: revision`, and `take_binding` as `findings_file:` lines on a cap escalation.

**Where this layer stops.** This task keeps the record and hands it to the caller on `HostStep.revision_findings`; it renders nothing. **Task 3** (`commands/render.py`) owns the precedence when it prints: `revision_findings` when non-empty, otherwise the `detail`s of the action's `closed_round` — which is exactly bash's single key, because this task clears the record whenever a round closes. Task 3 and Task 5 depend on the contract below and restate it.

**The contract this task produces:**

- `devscene_flow_host.host.revision_findings.RevisionFindingsStore(repo_root: Path, state_dir: str, branch: str)` with `read() -> tuple[str, ...]` (`()` when the file is absent), `write(files: tuple[str, ...]) -> None` and `clear() -> None`.
- `devscene_flow_host.host.revision_findings.revision_findings_path(repo_root, state_dir, branch) -> Path` = `<repo_root>/<state_dir>/.flow_walker_state/revision_findings/<quote(branch, safe="")>.json`.
- `HostStep.revision_findings: tuple[str, ...] = ()` — the kept record as it stands after the call, on every `HostStep` that `record_outcome`, `start_walk` and `current_step` return with a non-`Refused` action.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/revision_findings.py` (new)
- `devscene-flow-host/src/devscene_flow_host/host/round_gates.py`
- `devscene-flow-host/src/devscene_flow_host/host/re_entry.py`
- `devscene-flow-host/tests/test_revision_findings.py` (new)
- `devscene-flow-host/tests/test_round_gates.py`
- `devscene-flow-host/tests/test_re_entry.py`

**Work:**

- [ ] `host/revision_findings.py`: the store, modelled on `host/refusals.py` → `RefusalStore`. `REVISION_FINDINGS_DIRECTORY: Final = "revision_findings"` beside the imported `host/store.py` → `STATE_DIRECTORY`; `revision_findings_path` raises `ValueError("a walk's branch is empty")` for an empty branch, as `refusals_path` does. The document is `{"version": 1, "files": [<str>, …]}`; `write` replaces it through a temporary file in the same directory and `os.replace`, as `RefusalStore.write` does; `_load` refuses invalid JSON, another version, a missing or extra key and a non-string entry with `ValueError("<path>: <reason>")`. The module takes **no lock of its own**: its docstring's *"The rule:"* states that every write happens while the caller holds `RefusalStore`'s lock, that `read` is lock-free because the file is replaced whole, and names the bash key and the four writers above; *"Deliberately not covered"* lists rendering (the `commands` layer's) and removing a finished branch's file.
- [ ] `host/round_gates.py`: add `revision_findings: tuple[str, ...] = ()` to `HostStep` with its meaning in the docstring. In `record_outcome`, still inside `store.lock()`: on the non-gate branch, when `opened is None`, `findings` is given and the step is not `Refused`, write `(findings,)`; then, on every non-`Refused` result of either branch, clear the record when the action's `passed` carries a `RoundPassage` (a round closed on the way, so its files supersede, as `close_round` overwrites the key); return the `HostStep` carrying the record as read after that. A held outcome at a gate of an open set (`opened is not None`) writes nothing. Delete the `TODO: @claude` comment in the non-gate branch and the matching *"Deliberately not covered"* bullet, and state the kept-record rule under *"The rule:"*. The `TODO: @claude` at `_redispatch` (held-gate escalation, #472) stays exactly as it is.
- [ ] `host/re_entry.py`: `start_walk` clears the `RevisionFindingsStore` beside `store.clear()`, under the same `RefusalStore` lock and only when the walk started — a `Refused` start leaves it as it was, as bash's `start` writes nothing on a refusal. `current_step` returns `HostStep(step, store.read_announced(), RevisionFindingsStore(...).read())`, still taking no lock and changing nothing. Update the module docstring's rule.
- [ ] `tests/test_revision_findings.py` (new): the store on its own under `tmp_path` — absent file reads `()`; a write round-trips; `clear` removes it and a second `clear` is harmless; each malformed shape (`not valid JSON`, another `version`, a missing `files`, an extra key, a non-string entry) asserted with its exact `ValueError` text; the path for a branch carrying `/` stays one file inside `revision_findings/`; an empty branch is refused. Module docstring opens *"The rule this file exists to enforce"*.
- [ ] `tests/test_round_gates.py` and `tests/test_re_entry.py`: replace `test_a_non_round_reviewers_findings_file_is_required_but_not_kept` with cases that walk the real v4 graph (`_walker`, `_record`, `plant_review`): `ui_review`'s `FAIL` with a findings file returns `ui_writer`'s revision `Dispatch` with `revision_findings == (<that path>,)`; `answered` with a findings file at `plan_writer`'s `<ask>` keeps it; a `plan_round` that closes clears an earlier kept file; `error` recorded with `--findings` at a gate of an open set keeps nothing. Drop the *"not kept"* departure from that module's docstring; the held-gate one stays. In `test_re_entry.py`: `start_walk` removes the kept file, a refused start keeps it, and `current_step` returns it unchanged. Expected values are literals written from the bash rule above, never taken from the code's output.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_revision_findings.py`, `… test tests/test_round_gates.py` and `… test tests/test_re_entry.py` each pass, run as single foreground commands from the repository root.
- `git grep -n 'TODO: @claude' -- devscene-flow-host/src/devscene_flow_host/host/round_gates.py` shows only the held-gate marker above `_redispatch`.
- Everything the new store writes stays inside `<stateDir>/.flow_walker_state/revision_findings/`, which the walk-store test's *"everything written stays inside the state directory"* rule extends to.
