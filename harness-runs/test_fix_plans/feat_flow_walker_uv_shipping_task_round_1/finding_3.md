### 3. Stall fixture's `mkdir(bin)` collides with the shared fixture's uv-stub directory

**Site:** `cli/test/watcher-stall-reset-payloads.test.mjs`, in `async function createStallFixture(t, { job = false } = {})`, on the statement `await mkdir(bin);`, which follows `const bin = join(rec, 'bin');` near line 208; treat the number as a navigation hint only. The collision partner is `cli/test/helpers/watcher.mjs`, in `createWatcherFixture`, at the block commented `// Choice 9.`: `const uvBin = join(recorderDir, 'bin');` / `await mkdir(uvBin, { recursive: true });`.

**Failing test:** `cli/test/watcher-stall-reset-payloads.test.mjs`, `an honest hung run resumes: the edit discarded, the branch unmoved, the note written`

**Class:** Wrong behaviour

**Failure:** When the test suite runs `cli/test/watcher-stall-reset-payloads.test.mjs`, the test `an honest hung run resumes: the edit discarded, the branch unmoved, the note written` fails before it runs anything. The error is `EEXIST: file already exists, mkdir '…/watcher-test/bin'`, thrown from `createStallFixture`.

**Failure as logged:**

```
        not ok 2527 - an honest hung run resumes: the edit discarded, the branch unmoved, the note written
          location: 'cli/test/watcher-stall-reset-payloads.test.mjs:441:1'
          failureType: 'testCodeFailure'
          error: "EEXIST: file already exists, mkdir '/private/tmp/claude-501/harness-fixture-qPFmz2/watcher-test/bin'"
          code: 'EEXIST'
          stack: |-
            async mkdir (node:internal/fs/promises:858:10)
            async createStallFixture (file://cli/test/watcher-stall-reset-payloads.test.mjs:208:3)
            async TestContext.<anonymous> (file://cli/test/watcher-stall-reset-payloads.test.mjs:442:13)
```

**Diagnosis:** First round (no earlier logs). This branch's change to `cli/test/helpers/watcher.mjs` (choice 9, "A stub `uv` that exits 0 leads every pass's `PATH`") makes `createWatcherFixture` create `join(recorderDir, 'bin')`, and `recorderDir` is `join(dir, 'watcher-test')` (`RECORDER_DIR = 'watcher-test'`). `createStallFixture` calls `createWatcherFixture(t)` first. It then builds `rec = join(w.dir, 'watcher-test')` and `bin = join(rec, 'bin')`, the very same directory, and creates it with a plain `mkdir(bin)`, with no `recursive` option. That call throws `EEXIST` now that the directory already exists. Every case in this file goes through `createStallFixture`, which explains all 18 failures in the file. Sharing the directory is otherwise harmless. The stall fixture writes only an `npx` stub into `bin`, which sits beside the helper's `uv` stub. In job mode its own `PATH` is `${bin}${delimiter}…`, which the helper then prefixes with the same directory again. The sibling suite `cli/test/watcher-placeholder-host.test.mjs` already creates the same path with `await mkdir(bin, { recursive: true });` and passes.

**Fix:**

- [ ] In `cli/test/watcher-stall-reset-payloads.test.mjs`, in `createStallFixture`, change `await mkdir(bin);` to `await mkdir(bin, { recursive: true });`. That is the same form `watcher-placeholder-host.test.mjs` uses for the same directory. Change nothing in `cli/test/helpers/watcher.mjs`: its `uv` stub is the branch's intended behaviour.
- [ ] Leave the stall fixture's other `mkdir` calls (`markers`, `payloads`, `outside`) as they are. Those directories are siblings of the fixture directory, and the helper does not create them.
