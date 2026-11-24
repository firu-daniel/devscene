### 1. Blank the main-checkout anchor in the npm pack test's environment

**Site:** `cli/test/python-packages-staged.test.mjs`, test `npm pack lists the staged Python files`, the `execFileSync('npm', ['pack', '--dry-run', '--json'], …)` options object holding `env: { ...process.env, npm_config_cache: cache },` (near line 119, navigation hint only).

**Failing test:** `cli/test/main-anchor-isolation.test.mjs` — `every process.env spread in a test source blanks the anchor in the same object`

**Class:** Wrong behaviour

**Failure:** If gate 4 runs `npm test`, then `every process.env spread in a test source blanks the anchor in the same object` fails with `Expected values to be strictly deep-equal`, its actual list holding `'python-packages-staged.test.mjs: ...process.env, npm_config_cache: cache '`.

**Failure as logged:**

```
not ok 717 - every process.env spread in a test source blanks the anchor in the same object
  location: 'cli/test/main-anchor-isolation.test.mjs:56:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

    + [
    +   'python-packages-staged.test.mjs: ...process.env, npm_config_cache: cache '
    + ]
    - []
  code: 'ERR_ASSERTION'
  operator: 'deepStrictEqual'
```

**Diagnosis:** New this round. Round 1's fix (commit `b9aeeb56`) gave the npm pack test its own npm cache by passing `env: { ...process.env, npm_config_cache: cache }` to `execFileSync`. The guard test scans every `.mjs` under `cli/test/` for the `...process.env` spread, takes the text from the spread up to the next `}`, and requires that slice to name `ISOLATED_ENV` or `MAIN_REPO_ANCHOR_VARIABLE` (`main-anchor-isolation.test.mjs`, the `/ISOLATED_ENV|MAIN_REPO_ANCHOR_VARIABLE/` check). The new object names neither, so the child `npm` would inherit `DEVSCENE_MAIN_REPO` from a watcher-launched session, which is the leak the guard exists to stop. Verified in the current tree: the spread is still unguarded, and `python-packages-staged.test.mjs` does not import `MAIN_REPO_ANCHOR_VARIABLE`.

**Fix:** In `cli/test/python-packages-staged.test.mjs`:

- [ ] Add `import { MAIN_REPO_ANCHOR_VARIABLE } from '../dist/core/mainRepoAnchor.js';` beside the file's other `../dist/…` imports.
- [ ] Change the options object's env to `env: { ...process.env, [MAIN_REPO_ANCHOR_VARIABLE]: '', npm_config_cache: cache },`. The blanking key must sit inside the same `{ … }` literal as the spread, before its closing `}`, because the guard reads only that slice. This is the form `cli/test/test-time-scale.test.mjs` and `cli/test/daemon.test.mjs` already use.
- [ ] Keep the `npm_config_cache` override and the temp-dir cache exactly as they are. They are round 1's fix for the sandbox `EPERM`. Change no other test, and leave the guard in `main-anchor-isolation.test.mjs` unchanged.
