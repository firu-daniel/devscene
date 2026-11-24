### 2. `provisionFlowHost` keys a false-success decision on an undeclared, untested copy of the library's `SKIPPED` wording

**File:** `cli/src/flowHost/provision.ts` (`SKIPPED_MARKER`) — "const SKIPPED_MARKER = 'flow-host: provision: SKIPPED';"

`provisionFlowHost` decides between "built the Python environment ... with uv" and a warning by finding a stderr line starting with `SKIPPED_MARKER`, because the script exits `0` on a skip. That string is a copy of the wording `hr_flow_host_provision` prints in `cli/templates/scripts/lib/harness-run-lib.sh` ("printf 'flow-host: provision: SKIPPED — uv is not on PATH; ..." and "printf 'flow-host: provision: SKIPPED — no flow host at ..."). Neither side declares it:

- `cli/src/flowHost/layout.ts`'s `MIRRORS.` header and the library's `MIRROR OF cli/src/flowHost/layout.ts` block list only `FLOW_HOST_DIRNAME`, `FLOW_HOST_PROJECT` and `FLOW_HOST_ENV_DIRNAME`;
- `provision.ts`'s header names `hr_flow_host_provision` as the implementation but not this literal;
- `cli/test/init-provision-python.test.mjs` has no skip case (its cases are: stub `uv` succeeds, no flag, `--dry-run`, stub `uv` fails, `--upgrade` refusal, upgrade rebuild note), and `cli/test/flow-host-provision.test.mjs` asserts the shell's wording only against the script, never against `provision.ts`.

So a reword of the library's skip line passes every suite and turns `init --provision-python` on a host without `uv` into a `notes` line saying the environment was built, with exit 0 and nothing built. `.claude/context/conventions.md` → `## Configuration is the source of truth, and it is read at run time` holds that a value is imported from its owner or declared as a mirror where a shipped script cannot import it, and `.claude/context/cli.md` → `## What "done" means here` holds a change to its module's own header ("this is the one owner of every name the shipped Python layout is reached by").

This was confirmed by reading the two files and the two suites; no probe was run.

**Fix:**

1. In `cli/src/flowHost/provision.ts`, add to the module header, after the `spawnSync` bullet:

```
 * MIRROR. {@link SKIPPED_MARKER} is the prefix `hr_flow_host_provision` in
 * `cli/templates/scripts/lib/harness-run-lib.sh` opens each skip line with; a reword there is an
 * edit here, and `cli/test/init-provision-python.test.mjs` holds the two equal.
```

2. In `cli/templates/scripts/lib/harness-run-lib.sh`, in the `THE FLOW HOST'S ENVIRONMENT` section's `MIRRORS` comment, add one line:

```
#   skip prefix   'flow-host: provision: SKIPPED'  mirrored by  cli/src/flowHost/provision.ts → SKIPPED_MARKER
```

and apply the same edit to the self-adopted copy `scripts/lib/harness-run-lib.sh`, keeping the two byte-identical.

3. Add a case to `cli/test/init-provision-python.test.mjs`: build a `PATH` directory holding symlinks to only `bash`, `dirname`, `git`, `jq` and the running `node` (resolved with `command -v`, as `cli/test/flow-host-provision.test.mjs` → `whichOf` does; skip the case where `jq` does not resolve), run `init --provision-python` with that `PATH`, and assert exit `0`, that `result.stderr` matches `/was not built: flow-host: provision: SKIPPED — uv is not on PATH/`, and that the output does not match `/built the Python environment the flow walker runs in at/`. Run that one file: `npm test --workspace cli -- test/init-provision-python.test.mjs`.

**Deviations from plan:**
- Step 3's `node` link targets `process.execPath` (the running `node`) rather than `command -v node`, which may resolve a different binary; `bash`, `dirname`, `git` and `jq` resolve through `command -v` as specified.
- Step 2's self-adopted copy `scripts/lib/harness-run-lib.sh` is outside the `cli` layer's path and is left to this unit's general-layer dispatch, which mirrors the template line byte-for-byte.
- Evidence downgrade — tree guard `test/python-packages-staged.test.mjs` (selected by `cli/src/flowHost/**`), run as `npm test --workspace cli -- test/python-packages-staged.test.mjs`: 3 of 4 pass; case `npm pack lists the staged Python files` fails with `npm error code EPERM` / `npm error path ~/.npm/_cacache/tmp/c5d16fab`, the run's sandbox refusing npm's cache write outside the writable set. The failure names no symbol or path this unit changed (`provision.ts`'s header comment, the library's MIRRORS comment, `init-provision-python.test.mjs`); that case rests on the Run gates phase's `commands.test` run.
- General-layer dispatch: step 2's line added to `scripts/lib/harness-run-lib.sh`; `cmp` against `cli/templates/scripts/lib/harness-run-lib.sh` reports the two byte-identical. Evidence downgrade — the same tree guard rerun from this dispatch (`npm test --workspace cli -- test/python-packages-staged.test.mjs`) again passes 3 of 4 and fails `npm pack lists the staged Python files` with `npm error code EPERM` / `npm error path ~/.npm/_cacache/tmp/b7ed5c89`, the sandbox refusing npm's cache write; it names no path this dispatch changed and rests on the Run gates phase's `commands.test` run.
