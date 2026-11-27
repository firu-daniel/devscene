/**
 * The flow walker's round, recorded by simultaneous calls: several sessions each issue their own
 * gate's `next --node` at the same moment, as a per-gate driver does.
 *
 * **The rule this suite exists to enforce: recording is safe under concurrent calls — every outcome
 * of simultaneous `next` calls lands and exactly one call prints the round's result.** It is asserted
 * only where a driver can observe it: the outcomes, the single result, and a later `current` that a
 * held lock would block. Lock waiting and timeouts are pinned by
 * `devscene-flow-host/tests/test_flow_walker_concurrency.py`.
 *
 * Deliberately not covered here: breaking a stale lock, waiting on a fresh lock directory, and two
 * waiters on a stale lock. The command's `flock` locks die with their process, so there is no stale
 * lock to break and no lock directory to plant (`devscene-flow-host/README.md` →
 * `## Differences from flow-walker.sh` → **The locks.**). A `.lock` file left beside the state file
 * after a walk is GraphScene's documented behaviour and harmless:
 * `graphscene/src/graphscene/adapters/state_file.py` → `FileStateStore.lock` releases it and never
 * unlinks it.
 *
 * Every fixture repository is built under the system temp directory and torn down in process; no
 * case is ever aimed at this checkout (`.claude/context/conventions.md` → `## The testing bar`).
 */

import assert from 'node:assert/strict';
import test from 'node:test';

import {
  run,
  runConcurrently,
  walk,
  walkerFixture,
  walkerUnavailable,
  WALKER_FLOW,
} from './helpers/walker.mjs';

const SKIP = walkerUnavailable();
const BRANCH = 'feat_x';

/**
 * Fresh fixtures per verdict mix. A lost update needs two calls to interleave between reading and
 * replacing the state, which a single run may not hit, so one green run proves nothing.
 */
const REPETITIONS = 5;

const OPEN = [{ start: true }, { outcome: 'returned' }];

const gate = (node, folder, outcome) => ({ node, outcome, review: [folder, 0] });

const roundLines = (action) => action.filter(([k]) => k === 'round').map(([, v]) => v);

async function fixture(t) {
  const fx = await walkerFixture({ parity: true, qa: false, branch: BRANCH });
  t.after(fx.cleanup);
  return fx.dir;
}

test("(1) three outcomes recorded by simultaneous next calls all land, and exactly one prints the round's result", { skip: SKIP }, async (t) => {
  const mixes = [
    { name: 'three PASS', archOutcome: 'PASS', round: '0 PASS' },
    // `# ROUNDS`: "the round closes FAIL when a gate recorded FAIL".
    { name: 'two PASS and one FAIL', archOutcome: 'FAIL', round: '0 FAIL' },
  ];
  for (const mix of mixes) {
    for (let i = 0; i < REPETITIONS; i += 1) {
      await t.test(`${mix.name}, repetition ${i + 1} of ${REPETITIONS}`, async (st) => {
        const dir = await fixture(st);
        await run(dir, OPEN);

        const results = await runConcurrently(dir, [
          gate('business_parity_review', 'business_parity_reviews', 'PASS'),
          gate('architecture_review', 'architecture_reviews', mix.archOutcome),
          gate('plan_review', 'task_plan_reviews', 'PASS'),
        ]);

        for (const r of results) assert.equal(r.status, 0, `a simultaneous next exited ${r.status}\n${r.stdout}\n${r.stderr}`);
        // `# ROUNDS`: "until the last one the walker prints `wait`"; the last outcome is the join.
        const closers = results.filter((r) => roundLines(r.action).length > 0);
        assert.equal(closers.length, 1, `expected one call to print the round's result, got ${closers.length}`);
        assert.deepEqual(roundLines(closers[0].action), [mix.round]);
        const waits = results.filter((r) => r !== closers[0]);
        for (const w of waits) assert.deepEqual(w.action[0], ['action', 'wait']);
        // Every outcome landed: the two waits recorded two distinct gates, the join the third.
        const recorded = waits.map((w) => w.action.find(([k]) => k === 'recorded')[1].split(' ')[0]);
        assert.equal(new Set(recorded).size, 2, `the waits recorded ${recorded.join(', ')}`);

        // The no-lock-held check: a lock still held once the calls returned would block this call
        // until the command's lock timeout and fail it.
        const current = await walk(dir, ['current', '--flow', WALKER_FLOW, '--branch', BRANCH]);
        assert.equal(current.status, 0, current.stderr);
        assert.equal(current.stdout, closers[0].stdout);
      });
    }
  }
});
