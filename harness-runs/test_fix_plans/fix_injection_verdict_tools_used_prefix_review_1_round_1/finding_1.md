### 1. The daemon-path test's gh-name assertion collides with the random fixture directory name

**Site:** `cli/test/doctor.test.mjs` — `const FIXTURE_GH_CLI = 'harness-fixture-gh';` (near line 5982), as asserted by the test `daemon-path names gh when remote execution is on, and not when it is off` at `assert.ok(!offLine.includes(FIXTURE_GH_CLI), offLine);` (near line 6336).

**Failing test:** `cli/test/doctor.test.mjs` — `daemon-path names gh when remote execution is on, and not when it is off` (and its parent suite `doctor`, `1 subtest failed`).

**Class:** Wrong behaviour

**Failure:** If the running program executes the `daemon-path names gh when remote execution is on, and not when it is off` test of `cli/test/doctor.test.mjs` and `mkdtemp` gives the fixture a suffix starting with `gh`, then the assertion `!offLine.includes(FIXTURE_GH_CLI)` fails with `AssertionError` (`expected: true`, `actual: false`) even though doctor's `daemon-path` line names no gh binary.

**Failure as logged:**

```
not ok 91 - daemon-path names gh when remote execution is on, and not when it is off
  location: 'cli/test/doctor.test.mjs:6319:1'
  error: "PASS  daemon-path                    the launchd unit for com.devscene.watcher.lders-5t-ht-j4jgs5h51bf16nmfz885m0000gn-t-harness-fixture-ghobss at /var/folders/5t/ht_j4jgs5h51bf16nmfz885m0000gn/T/harness-home-sr9fDc/Library/LaunchAgents/com.devscene.watcher.lders-5t-ht-j4jgs5h51bf16nmfz885m0000gn-t-harness-fixture-ghobss.plist carries a PATH reaching every binary an unattended run invokes by name, ..."
  code: 'ERR_ASSERTION'
  expected: true
  actual: false
  operator: '=='
  stack: TestContext.<anonymous> (file://cli/test/doctor.test.mjs:6336:10)
```

**Diagnosis:** first round, no earlier log, so it is not classed as new or persisting. The failure is a name collision in the test, not a doctor defect. `wiredFixture` builds its repository through `createFixture`, whose directory prefix is `FIXTURE_PREFIX = 'harness-fixture-'` (`cli/test/helpers/fixture.mjs`) followed by a random `mkdtemp` suffix. The launchd label and plist path doctor prints are derived from that directory, and this run's suffix was `ghobss`. So the `off` line contains `harness-fixture-ghobss`, which contains the substring `harness-fixture-gh` — exactly `FIXTURE_GH_CLI`. The quoted line names no gh binary at all (it lists `git`, `jq`, `claude`, `bash`, `npm`), so doctor behaved correctly; the negative assertion matched the fixture path instead. Any suffix beginning `gh` (roughly 1 run in a few thousand) reproduces it, and the positive assertion at `onLine?.includes(FIXTURE_GH_CLI)` could pass falsely for the same reason. The same constant also feeds `ghStub` (`join(dir, FIXTURE_GH_CLI)`), the `${FIXTURE_GH_CLI}-absent` cases and `join(dir, FIXTURE_GH_CLI)` in the gh-answers helper; all of them only need a name, never this value. The branch's own changes (the prompt-injection screen) do not touch this code.

**Fix:**

- [ ] In `cli/test/doctor.test.mjs`, change the value of `FIXTURE_GH_CLI` to a name that no fixture path or launchd label in this suite can contain — one that does not begin with `harness-fixture-` or with any other `mkdtemp` prefix the file uses (`harness-home-`, `harness-gh-stub-`, `harness-gh-answers-`, …), for example `'fixture-unit-gh-cli'`. Keep the constant's name and every use of it unchanged, so the `-absent` variants and the stub file name follow automatically.
- [ ] Add a one-line comment above the constant stating why its value must not share a prefix with a fixture directory (the daemon-path case asserts its absence from a line that prints the fixture's path).
- [ ] Do not weaken, skip or delete either assertion of the daemon-path test; the fix is the name alone.
