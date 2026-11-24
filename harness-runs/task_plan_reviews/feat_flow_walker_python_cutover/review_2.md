# Task plan review — round 2

verdict: PASS
review_mode: converging

Round-1 Must Fix items:
- 1 (`task_7_plan.md`, concurrency case (1)'s lock assertion): resolved. The `existsSync(lockPath(dir))` check, the `lockPath` helper and its doc comment are now in `### Targets` and `**Work:**`. The rewritten header states the leftover `.lock` file as GraphScene's documented behaviour (`graphscene/src/graphscene/adapters/state_file.py` → `FileStateStore.lock`). A new verification grep holds that state.
- 2 (`task_16_plan.md`, the third verification grep): resolved. The grep is now held to the four target files. Run on today's tree, every hit sits in a case or line the task's `**Work:**` rewrites: `flow-host-provision.test.mjs` 113/122/128/143 and `setup-worktree-flow-host.test.mjs` 165/171/178/185. `cli/test/init-provision-python.test.mjs` exists, and it is a target of `task_4_plan.md`, as the new sentence says.

## Should Fix
1. **`task_7_plan.md` — the "no lock held" replacement check is vacuous, and the comment it asks for is false.** The Work makes case (1)'s existing `current` call the no-lock-held check and asks for a comment that *"a held lock would block it until the command's lock timeout and fail it"*. But `current` takes no lock:
   - `devscene-flow-host/src/devscene_flow_host/host/re_entry.py` → module docstring: *"`current_step` takes no lock and changes nothing"*;
   - `graphscene/src/graphscene/engine/walker.py` → `Walker.current` reads `self.store.read()` without `self.store.lock()`.

   A lock still held would not block `current`, so the check proves nothing about the property it names, and the comment would be false. Either drop the claim and just remove the assertion, as round 1's **Must hold** allowed, or name a call that takes the walk's lock, such as a following `next` refused for a finished round. That would still need checking against what `next` does there. Graded Should Fix: the suite still passes, and a false comment is never a Must Fix on its own.
2. **`task_7_plan.md` — imports and constants left orphaned when (2)–(4) go.** The Work lists the imports to drop as `mkdir`, `rmdir`, `utimes`, `existsSync` and `delay`. These are used only by (2)–(4) and would be left behind:
   - the imports `INIT_SCRIPTS_DIR`, `runBash`, `plantReview` and `blocksOf`;
   - the constants and helper `PLAN_WAIT`, `PLAN_PASS`, `plantStaleLock`, `WAIT_BOUND_MS` and `HOLD_MS`.

   `cli/tsconfig.json` includes only `src/**/*.ts`, so nothing fails, but the suite would carry dead code tied to the bash lock.
3. **`devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **The locks.** now contradicts Task 7.** The paragraph still says *"(1) three outcomes recorded by simultaneous next calls" holds unchanged*. Task 7 now changes (1), and Task 11, the owner of that section, rewrites only the `**Who reads this:**` line and **The walk's state.** The story index's Context sentence *"Task 7 moves exactly the suite cases it names"* has the same gap. Add **The locks.** suite sentence to Task 11's Work, or have Task 7 restate it.
