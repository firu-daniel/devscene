### Task 4 — Pin `typecheck.sh`'s Python step and its `BLOCKED` grading in `cli/test/check-shell-parse.test.mjs`

**Goal:** Pin how this repository's `scripts/typecheck.sh` grades its new Python step: `BLOCKED` is not a failure, the verdict line keeps its two forms, and the build's and the parse check's statuses still take precedence. The pins go in the suite that already runs a copy of that wrapper.

**Depends on:** Task 2. The contract pinned here: between `bash scripts/check-shell-parse.sh` and `npm run build "$@"`, the wrapper runs `bash scripts/python-service.sh check` with **no argument** when `scripts/python-service.sh` is a regular file. Otherwise it prints `typecheck: python checks SKIPPED - scripts/python-service.sh is not in this checkout`. Status `3` prints `typecheck: python checks BLOCKED - a package environment is not provisioned; run bash scripts/python-service.sh provision outside the sandbox` and is not a failure. Any other non-zero status is a failure. Exit precedence: build, then parse, then Python. One verdict line, `PASS: typecheck` or `FAIL: typecheck (exit <status>)`.

### Targets

- `cli/test/check-shell-parse.test.mjs` — the suite whose last case runs a copy of `scripts/typecheck.sh`.

**Work:**

- [ ] **Header.** Extend the paragraph on *"This repository's own `scripts/typecheck.sh` runs the check too"*: the wrapper also runs `python-service.sh check`, and the new case plants a stub of it whose exit status the case chooses, so the grading is pinned without `uv`. The real `check` is `cli/test/python-service.test.mjs`'s to pin.
- [ ] **The existing case.** Its fixture plants no `python-service.sh`, so assert that its output now carries the `SKIPPED` line and that every existing assertion still holds (`^PASS: typecheck$`, the forwarded `build-args:x`, the two `FAIL` statuses).
- [ ] **A new case.** In the same `repoWith` fixture, plant `scripts/python-service.sh` as a stub that prints `python-service-args:<its arguments joined by commas>` and exits `$FIXTURE_PYTHON_STATUS` (default `0`). The stub must parse, because the parse step lists it. Assert: status `0` gives exit `0`, `^PASS: typecheck$` and `python-service-args:check`; a caller argument `x` reaches `build-args:x` but not the stub (`python-service-args:check` still); status `3` gives exit `0`, the `BLOCKED` line and `^PASS: typecheck$`; status `1` gives exit `1` and `^FAIL: typecheck \(exit 1\)$`; status `1` with `FIXTURE_BUILD_STATUS=4` gives exit `4` (the build wins).

**Verification:**

- `npm test --workspace cli -- test/check-shell-parse.test.mjs` passes, run once from the repository root as one foreground command, and its counts include the new case.
