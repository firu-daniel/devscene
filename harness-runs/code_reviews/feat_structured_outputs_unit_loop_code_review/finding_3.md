### 3. The stop-condition bullets name a findings file path for a `layer-reviewer` blocker, which writes no findings file

**Files:**
- `plugin/instructions/plan_orchestration_instructions_core.md` (`## Stop conditions (halt and do NOT continue)`): the bullet "Any review loop hits `iteration >= 5` without `PASS`, or a per-unit `layer-reviewer` returns an `outcome` of `blocker`".
- `plugin/instructions/user_review_fixes_instructions_core.md` (`## Stop conditions (halt and do NOT continue)`): the same bullet, byte-identical in its first clause.

**Problem.**

This branch extended both bullets to two new cases: a `layer-reviewer` `blocker` and a third failed routing check. Each bullet still ends "— `<escalate>`, naming the latest findings file path.", and that clause now governs all three cases.

`layer-reviewer.md` writes no findings file on its `blocker` outcome (`## Read first`: "write no findings file, and stop"). A failed routing check has no path either. The section that decides the handling, `plugin/instructions/unit_loop_core.md` → `### Per-unit review step`, says to escalate "quoting `` `layer-reviewer.blocker` `` or naming the check that failed".

So the two statements disagree. An orchestrator reading the stop list is told to name a path that does not exist, or to name a stale one from an earlier iteration.

**Fix.**

In both files, replace the bullet's closing clause:

> — `<escalate>`, naming the latest findings file path.

with:

> — `<escalate>`, naming the latest findings file path on the iteration cap, and otherwise as `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `### Per-unit review step` states.

Leave the rest of each bullet unchanged. No test runs for this prose-only change beyond the tree guards the unit loop selects.
