# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`finding_1.md` — the in-class accepted set does not name a literal `-` at a class edge, which four shipped patterns use.** The accepted set inside a character class lists "a literal character; a leading `^`; a `-` range between two literals; the closing `]`". Four patterns in `graphscene/src/graphscene/schemas/flow-graph.schema.json` end a class with an unranged `-`: `^[a-z][a-z0-9_-]*$`, `^[a-z][a-z-]*$`, `^[a-z][a-z0-9-]*$` and `^[a-z][a-z_-]*$`. An implementer who reads "a `-` range between two literals" as the only legal use of `-` in a class will refuse those patterns, and `_validator()` will raise the first time it is built. The plan's own `test_every_shipped_schema_pattern_is_translatable` would catch this, so it is not a silent failure. Still, the finding should say that a `-` as the first or last character of a class (after any leading `^`) is accepted as a literal, since it reads the same in both engines. Its docstring sentence should say so too. This is a correctness point outside the layering lens, so it does not gate the round.
