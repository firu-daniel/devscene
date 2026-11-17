### 4. `### The dispositioned outcome` still says the implementer's return "carr[ies] the marker"

**File:** `plugin/instructions/unit_loop_core.md` (`### The dispositioned outcome`), in the bullet "**What it is.**", at the quoted substring "the admissibility test that let the return carry the marker".

**Problem.**

This branch replaced the `prohibited — ` / `already passing — ` markers with outcome values. It rewrote the section's lead paragraph and its "**What already exists on disk.**" bullet to match ("the outcome is the whole decision"). The "**What it is.**" bullet two lines above still says the implementer's contract "states the admissibility test that let the return carry the marker".

No marker exists any more. A maintainer grepping for the wire this section routes on is pointed at a literal that is gone. No routing decision turns on the sentence, so this is a wording defect rather than a behaviour one.

**Fix.**

Replace:

> `layer-implementer`'s contract states the admissibility test that let the return carry the marker.

with:

> `layer-implementer`'s contract states the admissibility test that let it return that outcome.

No test runs for this prose-only change beyond the tree guards the unit loop selects.
