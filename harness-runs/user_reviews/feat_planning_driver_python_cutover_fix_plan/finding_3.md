### 3. Two tree guards name a Python test that a plugin or cli unit's single-file command cannot run

**File:** `devscene.config.json` (`treeGuards`) — `"test": "tests/test_driver_return_fields.py"`. There are two entries: one covers `"plugin/schemas/**"` and the other covers `"cli/templates/scripts/flows/task_plan_writing.graph.json"`.
**Class:** Wrong action from operative text
**Failure:** If a plugin-layer or cli-layer unit edits a file under `plugin/schemas/` or edits `cli/templates/scripts/flows/task_plan_writing.graph.json`, then `unit_loop_core.md` → `## The test-run rule` point 7 selects the guard `tests/test_driver_return_fields.py`. The unit runs it through its own single-file command, `npm test --workspace cli -- tests/test_driver_return_fields.py`, as `.claude/context/conventions.md` → *"A unit's own verification runs the one test file it created or edited"* gives it. No such file exists under `cli/`, so the guard run fails on a change that broke nothing.

**Problem.** Commit `1ec61a29` (architecture review Finding 4) added the two entries. Each `treeGuards[].test` value is passed verbatim to the dispatched layer's single-file command (`docs/config.md` → the `treeGuards` row). The two `covers` globs match only plugin-layer and cli-layer paths, and those layers' units run tests through npm. The path `tests/test_driver_return_fields.py` resolves only under `devscene-flow-host/`, through `bash scripts/python-service.sh --package devscene-flow-host test …`.

The test itself stays. `devscene-flow-host/tests/test_driver_return_fields.py` remains part of the flow host's `pytest` suite and still runs at Run gates (gate 13).

**Fix:**

- [ ] In `devscene.config.json` → `treeGuards`, delete exactly these two objects and leave every other entry and the array order as they are:

  ```json
  {
    "test": "tests/test_driver_return_fields.py",
    "covers": "plugin/schemas/**"
  },
  {
    "test": "tests/test_driver_return_fields.py",
    "covers": "cli/templates/scripts/flows/task_plan_writing.graph.json"
  },
  ```

  Keep the JSON valid. The entry before them (`tests/test_layers.py` covering `devscene-flow-host/pyproject.toml`) and the entry after them (`test/python-packages-staged.test.mjs` covering `cli/src/flowHost/**`) keep their own commas correct.
- [ ] Update whatever describes those entries. A `git grep -n "test_driver_return_fields"` over the tracked tree, excluding `harness-runs/`, finds no document that describes the two guard entries. The only hits are:
  - `devscene.config.json`, which this fix edits.
  - The `test_planning_driver_walk.py` docstring's pointer to the test.
  - `docs/structured-agent-returns.md`'s **Decision.** paragraph, which describes what the test holds and does not mention a guard.

  So no prose edit is owed. Re-run that grep after the edit to confirm, and if a tracked document does call `test_driver_return_fields.py` a tree guard, change that sentence to say the test runs with the flow host's suite at Run gates. Leave `docs/structured-agent-returns.md`'s *"A schema-only edit triggers that suite through its own `devscene.config.json` → `treeGuards` entry, `plugin/schemas/**`"* unchanged: it describes `cli/test/agent-return-schemas.test.mjs`'s guard, which stays.
- Do not edit `harness-runs/architecture_branch_reviews/feat_planning_driver_python_cutover_arch_review.md`. It is a point-in-time run record.
