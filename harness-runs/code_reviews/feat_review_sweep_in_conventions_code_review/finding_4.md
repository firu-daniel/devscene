### 4. The generator spells the `sweep` target as an untyped literal, where `doctor` types it against the reserved list

**File:** `cli/src/generators/claudeContext.ts` (`writeClaudeContext`) — "analyzeInvocation: `${ANALYZE_COMMAND} sweep`"

**The problem.** `cli/src/doctor/checks.ts` declares `const SWEEP_TARGET: (typeof RESERVED_ANALYZE_TARGETS)[number] = 'sweep';`. It is typed against the one list that declares the reserved targets, for the reason its `LAYERS_TARGET` sibling's doc comment states: dropping the target from that list then becomes a compile error, not a remedy naming an argument the command no longer takes. The generator that owns `RESERVED_ANALYZE_TARGETS` renders the skeleton's footer invocation from a bare `'sweep'` inside a template literal. If the reserved word were renamed or removed, `doctor` would fail to compile, but the skeleton would go on telling every adopter to run a target the command refuses.

**Fix.** In `cli/src/generators/claudeContext.ts`, directly below the `RESERVED_ANALYZE_TARGETS` declaration, add:

```ts
/** The reserved target that fills {@link REVIEW_SWEEP_PATH}, typed against the list so dropping it is a compile error here. */
const SWEEP_TARGET: (typeof RESERVED_ANALYZE_TARGETS)[number] = 'sweep';
```

and change the render call to `render('review-sweep.md', { analyzeInvocation: `${ANALYZE_COMMAND} ${SWEEP_TARGET}` })`. Leave `doctor`'s own constant as it is.

The change does not alter any rendered byte. The test that already asserts the skeleton's fenced invocation is `cli/test/init.test.mjs`, but this fix edits no test file, so it runs none. The typecheck and the full suite run later, in the Run gates phase.
