### 1. `init` re-run says the walker's environment "is not built" when it is, and that package files "were written" when none were

**File:** `cli/src/commands/init.ts` (`run`) — "else if (!flowHostProvisioned(repoRoot, effective) || (flowHostPackages?.written.length ?? 0) > 0)", and the note above it, "files of the shipped Python packages were written into"

`writeFlowHostPackages` returns `written` = **every file it enqueued**, not every file the plan wrote (`cli/src/generators/flowHostPackages.ts` → `enqueueFlowHostPackages` pushes each shipped file unconditionally, and `shippedFiles` throws when the set is empty). So outside the self-adopted repository `flowHostPackages.written.length > 0` holds on **every** run. That has two wrong outputs:

1. The pre-plan note `"<N> files of the shipped Python packages were written into <scriptsDir>/python/"` prints on a re-run that kept every file (`create-if-absent`), so it claims writes that never happened.
2. The post-plan branch `else if (!flowHostProvisioned(...) || (flowHostPackages?.written.length ?? 0) > 0)` is always true when `--provision-python` was not given, so every plain `init` re-run notes `"the Python environment the flow walker runs in is not built: run bash <scriptsDir>/flow-host-provision.sh ..."` — including in a repository whose `<scriptsDir>/python/.venv/pyvenv.cfg` exists. `resolveProvisionPython` deliberately does not ask in that state ("in a repository without the environment"), and then the run tells the adopter the environment is missing.

**Probe (executed):** `bash scripts/scratch-run.sh harness-runs/scratch/branch_review_provision_note.mjs` — a throwaway repository under the system temp directory, `node cli/dist/cli.js init` twice with stdin piped, `devscene-scripts/python/.venv/pyvenv.cfg` planted between the runs. The second run (exit 0) printed:

```
- 55 files of the shipped Python packages were written into devscene-scripts/python/, copied verbatim from this CLI: ...
- the Python environment the flow walker runs in is not built: run bash devscene-scripts/flow-host-provision.sh outside the sandbox to build it with uv, or pass --provision-python to init
```

**Fix:** key both notes on what the plan actually did, read from `applied` (the `WriteResult[]` `plan.apply` returns — `effect` is the same under `--dry-run`, so the preview stays faithful).

1. Delete the `else if (flowHostPackages.written.length > 0)` note block before `plan.apply` (keep the `flowHostPackages === undefined` self-adoption note where it is).
2. Directly after `const applied = plan.apply(...)`, compute the package files this run created or replaced, and push the count note only when it is non-zero:

```ts
const flowHostRoot = `${join(repoRoot, ...flowHostDir(effective).split('/'))}${sep}`;
const flowHostChanged = applied.filter(
  (result) =>
    result.policy !== 'ensure-dir' &&
    result.path.startsWith(flowHostRoot) &&
    (result.effect === 'created' || result.effect === 'backed-up-and-replaced'),
).length;
if (flowHostChanged > 0) {
  notes.push(
    `${flowHostChanged} files of the shipped Python packages ${ctx.flags.dryRun ? 'would be' : 'were'} written into ${flowHostDir(effective)}/, copied verbatim from this CLI: a re-run leaves an edited copy as it is, --force replaces it after copying the current file to <name>.bak, and init --upgrade brings each file to this CLI's bytes after a backup`,
  );
}
```

(`sep` from `node:path`; `join` and `flowHostDir` are already imported.)

3. Change the post-plan condition to `} else if (!flowHostProvisioned(repoRoot, effective) || flowHostChanged > 0) {`, so the "is not built" note prints only when the environment is absent or the packages it was built from just changed. When the environment exists and packages changed, word that case as a rebuild rather than "is not built": split the branch so `!flowHostProvisioned(...)` keeps the current sentence and the `flowHostChanged > 0` arm says `the Python environment the flow walker runs in was built from the previous packages: rebuild it by running ${flowHostProvisionInvocation(effective)} outside the sandbox, or pass ${PROVISION_PYTHON_FLAG} to init`.

4. Add a case to `cli/test/init-provision-python.test.mjs`: run `init`, plant `<INIT_SCRIPTS_DIR>/python/.venv/pyvenv.cfg`, run `init` again, and assert the second run's output matches neither `/is not built/` nor `/files of the shipped Python packages were written/`. Run that one file: `npm test --workspace cli -- test/init-provision-python.test.mjs`.
