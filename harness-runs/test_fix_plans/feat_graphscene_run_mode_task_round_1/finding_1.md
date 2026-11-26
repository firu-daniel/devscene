### 1. Bound the full-run grade suite's driver call so a hang fails one case instead of the whole file

**Site:** `cli/test/gate12-sandbox-round-full-run.test.mjs` → `async function grade(fixture)`, the line `const result = await runRound(fixture, ['grade', '--repo', GATE12_SLUG, '--full-run', B]);` (around line 406, navigation hint only).

**Failing test:** `cli/test/gate12-sandbox-round-full-run.test.mjs` — `test/gate12-sandbox-round-full-run.test.mjs` (the file-level test, as the log reports it).

**Class:** Wrong behaviour

**Failure:** If the running program runs gate 4 (`npm test` in `cli`), then `test/gate12-sandbox-round-full-run.test.mjs` fails with `failureType: 'testTimeoutFailure'` and `error: 'test timed out after 1800000ms'`, cancelling the file and failing the test gate.

**Failure as logged:**

```
  FAIL  4 npm test (exit 1, 2411 s)
        not ok 58 - test/gate12-sandbox-round-full-run.test.mjs
          ---
          duration_ms: 1800002.234958
          type: 'test'
          location: 'cli/test/gate12-sandbox-round-full-run.test.mjs:1:1'
          failureType: 'testTimeoutFailure'
          error: 'test timed out after 1800000ms'
          code: 'ERR_TEST_FAILURE'
```

and, from the slowest-files table:

```
  1856.6 s  test/gate12-sandbox-round-full-run.test.mjs  (9 tests, 1 failed)
```

**Diagnosis:**

- Class: *new this round* — this is round 1 and no earlier log was given.
- The suite has ~21 top-level cases; the timing table records 9 tests and 1856.6 s for the file, i.e. roughly eight cases finished in about 56 s and then one case blocked until the runner's 1800000 ms file timeout killed the file. The log does not name which case blocked, because the runner reports only the file-level timeout.
- This branch does not touch this suite or anything it exercises: `git diff --stat origin/dev...HEAD` lists only `graphscene/` files and `harness-runs/` artifacts — no change under `cli/test/`, `cli/test/helpers/gate12-round.mjs`, `scripts/gate12-sandbox-round.sh`, `scripts/lib/gate12-sandbox-round/` or `cli/templates/scripts/`. Its sibling suites (`gate12-sandbox-round-grade`, `-default-branch`, `-plant`, `-cli`, `-teardown`) all passed in the same run. The whole run was also unusually slow (`test/doctor.test.mjs  (1 tests, 0 failed)` took 590.8 s), so a host stall during one `grade --full-run` child is the likeliest trigger; the root cause of the block is not established from the log.
- What *is* a defect in the tree: `grade()` calls `runRound` with no `timeoutMs`. `cli/test/helpers/gate12-round.mjs` → `runRound` documents that "without it the call is unbounded", and `cli/test/helpers/fixture.mjs`'s module header, choice 6, states that a `--test-timeout` expiry kills the file's process and leaves the child's process group running, and that "`timeoutMs` below the test timeout is the half that reaps". So one stuck driver call costs the full 30-minute file timeout, cancels every remaining case in the file, leaves a detached `bash` group behind, and the report names no case and carries none of the driver's output. The sibling suite `cli/test/gate12-sandbox-round-default-branch.test.mjs` already bounds every `runRound` call with `timeoutMs: ROUND_BOUND_MS`, where `const ROUND_BOUND_MS = scaleBound(120_000);` and `scaleBound` comes from `./helpers/timing.mjs`.

**Fix:**

- [ ] In `cli/test/gate12-sandbox-round-full-run.test.mjs`, import `scaleBound` from `./helpers/timing.mjs` and declare a bound the way `cli/test/gate12-sandbox-round-default-branch.test.mjs` does (`const ROUND_BOUND_MS = scaleBound(120_000);`).
- [ ] In `grade(fixture)`, pass that bound to the driver call: `runRound(fixture, ['grade', '--repo', GATE12_SLUG, '--full-run', B], { timeoutMs: ROUND_BOUND_MS })`. A blocked grade then rejects with `runBash timed out after … ms: <argv>`, fails only its own case, and its process group is reaped.
- [ ] Keep every assertion and every case unchanged: no case is deleted, skipped or weakened.
- [ ] This finding's fix stays inside `cli/test/` (the `cli` layer). Do not edit `scripts/lib/gate12-sandbox-round/` or any other `general`-layer file under this finding. If the named file shows a case that still blocks or now fails on the bound, return it as this unit's blocker. Name the case and quote the `runBash timed out after … ms` rejection, along with the driver output it carries. Do not fix the cause outside `cli`.
