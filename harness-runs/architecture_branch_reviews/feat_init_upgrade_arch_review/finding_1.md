### 1. Use the shared stringsAt instead of a private copy in the permission profile

**Severity:** Must Fix

**Site:** `cli/src/generators/permissionProfile.ts` → `stringsIn`, quoted: `function stringsIn(value: JsonValue | undefined): readonly string[]`

**Problem.** This branch adds `stringsIn`, a private function whose body is identical to `stringsAt`, which `cli/src/core/json.ts` already exports:

```ts
return Array.isArray(value) ? value.filter((entry): entry is string => typeof entry === 'string') : [];
```

`cli/src/doctor/checks.ts` and `cli/src/generators/projectSettings.ts` already import `stringsAt`. The new copy gives one behaviour a second home.

**Rule violated.** `.claude/context/conventions.md` → `## Shared code, and where it lives`: a value or behaviour two `cli/src` areas need lives in `cli/src/core/`, "never duplicated into both". Also `.claude/context/conventions.md` → `### Where a new responsibility goes`: "A responsibility that already has a home does not get a second one" and "Before adding a copy of anything, grep for it."

**Fix.** In `cli/src/generators/permissionProfile.ts`:

1. Add `stringsAt` to the existing `../core/json.js` import.
2. Delete `stringsIn` and its doc comment.
3. Replace its three calls with `stringsAt`, in `localPermissionEntries`, `existingAllowEntries` and `recordedLocalEntries`.

Behaviour does not change.
