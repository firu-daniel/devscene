### 1. `typecheck.sh`'s `BLOCKED` line sends a host with no `uv` to `provision`, which skips and leaves the check `BLOCKED`

**File:** `scripts/typecheck.sh` — "typecheck: python checks BLOCKED - a package environment is not provisioned; run bash scripts/python-service.sh provision outside the sandbox"
**Class:** Wrong action from operative text
**Failure:** If an operator on a host with no `uv` on `PATH` runs `bash scripts/typecheck.sh` and follows its `BLOCKED` line by running `bash scripts/python-service.sh provision` outside the sandbox, then `provision` prints `python-service: provision: SKIPPED — uv is not on PATH; …` and exits 0 having synced nothing, and the next `bash scripts/typecheck.sh` prints the same `BLOCKED` line.

`bash scripts/python-service.sh check` exits `3` for either of two causes, which `require_uv` and `require_env` in `scripts/python-service.sh` tell apart: `uv` is not on `PATH`, or no synced environment exists. `scripts/typecheck.sh` maps every exit `3` onto one line whose remedy is `provision` alone. That is right for the second cause only. For the first, `provision`'s own no-`uv` arm (`scripts/python-service.sh` → "python-service: provision: SKIPPED — uv is not on PATH") prints a `SKIPPED` line and exits `0` with nothing written, so the remedy the line names does not clear the condition it reports. The line's first clause, "a package environment is not provisioned", is also inaccurate in that case. The wrapper's own `require_uv` message already gives the full remedy ("install uv, then run bash scripts/python-service.sh provision outside the sandbox"). The type check's summary line should give the same remedy for both causes, because both sit behind the same exit status.

This was confirmed by reading only: no probe was run on a host without `uv`. The read sites are `scripts/typecheck.sh` (the `python_status -eq 3` arm), `scripts/python-service.sh` (`require_uv`, `require_env`, and the `provision` arm's `command -v uv` test), and `docs/development.md` → **Gate 13 — the Python packages.**, which quotes the line verbatim.

**Fix:**

1. In `scripts/typecheck.sh`, replace the `echo` in the `if [ "$python_status" -eq 3 ]; then` arm with this line:

   ```bash
       echo "typecheck: python checks BLOCKED - uv is not on PATH or a package environment is not provisioned; install uv if it is missing, then run bash scripts/python-service.sh provision outside the sandbox"
   ```

2. In `cli/test/check-shell-parse.test.mjs`, in the test `"this repository's typecheck.sh runs python-service.sh check, grading its exit 3 BLOCKED and not failed"`, replace the `BLOCKED` constant with:

   ```js
   const BLOCKED =
     /^typecheck: python checks BLOCKED - uv is not on PATH or a package environment is not provisioned; install uv if it is missing, then run bash scripts\/python-service\.sh provision outside the sandbox$/m;
   ```

3. In `docs/development.md` → **Gate 13 — the Python packages.**, in the sentence beginning "Where a package environment is not provisioned, `check` exits `3`", change it to read: "Where `uv` is not on `PATH` or a package environment is not provisioned, `check` exits `3` with no leg failed, and the type check prints `typecheck: python checks BLOCKED - uv is not on PATH or a package environment is not provisioned; install uv if it is missing, then run bash scripts/python-service.sh provision outside the sandbox` and does not fail the unit."

This fix edits `cli/test/check-shell-parse.test.mjs`, so that file is the one test this fix runs: `npm test --workspace cli -- test/check-shell-parse.test.mjs`.

**Deviations from plan:** `cli` dispatch implemented Fix step 2 only; steps 1 and 3 (`scripts/typecheck.sh`, `docs/development.md`) are the `general` layer's half of this `(layer: cli, general)` entry. `npm test --workspace cli -- test/check-shell-parse.test.mjs` after the `cli` edit: `# tests 12`, `# pass 11`, `# fail 1` — the failing case is "this repository's typecheck.sh runs python-service.sh check, grading its exit 3 BLOCKED and not failed", whose input was still the old `scripts/typecheck.sh` line. It passes only once Fix step 1 lands, so it has to be rerun after the `general` dispatch.

- `general` dispatch implemented Fix steps 1 and 3 as written. Rerun after it: `npm test --workspace cli -- test/check-shell-parse.test.mjs` → `# tests 10`, `# pass 10`, `# fail 0`; `bash scripts/typecheck.sh` → `PASS: typecheck`, every `python-service: check:` leg `PASS`.
