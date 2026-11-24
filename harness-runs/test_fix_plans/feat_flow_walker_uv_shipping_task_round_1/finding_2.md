### 2. Doctor Acceptance 1 fails: frozen check-id list lacks `uv` and `flow-host`

**Site:** `cli/test/doctor.test.mjs`, at the `const PRE_BRANCH_CHECK_IDS = Object.freeze([` list. Its last line is `'retrieval-dependencies', 'retrieval-model-cache', 'retrieval-index',`, near line 5669; treat the number as a navigation hint only. The list is asserted in the test `Acceptance 1: with docs.retrievalBackend absent, doctor reports what an explicit typescript does, plus three not-selected passes` (near line 5942), by the statement `assert.deepEqual([...before.keys()].sort(), [...PRE_BRANCH_CHECK_IDS, ...PYTHON_CHECK_IDS].sort(), report);`.

**Failing test:** `cli/test/doctor.test.mjs`, `Acceptance 1: with docs.retrievalBackend absent, doctor reports what an explicit typescript does, plus three not-selected passes` (its parent suite `doctor` fails with `1 subtest failed` as a consequence)

**Class:** Wrong behaviour

**Failure:** When the test suite runs `cli/test/doctor.test.mjs`, the test `Acceptance 1: with docs.retrievalBackend absent, …` fails with `failureType: 'testCodeFailure'`. The suite `doctor` then reports `error: '1 subtest failed'`.

**Failure as logged** (machine paths rewritten):

```
            not ok 89 - Acceptance 1: with docs.retrievalBackend absent, doctor reports what an explicit typescript does, plus three not-selected passes
              location: 'cli/test/doctor.test.mjs:5942:1'
              failureType: 'testCodeFailure'
              error: |-
                == checks (/private/tmp/claude-501/harness-fixture-4hw8uz)
                ...
                PASS  jq                             jq 1.8 is on PATH ...
                PASS  uv                             uv 0.12.23 is on PATH (`uv --version` printed "uv 0.12.23 (Homebrew 2026-10-03 aarch64-apple-darwin)"), so the flow walker's Python environment can be provisioned
                PASS  worktrees                      git worktree list answers with 1 checkout, ...
                ...
                Summary: 28 pass, 14 warn, 14 fail — exit 1 (14 checks failed)
                ...
                [diagnostic truncated after 40 lines]
        not ok 382 - doctor
          location: 'cli/test/doctor.test.mjs:295:1'
          failureType: 'subtestsFailed'
          error: '1 subtest failed'
```

**Diagnosis:** First round (no earlier logs). The failing assertion is the report text, which is the assertion message of the first `deepEqual`, the check-id set comparison. This branch adds two unconditional doctor checks to `CHECKS` in `cli/src/doctor/checks.ts`. `UV_CHECK` (`id: 'uv'`) sits right after `JQ_CHECK`, and the report above shows a `PASS  uv` line. `FLOW_HOST_CHECK` (`id: 'flow-host'`) sits right after `OUTER_LOOP_SCRIPTS_CHECK`. Its line falls in the truncated WARN/FAIL tail, but it is unconditional: it always returns `pass`, `warn` or `unevaluated`. The doctor therefore reports both ids. `PRE_BRANCH_CHECK_IDS` is commented `The ids \`CHECKS\` holds other than the Python backend's, frozen so an added id is visible`, and it holds neither id, so the sorted key set and the expected list differ by `flow-host` and `uv`. No other test reads `PRE_BRANCH_CHECK_IDS`. The doctor's behaviour is intended: `cli/test/doctor-flow-host.test.mjs` owns both checks. Only the frozen list is stale.

**Fix:**

- [ ] In `cli/test/doctor.test.mjs`, add `'uv'` to `PRE_BRANCH_CHECK_IDS` directly after `'jq'`, and add `'flow-host'` directly after `'outer-loop-scripts'`. That mirrors their positions in `CHECKS` in `cli/src/doctor/checks.ts`.
- [ ] Leave the rest of the test unchanged. Do not change `cli/src/doctor/checks.ts`: the per-id loop `for (const id of PRE_BRANCH_CHECK_IDS)` then also asserts that `uv` and `flow-host` report the same thing with and without `docs.retrievalBackend` written, and neither check reads that key.
