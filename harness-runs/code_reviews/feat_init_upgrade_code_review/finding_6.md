### 6. `writePermissionProfile` calls `lstatSync` directly beside the shared "what is at this path" probe

**File:** `cli/src/generators/permissionProfile.ts` (`writePermissionProfile`) — "lstatSync(path, { throwIfNoEntry: false }) === undefined"

This branch moved `lstatOrUndefined` into `cli/src/core/paths.ts`, whose header now says it "is the one \"what is at this path\" probe shared across areas". The write engine uses it to decide `create-if-absent`. `writePermissionProfile` asks the same question to predict that decision, and its doc comment calls the result "the same `lstat` answer the write engine's `create-if-absent` gives", but it spells the probe separately with `lstatSync`.

The two agree today: a check on this Node version showed `lstatSync` with `throwIfNoEntry: false` still throwing `ENOTDIR`, as `lstatOrUndefined`'s default does. The defect is the second spelling of an answer the header says has one owner, and it is the only new `lstatSync` import in this module.

**Fix:** in `cli/src/generators/permissionProfile.ts`, delete `import { lstatSync } from 'node:fs';`, add `lstatOrUndefined` to the existing import from `'../core/paths.js'`, and change the line to:

```ts
  const willWrite = force === true || lstatOrUndefined(path) === undefined;
```

No test file changes, so this fix runs no test file.
