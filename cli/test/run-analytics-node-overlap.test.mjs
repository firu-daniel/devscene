/**
 * The written `run-analytics.sh` over a run whose planning node sessions overlapped in time, run
 * from the root of a fixture `init` adopted.
 *
 * **The rule these tests exist to enforce: the run's wall, active, idle and host-suspended time
 * count overlapping sessions' time once, while cost and tokens stay summed; engine and planning
 * node sessions are counted apart and classed only from the driver's node-session manifest; and
 * sessions that never overlap roll up to exactly their sums, as before.** The roll-up method is
 * `lib/run-analytics-report.jq` → `RUN TIME`; the manifest is `run-analytics.sh` → `NODE SESSIONS`.
 *
 * Hand-computed values (threshold 60 s; timestamps are 2026-01-01, UTC, written mm:ss after 00:00):
 *
 *   engine `e1`        00:00 → 01:00, events every 30 s: wall 60 000, idle 0, duration 60 000.
 *   `1-architecture_review` (`n-arch`) 12:00 → 18:00, events 12:00, 12:30, 16:00, 16:30, 18:00:
 *                      gaps 12:30–16:00 (210 000) and 16:30–18:00 (90 000); wall 360 000,
 *                      idle 300 000, active 60 000, duration 360 000 (host-suspended 0).
 *   `1-business_parity_review` (`n-bpr`) 10:00 → 20:00, events 10:00, 10:30, 15:00, 20:00:
 *                      gaps 10:30–15:00 (270 000) and 15:00–20:00 (300 000); wall 600 000,
 *                      idle 570 000, active 30 000, duration 540 000 (host-suspended 60 000).
 *   `2-plan_review` (`n-plan`) 19:00 → 25:00, events 19:00, 19:30, 25:00: gap 19:30–25:00
 *                      (330 000); wall 360 000, idle 330 000, active 30 000, duration 300 000
 *                      (host-suspended 60 000).
 *
 *   The three nodes form one cluster, 10:00 → 25:00: wall 900 000. Their non-idle stretches are
 *   10:00–10:30, 12:00–12:30, 16:00–16:30 and 19:00–19:30, 120 000 in all, so the cluster's idle is
 *   780 000. Its host-suspended time is the largest member's, 60 000.
 *   Run: wall 60 000 + 900 000 = 960 000; active 60 000 + 120 000 = 180 000; idle 780 000;
 *   host-suspended 60 000. Summed session wall 60 000 + 360 000 + 600 000 + 360 000 = 1 380 000.
 *   Cost 0.5 + 0.125 + 0.25 + 0.0625 = 0.9375. Tokens (input / output / cache read / cache write):
 *   10/100/1000/50, 30/300/3000/70, 20/200/2000/60, 40/400/4000/80 → 100 / 1000 / 10 000 / 260.
 *
 * The stream holds the sessions in reap order — engine, then `n-arch`, `n-bpr`, `n-plan` — as
 * the planning driver, `devscene-planning-driver`, appends each node's stream when it ends.
 */

import assert from 'node:assert/strict';
import { appendFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { createFixture, INIT_SCRIPTS_DIR, readJson, runBash, runCli } from './helpers/fixture.mjs';

const BRANCH = 'feat_x';
const SCRIPT = join(INIT_SCRIPTS_DIR, 'run-analytics.sh');

const at = (mmss) => `2026-01-01T00:${mmss}.000Z`;

/** One session: init, a user prompt at the first time, assistants at the rest, a result at the last. */
function session(id, times, { duration, cost, usage }) {
  const [first, ...rest] = times;
  const last = rest.pop();
  return [
    { type: 'system', subtype: 'init', session_id: id },
    { type: 'user', timestamp: at(first), message: { role: 'user', content: 'Go.' } },
    ...rest.map((t, i) => ({ type: 'assistant', timestamp: at(t), message: { id: `${id}-m${i}`, content: [] } })),
    {
      type: 'result',
      subtype: 'success',
      timestamp: at(last),
      duration_ms: duration,
      total_cost_usd: cost,
      usage: {
        input_tokens: usage[0],
        output_tokens: usage[1],
        cache_read_input_tokens: usage[2],
        cache_creation_input_tokens: usage[3],
      },
    },
  ];
}

const lines = (events) => events.map((e) => JSON.stringify(e)).join('\n') + '\n';

const ENGINE = session('e1', ['00:00', '00:30', '01:00'], { duration: 60000, cost: 0.5, usage: [10, 100, 1000, 50] });
const NODES = [
  session('n-arch', ['12:00', '12:30', '16:00', '16:30', '18:00'], { duration: 360000, cost: 0.125, usage: [30, 300, 3000, 70] }),
  session('n-bpr', ['10:00', '10:30', '15:00', '20:00'], { duration: 540000, cost: 0.25, usage: [20, 200, 2000, 60] }),
  session('n-plan', ['19:00', '19:30', '25:00'], { duration: 300000, cost: 0.0625, usage: [40, 400, 4000, 80] }),
];
const MANIFEST = [
  { session_id: 'n-arch', seq: '1', node: 'architecture_review' },
  { session_id: 'n-bpr', seq: '1', node: 'business_parity_review' },
  { session_id: 'n-plan', seq: '2', node: 'plan_review' },
];

/** An adopted fixture with an empty stream, and writers for the stream and the manifest. */
async function adopted(t) {
  const fixture = await createFixture({
    files: {
      'package.json': { name: 'fixture-project', private: true, version: '0.0.0', scripts: { test: 'echo test' } },
      'README.md': '# fixture project\n',
    },
  });
  t.after(fixture.cleanup);
  const { dir } = fixture;
  const init = await runCli(dir, ['init']);
  assert.equal(init.status, 0, `init exited ${init.status}\n${init.stdout}\n${init.stderr}`);
  const claudeHome = await mkdtemp(join(tmpdir(), 'run-analytics-node-home-'));
  t.after(() => rm(claudeHome, { recursive: true, force: true }));

  const { stateDir } = readJson(join(dir, 'devscene.config.json'));
  const logs = join(dir, stateDir, 'autonomous_logs');
  mkdirSync(join(logs, `${BRANCH}.planning`), { recursive: true });
  const streamRel = join(stateDir, 'autonomous_logs', `${BRANCH}.stream.jsonl`);
  const streamPath = join(dir, streamRel);
  writeFileSync(streamPath, '');
  const manifestPath = join(logs, `${BRANCH}.planning`, 'node-sessions.jsonl');
  const outDir = join(dir, stateDir, 'run_analytics', BRANCH);
  const jsonPath = join(outDir, 'run-analytics.json');
  return {
    jsonPath,
    mdPath: join(outDir, 'run-analytics.md'),
    append: (events) => appendFileSync(streamPath, lines(events)),
    manifest: (entries) => writeFileSync(manifestPath, entries.map((e) => (typeof e === 'string' ? e : JSON.stringify(e))).join('\n') + '\n'),
    run: () =>
      runBash(dir, [join(dir, SCRIPT), streamRel, BRANCH], {
        RUN_ANALYTICS_SUSPEND_SOURCE: 'none',
        RUN_ANALYTICS_IDLE_SECS: '60',
        CLAUDE_CONFIG_DIR: claudeHome,
      }),
    doc: () => readJson(jsonPath),
  };
}

const output = (r) => `exit ${r.status}\n${r.stdout}\n${r.stderr}`;

async function recorded(f, n) {
  const r = await f.run();
  assert.equal(r.status, 0, output(r));
  assert.equal(r.stdout, `recorded ${n} session(s) for ${BRANCH}\n`, output(r));
}

/** The figures the roll-up summed before schema 4. */
const summed = (sessions, key) => sessions.reduce((a, s) => a + s.time[key], 0);

test('overlapping node sessions: union time, summed cost and tokens, split counts, each node listed', async (t) => {
  const f = await adopted(t);
  f.append([...ENGINE, ...NODES.flat()]);
  f.manifest(['not a manifest line', ...MANIFEST]);
  await recorded(f, 4);
  const doc = f.doc();
  assert.equal(doc.schema, 4);

  await t.test('each session is classed from the manifest', () => {
    assert.deepEqual(doc.sessions.map((s) => [s.session_id, s.kind, s.node]), [
      ['e1', 'engine', null],
      ['n-arch', 'planning_node', '1-architecture_review'],
      ['n-bpr', 'planning_node', '1-business_parity_review'],
      ['n-plan', 'planning_node', '2-plan_review'],
    ]);
    assert.deepEqual(doc.sessions.map((s) => [s.time.wall_ms, s.time.idle_ms, s.time.active_ms, s.time.host_suspended_ms]), [
      [60000, 0, 60000, 0],
      [360000, 300000, 60000, 0],
      [600000, 570000, 30000, 60000],
      [360000, 330000, 30000, 60000],
    ]);
  });

  await t.test('the run time is the union, and the summed wall sits beside it', () => {
    assert.equal(doc.run.wall_ms, 960000);
    assert.equal(doc.run.active_ms, 180000);
    assert.equal(doc.run.idle_ms, 780000);
    assert.equal(doc.run.host_suspended_ms, 60000);
    assert.equal(doc.run.session_wall_sum_ms, 1380000);
    assert.equal(doc.run.session_wall_sum_ms, summed(doc.sessions, 'wall_ms'));
    assert.equal(doc.run.span_ms, 1500000);
    assert.equal(doc.run.first_at, at('00:00'));
    assert.equal(doc.run.last_at, at('25:00'));
  });

  await t.test('engine and planning node sessions are counted apart', () => {
    assert.equal(doc.run.sessions, 4);
    assert.equal(doc.run.engine_sessions, 1);
    assert.equal(doc.run.node_sessions, 3);
  });

  await t.test('cost and tokens are sums over every session', () => {
    assert.equal(doc.run.total_cost_usd, 0.9375);
    assert.equal(doc.run.input_tokens, 100);
    assert.equal(doc.run.output_tokens, 1000);
    assert.equal(doc.run.cache_read_tokens, 10000);
    assert.equal(doc.run.cache_write_tokens, 260);
    assert.equal(doc.run.token_sessions, 4);
  });

  await t.test('each node session is listed with its own figures, in the record and in the Markdown', () => {
    assert.deepEqual(doc.run.planning_nodes, [
      { session: 2, node: '1-architecture_review', session_id: 'n-arch', complete: true, wall_ms: 360000, active_ms: 60000, idle_ms: 300000, duration_ms: 360000, total_cost_usd: 0.125 },
      { session: 3, node: '1-business_parity_review', session_id: 'n-bpr', complete: true, wall_ms: 600000, active_ms: 30000, idle_ms: 570000, duration_ms: 540000, total_cost_usd: 0.25 },
      { session: 4, node: '2-plan_review', session_id: 'n-plan', complete: true, wall_ms: 360000, active_ms: 30000, idle_ms: 330000, duration_ms: 300000, total_cost_usd: 0.0625 },
    ]);
    const md = readFileSync(f.mdPath, 'utf8');
    for (const row of [
      '| Engine / planning node sessions | 1 / 3 |',
      '| Wall | 16m 00s |',
      '| Session wall, summed over sessions | 23m 00s |',
      '| Active | 3m 00s |',
      '| Host-suspended | 1m 00s |',
      '| Idle | 13m 00s |',
      '| Cost | $0.94 |',
      '| 2 | 1-architecture_review | 6m 00s | 1m 00s | 5m 00s | 6m 00s | $0.13 |',
      '| 3 | 1-business_parity_review | 10m 00s | 30.0s | 9m 30s | 9m 00s | $0.25 |',
      '| 4 | 2-plan_review | 6m 00s | 30.0s | 5m 30s | 5m 00s | $0.06 |',
      'Planning node: `2-plan_review`',
    ]) {
      assert.ok(md.split('\n').includes(row), `${row}\n${md}`);
    }
    const order = ['## Whole run', '## Planning node sessions', '## Network refusals', '## Session 1'].map((h) => md.indexOf(h));
    assert.deepEqual([...order].sort((a, b) => a - b), order, md);
    assert.ok(order.every((i) => i >= 0), md);
  });
});

test('without a manifest every session is an engine session', async (t) => {
  const f = await adopted(t);
  f.append([...ENGINE, ...NODES.flat()]);
  await recorded(f, 4);
  const doc = f.doc();
  assert.deepEqual(doc.sessions.map((s) => s.kind), ['engine', 'engine', 'engine', 'engine']);
  assert.equal(doc.run.node_sessions, 0);
  assert.deepEqual(doc.run.planning_nodes, []);
  assert.equal(readFileSync(f.mdPath, 'utf8').includes('## Planning node sessions'), false);
  assert.equal(doc.run.wall_ms, 960000, 'the union does not depend on the classing');
});

test('a schema-3 document is read and extended to schema 4, its records counted as engine sessions', async (t) => {
  const f = await adopted(t);
  f.append(ENGINE);
  await recorded(f, 1);
  const written = f.doc();
  const old = written.sessions.map(({ kind, node, ...rest }) => rest);
  writeFileSync(f.jsonPath, `${JSON.stringify({ schema: 3, branch: BRANCH, sessions: old, run: written.run, rounds: [], gate_logs: [] })}\n`);

  f.append(NODES.flat());
  f.manifest(MANIFEST);
  await recorded(f, 3);
  const doc = f.doc();
  assert.equal(doc.schema, 4);
  assert.equal(JSON.stringify(doc.sessions[0]), JSON.stringify(old[0]), 'the recorded session was rewritten');
  assert.equal('kind' in doc.sessions[0], false);
  assert.deepEqual(doc.sessions.slice(1).map((s) => s.kind), ['planning_node', 'planning_node', 'planning_node']);
  assert.equal(doc.run.engine_sessions, 1);
  assert.equal(doc.run.node_sessions, 3);
  assert.equal(doc.run.wall_ms, 960000);
  assert.deepEqual(doc.rounds, []);
  assert.deepEqual(doc.gate_logs, []);
});

test('sessions that never overlap roll up to exactly their sums', async (t) => {
  const f = await adopted(t);
  // The three nodes moved apart: 10:00–20:00, 30:00–36:00 and 40:00–46:00.
  const shifted = [
    session('n-bpr', ['10:00', '10:30', '15:00', '20:00'], { duration: 540000, cost: 0.25, usage: [20, 200, 2000, 60] }),
    session('n-arch', ['30:00', '30:30', '34:00', '34:30', '36:00'], { duration: 360000, cost: 0.125, usage: [30, 300, 3000, 70] }),
    session('n-plan', ['40:00', '40:30', '46:00'], { duration: 300000, cost: 0.0625, usage: [40, 400, 4000, 80] }),
  ];
  f.append([...ENGINE, ...shifted.flat()]);
  f.manifest(MANIFEST);
  await recorded(f, 4);
  const { run, sessions } = f.doc();
  for (const key of ['wall_ms', 'active_ms', 'idle_ms', 'host_suspended_ms']) {
    assert.equal(run[key], summed(sessions, key), key);
  }
  assert.equal(run.wall_ms, run.session_wall_sum_ms);
  assert.deepEqual([run.wall_ms, run.active_ms, run.idle_ms, run.host_suspended_ms], [1380000, 180000, 1200000, 120000]);
});
