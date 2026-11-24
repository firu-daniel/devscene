### 3. `doctor`'s `flow-host` drift remedy in the self-adopted repository names `init --upgrade`, which skips the packages there

**File:** `cli/src/doctor/checks.ts` (`FLOW_HOST_CHECK`) — "the flow walker's Python packages differ from this CLI's"

In the harness's own self-adopted repository, `scripts/python/graphscene` and `scripts/python/devscene-flow-host` are symbolic links to `../../graphscene` and `../../devscene-flow-host` (Task 12), and the CLI that grades them is this checkout's `cli/dist/cli.js`, whose `dist/python/` was staged at the last `npm run build`. `flowHostPackageDrift` therefore reports drift whenever a maintainer edits a tracked file under `graphscene/src/`, `devscene-flow-host/src/` or either `pyproject.toml` / `uv.lock` without rebuilding, and `FLOW_HOST_CHECK` then tells them to run `init --upgrade`. But `cli/src/upgrade/initUpgrade.ts` → `runInitUpgrade` skips the packages under self-adoption (`if (!target.selfAdopted) planFlowHostPackageUpgrade(...)`), so the upgrade writes nothing to them and the next `doctor` reports the same drift with the same remedy. The step that clears it is re-staging, `npm run build`. This is the `harness-runs/lessons.md` → `## Adopter-facing documentation` rule "A remedy never sends an adopter to a place the CLI refuses: derive the advice from the same predicate as the refusal" — here the run silently declines instead of refusing, and only this repository's maintainers are affected.

Confirmed by reading `FLOW_HOST_CHECK`, `flowHostPackageDrift` and `runInitUpgrade`; no probe was run.

**Fix:** in `FLOW_HOST_CHECK.run`, after `flowHostPackageDrift` reports drift, test whether the packages are links (the self-adopted layout) and name the re-stage there:

```ts
const linked = FLOW_HOST_PACKAGES.some((pkg) =>
  lstatOrUndefined(join(ctx.profileRoot!, ...flowHostDir(ctx.config!).split('/'), pkg))?.isSymbolicLink() === true,
);
const remedy = linked
  ? 'Run `npm run build` from the repository root, which re-stages dist/python/ from the packages these links point at'
  : `Run \`${INIT_UPGRADE_COMMAND}\`, which writes this CLI's copies after a backup, then rebuild the environment as it says`;
return warn(`the flow walker's Python packages differ from this CLI's — ${findings.join('; ')}. ${remedy}`);
```

Import `FLOW_HOST_PACKAGES` from `../flowHost/layout.js` beside `flowHostDir` and `flowHostEnvDir`, and `lstatOrUndefined` from `../core/paths.js` if the file does not already import it. Add the sentence "In the harness's own repository, where the packages are links, the remedy is `npm run build` instead" to the `FLOW_HOST_CHECK` doc comment.

Add a case to `cli/test/doctor-flow-host.test.mjs`: after `init`, replace `<INIT_SCRIPTS_DIR>/python/graphscene` with a symbolic link to a copy of `cli/dist/python/graphscene` under the system temp directory whose `pyproject.toml` has one appended line, run `doctor`, and assert the `flow-host` line names `npm run build` and does not name `init --upgrade`. Run that one file: `npm test --workspace cli -- test/doctor-flow-host.test.mjs`.
