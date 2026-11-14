### 1. Two calls waiting on a stale walker lock can both break it, so two calls hold the lock at once

**File:** `cli/templates/scripts/flow-walker.sh` (`lock_take`) — `if [ "$stale" -eq 0 ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +1 2>/dev/null)" ]; then`. Its self-adopted copy `scripts/flow-walker.sh` must stay byte-identical to the template, so it takes the same edit.

**Problem.** `lock_take` breaks a stale lock in two separate steps. First a `find` subprocess decides the lock is older than a minute. Then a separate `rmdir "$LOCK"` removes whatever directory is at that path. Nothing checks that the directory being removed is still the stale one.

The header's `# CONCURRENCY` paragraph says *"removed once as stale when older than a minute"*. The `once` is per call (the `stale` flag), not per lock. So when a killed call has left a lock behind and two calls are already waiting on it, this can happen:

1. Waiter W1's `find` prints the stale lock L0. Waiter W2's `find` prints it too.
2. W1 runs `rmdir "$LOCK"` (removes L0), then `continue`, then `mkdir "$LOCK"` succeeds. W1 now holds a fresh lock L1.
3. W2 runs its own `rmdir "$LOCK"`. That removes L1, the lock W1 holds, because L1 is an empty directory at the same path. W2 then runs `continue` and `mkdir "$LOCK"`, which succeeds.

W1 and W2 now both hold the lock. Each has read the state before the other wrote it, so the last `mv` wins and one gate's recorded outcome is lost. That breaks the guarantee the header and `cli/test/flow-walker-concurrency.test.mjs` case (1) state: *"every outcome of simultaneous `next` calls lands, exactly one call prints the round's result"*. The round then waits forever for a gate whose return the driver believes it already recorded.

This is the exact situation the stale break exists for: a recording call was killed while holding the lock, and the set's other recordings arrive together. That is the story index's first `Top risks:` entry.

Today's orchestrator records one outcome at a time, so it cannot have two waiters. A per-gate driver (#159, which `docs/flow-graph-walker.md` → `### Item 8 — a round's gates fan out, and the round node joins` → **What a second driver must do.** tells to record "concurrently") can.

**Fix.** Guard the break with a second `mkdir` lock, `$LOCK.break`. Only the call holding it re-checks the lock's age and removes the lock. Release it on every exit path, as the main lock is released.

1. In both copies, add a second flag beside `LOCK_HELD`, and release both in `lock_release`:

   ```bash
   LOCK="$STATE_FILE.lock"
   LOCK_HELD=0
   BREAK_HELD=0

   lock_release() {
     if [ "$BREAK_HELD" -eq 1 ]; then
       rmdir "$LOCK.break" 2>/dev/null
       BREAK_HELD=0
     fi
     if [ "$LOCK_HELD" -eq 1 ]; then
       rmdir "$LOCK" 2>/dev/null
       LOCK_HELD=0
     fi
   }
   ```

2. In `lock_take`, replace the whole stale block, from `if [ "$stale" -eq 0 ] && …` through its closing `fi`, with:

   ```bash
       if [ "$stale" -eq 0 ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +1 2>/dev/null)" ] \
         && mkdir "$LOCK.break" 2>/dev/null; then
         # Only the holder of the break lock re-checks and removes, so a lock
         # another waiter has just taken is never removed.
         BREAK_HELD=1
         stale=1
         if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +1 2>/dev/null)" ]; then
           rmdir "$LOCK" 2>/dev/null
         fi
         rmdir "$LOCK.break" 2>/dev/null
         BREAK_HELD=0
         continue
       fi
   ```

   A waiter that cannot take `$LOCK.break` does not break anything. It falls through to the existing `sleep 0.1` retry, and its next pass sees either the lock the breaker took or no lock.

3. In the same function, extend the give-up message so it also names the break lock. Change `remove $LOCK with rmdir` to `remove $LOCK (and $LOCK.break, if present) with rmdir`. The header's `EXIT CODES` exit-2 entry and the `# CONCURRENCY` paragraph change the same way. Replace *"removed once as stale when older than a minute"* with *"removed as stale when older than a minute, by one waiting call at a time under the sibling directory `<state_dir>/.flow_walker_state.lock.break`, which it re-checks the age under"*.

4. Add case `(4) two calls waiting on a stale lock both record their gate, and neither lock is left behind` to `cli/test/flow-walker-concurrency.test.mjs`. Build it like case (2): open the round with `run(dir, OPEN)`, plant `lockPath(dir)`, and back-date it two minutes with `utimes`. Then record two of the three gates through `runConcurrently`, `business_parity_review` and `architecture_review`, both `PASS`. Repeat this `REPETITIONS` times on fresh fixtures, as case (1) does. Assert that:
   - both calls exit 0;
   - both print `action: wait`, and their `recorded:` lines name two distinct gates;
   - `current` then prints exactly one `action: dispatch` block, whose `node:` is `plan_review`;
   - `lockPath(dir)` and `` `${lockPath(dir)}.break` `` are both absent afterwards.

   In the file's header paragraph, name the mutation that turns this case red: the stale branch without the `mkdir "$LOCK.break"` guard.

5. Run the edited test file once, as one plain foreground command from the repository root: `npm test --workspace cli -- test/flow-walker-concurrency.test.mjs`. It is the only test file this fix edits. The full suite runs later, in the Run gates phase.
