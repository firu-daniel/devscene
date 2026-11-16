### 5. Step 4a adds its own narration line, `PLANNING HANDED TO SCRIPT: <branch>`, which nothing reads

**File:** `plugin/commands/branch-start-plan-autonomous.md` (`## Steps`, step 4a, sub-step 3) — "3. Emit `PLANNING HANDED TO SCRIPT: <branch>` to the run log and end the session."

**The problem.** `.claude/context/plugin.md` → `## Wires: dispatch in, return out` says *"Narration surfaces are prescribed, and an asset adds none of its own."* The channels it lists are the pre-dispatch heartbeat line, the Done-summary disclosure line and a guard's single JSON object. Step 4a's sub-step 3 adds another: a fixed-format line the setup session writes to the run log.

The line has no reader. A `git grep -nF 'PLANNING HANDED TO SCRIPT'` over the repository, run-artifact tree excluded, finds this step and nothing else. `cli/templates/scripts/autonomous-watcher.sh` does not key on it, and neither does any library under `cli/templates/scripts/lib/`, `docs/watcher.md`'s account of the three-session sequence or any test. The watcher decides whether to run the driver from the setup session's exit and the ledger it wrote. So the line is not a hand-off signal, though its wording reads like one. A maintainer reading the step will take it as a wire the watcher matches. They will carry it byte-for-byte through every edit, or look for a reader that does not exist.

The other wire literal in step 4a, `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH`, does have a reader. It matches the watcher's `planning_clause` in `spawn_engine` byte for byte, and this finding does not touch it.

**Fix.** In step 4a, replace sub-step 3 with:

```markdown
   3. End the session.
```

No test covers this prose, so the fix runs no test.
