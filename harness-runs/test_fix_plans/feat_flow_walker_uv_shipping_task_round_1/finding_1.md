### 1. Tracked run artifacts carry home-directory npm-cache paths (gate 6a)

**Site:**
- `harness-runs/code_reviews/feat_flow_walker_uv_shipping_code_review/finding_2.md`: the two bullets beginning `- Evidence downgrade — tree guard` and `- General-layer dispatch:`. Each holds the substring `` `npm error path <home>/.npm/_cacache/tmp/…` `` with the literal home directory where `<home>` is written here. The lines are near 38 and 39; treat those numbers as a navigation hint only.
- `harness-runs/task_plans/feat_flow_walker_uv_shipping/task_1_plan.md`: the bullet beginning `- **Deviations from plan:** Evidence downgrade on the first Verification bullet.` It holds the substring `` `npm error path <home>/.npm/_cacache/tmp/bd9bc39b` ``, again with the literal home directory. The line is near 46.

**Failing test:** none — test (gate 6a no machine paths, `scripts/check-machine-paths.sh`)

**Class:** Broken contract

**Failure:** When the Run gates phase runs gate 6a (`scripts/check-machine-paths.sh`) over this tree, it prints those three lines. The test gate then fails with `run-gates: 2 failed, 34 passed` / `- 6a no machine paths`.

**Failure as logged** (machine paths rewritten, long lines cut with `…`):

```
  FAIL  6a no machine paths (printed output, which is the finding, 2 s)
        ./harness-runs/code_reviews/feat_flow_walker_uv_shipping_code_review/finding_2.md:38:- Evidence downgrade — tree guard `test/python-packages-staged.test.mjs` … fails with `npm error code EPERM` / `npm error path <home>/.npm/_cacache/tmp/c5d16fab`, the run's sandbox refusing npm's cache write outside the writable set. …
        ./harness-runs/code_reviews/feat_flow_walker_uv_shipping_code_review/finding_2.md:39:- General-layer dispatch: … fails `npm pack lists the staged Python files` with `npm error code EPERM` / `npm error path <home>/.npm/_cacache/tmp/b7ed5c89`, the sandbox refusing npm's cache write; …
        ./harness-runs/task_plans/feat_flow_walker_uv_shipping/task_1_plan.md:46:- **Deviations from plan:** Evidence downgrade on the first Verification bullet. … `npm error code EPERM` / `npm error syscall open` / `npm error path <home>/.npm/_cacache/tmp/bd9bc39b`. That path is outside the run's writable set, which admits only `~/.npm/_logs`. …
```

**Diagnosis:** First round (no earlier logs). Gate 6a runs `grep -rn "$HOME" .` over the working tree. It excludes only `node_modules`, `dist`, `.git`, `test_run_logs`, `scratch`, the Python cache and venv directories, `harness-runs/clarifications/<sub>/` and `harness-runs/.flow_walker_state`. Both files are tracked (`git ls-files` lists them), neither is excluded, and each quotes an npm error line with the absolute home-directory path to npm's cache. The current tree was checked: a fixed-string grep for the home directory still matches each of the three lines, once per line.

**Fix:**

- [ ] In `harness-runs/code_reviews/feat_flow_walker_uv_shipping_code_review/finding_2.md`, in both bullets named above, replace the literal home directory in `npm error path <home>/.npm/_cacache/tmp/<hex>` with `~`, giving `npm error path ~/.npm/_cacache/tmp/c5d16fab` and `npm error path ~/.npm/_cacache/tmp/b7ed5c89`. Leave every other word unchanged.
- [ ] In `harness-runs/task_plans/feat_flow_walker_uv_shipping/task_1_plan.md`, in the `**Deviations from plan:**` bullet, make the same replacement, giving `npm error path ~/.npm/_cacache/tmp/bd9bc39b`. That matches the `~/.npm/_logs` spelling the same sentence already uses.
- [ ] Confirm that a fixed-string grep for the home directory over both files prints nothing.
