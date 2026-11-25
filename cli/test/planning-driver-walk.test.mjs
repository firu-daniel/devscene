/**
 * `pd_drive`'s walk, end to end, from the libraries `init` ships, with a stub agent CLI standing in
 * for every node session (`cli/test/helpers/planning-driver.mjs`).
 *
 * **The rule this suite enforces: the driver walks the planning graph the walker routes, launching
 * a round's three gates as one concurrent set that closes once, and a session whose return it
 * cannot take — a return failing its schema, a gate `PASS` whose schema-valid return object omits
 * the `findings_file` the round needs, or no `init` event, on each of its three attempts — is held as `error` while its siblings run to their end, then parks; one
 * whose `init` event merely lacks declared tools is not refused, and is logged. A hand-off logs the
 * `tasks_count` the writer's return object carries.** Each case is graded on `git log`, the ledger, the
 * clarification files, the calls log the stub keeps and the prompts it was handed.
 *
 * Every expected literal — a subject, a prompt's first line, a `held:` line — is written here,
 * never read from the graph, the walker or the library under test.
 */

import assert from 'node:assert/strict';
import { mkdtemp, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { INIT_SCRIPTS_DIR, runGit } from './helpers/fixture.mjs';
import { assertInOrder, BRANCH, drive, driverFixture, driverUnavailable, show } from './helpers/planning-driver.mjs';
import { walkerFixture } from './helpers/walker.mjs';

const SKIP = driverUnavailable();
const GATES = ['business-parity-reviewer', 'architecture-reviewer', 'task-plan-reviewer'];
const WRITER = 'task-plan-writer';

test('a full walk: writer, round 0 with one FAIL, revision, round 1 all PASS, hand-off', { skip: SKIP }, async (t) => {
  const f = await driverFixture(t, { script: { 'architecture-reviewer': [{ outcome: 'FAIL' }] } });
  const r = await drive(t, f);
  assert.equal(r.status, 0, show(r));

  assertInOrder(
    r.subjects,
    [
      `chore: Plan round 0 for ${BRANCH}`,
      `chore: Plan round 1 for ${BRANCH}`,
      `chore: Flow progress P1 for ${BRANCH}`,
      `chore: Flow progress P3 for ${BRANCH}`,
    ],
    show(r),
  );
  assert.ok(!r.subjects.includes(`chore: Add task plan for ${BRANCH}`), show(r));

  const ledger = await f.read(`${f.sd}/flow_progress/${BRANCH}_progress.md`);
  assert.match(ledger, /^- \[x\] P1\./m);
  assert.match(ledger, /^- \[x\] P3\./m);

  const writers = r.calls.filter((c) => c.agent === WRITER);
  assert.equal(writers.length, 2, show(r));
  const s = f.sd;
  assert.equal(
    writers[1].prompt.split('\n')[0],
    `Revise the task plan per findings at ${s}/business_parity_reviews/${BRANCH}/review_0.md, ` +
      `${s}/architecture_reviews/${BRANCH}/review_0.md, ${s}/task_plan_reviews/${BRANCH}/review_0.md.`,
  );
  for (const gate of GATES) assert.equal(r.calls.filter((c) => c.agent === gate).length, 2, gate);

  const lines = r.log.split('\n');
  assert.ok(lines.includes('[plan-drive] tasks_count: 1'), r.log);
  assert.ok(lines.includes('[plan-drive] ui_test: QA phase not enabled'), r.log);
});

test('a round\'s three gates run concurrently, and the round closes once', { skip: SKIP }, async (t) => {
  const f = await driverFixture(t, {
    script: {
      'business-parity-reviewer': [{ sleepMs: 2400 }],
      'architecture-reviewer': [{ sleepMs: 1600 }],
      'task-plan-reviewer': [{ sleepMs: 800 }],
    },
  });
  const r = await drive(t, f);
  assert.equal(r.status, 0, show(r));
  const round0 = GATES.map((agent) => r.calls.find((c) => c.agent === agent && c.index === 0));
  assert.ok(Math.max(...round0.map((c) => c.start)) < Math.min(...round0.map((c) => c.end)), JSON.stringify(round0));
  const ends = round0.map((c) => c.end);
  assert.ok(ends[2] < ends[1] && ends[1] < ends[0], `the stub finished them in reverse gates order: ${ends}`);
  assert.equal(r.subjects.filter((s) => s === `chore: Plan round 0 for ${BRANCH}`).length, 1, show(r));
});

/**
 * Round 0 with one gate's session unreadable at once and its two siblings `PASS` after a delay:
 * neither sibling is killed, and the one park names the held gate. `entries` is the held gate's
 * script, one entry per dispatch it is expected to get.
 */
async function heldCase(t, agent, entries, held, reason) {
  const others = GATES.filter((g) => g !== agent);
  const f = await driverFixture(t, {
    script: { [agent]: entries, [others[0]]: [{ sleepMs: 2000 }], [others[1]]: [{ sleepMs: 2000 }] },
  });
  const r = await drive(t, f);
  assert.equal(r.status, 3, show(r));
  assert.equal(r.calls.filter((c) => c.agent === agent).length, entries.length, show(r));
  for (const other of others) assert.equal(r.calls.filter((c) => c.agent === other).length, 1, `${other} dispatched once`);
  const held0 = r.calls.find((c) => c.agent === agent);
  for (const other of others) {
    const call = r.calls.find((c) => c.agent === other);
    assert.ok(Number.isFinite(call.end), `${other} ran to its end`);
    assert.ok(held0.end < call.end, `${agent} ended before ${other}`);
  }
  const folders = { 'business-parity-reviewer': 'business_parity_reviews', 'architecture-reviewer': 'architecture_reviews', 'task-plan-reviewer': 'task_plan_reviews' };
  for (const other of others) assert.ok(f.exists(`${f.sd}/${folders[other]}/${BRANCH}/review_0.md`), `${other}'s round file`);
  assert.deepEqual(Object.keys(r.clarifications), ['question_1.md'], show(r));
  const question = r.clarifications['question_1.md'];
  assert.ok(question.split('\n').includes(`held: ${held}`), question);
  if (reason !== undefined) assert.ok(question.includes(`- reason: ${reason}\n`), question);
  assert.ok(!r.calls.some((c) => c.agent === WRITER && c.index > 0), 'nothing dispatched after the park');
}

test('an architecture_review PASS with no findings_file on all three attempts is held as error and parks', { skip: SKIP }, async (t) => {
  const noFile = { outcome: 'PASS', findings: 'FAIL' };
  await heldCase(t, 'architecture-reviewer', [noFile, noFile, noFile], 'architecture_review error', 'PASS carries no findings_file');
});

test('a return failing its schema on all three attempts is held as error and parks', { skip: SKIP }, async (t) => {
  const invalid = { mode: 'invalid' };
  await heldCase(
    t,
    'task-plan-reviewer',
    [invalid, invalid, invalid],
    'plan_review error',
    'the return fails its schema: unknown key stub_unknown',
  );
});

test('a session with no init event on all three attempts is held as error and parks', { skip: SKIP }, async (t) => {
  const noInit = { mode: 'no-init' };
  await heldCase(t, 'business-parity-reviewer', [noInit, noInit, noInit], 'business_parity_review error', 'the agent did not resolve: no init event');
});

test('sessions whose init withholds Glob and Grep beside Bash are not refused, and each is logged', { skip: SKIP }, async (t) => {
  const f = await driverFixture(t, {
    script: { [WRITER]: [{ mode: 'withhold' }], 'architecture-reviewer': [{ mode: 'withhold' }] },
  });
  const r = await drive(t, f);
  assert.equal(r.status, 0, show(r));
  assert.ok(r.subjects.includes(`chore: Flow progress P3 for ${BRANCH}`), show(r));
  const lines = r.log.split('\n');
  assert.ok(
    lines.includes('[plan-drive] #1 plan_writer (task-plan-writer): the init event lacks declared tools [Glob, Grep] (a lacking tool is never refused)'),
    show(r),
  );
  assert.ok(
    lines.some(
      (l) =>
        l.startsWith('[plan-drive] #') &&
        l.includes('architecture_review (architecture-reviewer): the init event lacks declared tools [Glob, Grep]'),
    ),
    show(r),
  );
  const lacking = lines.filter((l) => l.includes('lacks declared tools'));
  for (const agent of ['business-parity-reviewer', 'task-plan-reviewer']) {
    assert.ok(!lacking.some((l) => l.includes(agent)), `${agent} ran with no mode\n${show(r)}`);
  }
});

test('every prompt is the copied core\'s dispatch block', { skip: SKIP }, async (t) => {
  const f = await driverFixture(t);
  const r = await drive(t, f);
  assert.equal(r.status, 0, show(r));
  const writer = r.calls.find((c) => c.agent === WRITER && c.index === 0);
  assert.equal(writer.prompt.split('\n')[0], 'Write the task plan.');
  const folders = { 'business-parity-reviewer': 'business_parity_reviews', 'architecture-reviewer': 'architecture_reviews', 'task-plan-reviewer': 'task_plan_reviews' };
  for (const gate of GATES) {
    const call = r.calls.find((c) => c.agent === gate && c.index === 0);
    assert.ok(call.prompt.split('\n').includes(`findings_folder: ${f.sd}/${folders[gate]}/${BRANCH}/`), call.prompt);
  }
});

test('a resume entering at convergence with P2 [x] and an uncommitted UI-test plan commits that plan before P3', { skip: SKIP }, async (t) => {
  const f = await driverFixture(t);
  const ledger = `${f.sd}/flow_progress/${BRANCH}_progress.md`;
  const seeded = await f.read(ledger);
  await f.write(ledger, seeded.replace('- [ ] P1.', '- [x] P1.').replace('- [ ] P2.', '- [x] P2.'));
  await f.write(`${f.sd}/story_plans/${BRANCH}_story_plan.md`, '# Story plan\n');
  const uiIndex = `${f.sd}/ui_test_plans/${BRANCH}_ui_test_plan.md`;
  const uiTest = `${f.sd}/ui_test_plans/${BRANCH}/ui_test_1.md`;
  await f.write(uiIndex, '# UI-test plan\n');
  await f.write(uiTest, '# UI test 1\n');
  const r = await drive(t, f);
  assert.equal(r.status, 0, show(r));
  assert.equal(r.calls.length, 0, show(r));
  assertInOrder(r.subjects, [`chore: Add UI-test plan for ${BRANCH}`, `chore: Flow progress P3 for ${BRANCH}`], show(r));
  const tracked = (await runGit(f.dir, ['ls-files'])).stdout.split('\n');
  assert.ok(tracked.includes(uiIndex), tracked.join('\n'));
  assert.ok(tracked.includes(uiTest), tracked.join('\n'));
});

/**
 * The driver runs outside the sandbox, so the walker it runs is the main checkout's, over the main
 * checkout's own environment: the run copy's `flow-walker.sh` and `<scriptsDir>/python/` are
 * writable from inside the sandbox, and an inherited `DEVSCENE_FLOW_HOST_ENV`,
 * `DEVSCENE_FLOW_HOST_PROJECT` or `PYTHONPATH` chooses none of it.
 */
test('the walker that runs is the main checkout\'s, whatever the run copy\'s walker and the inherited environment name', { skip: SKIP }, async (t) => {
  const main = await walkerFixture({ parity: true, qa: false, branch: BRANCH });
  t.after(main.cleanup);
  const f = await driverFixture(t, { mainRepo: main.dir, script: { [WRITER]: [{ touch: 'STOP' }] } });
  await writeFile(join(f.dir, INIT_SCRIPTS_DIR, 'flow-walker.sh'), '#!/usr/bin/env bash\nexit 9\n', 'utf8');
  const empty = await realpath(await mkdtemp(join(tmpdir(), 'planning-driver-empty-')));
  t.after(() => rm(empty, { recursive: true, force: true }));
  Object.assign(f.env, { DEVSCENE_FLOW_HOST_ENV: empty, DEVSCENE_FLOW_HOST_PROJECT: empty, PYTHONPATH: empty });

  const r = await drive(t, f);
  assert.equal(r.status, 3, show(r));
  assert.ok(!r.log.split('\n').includes('[plan-drive] walker exited 9'), show(r));
  assert.ok(r.log.split('\n').includes('[plan-drive]   | action: dispatch'), show(r));
  assert.equal(r.calls.filter((c) => c.agent === WRITER).length, 1, show(r));
});
