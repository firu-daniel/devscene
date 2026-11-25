### 3. `--check-registry` no-client doctor case exits 1: its `PATH` has no `uv`

**File:** `cli/test/doctor.test.mjs` (`pathWithNpxButNoNpm`) — "for (const name of ['git', 'jq'])" and "writeFileSync(join(dir, 'npx'), '#!/bin/sh\nexit 0\n', { mode: 0o755 });" (around line 2338, navigation hint only); its one caller is the test below, "const PATH = await pathWithNpxButNoNpm(t);".

**Failing test:** `cli/test/doctor.test.mjs` — `--check-registry claims no registry read when npm does not resolve on PATH` (TAP `not ok 59`, inside the suite `not ok 382 - doctor`).

**Class:** Wrong behaviour
**Failure:** If the running program runs `cli/test/doctor.test.mjs` → `--check-registry claims no registry read when npm does not resolve on PATH`, then it fails with `doctor exited 1 with no registry client on PATH`, because the `PATH` it builds holds only `git`, `jq` and an `npx` stub, and `doctor`'s `uv` check now fails when `uv` does not resolve.

**Failure as logged** (gate 4, first round; the diagnostic was truncated by the reporter after 40 lines, all of them `PASS` lines from stdout):

```
not ok 59 - --check-registry claims no registry read when npm does not resolve on PATH
  location: 'cli/test/doctor.test.mjs:2429:1'
  error: |-
    doctor exited 1 with no registry client on PATH
    == checks (/private/tmp/claude-501/harness-fixture-HROKZa)
    PASS  git                            git 2.50 answered, …
    …
    PASS  jq                             jq 1.8 is on PATH …
    PASS  worktrees                      git worktree list answers with 1 checkout, …
    …
    [diagnostic truncated after 40 lines]
not ok 382 - doctor
  failureType: 'subtestsFailed'
  error: '1 subtest failed'
```

**Diagnosis.** Class: first round (no earlier log). This branch's Task 5 (commit `fe69459c`, "Grade a missing uv as a doctor failure") made the `uv` check in `cli/src/doctor/checks.ts` (`id: 'uv'`) return a `fail` when `resolvesOnPath('uv')` is false — "uv does not resolve on PATH: DevScene requires uv to run its flow walker …". A `fail` makes `doctor` exit 1. `pathWithNpxButNoNpm` builds a `PATH` of exactly one directory holding symlinks to the real `git` and `jq` plus an `npx` stub, so `uv` cannot resolve and the run exits 1 regardless of what the registry probe answers. The stdout excerpt confirms the shape: `PASS  jq` is followed directly by `PASS  worktrees` with no `uv` line on stdout, consistent with the `uv` check's `FAIL` line having gone to stderr, past the 40-line truncation. Every other case in this file runs with the host `PATH`, where the real `uv` resolves, which is why only this case broke. `cli/test/doctor-flow-host.test.mjs` was updated with Task 5; this file's helper was not. The production grade is intended; the helper is stale.

**Fix** (test helper only; no change to `cli/src/doctor/checks.ts`):

- [ ] In `pathWithNpxButNoNpm`, beside the `npx` stub, write an executable `uv` stub that prints a version the `uv` check recognises (its `UV_VERSION_PATTERN` is `/^uv (\d+\.\d+(?:\.\d+)?)/`), e.g. `writeFileSync(join(dir, 'uv'), "#!/bin/sh\nprintf '%s\\n' 'uv 0.9.0'\n", { mode: 0o755 });` — the same stub shape `cli/test/doctor-flow-host.test.mjs` uses (`STUB_VERSION = 'uv 0.9.0'`). A stub, not a symlink to the real `uv`: the helper must not depend on `uv` being installed, and a stub keeps the case off the network.
- [ ] Update the helper's doc comment: it currently says "an `npx` stub beside symlinks to the real `git` and `jq`"; add the `uv` stub and one clause on why — `doctor` grades a missing `uv` as a failure, which would move the exit status this case asserts is 0.
- [ ] Leave the test's assertions unchanged (`status === 0`, `PASS browser-wiring`, "The registry probe ran nothing", no `the registry was read`).
