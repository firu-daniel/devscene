### 2. Give the two lstatOrUndefined copies one owner in core

**Severity:** Must Fix

**Sites:**

- `cli/src/generators/outerLoopScripts.ts` → `lstatOrUndefined`, quoted: `if (code === 'ENOENT' || code === 'ENOTDIR') return undefined;` (added by this branch)
- `cli/src/core/writer.ts` → `lstatOrUndefined`, quoted: `if ((error as NodeJS.ErrnoException | null)?.code === 'ENOENT') return undefined;`

**Problem.** The branch adds a second function named `lstatOrUndefined`, and its body differs from the one in the write engine. The writer's copy treats only `ENOENT` as absent and throws on `ENOTDIR`. The new copy treats both as absent. A caller moved between the two modules silently changes behaviour, with no compile error.

**Rule violated.** `.claude/context/conventions.md` → `### Where a new responsibility goes` → "Before adding a copy of anything, grep for it." That paragraph describes this exact failure: private copies that "had drifted, and two divergent bodies had been given the same name — so a caller moved between those two files silently changed behaviour, with no compile error and no test". Also `.claude/context/conventions.md` → `## Shared code, and where it lives`: behaviour two `cli/src` areas need lives in `cli/src/core/`.

**Fix.** Keep both callers' current semantics and make the difference explicit at the call site.

1. In `cli/src/core/paths.ts`, export one helper and extend the module header to name it:

   ```ts
   export function lstatOrUndefined(
     path: string,
     absentCodes: readonly string[] = ['ENOENT'],
   ): ReturnType<typeof lstatSync> | undefined {
     try {
       return lstatSync(path);
     } catch (error) {
       const code = (error as NodeJS.ErrnoException | null)?.code;
       if (code !== undefined && absentCodes.includes(code)) return undefined;
       throw error;
     }
   }
   ```

2. In `cli/src/core/writer.ts`, delete the private function and import the helper from `./paths.js`. Keep the default codes: `resolveRequests` relies on `ENOTDIR` throwing, so a target under a file is refused before any request commits. Remove `lstatSync` from the `node:fs` import if nothing else there uses it.
3. In `cli/src/generators/outerLoopScripts.ts`, delete the private function, import the helper from `../core/paths.js`, and call it from `outerLoopScriptDrift` with `['ENOENT', 'ENOTDIR']`, held in a named constant. Remove `lstatSync` from the `node:fs` import.
4. In `cli/test/outer-loop-upgrade.test.mjs`, add a case where the scripts directory's `lib` is a regular file and `outerLoopScriptDrift` reports its rows as `missing`. No current test covers the `ENOTDIR` arm this change moves.
