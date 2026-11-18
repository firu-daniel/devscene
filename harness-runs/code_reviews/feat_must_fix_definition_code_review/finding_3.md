### 3. `docs/watcher.md` omits `check-round-file` and the user-review fix-plan caller

**File:** `docs/watcher.md` (the script table's `flow-walker.sh` row) — "prints the planning loop's next action (`start`, `next`, `current`)"

The row lists the walker's subcommands as `start`, `next` and `current`, and names only the orchestrating session of a planning flow as its caller. This branch adds `check-round-file`, and `plugin/instructions/user_review_fix_plan_writing_instructions_core.md` → `## Flow` step 7 now has the user-review fix-plan flow call it. The row is descriptive and no step fails because of it, so this is a Should Fix.

**Fix:** replace the row with:

```markdown
| `flow-walker.sh` | Walks a declared flow graph and prints the planning loop's next action (`start`, `next`, `current`), and checks a review round file (`check-round-file`) | the orchestrating session of a planning flow or of a user-review fix-plan flow | **yes** |
```
