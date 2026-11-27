/**
 * The flow walker's parallel round, driven through the walker's CLI alone, as a second driver would:
 * `start` and `next --node`, with no orchestrator prose between the calls.
 *
 * **The rule this suite exists to enforce: a round's due gates are dispatched as one set, their
 * outcomes are recorded in any order, the round closes exactly once at the last of them, and an
 * outcome the round does not await is refused and changes nothing; a gate's invalid round file
 * records no verdict, never reaches the writer, and sends that gate back within the same round until
 * its third refusal escalates.** The set, the join and the held
 * binding are cited from the shipped walker's own header (`cli/templates/scripts/flow-walker.sh` →
 * `# ROUNDS`, `# OUTPUT` and `# EXIT CODES`); a refusal is asserted on the state file's bytes, as
 * `cli/test/config-command.test.mjs`'s are (`.claude/context/cli.md` → `## What "done" means here`).
 * Every expected action is a literal written here and never read out of the walker's graph.
 *
 * Not covered here, deliberately: the cap, the review mode, resuming a saved walk and gates recorded
 * by simultaneous calls. Those are other suites'.
 *
 * Every fixture repository is built under the system temp directory and torn down in process; no
 * case is ever aimed at this checkout (`.claude/context/conventions.md` → `## The testing bar`).
 */

import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { appendFile } from 'node:fs/promises';
import { join } from 'node:path';
import test from 'node:test';

import { createFixture, INIT_SCRIPTS_DIR, runBash } from './helpers/fixture.mjs';
import {
  blocksOf,
  mustFixSection,
  plantMalformedReview,
  plantReview,
  run,
  walk,
  walkerFixture,
  walkerStatePath,
  walkerUnavailable,
  WALKER_FLOW,
} from './helpers/walker.mjs';

const SKIP = walkerUnavailable();
const BRANCH = 'feat_x';

// `## Safety contract` step 3: "[plan-write · iter <i>] → <agent_name>  (#<total_dispatches>)".
const PLAN_WRITE_HB = (agent) => ['heartbeat', `[plan-write · iter 0] → ${agent}  (#<total_dispatches>)`];

/** `### 1. Spawn task-plan-writer`, first iteration, feeding round 0. */
const WRITER = [
  ['action', 'dispatch'],
  ['node', 'plan_writer'],
  ['agent', 'task-plan-writer'],
  ['prompt', 'initial'],
  ['arg.iteration', '0'],
  PLAN_WRITE_HB('task-plan-writer'),
];

/**
 * A round-0 gate's dispatch block at counter 0: `# OUTPUT`, `dispatch` — "arg.iteration: (a round
 * gate: the round number)" and "arg.review_mode: full|converging (a round gate: `full` while the
 * counter is below the round node's `convergingFrom`)".
 */
function block(node, agent, heartbeat, passed = []) {
  return [
    ['action', 'dispatch'],
    ['node', node],
    ['agent', agent],
    ['arg.iteration', '0'],
    ['arg.review_mode', 'full'],
    ...passed,
    heartbeat,
  ];
}

const PARITY_BLOCK = (passed) =>
  block('business_parity_review', 'business-parity-reviewer', [
    'heartbeat',
    '[plan-write · parity · iter 0] → business-parity-reviewer  (#<total_dispatches>)',
  ], passed);
const ARCH_BLOCK = (passed) =>
  block('architecture_review', 'architecture-reviewer', [
    'heartbeat',
    '[plan-write · arch · iter 0] → architecture-reviewer  (#<total_dispatches>)',
  ], passed);
const PLAN_BLOCK = (passed) => block('plan_review', 'task-plan-reviewer', PLAN_WRITE_HB('task-plan-reviewer'), passed);

/** `# ROUNDS`: "until the last one the walker prints `wait`" — `# OUTPUT`, `wait`. */
function wait(recorded, pending) {
  return [
    ['action', 'wait'],
    ['node', 'plan_round'],
    ['recorded', recorded],
    ...pending.map((name) => ['pending', name]),
  ];
}

/**
 * The join's `PASS` with `phases.qa` off: `## UI-test-plan write loop`, "Skip this loop unless
 * `phases.qa` is `true`", so the round's close hands off; `report:` lines follow `gates` order
 * whatever order the outcomes were recorded in.
 */
function handoff(parityReport) {
  return [
    ['action', 'binding'],
    ['binding', '<terminal_handoff>'],
    ['node', 'convergence'],
    ['report', `business_parity_review ${parityReport}`],
    ['report', 'architecture_review passed'],
    ['report', 'plan_review passed'],
    ['report', 'ui_test qa-phase-off'],
    ['round', '0 PASS'],
    ['ledger', 'P1'],
    ['skip', 'ui_writer skipped'],
  ];
}

const PARITY = { node: 'business_parity_review', outcome: 'PASS', review: ['business_parity_reviews', 0] };
const ARCH = { node: 'architecture_review', outcome: 'PASS', review: ['architecture_reviews', 0] };
const PLAN = { node: 'plan_review', outcome: 'PASS', review: ['task_plan_reviews', 0] };

const OPEN = [{ start: true }, { outcome: 'returned' }];

async function fixture(t, phases) {
  const fx = await walkerFixture({ ...phases, branch: BRANCH });
  t.after(fx.cleanup);
  return fx.dir;
}

/** One `next` call's argument vector, the flags the helper's `run` would pass. */
const nextArgs = (...flags) => ['next', '--flow', WALKER_FLOW, '--branch', BRANCH, ...flags, '--skipped', 'none'];

/**
 * `# EXIT CODES`: a refusal exits 1, prints one `flow-walker: <cause>` line and leaves the state file byte-identical.
 * Each `cause` is GraphScene's wording, not the bash walker's (`devscene-flow-host/README.md` →
 * `## Differences from flow-walker.sh` → **Refusal texts no caller parses.**).
 */
async function assertRefused(dir, args, cause) {
  const before = readFileSync(walkerStatePath(dir));
  const refused = await walk(dir, args);
  assert.equal(refused.status, 1, `\`${args.join(' ')}\` exited ${refused.status}\n${refused.stderr}`);
  assert.equal(refused.stdout, '');
  assert.match(refused.stderr, /^flow-walker: [^\n]*\n$/);
  assert.match(refused.stderr, cause);
  assert.deepEqual(readFileSync(walkerStatePath(dir)), before);
}

test("(1) the writer's return dispatches every non-skipped gate as one set", { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  const actions = await run(dir, OPEN);

  assert.deepEqual(actions[0], WRITER);
  // `# ROUNDS`: "every gate not skipped is due, all dispatched at once as one SET"; `# OUTPUT`, `set`:
  // "one dispatch block per due gate, in `gates` order, back to back".
  const blocks = blocksOf(actions[1]);
  assert.equal(blocks.length, 3);
  assert.deepEqual(blocks, [PARITY_BLOCK(), ARCH_BLOCK(), PLAN_BLOCK()]);
  // `# ROUNDS`: the round number "is the same index in every gate's folder".
  assert.deepEqual(new Set(blocks.map((b) => b.find(([k]) => k === 'arg.iteration')[1])), new Set(['0']));
});

test('(2) outcomes recorded in any order close the round only at the last', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  const actions = await run(dir, [...OPEN, PLAN, PARITY, ARCH]);

  assert.deepEqual(actions.slice(2), [
    // `# ROUNDS`: "Each gate's outcome is recorded by its own `next --node <gate>`, in any order" —
    // `pending:` names the gates still out, in `gates` order, whichever was recorded.
    wait('plan_review PASS', ['business_parity_review', 'architecture_review']),
    wait('business_parity_review PASS', ['architecture_review']),
    // "The last outcome is the JOIN": no gate recorded `FAIL`, so the round closes `PASS`, once.
    handoff('passed'),
  ]);
  assert.equal(actions.flat().filter(([k]) => k === 'round').length, 1, 'the round closed more than once');
});

test('(3) an outcome for a gate not pending in the round, or a second outcome for one gate, is refused and changes no state', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  await run(dir, [...OPEN, PLAN]);

  // `# EXIT CODES`, 1: "while a set is pending: … a `--node` that is not a pending gate of the round".
  await assertRefused(dir, nextArgs('--node', 'plan_writer', '--outcome', 'returned'), /not pending in round 0/);
  // … "a second outcome for one gate": `plan_review`'s `PASS` is recorded; its own file is re-offered.
  const planFile = `devscene/task_plan_reviews/${BRANCH}/review_0.md`;
  await assertRefused(
    dir,
    nextArgs('--node', 'plan_review', '--outcome', 'PASS', '--findings', planFile),
    /already recorded in round 0/,
  );
});

test('(4) a skipped gate is absent from the set and counts as passed', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: false, qa: false });
  const actions = await run(dir, [...OPEN, ARCH, PLAN]);

  // `# ROUNDS`: "each gate's skip constructs are evaluated in `gates` order before anything is
  // printed"; `# OUTPUT`, `set`: "the passed-through skip: … lines in the first block only".
  assert.deepEqual(blocksOf(actions[1]), [ARCH_BLOCK([['skip', 'business_parity_review skipped']]), PLAN_BLOCK()]);
  assert.deepEqual(actions[2], wait('architecture_review PASS', ['plan_review']));
  // "the round closes FAIL when a gate recorded FAIL (a skipped gate counts as passed), else PASS".
  assert.deepEqual(actions[3], handoff('skipped'));
});

test("(5) a gate's error with two verdicts recorded is held until the set is in, then escalates once, and the round files stand", { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  const actions = await run(dir, [...OPEN, { node: 'architecture_review', outcome: 'error' }, PARITY, PLAN]);

  assert.deepEqual(actions.slice(2), [
    // `# ROUNDS`: an `error` is "HELD, not routed when recorded" — the set still waits.
    wait('architecture_review error', ['business_parity_review', 'plan_review']),
    wait('business_parity_review PASS', ['plan_review']),
    // `# OUTPUT`, `binding`: "at a join with a held outcome, node: and agent: are the first held
    // gate's in `gates` order, reason: its outcome, then held: <gate> <outcome> per held gate, and
    // no round: line".
    [
      ['action', 'binding'],
      ['binding', '<escalate>'],
      ['node', 'architecture_review'],
      ['agent', 'architecture-reviewer'],
      ['reason', 'error'],
      ['held', 'architecture_review error'],
    ],
  ]);
  // "the first held gate's binding is printed and the round is not closed": the two verdicts' files
  // are not withdrawn.
  for (const folder of ['business_parity_reviews', 'task_plan_reviews']) {
    const file = join(dir, 'devscene', folder, BRANCH, 'review_0.md');
    assert.ok(existsSync(file), `${file} is absent`);
  }
  // `# USAGE`: a binding other than `<ask>` is "a finished walk … `next` refuses it with exit 1".
  await assertRefused(dir, nextArgs('--node', 'architecture_review', '--outcome', 'PASS'), /the walk has finished/);
});

test('(6) --node is required while a set is pending', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  await run(dir, OPEN);
  const findings = await plantReview(dir, `architecture_reviews/${BRANCH}`, 0, 'PASS');

  // `# USAGE`, `--node`: "Required while a set is pending"; `# EXIT CODES`, 1: "no `--node`".
  await assertRefused(dir, nextArgs('--outcome', 'PASS', '--findings', findings), /name the gate with node/);
});

const LACKS_CLASS = 'Must Fix entry 1 lacks **Class:**';

/** `# OUTPUT`: "refused: <gate> attempt <n> of 3: <reason>". */
const refusedLine = (gate, attempt, reason = LACKS_CLASS) => ['refused', `${gate} attempt ${attempt} of 3: ${reason}`];

/** `wait` after a refusal: `# OUTPUT`, the `refused:` line stands where `recorded:` would. */
function refusedWait(line, pending) {
  return [['action', 'wait'], ['node', 'plan_round'], line, ...pending.map((name) => ['pending', name])];
}

/** A gate's `FAIL` return naming a round file whose one Must Fix entry lacks `**Class:**`. */
async function returnMalformed(dir, node, folder) {
  const findings = await plantMalformedReview(dir, `${folder}/${BRANCH}`, 0, 'Class');
  const result = await walk(dir, nextArgs('--node', node, '--outcome', 'FAIL', '--findings', findings));
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  return result.action;
}

const malformedPlan = (dir) => returnMalformed(dir, 'plan_review', 'task_plan_reviews');
const malformedArch = (dir) => returnMalformed(dir, 'architecture_review', 'architecture_reviews');

test('(7) a refused gate waits for its siblings, then is dispatched alone in the same round', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  await run(dir, OPEN);

  // `# OUTPUT`, `wait`: "a gate marked for re-dispatch is not out", so `plan_review` is not listed.
  assert.deepEqual(
    await malformedPlan(dir),
    refusedWait(refusedLine('plan_review', 1), ['business_parity_review', 'architecture_review']),
  );
  const [parity, last] = await run(dir, [PARITY, ARCH]);
  assert.deepEqual(parity, wait('business_parity_review PASS', ['architecture_review']));
  // `# ROUNDS`: "dispatched again as one set, in the same round": `arg.iteration` and the heartbeat's
  // counter stay 0, and neither a `round:` line nor a writer block appears.
  assert.deepEqual(last, PLAN_BLOCK([refusedLine('plan_review', 1)]));
});

test("(8) a corrected return closes the round and the writer is handed the replaced file", { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  await run(dir, OPEN);
  await malformedPlan(dir);
  await run(dir, [PARITY, ARCH]);

  const [closed] = await run(dir, [{ node: 'plan_review', outcome: 'FAIL', review: ['task_plan_reviews', 0] }]);
  const planFile = `devscene/task_plan_reviews/${BRANCH}/review_0.md`;
  assert.deepEqual(closed, [
    ['action', 'dispatch'],
    ['node', 'plan_writer'],
    ['agent', 'task-plan-writer'],
    ['prompt', 'revision'],
    ['arg.iteration', '1'],
    ['arg.findings_file', `devscene/business_parity_reviews/${BRANCH}/review_0.md`],
    ['arg.findings_file', `devscene/architecture_reviews/${BRANCH}/review_0.md`],
    ['arg.findings_file', planFile],
    ['round', '0 FAIL'],
    ['heartbeat', '[plan-write · iter 1] → task-plan-writer  (#<total_dispatches>)'],
  ]);
  assert.match(readFileSync(join(dir, planFile), 'utf8'), /\*\*Class:\*\*/);
});

test('(9) two refused gates come back as one set', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: false, qa: false });
  await run(dir, OPEN);

  assert.deepEqual(await malformedArch(dir), refusedWait(refusedLine('architecture_review', 1), ['plan_review']));
  // `# OUTPUT`, `set`: the `refused:` lines sit among the first block's passed-through lines.
  assert.deepEqual(blocksOf(await malformedPlan(dir)), [
    ARCH_BLOCK([
      ['skip', 'business_parity_review skipped'],
      refusedLine('architecture_review', 1),
      refusedLine('plan_review', 1),
    ]),
    PLAN_BLOCK(),
  ]);
});

test('(10) the third refusal of a gate escalates and never reaches the writer', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: false, qa: false });
  await run(dir, [...OPEN, ARCH]);
  const skippedParity = ['skip', 'business_parity_review skipped'];

  assert.deepEqual(await malformedPlan(dir), PLAN_BLOCK([skippedParity, refusedLine('plan_review', 1)]));
  assert.deepEqual(await malformedPlan(dir), PLAN_BLOCK([skippedParity, refusedLine('plan_review', 2)]));
  assert.deepEqual(await malformedPlan(dir), [
    ['action', 'binding'],
    ['binding', '<escalate>'],
    ['node', 'plan_review'],
    ['agent', 'task-plan-reviewer'],
    ['reason', 'error'],
    ['held', 'plan_review error'],
    refusedLine('plan_review', 3),
  ]);
});

test('(11) `current` during the wait leaves out the refused gate, which the join re-dispatches', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  await run(dir, OPEN);
  await malformedPlan(dir);

  const current = await walk(dir, ['current', '--flow', WALKER_FLOW, '--branch', BRANCH]);
  assert.equal(current.status, 0, current.stderr);
  assert.deepEqual(blocksOf(current.action), [PARITY_BLOCK(), ARCH_BLOCK()]);
});

test('(12) a PASS file carrying a numbered Must Fix entry is refused and records no verdict', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  await run(dir, OPEN);
  const findings = await plantReview(dir, `task_plan_reviews/${BRANCH}`, 0, 'PASS');
  await appendFile(join(dir, findings), mustFixSection(), 'utf8');

  const result = await walk(dir, nextArgs('--node', 'plan_review', '--outcome', 'PASS', '--findings', findings));
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(
    result.action,
    refusedWait(
      refusedLine('plan_review', 1, 'verdict: PASS with a numbered entry under ## Must Fix'),
      ['business_parity_review', 'architecture_review'],
    ),
  );
  assert.doesNotMatch(readFileSync(walkerStatePath(dir), 'utf8'), /^round\.verdict\.plan_review=/m);
});

test('(13) check-round-file answers by exit status, with no walk and no configuration read', { skip: SKIP }, async (t) => {
  const dir = await fixture(t, { parity: true, qa: false });
  const check = (...flags) => walk(dir, ['check-round-file', ...flags]);
  const assertExit = (result, status, stderr) => {
    assert.deepEqual({ status: result.status, stdout: result.stdout, stderr: result.stderr }, { status, stdout: '', stderr });
  };

  const valid = await plantReview(dir, `task_plan_reviews/${BRANCH}`, 0, 'PASS');
  assertExit(await check('--findings', valid), 0, '');
  assertExit(await check('--findings', join(dir, valid)), 0, '');

  const invalid = await plantMalformedReview(dir, `architecture_reviews/${BRANCH}`, 0, 'Class');
  assertExit(await check('--findings', invalid), 3, `flow-walker: ${invalid}: ${LACKS_CLASS}\n`);
  assertExit(await check('--findings', 'devscene/absent.md'), 3, 'flow-walker: devscene/absent.md: no single verdict line\n');

  assertExit(await check('--flow', WALKER_FLOW, '--findings', valid), 1, "flow-walker: '--flow' is not a flag of 'check-round-file'\n");
  assertExit(await check('--branch', BRANCH, '--findings', valid), 1, "flow-walker: '--branch' is not a flag of 'check-round-file'\n");
  assertExit(await check(), 1, 'flow-walker: missing required flag --findings\n');

  const outside = await createFixture({ git: false });
  t.after(outside.cleanup);
  const walker = join(dir, INIT_SCRIPTS_DIR, 'flow-walker.sh');
  assertExit(
    await runBash(outside.dir, [walker, 'check-round-file', '--findings', 'review_0.md']),
    2,
    'flow-walker: not inside a git repository\n',
  );
  assert.equal(existsSync(walkerStatePath(dir)), false, 'check-round-file wrote walker state');
});
