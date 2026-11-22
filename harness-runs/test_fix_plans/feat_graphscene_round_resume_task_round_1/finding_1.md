### 1. Remove the machine paths from the code review's Pass 0 line

**Site:** `harness-runs/code_reviews/feat_graphscene_round_resume_code_review.md` → the paragraph beginning `**Pass 0.** (a) `, the backticked substring `` `bash `` … `/scripts/review-sweep.sh --repo ` … `` ` exited `0` `` (line 9 at writing, navigation hint only).

**Failing test:** none — test (gate 6a `no machine paths`, run by `scripts/run-gates.sh` through `scripts/check-machine-paths.sh`)

**Class:** Wrong behaviour

**Failure:** If the running program `scripts/run-gates.sh` runs gate 6a `no machine paths` over this tree, then it prints the hit `./harness-runs/code_reviews/feat_graphscene_round_resume_code_review.md:9:**Pass 0.** (a) `bash <home>/Work/devscene/scripts/review-sweep.sh --repo .` exited `0`: …` and grades the gate `FAIL`, so the test gate exits 1.

**Failure quoted from the log** (machine paths rewritten: the home directory as `<home>`; the second path is this run copy's root, whose repo-relative form is `.`):

```
  FAIL  6a no machine paths (printed output, which is the finding, 2 s)
        ./harness-runs/code_reviews/feat_graphscene_round_resume_code_review.md:9:**Pass 0.** (a) `bash <home>/Work/devscene/scripts/review-sweep.sh --repo .` exited `0`: 0 hits, so 0 findings. The sweep document came from `origin/dev`, because this run copy has no local `dev` ref. (b) The diff adds two non-test definitions under `graphscene/src`. `RoundResume` has call sites in `engine/walker.py`, `facade/__init__.py` and `__init__.py`. `enter_round` has its call site in `engine/walker.py` → `Walker.start`. The search covered every `layers[].path` scope, and neither symbol is dead.
```

```
run-gates: 1 failed, 32 passed
  - 6a no machine paths
FAIL: test (exit 1)
```

**Diagnosis.** New this round (no earlier round's log). `scripts/check-machine-paths.sh` runs `grep -rn "$HOME" .` over the working directory, excluding only `node_modules`, `dist`, `.git`, `test_run_logs`, `scratch`, the Python caches, files below `harness-runs/clarifications/<dir>/` and `harness-runs/.flow_walker_state`; `harness-runs/code_reviews/` is covered. Verified in the current tree: the code review's `**Pass 0.**` paragraph still quotes the sweep command literally, with the main checkout's absolute script path and the run copy's absolute root as its `--repo` argument — both under the home directory. It is the only hit the gate printed. `.claude/context/conventions.md` → `## The testing bar` makes this binding: *"nothing in this tree may name a location on the machine that wrote it"*. The rest of the review (its findings, readiness list and verdict) is correct and unaffected.

**Fix.** Edit only that backticked command in `harness-runs/code_reviews/feat_graphscene_round_resume_code_review.md`, replacing both absolute paths with the placeholder form the sweep design uses elsewhere in `harness-runs/code_reviews/` (`bash <MAIN_REPO>/<scripts_dir>/review-sweep.sh --repo <repo_root>`), so that the sentence reads:

> **Pass 0.** (a) `bash <MAIN_REPO>/scripts/review-sweep.sh --repo <repo_root>` exited `0`: 0 hits, so 0 findings. …

- [ ] Replace the two absolute paths in that one command; leave every other word of the paragraph and the file unchanged.
- [ ] Confirm with `grep -rnF` of the home directory over `harness-runs/code_reviews/feat_graphscene_round_resume_code_review.md` that the file no longer names it.

Do not add an exclusion to `scripts/check-machine-paths.sh` or otherwise weaken gate 6a: the review is a committed artifact, and the gate is right to refuse it.

- **Deviations from plan:** The row-`G.4` check ran no single-file test: the finding names no test file (`none — test`, gate 6a), and a gate script is never run by the unit. Took the fix-site fallback instead. Before the edit, the fix site still held the fix-free text: `grep -rnF` of the home directory over the code review matched line 9's `**Pass 0.**` paragraph. After the edit, the same `grep -rnF` returned no match (exit 1). Gate 6a itself (`scripts/check-machine-paths.sh`, reached through `commands.test` → `scripts/run-gates.sh`) was not run; that is deferred to the Run gates phase. `commands.typecheck` (`bash scripts/typecheck.sh`) ran from the repository root and printed `PASS: typecheck`.
