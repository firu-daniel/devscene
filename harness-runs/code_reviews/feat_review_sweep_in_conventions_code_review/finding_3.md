### 3. The review-sweep document's `--force` keep path has no test

**File:** `cli/src/generators/claudeContext.ts` (`writeClaudeContext`) — "const keepSweep = force && keepsRescuedBackup(repoRoot, REVIEW_SWEEP_PATH);"; test site `cli/test/init.test.mjs`, beside `test('a second init keeps an edited review-sweep document, and --force regenerates it after a .bak', …)`

**The problem.** The branch gives the sweep document the conventions stubs' conditional `--force` keep. A forced run keeps the document when it is already an untouched skeleton **and** its `.bak` holds a filled one, sets `forceOverride: 'never'` on that request and names the path in the kept-for-backup note. `cli/src/core/writer.ts`'s re-run-contract row, `docs/cli.md` §3 and `docs/analyze.md` §4 all state this as the contract.

No test reaches that branch:

- The new init case covers only the unforced keep and the plain `--force` regenerate-after-`.bak`.
- The existing two-pass case, `test('a second --force keeps the already-skeletal documents whose .bak holds the analysis', …)`, fills only the `.claude/context/` documents (`fillConventionsByHand`). The sweep document's `.bak` is therefore a skeleton there, and `keepsRescuedBackup` answers `false` for it.

So the keep for this document could be removed, or pointed at the wrong path, with every test still passing. That breaks `.claude/context/cli.md` → `## What "done" means here`: "A change to a command or a generator lands with a case that drives the compiled CLI against a throwaway fixture repository".

**Fix.** Add a case to `cli/test/init.test.mjs`, directly after the "a second init keeps an edited review-sweep document" test:

```js
test('a second --force keeps an already-skeletal review-sweep document whose .bak holds the filled rows', async (t) => {
  const dir = await fixtureFor(t, { files: nodeProjectFiles() });
  await initOk(dir);
  const filled = '# The review sweep\n\n## Sweep rows\n\n| Escape class | Regex | Covers | Exempts | A hit is a candidate for |\n|---|---|---|---|---|\n| Raw console | `console\\.log` | `.` | — | the logger |\n';
  writeFileSync(join(dir, REVIEW_SWEEP_FILE), filled, 'utf8');

  // Pass 1: the filled document goes back to a skeleton, its rows in the .bak.
  await initOk(dir, ['--force']);
  assert.ok(text(dir, REVIEW_SWEEP_FILE).includes(UNFILLED_MARKER), 'the first --force did not put the document back to a skeleton');
  assert.equal(text(dir, `${REVIEW_SWEEP_FILE}.bak`), filled, 'the first --force did not rescue the filled rows into the .bak');

  // Pass 2: nothing is left to rescue, so the .bak must not be spent.
  const { stdout } = await initOk(dir, ['--force']);
  assert.equal(text(dir, `${REVIEW_SWEEP_FILE}.bak`), filled, 'the second --force overwrote the rescued rows with a skeleton');
  const note = keptForBackupNote(stdout);
  assert.ok(note.includes(REVIEW_SWEEP_FILE), `the run kept ${REVIEW_SWEEP_FILE} and the note does not name it:\n${note}`);
});
```

`writeFileSync` comes from `node:fs`. Add it to that import if the file does not already take it. `UNFILLED_MARKER`, `keptForBackupNote`, `text`, `fixtureFor`, `nodeProjectFiles` and `initOk` are already defined in the file. `keptForBackupNote` is declared further down as a function declaration, so it is hoisted and callable from here.

This fix edits `cli/test/init.test.mjs`, so that is the one test file it runs: `npm test --workspace cli -- test/init.test.mjs`, from the repository root, as one plain foreground command. The full suite runs later, in the Run gates phase.
