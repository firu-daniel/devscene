/**
 * The script-driven planning pilot, end to end through the `autonomous-watcher.sh` that `init`
 * writes: `PLANNING_DRIVER_PLUGIN_DIR`, `planning_driver_ready`, `session_exec` and the
 * setup → driver → engine sequence in `spawn_engine`'s launch subshell.
 *
 * **The rule this suite enforces: with the switch empty a launch is one engine session, as today;
 * with it set to a usable plugin directory a task launch is a setup session carrying the
 * `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH` clause, then node sessions on the setup session's own
 * flag vector plus their per-node flags, then — only on the driver's hand-off — one engine session
 * without the clause; and the hand-off archives exactly the answered pairs the driver consumed,
 * leaving every other pair to the engine session and `classify_run_exit`.**
 *
 * Every pass is one `tick` of `cli/test/helpers/watcher.mjs`, launched through the pause-resume or
 * park-resume pass. The stub agent CLI is written here and imports nothing from
 * `cli/test/helpers/planning-driver.mjs`: it tells the three session kinds apart, records each argv
 * to a calls log, and every literal this suite asserts on is spelled in this file.
 */

import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { copyFile, mkdir, mkdtemp, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { INIT_SCRIPTS_DIR, WORKSPACE_ROOT, runBash, runGit } from './helpers/fixture.mjs';
import { scaleBound } from './helpers/timing.mjs';
import { TICK_TIMEOUT_MS, createWatcherFixture } from './helpers/watcher.mjs';

const BRANCH = 'feat_x';
const STATE_DIR = 'devscene';
const CLAUSE = 'PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH';
const PLUGIN_NAME = 'devscene';
const CORE = 'task_plan_writing_instructions_core.md';
const LEDGER = `${STATE_DIR}/flow_progress/${BRANCH}_progress.md`;
const STORY = `${STATE_DIR}/story_plans/${BRANCH}_story_plan.md`;
const TASK_PROMPT = `${STATE_DIR}/task_prompts/${BRANCH}_task_prompt.md`;
const CLAR = `${STATE_DIR}/clarifications/${BRANCH}`;

/** One pass that launches a setup session, several node sessions and an engine session. */
const PASS_TIMEOUT_MS = scaleBound(180_000);

/**
 * The stub. argv[2] is its own directory; the rest is the watcher's argv. A node session (an
 * `--agent` flag) prints an `init` event with the agent file's `tools:` list and a `success` result;
 * a setup session (the clause in its `-p` prompt) writes the task ledger with only `P0` closed; any
 * other session is the engine, which records the channel's top level and closes every ledger entry.
 */
const STUB_SOURCE = String.raw`
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const dir = process.argv[2];
const argv = process.argv.slice(3);
const flag = (name) => { const at = argv.indexOf(name); return at === -1 ? '' : argv[at + 1]; };
const prompt = flag('-p');
const cwd = process.cwd();
const mode = JSON.parse(readFileSync(join(dir, 'mode.json'), 'utf8'));
const record = (entry) => appendFileSync(join(dir, 'calls.log'), JSON.stringify({ ...entry, argv }) + '\n');
const put = (rel, text) => { mkdirSync(dirname(join(cwd, rel)), { recursive: true }); writeFileSync(join(cwd, rel), text); };
const names = (rel) => (existsSync(join(cwd, rel)) ? readdirSync(join(cwd, rel)).filter((n) => n !== 'answered').sort() : []);
// helpers/watcher.mjs → choice 1: a session launched in a pass stays running for the rest of it.
const linger = () => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 300);

const qualified = flag('--agent');
if (qualified !== '') {
  const agent = qualified.slice(qualified.indexOf(':') + 1);
  record({ kind: 'node', agent });
  const text = readFileSync(join(flag('--plugin-dir'), 'agents', agent + '.md'), 'utf8');
  const toolsLine = text.split('\n').find((l) => l.startsWith('tools:'));
  const tools = toolsLine.slice('tools:'.length).split(',').map((t) => t.trim()).filter(Boolean);
  if (mode.undelivered === true) {
    process.stdout.write(JSON.stringify({ type: 'system', subtype: 'init', session_id: 'stub', tools }) + '\n');
    process.exit(0);
  }
  const lines = prompt.split('\n');
  const value = (key) => { const line = lines.find((l) => l.startsWith(key)); return line === undefined ? '' : line.slice(key.length); };
  const decision = { outcome: '', findings_file: null, return: '', harness_friction: [] };
  const folder = value('findings_folder: ');
  if (agent === 'ui-tests-plan-writer') {
    decision.outcome = 'no_ui';
    decision.return = 'no_ui';
  } else if (folder !== '') {
    const findings = folder + 'review_' + value('iteration: ') + '.md';
    put(findings, '# review\nverdict: PASS\nreview_mode: ' + value('review_mode: ') + '\n');
    decision.outcome = 'PASS';
    decision.findings_file = findings;
    decision.return = 'verdict: PASS';
  } else if (mode.park === true) {
    decision.outcome = 'questions';
    decision.return = '## Questions\n1. Which storage key does the feature use?';
  } else {
    let story = value('Story index: ');
    let tasks = value('Per-task files: ');
    const initial = /^Outputs: story index at (\S+) and per-task files at (\S+)task_<N>_plan\.md$/m.exec(prompt);
    if (initial !== null) [, story, tasks] = initial;
    put(story, '# Story plan\n\nwritten by the stub\n');
    put(tasks + 'task_1_plan.md', '### Task 1\n\nwritten by the stub\n');
    const note = value('Revision note: ');
    if (note !== '') put(note, '# Revision\n\nwritten by the stub\n');
    decision.outcome = 'returned';
    decision.return = 'story_file: ' + story + '\ntask_files_dir: ' + tasks + '\ntasks_count: 1';
  }
  const events = [
    { type: 'system', subtype: 'init', session_id: 'stub', tools },
    { type: 'result', subtype: 'success', is_error: false, total_cost_usd: 0.01, permission_denials: [], structured_output: decision },
  ];
  process.stdout.write(events.map((e) => JSON.stringify(e)).join('\n') + '\n');
} else if (prompt.includes('${CLAUSE}')) {
  record({ kind: 'setup', prompt });
  linger();
  const config = JSON.parse(readFileSync(join(cwd, 'devscene.config.json'), 'utf8'));
  const on = (name) => ((config.phases ?? {})[name] === true ? 'true' : 'false');
  const later = ['A', 'A1.5g', 'A1.5f', 'A2g', 'A2f', 'Bg', 'Bm', 'C', 'C2g', 'C2m', 'C2f', 'E', 'G', 'D'];
  put('${LEDGER}', [
    '# Flow progress — ${BRANCH}   (engine: task)',
    '',
    '## Run mode',
    'Source: ${TASK_PROMPT} → ' + '\x60### Run mode\x60',
    '- skipped: none',
    '- phases: parity=' + on('parity') + ', qa=' + on('qa') + ', docs=' + on('docs'),
    '- remote-skipped: none',
    '',
    '## Planning',
    '- [x] P0. Untrusted input screened (prompt-injection-reviewer SAFE)',
    '- [ ] P1. Task plan converged',
    '- [ ] P2. UI-test plan converged — or no_ui',
    '- [ ] P3. Plans committed & pushed',
    '',
    '## Implementation',
    ...later.map((id) => '- [ ] ' + (id + '.').padEnd(8) + ' label for ' + id),
    '',
  ].join('\n'));
} else {
  record({ kind: 'engine', prompt, topLevel: names('${CLAR}'), answered: names('${CLAR}/answered') });
  linger();
  if (existsSync(join(cwd, '${LEDGER}'))) {
    put('${LEDGER}', readFileSync(join(cwd, '${LEDGER}'), 'utf8').replaceAll('- [ ] ', '- [x] '));
  }
}
`;

/** The planning agents the fixture's own graph names, read off the copy `init` wrote. */
function graphAgents(dir) {
  const graph = JSON.parse(readFileSync(join(dir, INIT_SCRIPTS_DIR, 'flows', 'task_plan_writing.graph.json'), 'utf8'));
  return [...new Set(Object.values(graph.nodes).map((node) => node.agent).filter(Boolean))];
}

/**
 * A watcher fixture on `feat_x`, a plugin directory under the system temp directory and the stub.
 *
 * @param {import('node:test').TestContext} t
 * @param {{ pluginJson?: boolean }} [options] `pluginJson: false` leaves `plugin.json` out.
 */
async function pilotFixture(t, { pluginJson = true } = {}) {
  const f = await createWatcherFixture(t, { branch: BRANCH });
  if (f === null) return null;
  const root = await realpath(await mkdtemp(join(tmpdir(), 'watcher-planning-driver-')));
  t.after(() => rm(root, { recursive: true, force: true }));

  await mkdir(join(f.dir, STATE_DIR, 'task_prompts'), { recursive: true });
  await writeFile(join(f.dir, TASK_PROMPT), '# Task prompt\n\nAdd a fixture feature.\n', 'utf8');
  await runGit(f.dir, ['checkout', '--quiet', '-b', BRANCH]);
  await runGit(f.dir, ['add', '--', 'devscene.config.json', TASK_PROMPT]);
  await runGit(f.dir, ['commit', '--quiet', '-m', 'fixture: seed']);

  const plugin = join(root, 'plugin');
  const source = join(WORKSPACE_ROOT, 'plugin');
  await mkdir(join(plugin, '.claude-plugin'), { recursive: true });
  await mkdir(join(plugin, 'agents'));
  await mkdir(join(plugin, 'instructions'));
  if (pluginJson) await copyFile(join(source, '.claude-plugin', 'plugin.json'), join(plugin, '.claude-plugin', 'plugin.json'));
  for (const agent of graphAgents(f.dir)) {
    await copyFile(join(source, 'agents', `${agent}.md`), join(plugin, 'agents', `${agent}.md`));
  }
  await copyFile(join(source, 'instructions', CORE), join(plugin, 'instructions', CORE));

  const stubDir = join(root, 'stub');
  await mkdir(stubDir);
  await writeFile(join(stubDir, 'stub.mjs'), STUB_SOURCE, 'utf8');
  await writeFile(join(stubDir, 'mode.json'), '{}', 'utf8');
  const cli = join(stubDir, 'agent-cli');
  await writeFile(cli, `#!/usr/bin/env bash\nexec '${process.execPath}' '${join(stubDir, 'stub.mjs')}' '${stubDir}' "$@"\n`, {
    mode: 0o755,
  });

  const callsPath = join(stubDir, 'calls.log');
  return {
    ...f,
    plugin,
    /**
     * A machine state directory outside `f.dir`: the pilot runs in place, so the default one under
     * `f.dir` lies under the session-writable worktree and the watcher writes no manifest there.
     */
    stateHome: join(root, 'state'),
    setMode: (mode) => writeFile(join(stubDir, 'mode.json'), JSON.stringify(mode), 'utf8'),
    /** Each session the stub saw, in launch order: `{ kind, agent?, prompt?, argv, topLevel?, answered? }`. */
    calls: () =>
      existsSync(callsPath)
        ? readFileSync(callsPath, 'utf8')
            .split('\n')
            .filter(Boolean)
            .map((line) => JSON.parse(line))
        : [],
    /** One pass with the stub as the agent CLI, and the switch set to `plugin` unless `null`. */
    passStderr: '',
    async pass(plugin = null, { env = {}, placeholderHost = false } = {}) {
      const result = await f.tick(
        {
          DEVSCENE_AGENT_CLI: cli,
          PLANNING_DRIVER_PLUGIN_DIR: plugin ?? '',
          PUSH_RETRY_DELAY_SECS: '0',
          GH_TOKEN: '',
          GITHUB_TOKEN: '',
          HARNESS_PR_TOKEN: '',
          DEVSCENE_GIT_TOKEN: '',
          GITHUB_ACTIONS: '',
          ...env,
        },
        { timeoutMs: PASS_TIMEOUT_MS, placeholderHost },
      );
      this.passStderr = result.stderr;
      return result;
    },
    /** A `paused` record and a RESUME, so the next pass launches through the pause-resume pass. */
    async armPauseResume() {
      await f.seedRecord({ status: 'paused' });
      await writeFile(join(f.dir, STATE_DIR, 'RESUME'), '', 'utf8');
    },
    /** The `.absent` placeholder manifest the watcher wrote for `BRANCH`'s launch under `env`. */
    async manifestFile(env = {}) {
      const printed = await runBash(
        f.dir,
        ['-c', '. "$1"; hr_run_profile_absent_file "$(hr_repo_slug "$2")" "$3"', '_', join(f.dir, INIT_SCRIPTS_DIR, 'lib', 'harness-run-lib.sh'), f.dir, BRANCH],
        f.watcherEnv(env),
        { timeoutMs: TICK_TIMEOUT_MS, signal: t.signal },
      );
      assert.equal(printed.status, 0, printed.stderr);
      return printed.stdout.trim();
    },
  };
}

/** Every value of `name` in `argv`, in order. */
function values(argv, name) {
  const out = [];
  argv.forEach((word, at) => {
    if (word === name) out.push(argv[at + 1]);
  });
  return out;
}

function show(f) {
  const runLog = join(f.dir, STATE_DIR, 'autonomous_logs', `${BRANCH}.log`);
  return [
    `--- calls\n${f.calls().map((c) => `${c.kind} ${c.agent ?? ''}`).join('\n')}`,
    `--- watcher log\n${f.watcherLog().split('\n').filter((l) => !l.includes('session environment for')).join('\n')}`,
    `--- run log, plan-drive and planning-driver lines\n${(existsSync(runLog) ? readFileSync(runLog, 'utf8') : '')
      .split('\n')
      .filter((l) => l.startsWith('[plan-drive]') || l.startsWith('planning-driver:') || l.includes('unbound'))
      .slice(-12)
      .join('\n')}`,
    `--- pass stderr\n${f.passStderr}`,
  ].join('\n');
}

test('switch unset: one engine session, with no clause and no --agent', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.equal(calls.length, 1, show(f));
  assert.equal(calls[0].kind, 'engine', show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  assert.equal(calls[0].argv.includes('--agent'), false);
  assert.equal(f.watcherLog().includes('planning driver'), false, f.watcherLog());
});

test('switch set: the setup session, then node sessions on its vector, then one engine session', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.armPauseResume();
  await f.pass(f.plugin);
  const calls = f.calls();
  assert.ok(calls.length >= 3, show(f));
  const [setup] = calls;
  assert.equal(setup.kind, 'setup', show(f));
  assert.equal(setup.argv.includes('--agent'), false);

  const nodes = calls.filter((c) => c.kind === 'node');
  assert.ok(nodes.length > 0, show(f));
  assert.deepEqual(calls.slice(1, 1 + nodes.length).map((c) => c.kind), nodes.map(() => 'node'), show(f));
  assert.equal(nodes[0].agent, 'task-plan-writer', show(f));
  assert.deepEqual(values(nodes[0].argv, '--agent'), [`${PLUGIN_NAME}:task-plan-writer`]);
  for (const node of nodes) {
    assert.deepEqual(values(node.argv, '--settings'), values(setup.argv, '--settings'), node.agent);
    assert.deepEqual(values(node.argv, '--permission-mode'), values(setup.argv, '--permission-mode'), node.agent);
    const dirs = values(node.argv, '--add-dir');
    for (const dir of values(setup.argv, '--add-dir')) assert.ok(dirs.includes(dir), `${node.agent} lacks --add-dir ${dir}`);
    assert.deepEqual(values(node.argv, '--plugin-dir'), [f.plugin], node.agent);
  }

  const engines = calls.filter((c) => c.kind === 'engine');
  assert.equal(engines.length, 1, show(f));
  assert.equal(calls.at(-1).kind, 'engine', show(f));
  assert.equal(engines[0].prompt.includes(CLAUSE), false);
  assert.equal(engines[0].argv.includes('--agent'), false);
  assert.equal(f.record().status, 'completed', show(f));
});

test('switch set, and the driver parks: no engine session follows, and the record is parked', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.setMode({ park: true });
  await f.armPauseResume();
  await f.pass(f.plugin);
  const calls = f.calls();
  assert.equal(calls[0]?.kind, 'setup', show(f));
  assert.ok(calls.some((c) => c.kind === 'node' && c.agent === 'task-plan-writer'), show(f));
  assert.equal(calls.filter((c) => c.kind === 'engine').length, 0, show(f));
  assert.equal(f.record().status, 'parked', show(f));
});

test('switch set, and every node dispatch is undelivered: the run pauses and its one paused notification names the overload', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.setMode({ undelivered: true });
  await f.armPauseResume();
  await f.pass(f.plugin, { env: { PD_BACKOFF_SECS: '0' } });
  assert.equal(f.record().status, 'paused', show(f));
  const paused = f.notifications().filter((n) => n.event === 'paused' && n.branch === BRANCH);
  assert.equal(paused.length, 1, `${JSON.stringify(f.notifications())}\n${show(f)}`);
  assert.ok(paused[0].detail.includes('three consecutive planning dispatches undelivered'), `${paused[0].detail}\n${show(f)}`);
  assert.equal(f.calls().some((c) => c.kind === 'engine'), false, show(f));
});

test('switch set to a directory with no plugin.json: one session, no clause, and the off line', async (t) => {
  const f = await pilotFixture(t, { pluginJson: false });
  if (f === null) return;
  await f.armPauseResume();
  await f.pass(f.plugin);
  const calls = f.calls();
  assert.equal(calls.length, 1, show(f));
  assert.equal(calls[0].kind, 'engine', show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  assert.ok(f.watcherLog().includes(`planning driver off for '${BRANCH}': `), f.watcherLog());
});

test('the hand-off archives only what the driver consumed', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.writeQuestion(
    1,
    '# Questions from task-plan-writer\n\nRaised by: task-plan-writer (script-driven planning)\n\n## Questions\n1. Which storage key?\n',
  );
  await f.writeAnswer(1, 'Use `fixture.storage`.\n');
  await f.writeQuestion(2, '# Questions from Phase G\n\nRaised by: Phase G — Run gates (test-fix-plan-writer)\n\n## Questions\n1. Which gate?\n');
  await f.writeAnswer(2, 'The typecheck gate.\n');
  await mkdir(join(f.dir, STATE_DIR, 'story_plans'), { recursive: true });
  await writeFile(join(f.dir, STORY), '# Story plan\n\nan existing draft\n', 'utf8');
  await f.seedRecord({ status: 'parked' });

  await f.pass(f.plugin);
  const calls = f.calls();
  assert.equal(calls[0]?.kind, 'setup', show(f));
  const engines = calls.filter((c) => c.kind === 'engine');
  assert.equal(engines.length, 1, show(f));
  assert.deepEqual(engines[0].answered, ['answer_1.md', 'question_1.md'], show(f));
  assert.deepEqual(engines[0].topLevel, ['answer_2.md', 'question_2.md'], show(f));
  assert.deepEqual(await f.topLevel(), []);
  assert.deepEqual(await f.archived(), ['answer_1.md', 'answer_2.md', 'question_1.md', 'question_2.md']);
});

test('on a placeholder host the pilot launch records the plugin directory .mcp.json in the manifest, and a launch with the switch empty records none', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.armPauseResume();
  const env = { XDG_STATE_HOME: f.stateHome };
  await f.pass(f.plugin, { env, placeholderHost: true });
  const manifest = await f.manifestFile(env);
  assert.ok(existsSync(manifest), `no manifest at ${manifest}:\n${show(f)}`);
  const lines = readFileSync(manifest, 'utf8').split('\n');
  assert.ok(lines.includes(`${f.plugin}/.mcp.json`), `${lines.join('\n')}\n${show(f)}`);

  const g = await pilotFixture(t);
  if (g === null) return;
  await g.armPauseResume();
  const plainEnv = { XDG_STATE_HOME: g.stateHome };
  await g.pass(null, { env: plainEnv, placeholderHost: true });
  const plainManifest = await g.manifestFile(plainEnv);
  assert.ok(existsSync(plainManifest), `no manifest at ${plainManifest}:\n${show(g)}`);
  const plain = readFileSync(plainManifest, 'utf8').split('\n');
  assert.equal(plain.some((line) => line.startsWith(`${g.plugin}/`)), false, `${plain.join('\n')}\n${show(g)}`);
});
