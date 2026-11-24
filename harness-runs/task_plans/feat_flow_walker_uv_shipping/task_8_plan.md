### Task 8 — Add `doctor`'s `uv` and `flow-host` checks

**Goal:** Make `doctor` report a host without `uv` and a repository whose shipped packages or walker environment are missing or stale. Both checks are **warnings** before #419, because nothing runs the walker yet (story index `## Context`). Neither ever fails, so `doctor`'s exit status keeps meaning "runnable as configured" (`.claude/context/cli.md` → *"`doctor` asks, grades and repairs nothing"*).

**Depends on:**

- **Task 2:** `cli/src/generators/flowHostPackages.ts` → `flowHostPackageDrift(repoRoot, config)` returns `{ missing, changed }`, repo-relative.
- **Task 1:** `cli/src/flowHost/layout.ts` → `flowHostEnvDir(config)`.
- **Task 3:** the outer-loop row `flow-host-provision.sh`, whose invocation comes from `scriptInvocation`.

- **Task 6** may already have edited `cli/src/doctor/checks.ts` → `IGNORE_RULES_CHECK` for the new ignore line. Leave that check as Task 6 left it.

Import each from its owner; re-derive nothing (`.claude/context/cli.md` → *"nothing it reports is re-derived from a second copy"*).

### Targets

- `cli/src/doctor/checks.ts`.
- `cli/test/doctor-flow-host.test.mjs` (new).

**Work:**

- [ ] `UV_CHECK`, id `uv`, title `uv is on PATH, so the flow walker's Python environment can be provisioned`. It is shaped like `JQ_CHECK`: existence through `resolvesOnPath`, then `uv --version` through `execFileSync` with a fixed argv and a bounded timeout. It reads no configuration.
  - Absent: **warn**. `DevScene requires uv to run its flow walker; install uv, then provision the walker's environment` (wording may tighten, the content may not).
  - Present but not answering, or printing an unparseable string: warn.
  - Answering: pass, quoting the printed version.
  - The doc comment states that the grade is a warning until #419 makes the walker needed.
- [ ] `FLOW_HOST_CHECK`, id `flow-host`, title `the flow walker's Python packages are the ones this CLI ships, and their environment is provisioned`:
  - Unevaluated without a root or a config, as `outer-loop-scripts` is.
  - Missing or changed packages: warn, naming each path and the remedy `npx devscene init --upgrade`, from the same constant `OUTER_LOOP_SCRIPTS_CHECK` uses.
  - Otherwise, when `<flowHostEnvDir>/pyvenv.cfg` is absent: warn, naming `bash <scriptsDir>/flow-host-provision.sh`, run outside the sandbox. When `uv` does not resolve, the remedy says to install `uv` first.
  - Otherwise pass.
- [ ] `CHECKS`: insert `UV_CHECK` after `JQ_CHECK`, and `FLOW_HOST_CHECK` after `OUTER_LOOP_SCRIPTS_CHECK`.
- [ ] `doctor-flow-host.test.mjs`, its header stating the rule. It runs the compiled CLI against a throwaway fixture wired by `init` and asserts:
  - `uv`: with a stub `uv` printing `uv 0.9.0`, the check passes and quotes it. With no `uv` reachable, through a `PATH` built from a temp bin directory holding links to only the binaries the run needs (as `cli/test/job-layout-root.test.mjs` builds its shim `PATH`), it warns, and `doctor` still exits `0` when nothing else fails.
  - `flow-host`: freshly wired with no environment, it warns naming the provisioning command. After `<scriptsDir>/python/.venv/pyvenv.cfg` is planted, it passes. After a shipped file is edited, it warns naming that path and `init --upgrade`. After one is deleted, it warns naming it as missing.

**Verification:**

- `npm test --workspace cli -- test/doctor-flow-host.test.mjs` passes.
- `node cli/dist/cli.js doctor` in a fixture lists both new check ids in the order above.
- Existing `doctor` suites that pin the full check list or its count: update only that expectation, and only in suites this task edits.
