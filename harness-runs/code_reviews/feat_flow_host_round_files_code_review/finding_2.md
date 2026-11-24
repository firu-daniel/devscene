### 2. The host README's `## Errors` paragraph now names four failures but still says "Which exit status either becomes"

**File:** `devscene-flow-host/README.md` (`## Errors`) — "Which exit status either becomes is the caller's"

Before this branch, the paragraph named two failures: `RecordError`, and any other `OSError`, which propagates. "Either" referred to that pair. Task 9 added two more to the same paragraph: a malformed refusal record raises `ValueError` and its lock raises `TimeoutError`, and a round gate with no `findingsFolder` raises `ValueError`. The closing sentence still says "either", which now names neither the pair nor the full set.

This is wording only. Every failure the paragraph names still propagates to the caller, so no step changes.

**Fix:** in `devscene-flow-host/README.md` → `## Errors`, replace

```
Which exit status either becomes is the caller's; the package has no command line yet.
```

with

```
Which exit status each of these becomes is the caller's; the package has no command line yet.
```

The fix touches a document only, so it runs no test.
