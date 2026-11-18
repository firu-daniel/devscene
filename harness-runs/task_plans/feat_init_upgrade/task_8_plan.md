### Task 8 — Add the `--upgrade` repository refusals

**Goal:** Decide, before anything is planned, whether this repository may be upgraded, so a refused run leaves it byte-identical.

**Depends on:** Task 3, for `runRegistryPath(repoRoot: string, config: HarnessConfig): string`, exported from `cli/src/generators/writeProtection.ts`. Task 7, for `readActiveRuns(registryPath: string): ActiveRuns`, where `ActiveRuns` is `{ state: 'none' } | { state: 'active'; branches: readonly string[] } | { state: 'unreadable'; detail: string }`.

**Where this task stops.** Flag combinations are parsed and refused in `cli/src/commands/init.ts` by Task 10. This module takes the check that refuses the harness's own repository as a callback, so it does not import `init.ts`.

### Targets

- `cli/src/upgrade/preconditions.ts` (new)
- `cli/test/upgrade-preconditions.test.mjs` (new)

**Work:**

- [ ] Create the module with a header stating its rule: every refusal comes before the first generator. Export `interface UpgradeTarget { readonly repoRoot: string; readonly config: HarnessConfig; readonly gitCommonDir: string; readonly notes: readonly string[] }`.
- [ ] Export `resolveUpgradeTarget({ cwd, dryRun, assertRepositoryAllowed }): UpgradeTarget`, where `assertRepositoryAllowed` is `(repoRoot: string) => unknown` and refuses by throwing. Resolve the root with `probeRepoRoot`, never creating or offering a repository, then call `assertRepositoryAllowed(root)`.
- [ ] Refuse with a `HarnessError` naming the remedy: no `devscene.config.json` (run `init` first), a configuration `loadConfig` cannot use (list its problems), a linked worktree (`mainWorktreeRoot` differs from the root, naming the main checkout), and no answer from `gitCommonDir`.
- [ ] Call `readActiveRuns(runRegistryPath(root, config))`, so this refusal reads the file the write protection covers. On `active`, refuse naming the branches and saying to wait for them or stop them. On `unreadable`, refuse naming the path and the detail. Under `dryRun`, neither refuses: each becomes a line in `notes` saying a real run would refuse.
- [ ] `upgrade-preconditions.test.mjs`: with compiled imports and fixtures, cover the outside-a-repository, unconfigured, invalid-configuration, linked-worktree, active-run and unreadable-registry cases, an active run found with `stateDir` absent from the configuration, a callback that throws, the two dry-run notes, and the accepted case. Each refusal case asserts the tree is byte-identical with `snapshotTree`.

**Verification:**

- `cli/test/upgrade-preconditions.test.mjs` passes.
- A directory outside any repository is still not a repository after the call.
