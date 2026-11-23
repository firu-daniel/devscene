### Task 2 — Read `devscene.config.json` into `HarnessConfig` in `records`, with `RecordError`

**Goal:** Give the package its one reader of `devscene.config.json`. It reads two keys, `stateDir` and `phases`, into a frozen `HarnessConfig`, and introduces the package's one anticipated-failure type, `RecordError`. Each key is read as the bash walker's readers read it: `hr_config_dir` / `hr_state_dir` and `hr_phase_enabled` in `cli/templates/scripts/lib/harness-run-lib.sh`.

**Depends on:** Task 1, which creates `devscene-flow-host/src/devscene_flow_host/records/` with its `__init__.py`. Under that package's rule, this task's modules import the standard library and `devscene_flow_host.records` only, never `graphscene`.

**Where this layer stops.** This task reads values and decides nothing. What a phase flag *means* to the walk — that `phase_<p>_off` is `True` when the phase is off — is **Task 4's** (`HarnessPredicateHost`). Where the walk's state lives under `state_dir` is **Task 5's**. Turning a `RecordError` into an exit status belongs to the `commands` layer, which has no module on this branch.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/errors.py` (new)
- `devscene-flow-host/src/devscene_flow_host/records/config.py` (new)
- `devscene-flow-host/tests/test_config.py` (new)

**Work:**

- [ ] **`records/errors.py`**: `class RecordError(Exception)`. Its docstring states the rule: `RecordError` is the one anticipated failure of reading a repository record, a record that is absent or cannot be read as the harness writes it, and its message is one line naming the file and the cause. An `OSError` other than a missing file is not wrapped: it propagates unchanged. Which exit status a `RecordError` becomes is the caller's.
- [ ] **`records/config.py` — the constants and the value.** `CONFIG_FILENAME: Final = "devscene.config.json"`. `DEFAULT_STATE_DIR: Final = "devscene"`, the schema's default `devscene/` normalised as `hr_state_dir` normalises it. `PHASES: Final = ("parity", "qa", "docs")`, the phases `hr_phase_enabled` accepts. And `@dataclass(frozen=True) class HarnessConfig` with `state_dir: str`, repo-relative with no trailing `/`, and `phases: Mapping[str, bool | None]`. `phases` holds exactly the three `PHASES` keys in that order: `True` on, `False` off, `None` unresolvable. Build it as a `types.MappingProxyType` over a fresh `dict`.
- [ ] **`read_config(repo_root: Path) -> HarnessConfig`**, reading `repo_root / CONFIG_FILENAME` and those two keys only. The module docstring states that rule and its *"Deliberately not checked:"* list: every other key, including `defaultBranch`, which `hr_config_load` requires and this reader never reads; and whether `stateDir` is a safe repo-relative path, which is the schema's. Raise `RecordError` with these exact messages, where `<path>` is `str(repo_root / CONFIG_FILENAME)`:
  - the file does not exist: `no devscene.config.json at <repo_root>`
  - the bytes are not UTF-8, or not JSON: `<path>: not valid JSON`
  - the top level is not an object: `<path>: not a JSON object`
  - `stateDir` is present and not a string: `<path>: stateDir is not a string`
- [ ] **The two keys' meanings**, each the bash reader's:
  - `stateDir` (`hr_config_dir`): absent → `DEFAULT_STATE_DIR`; otherwise strip every trailing `/`; if empty after that → `DEFAULT_STATE_DIR`.
  - `phases` (`hr_phase_enabled`): absent → all three `False`. An object → for each phase, an absent key → `False`, a JSON boolean → itself, any other value → `None`. Present but not an object → all three `None`. The schema defaults every phase to off, so absent is off, never unresolvable.
- [ ] **`tests/test_config.py`.** Its docstring opens *"The rule this file exists to enforce"*. Every case writes its configuration under `tmp_path` and asserts the exact value or the exact `RecordError` message, hand-written from the rules above. One case per rule:
  - a full configuration: `stateDir` `"harness-runs/"` → `"harness-runs"`, and `phases` `{"parity": true, "qa": false}` → `parity` `True`, `qa` `False`, `docs` `False`
  - `stateDir` absent, `"/"` and `"a//"` → `"devscene"`, `"devscene"`, `"a"`
  - `phases` absent → all `False`; `phases` `{"qa": "yes"}` → `qa` `None`, the others `False`; `phases` `[]` → all `None`
  - each of the four `RecordError` messages, with `pytest.raises(RecordError)` and an equality check on `str(error)`
  - `HarnessConfig` is frozen and `phases` cannot be assigned to

**Verification:**

- Run this task's own test file from the repository root, as one foreground command: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_config.py`. Every case passes.
- `commands.typecheck` exits zero.
- `grep -n "graphscene" devscene-flow-host/src/devscene_flow_host/records/*.py` finds no import line: the `records` layer never imports it.
- Every expected value in `tests/test_config.py` is a literal written from this file's rules, never taken from `read_config`'s output.
