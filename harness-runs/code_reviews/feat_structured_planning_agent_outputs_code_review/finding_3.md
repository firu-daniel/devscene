### 3. The roster check in `agent-return-schemas.test.mjs` reads every file under `plugin/`, but the suite is registered only for `plugin/**/*.md`

**File:** `cli/test/agent-return-schemas.test.mjs` — the test `'the plugin files naming the module equal its ## Who may cite this roster'`, which calls `checkRoster(moduleText, pluginFiles)`

**The problem.** `pluginFiles` is `walk('plugin')`, so it holds every file under `plugin/`: shell hooks, scripts, JSON manifests, `README.txt`. `checkRoster` therefore fails whenever any of those names `agent_return_contract.md` without being on the module's roster. The suite's `treeGuards` entries in `devscene.config.json` cover only `plugin/**/*.md` and `cli/templates/scripts/**`. A change to a non-Markdown plugin file that trips the roster check does not select this guard in the unit loop, and the failure first shows up in the Run gates round. The module's own roster rule speaks of plugin *assets* that point at it, and every one of those is Markdown. So the check's read scope is wider than both the registration and the rule. The citation check one test above already scans `pluginMarkdown` only.

**Fix.** Narrow the roster scan to the Markdown set the suite is registered for:

1. In the test `'the plugin files naming the module equal its ## Who may cite this roster'`, change `checkRoster(moduleText, pluginFiles)` to `checkRoster(moduleText, pluginMarkdown)`.
2. In the test `'bad samples: a roster that differs from the citing files is rejected'`, change both uses of `pluginFiles` to `pluginMarkdown`: the spread in `const extra = [...pluginFiles, …]` and the `pluginFiles.filter(…)` in `const fewer = …`.
3. `pluginFiles` is now read only to build `pluginMarkdown`. Leave it as it is: it is still used, so `noUnusedLocals` does not apply, and this file is not TypeScript anyway.

**Verification:** run the one test file this fix edits, from the repository root:

```
npm test --workspace cli -- test/agent-return-schemas.test.mjs
```
