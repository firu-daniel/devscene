### 2. `ALLOWED_LITERAL` is stripped from every plugin file, not only from the two orchestration cores its comment names

**File:** `cli/test/diff-base-corpus.test.mjs` (`ALLOWED_LITERAL`, and the `no-bare-base` case) — "const lines = text.split(ALLOWED_LITERAL).join('').split('\n');"

**Problem.** The comment above `ALLOWED_LITERAL` reads *"D.2's own no-remote fallback in the two orchestration cores — the one bare range allowed."* The `no-bare-base` case removes that literal from **every** file under `plugin/` before matching. So any other plugin file can issue `git rev-list --count <default_branch>..HEAD` as its primary command, with a bare base, and the guard passes it. The exemption is wider than the rule the suite exists to enforce, and wider than its own comment says.

**Fix.** Scope the exemption to the two files that carry D.2:

```js
/** D.2's own no-remote fallback — the one bare range allowed, and only in the two orchestration cores. */
const ALLOWED_LITERAL = 'git rev-list --count <default_branch>..HEAD';
const ALLOWED_IN = new Set([
  'plugin/instructions/plan_orchestration_instructions_core.md',
  'plugin/instructions/user_review_fixes_instructions_core.md',
]);
```

In `test('no-bare-base', …)`, replace:

```js
    const lines = text.split(ALLOWED_LITERAL).join('').split('\n');
```

with:

```js
    const body = ALLOWED_IN.has(rel) ? text.split(ALLOWED_LITERAL).join('') : text;
    const lines = body.split('\n');
```

The two paths are the files that carry D.2's `git rev-list --count <default_branch>..HEAD` today (`git grep -n 'git rev-list --count <default_branch>..HEAD' -- plugin`). This fix edits the test file, so that file is the one test the fix runs.
