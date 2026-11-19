### 3. Gate 13's leg comment in `run-gates.sh` is left with a broken wrap after the inserted run-copy sentence

**File:** `scripts/run-gates.sh` (the `# Gate 13's legs.` comment above `python_gate`): "a failure. 13c's bridge cases run"

The branch inserted the sentence "In a run copy, status 3 means …" and re-wrapped only the lines next to it. The comment now ends with a short line followed by a one-clause line:

```
# produce it ($2 = skip4); on any other leg the wrapper never produces it, so it falls through to
# a failure. 13c's bridge cases run
# `cli/dist`, so 13c depends on gate 2a.
```

This is style only.

**Fix:** join the last two lines so the paragraph wraps evenly:

```
# produce it ($2 = skip4); on any other leg the wrapper never produces it, so it falls through to
# a failure. 13c's bridge cases run `cli/dist`, so 13c depends on gate 2a.
```

The fix is a comment-only edit, so it runs no test.
