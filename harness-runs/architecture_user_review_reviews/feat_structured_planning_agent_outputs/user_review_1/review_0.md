# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`finding_1.md` and `finding_2.md` — the `_(layer: cli, plugin, general)_` order runs a layer's own test before the layer that writes what that test reads.** Source: `.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent` ("Contract before consumer, always"), and `plugin/instructions/unit_loop_core.md` → `#### Shared — multi-layer fixes run bottom-up` together with `## The test-run rule` points 3 and 7.
   - Finding 1: the `cli` layer runs first. It rewrites `cli/test/agent-return-schemas.test.mjs` to read `plugin/schemas/<agent>.return.json` and to reject any agent that still carries `## Return schema`, then has to run that file (point 3). At that point the `plugin` layer has not yet created the schema files or removed the inline sections, so the run fails on plugin-layer files the `cli` implementer may not edit. Putting `plugin` first does not fix this on its own. The plugin edit triggers the `plugin/**/*.md` tree guard, which still runs the old suite, and that suite's graph check fails as soon as the six `## Return schema` sections are gone.
   - Finding 2: the `cli` layer repoints `canonicalSentence` to `docs/structured-agent-returns.md` → `### The return block`. That section is written only by the `general` layer, which runs last, so the `cli` layer's own run fails on a file it does not own.
   - Not graded Must Fix: no single tag order clears both findings, and the conventions documents name no resolution for an atomic cross-layer move. The writer should still state in each finding which layer's test is expected to fail until a later layer of the same unit lands, or restructure the steps, so that no implementer treats that failure as its own to fix outside its layer. For example, Finding 2 could copy the authoring sections into the docs home in a step that precedes the suite repoint.

## Nice to Have

1. **`finding_2.md` — the new `treeGuards` entry `{ "test": "test/agent-return-schemas.test.mjs", "covers": "docs/structured-agent-returns.md" }` registers a guard for a single fixed file.** Source: `plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 8 ("a test reading one fixed file is not a tree guard and owes no entry"). The entry is allowed and does no harm, but the rule does not require it. Keep it only if triggering the suite on an edit to that document is wanted.
