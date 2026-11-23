### 1. `read_config` refuses a phase that the bash walker reads as off: a JSON `null` value, a non-object `phases`, and a `null` `stateDir`

**File:** `devscene-flow-host/src/devscene_flow_host/records/config.py` (`_phases`, `_phase`, `_state_dir`) — "resolved = {phase: None for phase in PHASES}"
**Class:** Broken contract
**Failure:** If `HarnessPredicateHost` answers `phase_qa_off` in a repository whose `devscene.config.json` carries `"phases": {"qa": null}` (or `"phases": null`, `[]` or `"x"`), then it returns `None` and `Walker.next` refuses at `ui_writer`. `flow-walker.sh` → `eval_skip` skips that node, because `fw_phase_on` returns `1` (off) there.

The story plan's decision is that the predicate host *"mirrors the bash walker's readers, construct for construct"*. `config.py`'s docstring says `phases` is read *"as `hr_phase_enabled`"* reads it. The README says `read_config` reads `stateDir` and `phases` *"as `hr_state_dir` and `hr_phase_enabled` read them"*. That does not hold for three inputs.

`hr_config_load` (`cli/templates/scripts/lib/harness-run-lib.sh`) emits nothing for a key whose value is JSON `null`. Its comment says: *"`null`, the string `"null"` and `""` are not emitted at all, so a reader reports them as 'not set'"*. Its `try (.phases.<p> | …) catch null` gives `null` for a phase whose parent `phases` is not an object. `hr_phase_enabled` then returns `1`, which means off, for an unset flag. `hr_state_dir` falls back to `devscene`. The port handles the same three inputs differently:

| Config | `fw_phase_on … qa` / `hr_state_dir` | `read_config` |
|---|---|---|
| `"phases": {"qa": null}` | `1` (off) | `qa=None` (refused) |
| `"phases": null` | `1` (off) | `qa=None` |
| `"phases": []` | `1` (off) | `qa=None` |
| `"phases": "x"` | `1` (off) | `qa=None` |
| `"stateDir": null` | `devscene` | `RecordError(...: stateDir is not a string)` |
| `"phases": {"qa": "yes"}` (control) | `2` (unresolvable) | `qa=None` (agrees) |

This was measured, not read. The probe `harness-runs/scratch/probe_phase_null.py` ran through `bash scripts/python-service.sh --package devscene-flow-host probe harness-runs/scratch/probe_phase_null.py`. For each config planted in a temporary directory, it sourced `harness-run-lib.sh` and `flow-walker-gates.sh`, called `fw_phase_on <root> qa` and `hr_state_dir <root>`, and called `read_config`. Its output was the table above, for example `qa null: bash['phase_qa_status=1\nstate_dir_status=0 state_dir=devscene'] python[state_dir='devscene' qa=None]`.

Nothing in the task prompt excludes this divergence. The task-plan rule *"Present but not an object → all three `None`"* (`task_2_plan.md`) and the test that pins it are not an exclusion basis (`harness-runs/lessons.md` → `## Ports and parallel implementations`, first entry).

**Fix.** In `devscene-flow-host/src/devscene_flow_host/records/config.py`, read a JSON `null` as absent and a non-object `phases` as no phases set:

```python
def _state_dir(document: dict[str, object], path: Path) -> str:
    value = document.get("stateDir")
    if value is None:
        return DEFAULT_STATE_DIR
    if not isinstance(value, str):
        raise RecordError(f"{path}: stateDir is not a string")
    return value.rstrip("/") or DEFAULT_STATE_DIR


def _phases(document: dict[str, object]) -> Mapping[str, bool | None]:
    # `hr_config_load` reads a `null` value as not set and a phase under a `phases` that is not an
    # object as `null`, and `hr_phase_enabled` reads not set as off; the schema defaults every
    # phase to off.
    value = document.get("phases")
    phases: dict[str, object] = value if isinstance(value, dict) else {}
    return MappingProxyType({phase: _phase(phases, phase) for phase in PHASES})


def _phase(phases: dict[str, object], phase: str) -> bool | None:
    value = phases.get(phase)
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return None
```

Leave the `HarnessConfig` docstring and the module docstring's rule as they are. They become true.

In `devscene-flow-host/tests/test_config.py`:

- Replace `test_phases_that_are_not_an_object_are_all_unresolvable` with a parametrized `test_phases_that_are_not_an_object_are_all_off` over the planted texts `'{"phases": []}'`, `'{"phases": null}'` and `'{"phases": "x"}'`. Each asserts `dict(config.phases) == {"parity": False, "qa": False, "docs": False}`.
- Add `test_a_null_phase_is_off`: `'{"phases": {"qa": null}}'` → `{"parity": False, "qa": False, "docs": False}`.
- Add `test_a_null_state_dir_takes_the_default`: `'{"stateDir": null}'` → `state_dir == "devscene"`.
- Keep `test_a_non_boolean_phase_is_unresolvable` (`"yes"` → `None`) and `test_a_state_dir_that_is_not_a_string_is_a_record_error` (`3`) unchanged. Both already agree with the bash readers on what they assert.

Run `devscene-flow-host/tests/test_config.py`, the one test file this fix edits, with `bash scripts/python-service.sh --package devscene-flow-host test tests/test_config.py`.
