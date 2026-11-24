### 12. (S4) config.worktree case fails on EEXIST

**Site:** `cli/test/watcher-stall-reset-payloads.test.mjs`, the test `(S4) a .git/config.worktree planted in the clone, carrying core.fsmonitor, is refused before the reset` (near line 605; a navigation hint only). Its first statement calls `createStallFixture`, whose `await mkdir(bin);` (after `const bin = join(rec, 'bin');`) is the statement that throws.

**Failing test:** `cli/test/watcher-stall-reset-payloads.test.mjs`, `(S4) a .git/config.worktree planted in the clone, carrying core.fsmonitor, is refused before the reset`

**Class:** Wrong behaviour

**Failure:** When the test suite runs `cli/test/watcher-stall-reset-payloads.test.mjs`, the test `(S4) a .git/config.worktree planted in the clone, carrying core.fsmonitor, is refused before the reset` fails in fixture setup with `EEXIST: file already exists, mkdir '…/watcher-test/bin'`.

**Failure as logged:**

```
        not ok 2536 - (S4) a .git/config.worktree planted in the clone, carrying core.fsmonitor, is refused before the reset
          location: 'cli/test/watcher-stall-reset-payloads.test.mjs:605:1'
          failureType: 'testCodeFailure'
          error: "EEXIST: file already exists, mkdir '/private/tmp/claude-501/harness-fixture-IrXIm5/watcher-test/bin'"
          code: 'EEXIST'
          stack: |-
            async mkdir (node:internal/fs/promises:858:10)
            async createStallFixture (file://cli/test/watcher-stall-reset-payloads.test.mjs:208:3)
            async TestContext.<anonymous> (file://cli/test/watcher-stall-reset-payloads.test.mjs:606:13)
```

**Diagnosis:** First round (no earlier logs). The test fails at the same statement as Finding 3, before any assertion of its own runs. `createWatcherFixture` in `cli/test/helpers/watcher.mjs` now creates `watcher-test/bin` for its `uv` stub (its `// Choice 9.` block). `createStallFixture` then creates the same directory again with `await mkdir(bin);`, which has no `recursive` option, and that call throws `EEXIST`.

**Suspected shared cause:** likely the same cause as Finding 3 — the identical `EEXIST` at `createStallFixture` (`:208:3`) on the shared `watcher-test/bin`.

**Fix:**

- [ ] Make sure `createStallFixture` creates `bin` with `await mkdir(bin, { recursive: true });`, the change Finding 3 makes. If that change has already landed, this test needs no edit of its own.
- [ ] If the test still fails once that change is in place, its failure is a new one past fixture setup. Diagnose it at the call site the new error names, in this test's body or in `createStallFixture` after the `mkdir`, and fix it there. Do not weaken or skip the case.
