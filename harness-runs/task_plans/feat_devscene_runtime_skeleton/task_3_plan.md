### Task 3 — Add gate 13's legs 13h–13j, the nightly `uv audit` step for the new lock, and the boundary test's tree-guard entry

**Goal:** Hold `devscene-runtime/` to gate 13's bar in every Run gates round, audit its lock nightly beside the other two, and register its tree-reading boundary test as a tree guard, so a later unit that changes the package's source runs it.

**Depends on:** Task 1, which creates `devscene-runtime/tests/test_boundary.py` (it scans every module under `devscene-runtime/src/devscene_runtime/` and reads `devscene-runtime/pyproject.toml` for the declared dependencies), and Task 2, which adds the wrapper row `devscene-runtime` — so `bash scripts/python-service.sh --package devscene-runtime lint|typecheck|test` exits `0` pass, `1` failure, `3` not provisioned — and `devscene-runtime/uv.lock`. This task calls those three commands and audits that lock; it changes neither.

**Where this task stops.** Task 5 documents the legs and the audited lock in `docs/development.md`; this task writes no prose outside the two files' own comments. `commands.typecheck` needs no edit: `scripts/typecheck.sh` runs `bash scripts/python-service.sh check`, which iterates the table Task 2 extended.

### Targets

- `scripts/run-gates.sh` — three units and the header.
- `.github/workflows/supply-chain.yml` — one `uv-audit` step and the header.
- `devscene.config.json` — two `treeGuards` entries.

**Work:**

- [ ] `scripts/run-gates.sh`: add three `run_unit` arms after `13g`, on its exact shape — `13h) gate_header 13 "Python packages"; python_gate "13h devscene-runtime lint" noskip bash scripts/python-service.sh --package devscene-runtime lint ;;`, then `13i … typecheck` and `13j … tests` (`… test`) the same way — and add `13h 13i 13j` after `13g` in the `gr_run_round run_unit …` list. None depends on gate 2a's build. In the header's gate 13 sentence, add *"and the DevScene runtime's legs 13h, 13i and 13j"*.
- [ ] `.github/workflows/supply-chain.yml`: in the `uv-audit` job, after the `graphscene` step, add `- working-directory: devscene-runtime` with `run: uv audit --preview-features audit-command --frozen`, byte for byte the two existing steps' form; and name `devscene-runtime/uv.lock` in the header's first paragraph beside the other two locks. No other job, action pin or permission changes.
- [ ] `devscene.config.json` → `treeGuards`: append `{"test": "tests/test_boundary.py", "covers": "devscene-runtime/src/devscene_runtime/**"}` and `{"test": "tests/test_boundary.py", "covers": "devscene-runtime/pyproject.toml"}`, after the two `graphscene` entries and in their shape. The `test` value is relative to the package directory, as the `graphscene` entries' `tests/test_layers.py` is. Change no other key.

**Verification:**

- Read the three new arms against `13e`–`13g`: same `gate_header`, same `python_gate … noskip` call, only the leg id, label and `--package` value differ; the `gr_run_round` list carries each new id exactly once, after `13g` and before `14a`. Gate 16 grades the script's parse in the Run gates round.
- `git diff .github/workflows/supply-chain.yml` shows only the new step and the header sentence; the new step's `run` line is identical to the two existing ones.
- `devscene.config.json` still parses as JSON (`jq . devscene.config.json` exits `0`), and `git diff devscene.config.json` touches only `treeGuards`.
