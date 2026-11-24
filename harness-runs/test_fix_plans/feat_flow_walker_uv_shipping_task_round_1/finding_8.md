### 8. (S6) forged base case fails on EEXIST

**Site:** `cli/test/watcher-stall-reset-payloads.test.mjs`, the test `(S6) a forged base: the local default-branch refs pointed at a payload tip do not pass it` (near line 518; a navigation hint only). Its first statement calls `createStallFixture`, whose `await mkdir(bin);` (after `const bin = join(rec, 'bin');`) is the statement that throws.

**Failing test:** `cli/test/watcher-stall-reset-payloads.test.mjs`, `(S6) a forged base: the local default-branch refs pointed at a payload tip do not pass it`

**Class:** Wrong behaviour

**Failure:** When the test suite runs `cli/test/watcher-stall-reset-payloads.test.mjs`, the test `(S6) a forged base: the local default-branch refs pointed at a payload tip do not pass it` fails in fixture setup with `EEXIST: file already exists, mkdir '…/watcher-test/bin'`.

**Failure as logged:**

```
        not ok 2532 - (S6) a forged base: the local default-branch refs pointed at a payload tip do not pass it
          location: 'cli/test/watcher-stall-reset-payloads.test.mjs:518:1'
          failureType: 'testCodeFailure'
          error: "EEXIST: file already exists, mkdir '/private/tmp/claude-501/harness-fixture-ybY60U/watcher-test/bin'"
          code: 'EEXIST'
          stack: |-
            async mkdir (node:internal/fs/promises:858:10)
            async createStallFixture (file://cli/test/watcher-stall-reset-payloads.test.mjs:208:3)
            async TestContext.<anonymous> (file://cli/test/watcher-stall-reset-payloads.test.mjs:519:13)
```

**Diagnosis:** First round (no earlier logs). The test fails at the same statement as Finding 3, before any assertion of its own runs. `createWatcherFixture` in `cli/test/helpers/watcher.mjs` now creates `watcher-test/bin` for its `uv` stub (its `// Choice 9.` block). `createStallFixture` then creates the same directory again with `await mkdir(bin);`, which has no `recursive` option, and that call throws `EEXIST`.

**Suspected shared cause:** likely the same cause as Finding 3 — the identical `EEXIST` at `createStallFixture` (`:208:3`) on the shared `watcher-test/bin`.

**Fix:**

- [ ] Make sure `createStallFixture` creates `bin` with `await mkdir(bin, { recursive: true });`, the change Finding 3 makes. If that change has already landed, this test needs no edit of its own.
- [ ] If the test still fails once that change is in place, its failure is a new one past fixture setup. Diagnose it at the call site the new error names, in this test's body or in `createStallFixture` after the `mkdir`, and fix it there. Do not weaken or skip the case.
