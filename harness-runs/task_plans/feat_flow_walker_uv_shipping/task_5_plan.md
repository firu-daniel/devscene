### Task 5 — Write-protect the main checkout's `<scriptsDir>/python/` in the unattended profile

**Goal:** Make sure no run can write the source an unsandboxed provisioning builds. `uv sync` runs the packages' build backend outside the sandbox, from the main checkout's `<scriptsDir>/python/`, both in `init` and in every run copy's bootstrap (Task 4). So that directory joins the protected set, under `cli/src/generators/writeProtection.ts`'s own rule: *"anything that runs outside the sandbox must not be writable from inside it."*

**Depends on:** Task 1, whose `cli/src/flowHost/layout.ts` → `flowHostDir(config)` returns the repo-relative `<scriptsDir>/python`. Build the path through it, never by joining `python` by hand (`writeProtection.ts` header: *"Every path is built through its owner"*). Task 4 is the reason the main checkout's tree is the one built for every run copy.

**Where this task stops.** It protects the main checkout's directory only. A run copy's `<scriptsDir>/python/` is not protected, because no unsandboxed step builds from a copy's tree under `--target` (Task 4). So `copySurfacePaths` and its shell mirror `hr_run_protected_rel_paths` stay unchanged. `jobSurfacePaths` is derived from `protectedPaths`, so it gains the directory with no edit, and a remote job then refuses a branch whose own commits changed it.

### Targets

- `cli/src/generators/writeProtection.ts`.
- `cli/test/flow-host-protection.test.mjs` (new).

**Work:**

- [ ] `protectedPaths`: push `{ path: join(repoRoot, flowHostDir(config)), kind: 'directory', reason: "the main checkout's Python packages are built outside the sandbox when the flow walker's environment is provisioned" }` after the `lib` directory entry. Add the directory to the header's *"The set:"* sentence.
- [ ] Check that the per-run profile carries the new main-checkout entry. `cli/templates/scripts/autonomous-watcher.sh` → `run_profile_render` reads the generated profile, so a new main-checkout path needs no edit there. Confirm that by reading it, and state the finding in your return. If it does need an edit, report a blocker naming it rather than widening this task.
- [ ] `flow-host-protection.test.mjs`, its header stating the rule. It runs `init` in a throwaway fixture and asserts:
  - The generated profile's `sandbox.filesystem.denyWrite` holds `<root>/<scriptsDir>/python`.
  - Its `permissions.deny` holds `fileToolDenyRules`' directory rule for it.
  - `doctor --job-surfaces=<default branch>` fails for a branch whose own commit changed `<scriptsDir>/python/devscene-flow-host/pyproject.toml`, naming that path. Model this on `cli/test/doctor-job-surfaces.test.mjs`.
  - `copySurfacePaths` does not carry the directory.

**Verification:**

- `npm test --workspace cli -- test/flow-host-protection.test.mjs` passes.
- Existing suites that list the exact protected set or the job-surface list now differ by this one entry. Update only that expectation, and only in suites this task edits.
