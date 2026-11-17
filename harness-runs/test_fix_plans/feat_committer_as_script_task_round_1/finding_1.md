### 1. Gate-12 full-run suite still looks for the commit wrapper's refusals in their old `echo … >&2` spelling

**Site:** `cli/test/gate12-sandbox-round-full-run.test.mjs`, at the two module-level `extract(commitOnBranchText, …)` calls that bind `COMMIT_REFUSAL_OPEN` and `COMMIT_DETACHED` (near line 136; this is only a navigation hint). These are the regexes to change:

- `/echo "(commit-on-branch\.sh: refusing to commit: )\$HR_WT_CONFIG_REFUSAL" >&2/`
- `/echo "(commit-on-branch\.sh: detached HEAD — refusing to commit)" >&2/`

**Shipped source they read:** `cli/templates/scripts/commit-on-branch.sh`. It now prints both refusals through its `fail()` helper:

- `fail 1 "commit-on-branch.sh: refusing to commit: $HR_WT_CONFIG_REFUSAL"`
- `fail 1 "commit-on-branch.sh: detached HEAD — refusing to commit"`

`fail()` writes its line with `printf '%s\n' "$line" >&2`.

**Failing test:** `cli/test/gate12-sandbox-round-full-run.test.mjs`, reported as `test/gate12-sandbox-round-full-run.test.mjs`. This is test 49, and it is the file itself.

**Failure (from the log):**

```
not ok 49 - test/gate12-sandbox-round-full-run.test.mjs
  ---
  duration_ms: 256.417333
  type: 'test'
  location: 'cli/test/gate12-sandbox-round-full-run.test.mjs:1:1'
  failureType: 'testCodeFailure'
  exitCode: 1
  signal: ~
  error: 'test failed'
  code: 'ERR_TEST_FAILURE'
```

The run's timing record lists the file as `fail 0.3 s, 1 test, 1 failed`. The whole file fails in about a quarter of a second, before any of its cases runs.

**Class:** first round. No earlier log exists, so this failure cannot be classed as new or persisting. This branch introduced the regression.

**Diagnosis:** When the module loads, the suite reads every log string it fakes out of the shipped scripts. `extract()` asserts that its regex matches (`the shipped source no longer carries …`). A failed assertion at module scope crashes the whole file, which is why the log shows a file-level `not ok` with no failing subtest.

This branch rewrote `commit-on-branch.sh`, and every refusal moved from `echo "…" >&2` to `fail 1 "…"`. The printed bytes did not change: `fail()` writes the same line to stderr. Only the source spelling changed, and these two regexes match on the spelling.

The evidence:

- `git grep` on `origin/dev` still finds `echo "commit-on-branch.sh: refusing to commit: $HR_WT_CONFIG_REFUSAL" >&2` and `echo "commit-on-branch.sh: detached HEAD — refusing to commit" >&2`.
- The branch tree has neither. It has `fail 1 "commit-on-branch.sh: refusing to commit: $HR_WT_CONFIG_REFUSAL"` and `fail 1 "commit-on-branch.sh: detached HEAD — refusing to commit"`.
- The `push-branch.sh` extractions next to them still match, because that script was not restyled.

**Fix:**

- [ ] In `cli/test/gate12-sandbox-round-full-run.test.mjs`, change the `COMMIT_REFUSAL_OPEN` regex to match the `fail` spelling: `/fail 1 "(commit-on-branch\.sh: refusing to commit: )\$HR_WT_CONFIG_REFUSAL"/`. Keep the capture group unchanged, so the extracted prefix stays byte-identical to what the wrapper prints.
- [ ] Change the `COMMIT_DETACHED` regex the same way: `/fail 1 "(commit-on-branch\.sh: detached HEAD — refusing to commit)"/`.
- [ ] Keep the `what` labels (`'commit-on-branch.sh worktree-config refusal'` and `'commit-on-branch.sh detached HEAD refusal'`). The header comment's `cli/templates/scripts/commit-on-branch.sh` bullet does not describe the source spelling, so leave it as it is.
- [ ] Leave the wrapper alone. The lines it prints are correct, and this test exists to follow them.
