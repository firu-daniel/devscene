### 3. A permission-bits repair on the watcher or a library tells the operator to restart a daemon whose code did not change

**File:** `cli/src/upgrade/report.ts` (`upgradeReport`) — "if (changed.some(({ path }) => daemonLoadedPaths.has(path))) {"

`changed` holds every `created` and `backed-up-and-replaced` result, and `backed-up-and-replaced` with no `backupPath` means `replace-if-changed` corrected permission bits only (`cli/src/core/writer.ts` → `WriteEffect`'s doc comment). The restart line is keyed on `changed`, so a mode-only result on `autonomous-watcher.sh` or a `lib/` file produces "A running daemon keeps the code it already loaded: restart it with …", although the bytes are identical.

This is an ordinary case. The writer compares all nine permission bits against the table, while git records only the owner-execute bit, so a checkout made under umask `002` holds `0775` and `0664` files. `outerLoopScriptDrift` ignores that difference for this very reason. Such a checkout's first upgrade repairs the modes of every script and prints a restart demand that nothing requires.

**Fix:** key the restart line on files whose content changed. In `upgradeReport`, replace the condition with:

```ts
  const contentChanged = changed.filter(({ effect, backupPath }) => effect === 'created' || backupPath !== undefined);
  if (contentChanged.some(({ path }) => daemonLoadedPaths.has(path))) {
```

Leave `changed` itself as it is: the backup count and the closing file count still use it.

In `cli/test/upgrade-report.test.mjs`, add this row to the `cases` object of the test `no restart line when the watcher and lib rows are untouched`:

```js
    'the watcher only had its permission bits corrected': [write('scripts/autonomous-watcher.sh', 'backed-up-and-replaced')],
```

That test file is the only one this fix edits, so it is the only test the fix runs.
