### Task 12 — Prove an upgraded profile passes the watcher's per-run check

**Goal:** Show that the profile `--upgrade` writes, local additions included, is one the shipped watcher will launch a run with on both macOS-style and bubblewrap-style hosts.

**Depends on:** Task 10, for `init --upgrade`.

**Where this task stops.** It changes no product file. The real Seatbelt and bubblewrap sessions are the hand-run Gate 15 named under `Manual setup required:` in the story index.

### Targets

- `cli/test/upgrade-run-profile.test.mjs` (new)

**Work:**

- [ ] Build a fixture wired by the compiled CLI, add a local file with one entry in each of the four lists, and run `init --upgrade`.
- [ ] Source the written `autonomous-watcher.sh` in a `bash` process, using the same no-launch calling pattern as `adoptedFixture` and `watcherCall` in `cli/test/watcher-run-profile.test.mjs`, without importing from that test file. Call `run_profile_render <branch> <copy> clone`, then `run_profile_check <rendered file> <copy>`.
- [ ] Run that pair with `HR_PLACEHOLDER_HOST=0` and `HR_PLACEHOLDER_HOST=1`, and assert exit 0 and an empty `RUN_PROFILE_REFUSAL` on each. Also assert `run_profile_check <profile>` with no copy, the job-mode form, passes.
- [ ] Assert the local entries are in the base profile and in the per-run copy, the local file's own protection entries are present in both, and a 0-byte read-only file at the local path, the placeholder shape, leaves a further `init --upgrade` unchanged.

**Verification:**

- `cli/test/upgrade-run-profile.test.mjs` passes.
- The test removes every fixture and per-run file it creates.
