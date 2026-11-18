### 1. `init --upgrade` accepts a run copy, so it reports success without touching the profile runs load and skips the active-run refusal

**File:** `cli/src/upgrade/preconditions.ts` (`assertMainCheckout`) — "is a linked worktree; run --upgrade in the main checkout at"; call site `resolveUpgradeTarget` — "const notes = registryLocatable(config)"

`assertMainCheckout` decides "is this the main checkout" by comparing the root with `mainWorktreeRoot`, the first `worktree` line of `git worktree list --porcelain`. That catches a linked worktree only. The harness's run copies are **clones** (`copy_kind: "clone"` in the run registry, borrowing objects through `.git/objects/info/alternates`), and in a clone the first `worktree` line is the clone itself (`plugin/instructions/main_repo_resolution.md` → `## The fallback` has a separate alternates arm for exactly this reason). So the check passes in a run copy.

What follows from `npx devscene init --upgrade` run there:

- The tracked scripts of the **run branch** are replaced, leaving that copy dirty.
- A profile is written into the copy. No run loads it: the watcher renders from the main checkout's, which is why `writeProtection.ts` protects only the main checkout's copy. The command still prints `Upgrade complete`, so the operator believes the repository is upgraded while the main checkout is unchanged.
- The active-run refusal reads `<copy>/<stateDir>/autonomous_logs/registry.json`. The registry lives in the main checkout, so in a copy it is absent and reads as "no runs", even while a run is executing in that very copy.

The story index states the rule as "`--upgrade` runs in the main checkout only", and its reason for refusing a linked worktree, that it "has no profile a run loads", holds equally here. No case in `cli/test/upgrade-preconditions.test.mjs` or `cli/test/init-upgrade.test.mjs` covers a clone. This comes from reading the code and git's documented output; the review did not execute it.

**Fix:** refuse a checkout the main checkout's registry records as its run copy, using the same three facts `main_repo_resolution.md` → `## The fallback` checks. An ordinary clone a person made is not in that registry and stays allowed. When the alternates file names a candidate whose registry cannot be read, the check cannot show the checkout is not a run copy, so it fails closed: the story index decides that "An unreadable run registry refuses the upgrade". That case uses the existing unreadable-registry wording and, like every run-registry refusal, becomes a note under `--dry-run`.

In `cli/src/upgrade/preconditions.ts`, add `readFileSync` from `node:fs` and `join` from `node:path`, then:

```ts
/** Where a clone that borrows its objects names the repository it borrows from. */
const ALTERNATES_SEGMENTS: readonly string[] = Object.freeze(['objects', 'info', 'alternates']);
const BORROWED_OBJECTS_SUFFIX = '/.git/objects';

/** What {@link checkRunCopy} found. */
type RunCopyCheck =
  | { readonly kind: 'not-a-run-copy' }
  | { readonly kind: 'run-copy'; readonly main: string }
  | { readonly kind: 'registry-unreadable'; readonly registryPath: string };

const NOT_A_RUN_COPY: RunCopyCheck = Object.freeze({ kind: 'not-a-run-copy' });

/**
 * Whether `root` is a run copy: its alternates file names a checkout whose run registry records
 * `root` as a clone. `git worktree list` cannot answer this, because a clone is its own first
 * worktree. A registry that cannot be read cannot rule the answer out, so it is reported.
 */
function checkRunCopy(root: string, commonDir: string, config: HarnessConfig): RunCopyCheck {
  let line: string;
  try {
    line = readFileSync(join(commonDir, ...ALTERNATES_SEGMENTS), 'utf8').trim();
  } catch {
    return NOT_A_RUN_COPY;
  }
  if (line.includes('\n') || !line.endsWith(BORROWED_OBJECTS_SUFFIX)) return NOT_A_RUN_COPY;
  const candidate = line.slice(0, -BORROWED_OBJECTS_SUFFIX.length);
  const registryPath = runRegistryPath(candidate, config);
  const registry = readRegistryRecords(registryPath);
  if (registry.state !== 'read' || registry.malformedKeys.length > 0) {
    return { kind: 'registry-unreadable', registryPath };
  }
  const recorded = registry.records.some(
    ({ record }) => record['worktree'] === root && record['copy_kind'] === 'clone',
  );
  return recorded ? { kind: 'run-copy', main: candidate } : NOT_A_RUN_COPY;
}
```

In `resolveUpgradeTarget`, replace the `notes` statement with:

```ts
  let notes: readonly string[] = [];
  if (registryLocatable(config)) {
    const runCopy = checkRunCopy(repoRoot, commonDir, config);
    if (runCopy.kind === 'run-copy') {
      throw new HarnessError(`${REFUSAL_PREFIX}: ${repoRoot} is a run copy; run --upgrade in the main checkout at ${runCopy.main}`);
    }
    const borrowedRegistryNotes =
      runCopy.kind === 'registry-unreadable' ? runRegistryNotes(runCopy.registryPath, request.dryRun) : [];
    notes = [...borrowedRegistryNotes, ...runRegistryNotes(runRegistryPath(repoRoot, config), request.dryRun)];
  }
```

The run-copy refusal is not softened under `--dry-run`, like the linked-worktree one. `runRegistryNotes` supplies the unreadable-registry refusal and its dry-run note, so that wording stays in one place.

In `docs/cli.md` → `### Updating an adopted repository`, after the bullet beginning "the checkout is a linked worktree", add:

```markdown
- the checkout is a run copy the main checkout's run registry records, for the same reason, and the refusal names that checkout;
```

Add three cases to `cli/test/upgrade-preconditions.test.mjs`. In each, the repository under test has a `.git/objects/info/alternates` file naming a second fixture's `.git/objects`, with both paths taken from the fixtures' resolved roots so the registry's `worktree` value compares equal:

1. The second fixture's registry records the repository as `{ "worktree": <root>, "copy_kind": "clone" }`: the run is refused with the main checkout named, under `--dry-run` too, and writes nothing.
2. The second fixture's registry has no such record: the run is not refused.
3. The second fixture's registry file holds `MALFORMED_REGISTRY`: a real run is refused with `assertRefused`, matching that registry's path and `/not valid JSON/`; a `dryRun: true` run returns one note matching `/would refuse: .*not valid JSON/` and leaves the repository byte-identical.

That test file is the only one this fix edits, so it is the only test the fix runs.
