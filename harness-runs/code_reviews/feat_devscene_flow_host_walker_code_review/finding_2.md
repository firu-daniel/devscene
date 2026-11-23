### 2. `read_config` accepts a configuration with no `defaultBranch`, which every bash reader it ports treats as unresolvable

**File:** `devscene-flow-host/src/devscene_flow_host/records/config.py` (`read_config`) — "Every other key, including `defaultBranch`, which `hr_config_load` requires and this reader"
**Class:** Broken contract
**Failure:** If `open_walker` runs in a repository whose `devscene.config.json` has no `defaultBranch` (or `"defaultBranch": ""`, or `null`), then it returns a walker, and `HarnessPredicateHost.answer("phase_qa_off", …)` returns the configured flag. `flow-walker.sh` stops at start-up on the same repository with `fault "cannot resolve stateDir from …/devscene.config.json"`, because `hr_state_dir` returns `2`, and `fw_phase_on` returns `2` (unresolvable) as well.

The host ports `hr_state_dir` and `hr_phase_enabled` (`cli/templates/scripts/lib/harness-run-lib.sh`). Both go through `hr_config_load`, which returns `2` (*"unresolvable"*) unless `defaultBranch` is emitted non-empty: `hr_cfg_scalar_var "defaultBranch" || return 2`. `read_config` reads only `stateDir` and `phases`, and its docstring lists `defaultBranch` under *"Deliberately not checked"*. So this port answers where the reader it mirrors refuses.

This was measured, not read. The probe `harness-runs/scratch/probe_default_branch.py` ran through `bash scripts/python-service.sh --package devscene-flow-host probe harness-runs/scratch/probe_default_branch.py` and printed:

- `no defaultBranch: bash['phase_qa_status=2\nstate_dir_status=2 state_dir='] python[state_dir='devscene' qa=True]`
- `defaultBranch empty: bash['phase_qa_status=2\nstate_dir_status=2 state_dir='] python[state_dir='devscene' qa=True]`
- `with defaultBranch: bash['phase_qa_status=0\nstate_dir_status=0 state_dir=devscene'] python[state_dir='devscene' qa=True]` (control)

The task prompt excludes nothing here. A docstring's *"Deliberately not checked"* line and the task plan's rule are not an exclusion basis (`harness-runs/lessons.md` → `## Ports and parallel implementations`, first entry). The package already settles how an unresolvable configuration is reported: as a `RecordError`, the same way `read_config` reports a configuration that is not JSON. So the fix adds one more refusal of that shape. It does not add a new channel.

**Fix.** In `devscene-flow-host/src/devscene_flow_host/records/config.py` → `read_config`, directly after the `not a JSON object` check, refuse the shapes `hr_config_load` does not emit. Those shapes are absent, `null`, `""` and the string `"null"`. Any other value is emitted through `tostring`, so a non-null value passes:

```python
    if document.get("defaultBranch") in (None, "", "null"):
        raise RecordError(f"{path}: no defaultBranch")
```

In the module docstring, change the rule's first sentence to say that `read_config` reads `stateDir` and `phases` and refuses a configuration with no `defaultBranch`, as `hr_config_load` does. Drop `defaultBranch` from the *"Deliberately not checked:"* bullet, which becomes *"Every other key."*

In `devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Records.**, change *"reads `devscene.config.json` for `stateDir` and `phases` only"* to *"reads `devscene.config.json` for `stateDir` and `phases` only, and refuses one with no `defaultBranch` as `hr_config_load` does"*.

Every planted configuration that omits `defaultBranch` must now carry one:

- `devscene-flow-host/tests/test_config.py`: each `_plant(tmp_path, "{…}")` text gets `"defaultBranch": "main"`. For example, `"{}"` becomes `'{"defaultBranch": "main"}'`, and `'{"stateDir": "/"}'` becomes `'{"defaultBranch": "main", "stateDir": "/"}'`. Do not change `test_a_top_level_that_is_not_an_object_is_a_record_error` (`"[]"`) or the two not-JSON cases. Add a parametrized `test_a_missing_default_branch_is_a_record_error` over `"{}"`, `'{"defaultBranch": ""}'` and `'{"defaultBranch": null}'`, each asserting `str(error.value) == f"{tmp_path / 'devscene.config.json'}: no defaultBranch"`. In `test_a_state_dir_that_is_not_a_string_is_a_record_error`, plant `'{"defaultBranch": "main", "stateDir": 3}'`. Also add `defaultBranch` to the planted texts Finding 1 adds, if that fix has landed.
- `devscene-flow-host/tests/test_predicates.py` → `_plant_config`: `json.dumps({"defaultBranch": "main", "stateDir": "state/", "phases": phases})`.
- `devscene-flow-host/tests/test_walking.py` → `_plant`: `json.dumps({"defaultBranch": "main", "stateDir": "state", "phases": phases})`.

Run the three test files this fix edits with `bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py`: `tests/test_config.py`, `tests/test_predicates.py` and `tests/test_walking.py`.
