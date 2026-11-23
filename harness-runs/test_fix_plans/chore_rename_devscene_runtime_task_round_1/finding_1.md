### 1. Code review artifact carries absolute home-directory paths (gate 6a)

**Site:** `harness-runs/code_reviews/chore_rename_devscene_runtime_code_review.md` — the bullet beginning `- **Pass 0 sweep.**` (around line 15, navigation hint only), specifically the substring `` `bash <home>/Work/devscene/scripts/review-sweep.sh --repo <home>/Work/devscene-chore_rename_devscene_runtime` `` as written there with the literal home directory in place of `<home>`.

**Failing test:** none — test (gate 6a no machine paths, `scripts/check-machine-paths.sh`)

**Class:** Broken contract

**Failure:** If the Run gates phase runs gate 6a (`scripts/check-machine-paths.sh`) over this tree, then it prints the code review's Pass 0 sweep line — `./harness-runs/code_reviews/chore_rename_devscene_runtime_code_review.md:15:- **Pass 0 sweep.** ...` — and the test gate fails with `run-gates: 1 failed, 32 passed` / `- 6a no machine paths`.

**Failure as logged** (machine paths rewritten):

```
  FAIL  6a no machine paths (printed output, which is the finding, 2 s)
        ./harness-runs/code_reviews/chore_rename_devscene_runtime_code_review.md:15:- **Pass 0 sweep.** `bash <home>/Work/devscene/scripts/review-sweep.sh --repo .` exited `0` with no hits, so no hit became a finding. Half (b), the new-exported-symbol caller check, had nothing to check. The diff adds no new exported symbol: the added assignments (`_PACKAGE_DIR`, `_STDLIB_AND_SELF`, `_RELOCK`, `PACKAGES`) are re-spellings of existing private constants.
...
run-gates: 1 failed, 32 passed
  - 6a no machine paths
FAIL: test (exit 1)
== run-test-suite.sh: gate test exited 1 ==
```

**Diagnosis:** New this round (round 1, no earlier logs). Gate 6a runs `grep -rn "$HOME" .` over the working tree, excluding only `node_modules`, `dist`, `.git`, `test_run_logs`, `scratch`, the Python cache/venv directories, `harness-runs/clarifications/<sub>/` and `harness-runs/.flow_walker_state`. The code review file is tracked (`git ls-files` lists it) and not excluded, and its Pass 0 sweep bullet records the sweep command verbatim with two absolute paths: the wrapper's invocation path under the main checkout, and the `--repo` argument equal to this checkout's root. Verified in the current tree: the line is still present, and it is the only hit under `harness-runs/` outside the excluded paths (`harness-runs/.flow_walker_state` also matches but is filtered by the gate).

**Fix:**

- [ ] In `harness-runs/code_reviews/chore_rename_devscene_runtime_code_review.md`, in the `- **Pass 0 sweep.**` bullet, replace the recorded command with its repo-relative form: `` `bash scripts/review-sweep.sh --repo .` `` (the script exists in this tree at `scripts/review-sweep.sh`; the checkout root becomes `.`). Leave the rest of the sentence — the exit status, the no-hits statement and the Half (b) text — unchanged.
- [ ] Confirm no other absolute home-directory path remains in that file (a `grep -nF` for the home directory over the file prints nothing).

**Deviations from plan:** Evidence downgrade: `bash scripts/typecheck.sh` ended `PASS: typecheck`, but its own output reported two steps not run: `python-service: check: devscene-flow-host lint BLOCKED` and `python-service: check: devscene-flow-host typecheck BLOCKED` (`typecheck: python checks BLOCKED - uv is not on PATH or a package environment is not provisioned`). This unit edits only a Markdown run artifact, so those legs cover no part of the change. The Run gates phase's whole-tree run verifies them. The finding's own gate 6a (`scripts/check-machine-paths.sh`) was not run, because the Run gates phase runs it through `commands.test`. Its condition rests on a `grep -nF` for the home directory over the edited file, which printed nothing (exit 1).
