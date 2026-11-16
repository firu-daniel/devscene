/**
 * The script-driven planning pilot, end to end through the `autonomous-watcher.sh` that `init`
 * writes: the `execution.scriptDrivenPlanning` key, the plugin runtime root derived by
 * `hr_plugin_runtime_root_var`, `planning_driver_ready`, `session_exec` and the
 * setup → driver → engine sequence in `spawn_engine`'s launch subshell, locally and in job mode.
 *
 * **The rule this suite enforces: with the key off or absent a launch is one engine session, as
 * today; with it on and a runtime root that resolves to a usable plugin directory a task launch is a
 * setup session carrying the `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH` clause, then node sessions
 * on the setup session's own flag vector plus `--plugin-dir <derived root>` and their other per-node
 * flags, then — only on the driver's hand-off — one engine session without the clause; a job launch
 * runs the same three steps; and the hand-off archives exactly the answered pairs the driver
 * consumed, leaving every other pair to the engine session and `classify_run_exit`.**
 *
 * The runtime root is planted in the agent runner's records under a `CLAUDE_CONFIG_DIR` each case
 * creates under the system temp directory, never the real account home: an `installed_plugins.json`
 * `user` row by default, and a `directory`-sourced marketplace — the job's own install shape — for
 * the job case.
 *
 * Every local pass is one `tick` of `cli/test/helpers/watcher.mjs`, launched through the
 * pause-resume or park-resume pass. The stub agent CLI is written here and imports nothing from
 * `cli/test/helpers/planning-driver.mjs`: it tells the three session kinds apart, records each argv
 * to a calls log, answers a node session the way a real one does — a `result` whose text ends in a
 * return block, the return objects written out here rather than built from a schema — and every
 * literal this suite asserts on is spelled in this file.
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
 * `--agent` flag) prints an `init` event with the agent file's `tools:` list and a `success` result
 * whose `result` text ends in a ```` ```json ```` return block valid against the agent's `## Return
 * schema` and no other field carrying the return;
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
  let ret;
  const folder = value('findings_folder: ');
  if (agent === 'ui-tests-plan-writer') {
    ret = { outcome: 'no_ui', reason: 'The branch delivers no user-facing surface.' };
  } else if (folder !== '') {
    const findings = folder + 'review_' + value('iteration: ') + '.md';
    put(findings, '# review\nverdict: PASS\nreview_mode: ' + value('review_mode: ') + '\n');
    ret = { outcome: 'PASS', findings_file: findings };
  } else if (mode.park === true) {
    ret = { outcome: 'questions', questions: ['Which storage key does the feature use?'] };
  } else {
    let story = value('Story index: ');
    let tasks = value('Per-task files: ');
    const initial = /^Outputs: story index at (\S+) and per-task files at (\S+)task_<N>_plan\.md$/m.exec(prompt);
    if (initial !== null) [, story, tasks] = initial;
    put(story, '# Story plan\n\nwritten by the stub\n');
    put(tasks + 'task_1_plan.md', '### Task 1\n\nwritten by the stub\n');
    const note = value('Revision note: ');
    if (note !== '') put(note, '# Revision\n\nwritten by the stub\n');
    ret = { outcome: 'returned', story_file: story, task_files_dir: tasks, tasks_count: 1, story_points_total: 3 };
  }
  const result = 'Done.\n\n' + '\x60\x60\x60json\n' + JSON.stringify(ret, null, 2) + '\n\x60\x60\x60';
  const events = [
    { type: 'system', subtype: 'init', session_id: 'stub', tools },
    { type: 'result', subtype: 'success', is_error: false, total_cost_usd: 0.01, permission_denials: [], result },
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
 * A watcher fixture on `feat_x`, a plugin directory under the system temp directory holding each
 * graph agent's `agents/<agent>.md` and `schemas/<agent>.return.json`, the agent runner's records
 * naming it under a temp `CLAUDE_CONFIG_DIR`, and the stub.
 *
 * `key` is `execution.scriptDrivenPlanning`, committed with the fixture; `null` leaves it out.
 * `layout` is how the records name the plugin: `installed`, an `installed_plugins.json` `user` row
 * whose `installPath` is the plugin; `directory`, a `directory`-sourced marketplace whose manifest's
 * `./plugin` source is the plugin, beside an install row naming a cache directory that does not
 * exist; `none`, no records at all.
 *
 * @param {import('node:test').TestContext} t
 * @param {{ pluginJson?: boolean, key?: boolean | null, layout?: 'installed' | 'directory' | 'none', qa?: boolean }} [options]
 *   `pluginJson: false` leaves `plugin.json` out; `qa: true` turns `phases.qa` on.
 */
async function pilotFixture(t, { pluginJson = true, key = true, layout = 'installed', qa = false } = {}) {
  const f = await createWatcherFixture(t, { branch: BRANCH });
  if (f === null) return null;
  const root = await realpath(await mkdtemp(join(tmpdir(), 'watcher-planning-driver-')));
  t.after(() => rm(root, { recursive: true, force: true }));

  const configPath = join(f.dir, 'devscene.config.json');
  const config = JSON.parse(readFileSync(configPath, 'utf8'));
  if (key !== null) config.execution = { ...(config.execution ?? {}), scriptDrivenPlanning: key };
  if (qa) config.phases = { ...(config.phases ?? {}), qa: true };
  await writeFile(configPath, `${JSON.stringify(config, null, 2)}\n`, 'utf8');

  await mkdir(join(f.dir, STATE_DIR, 'task_prompts'), { recursive: true });
  await writeFile(join(f.dir, TASK_PROMPT), '# Task prompt\n\nAdd a fixture feature.\n', 'utf8');
  await runGit(f.dir, ['checkout', '--quiet', '-b', BRANCH]);
  await runGit(f.dir, ['add', '--', 'devscene.config.json', TASK_PROMPT]);
  await runGit(f.dir, ['commit', '--quiet', '-m', 'fixture: seed']);

  const claudeHome = join(root, 'claude-home');
  const records = join(claudeHome, 'plugins');
  await mkdir(records, { recursive: true });
  const marketplace = join(root, 'harness-marketplace');
  const plugin = layout === 'directory' ? join(marketplace, 'plugin') : join(root, 'plugin');
  const installRow = (installPath) =>
    JSON.stringify({ version: 2, plugins: { [`${PLUGIN_NAME}@${PLUGIN_NAME}`]: [{ scope: 'user', installPath }] } });
  if (layout === 'installed') {
    await writeFile(join(records, 'installed_plugins.json'), installRow(plugin), 'utf8');
  } else if (layout === 'directory') {
    await writeFile(join(records, 'installed_plugins.json'), installRow(join(root, 'cache', 'devscene')), 'utf8');
    await writeFile(
      join(records, 'known_marketplaces.json'),
      JSON.stringify({ [PLUGIN_NAME]: { source: { source: 'directory', path: marketplace }, installLocation: marketplace } }),
      'utf8',
    );
    await mkdir(join(marketplace, '.claude-plugin'), { recursive: true });
    await writeFile(
      join(marketplace, '.claude-plugin', 'marketplace.json'),
      JSON.stringify({ name: PLUGIN_NAME, plugins: [{ name: PLUGIN_NAME, source: './plugin' }] }),
      'utf8',
    );
  }

  const source = join(WORKSPACE_ROOT, 'plugin');
  await mkdir(join(plugin, '.claude-plugin'), { recursive: true });
  await mkdir(join(plugin, 'agents'));
  await mkdir(join(plugin, 'schemas'));
  await mkdir(join(plugin, 'instructions'));
  if (pluginJson) await copyFile(join(source, '.claude-plugin', 'plugin.json'), join(plugin, '.claude-plugin', 'plugin.json'));
  for (const agent of graphAgents(f.dir)) {
    await copyFile(join(source, 'agents', `${agent}.md`), join(plugin, 'agents', `${agent}.md`));
    const schemaFile = `${agent}.return.json`;
    await copyFile(join(source, 'schemas', schemaFile), join(plugin, 'schemas', schemaFile));
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
  const runnerTemp = join(root, 'runner-temp');
  await mkdir(runnerTemp);
  const gh = join(stubDir, 'gh');
  await writeFile(gh, "#!/usr/bin/env bash\nprintf '[]\\n'\n", { mode: 0o755 });
  const sessionEnv = (env) => ({
    DEVSCENE_AGENT_CLI: cli,
    CLAUDE_CONFIG_DIR: claudeHome,
    PUSH_RETRY_DELAY_SECS: '0',
    GH_TOKEN: '',
    GITHUB_TOKEN: '',
    HARNESS_PR_TOKEN: '',
    DEVSCENE_GIT_TOKEN: '',
    GITHUB_ACTIONS: '',
    ...env,
  });
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
    /** One pass with the stub as the agent CLI and the fixture's own `CLAUDE_CONFIG_DIR`. */
    passStderr: '',
    async pass({ env = {}, placeholderHost = false } = {}) {
      const result = await f.tick(sessionEnv(env), { timeoutMs: PASS_TIMEOUT_MS, placeholderHost });
      this.passStderr = result.stderr;
      return result;
    },
    /**
     * One `job <branch> task none` run in job mode, every job input a runner would set pinned empty
     * (as `watcher-remote-job.test.mjs` pins them), `RUNNER_TEMP` a fixture directory and `gh` a stub
     * answering `[]`.
     */
    async job() {
      const result = await runBash(
        f.dir,
        [f.watcherPath, 'job', BRANCH, 'task', 'none'],
        f.watcherEnv(
          sessionEnv({
            HARNESS_JOB_MODE: '1',
            HARNESS_INPUT_CHAIN: '',
            HARNESS_REMOTE_SLUG: '',
            HARNESS_JOB_STARTED_EPOCH: '',
            HARNESS_JOB_DEADLINE_EPOCH: '',
            RUNNER_ENVIRONMENT: '',
            REMOTE_SELF_PAUSE_AFTER_SECS: '',
            GITHUB_RUN_ID: '',
            GITHUB_REPOSITORY: '',
            GITHUB_SERVER_URL: '',
            RUNNER_TEMP: runnerTemp,
            REMOTE_CONTROL_POLL_SECS: '1',
            REMOTE_AUTO_RESUME_DELAY_SECS: '0',
            DEVSCENE_GH_CLI: gh,
            POLL_INTERVAL_SECS: '1',
          }),
        ),
        { timeoutMs: PASS_TIMEOUT_MS, signal: t.signal },
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

for (const [name, key] of [
  ['key absent', null],
  ['key false', false],
]) {
  test(`${name}: one engine session, with no clause and no --agent, though the runtime root resolves`, async (t) => {
    const f = await pilotFixture(t, { key });
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
}

test('key on: the setup session, then node sessions on its vector, then one engine session', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.armPauseResume();
  await f.pass();
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

test('key on, and the driver parks: no engine session follows, and the record is parked', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.setMode({ park: true });
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.equal(calls[0]?.kind, 'setup', show(f));
  assert.ok(calls.some((c) => c.kind === 'node' && c.agent === 'task-plan-writer'), show(f));
  assert.equal(calls.filter((c) => c.kind === 'engine').length, 0, show(f));
  assert.equal(f.record().status, 'parked', show(f));
  const question = readFileSync(join(f.dir, CLAR, 'question_1.md'), 'utf8');
  const sections = question.split('\n').filter((l) => l.startsWith('## '));
  assert.deepEqual(sections, ['## Q1 — Which storage key does the feature use?'], question);
});

test('key on, and every node dispatch is undelivered: the run pauses and its one paused notification names the overload', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.setMode({ undelivered: true });
  await f.armPauseResume();
  await f.pass({ env: { PD_BACKOFF_SECS: '0' } });
  assert.equal(f.record().status, 'paused', show(f));
  const paused = f.notifications().filter((n) => n.event === 'paused' && n.branch === BRANCH);
  assert.equal(paused.length, 1, `${JSON.stringify(f.notifications())}\n${show(f)}`);
  assert.ok(paused[0].detail.includes('three consecutive planning dispatches undelivered'), `${paused[0].detail}\n${show(f)}`);
  assert.equal(f.calls().some((c) => c.kind === 'engine'), false, show(f));
});

test('key on, and the runtime root has no plugin.json: one session, no clause, and the off line', async (t) => {
  const f = await pilotFixture(t, { pluginJson: false });
  if (f === null) return;
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.equal(calls.length, 1, show(f));
  assert.equal(calls[0].kind, 'engine', show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  const off = f.watcherLog().split('\n').filter((l) => l.includes(`planning driver off for '${BRANCH}': `));
  assert.equal(off.length, 1, f.watcherLog());
  assert.ok(off[0].includes(`'${f.plugin}/.claude-plugin/plugin.json' is not readable`), off[0]);
});

test('key on, and no runtime root resolves from the records: one session, no clause, and one off line naming it', async (t) => {
  const f = await pilotFixture(t, { layout: 'none' });
  if (f === null) return;
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.equal(calls.length, 1, show(f));
  assert.equal(calls[0].kind, 'engine', show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  const off = f.watcherLog().split('\n').filter((l) => l.includes(`planning driver off for '${BRANCH}': `));
  assert.equal(off.length, 1, f.watcherLog());
  assert.ok(
    off[0].endsWith(`planning driver off for '${BRANCH}': the plugin's runtime root could not be resolved from the agent runner's records`),
    off[0],
  );
});

test('key not a boolean: one session, no clause, and one off line naming the key', async (t) => {
  const f = await pilotFixture(t, { key: null });
  if (f === null) return;
  const configPath = join(f.dir, 'devscene.config.json');
  const config = JSON.parse(readFileSync(configPath, 'utf8'));
  config.execution = { ...(config.execution ?? {}), scriptDrivenPlanning: 'true' };
  await writeFile(configPath, `${JSON.stringify(config, null, 2)}\n`, 'utf8');
  await runGit(f.dir, ['commit', '--quiet', '-am', 'fixture: a string key']);
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.equal(calls.length, 1, show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  const off = f.watcherLog().split('\n').filter((l) => l.includes(`planning driver off for '${BRANCH}': `));
  assert.equal(off.length, 1, f.watcherLog());
  assert.ok(off[0].includes('execution.scriptDrivenPlanning is not a boolean'), off[0]);
});

test('a job with the key on: the setup session, node sessions pinned to the installed runtime root, then the engine session', async (t) => {
  const f = await pilotFixture(t, { layout: 'directory', qa: true });
  if (f === null) return;
  // The job's `init --plugin-root-entries` lists the runtime root in the base profile.
  const profilePath = join(f.dir, '.claude', 'settings.autonomous.json');
  const profile = JSON.parse(readFileSync(profilePath, 'utf8'));
  profile.permissions.additionalDirectories = [...(profile.permissions.additionalDirectories ?? []), f.plugin];
  await writeFile(profilePath, `${JSON.stringify(profile, null, 2)}\n`, 'utf8');

  const result = await f.job();
  const detail = `${result.stdout}\n${show(f)}`;
  assert.equal(result.status, 0, detail);
  assert.equal(result.stdout.trimEnd().split('\n').at(-1), 'job: completed stop', detail);

  const calls = f.calls();
  const [setup] = calls;
  assert.equal(setup?.kind, 'setup', detail);
  assert.ok(setup.prompt.includes(CLAUSE), detail);
  assert.match(setup.prompt, /executes in a GitHub Actions job \(execution: github-actions\), where the interactive-test phase is unsupported/);
  assert.equal(values(setup.argv, '--add-dir').filter((d) => d === f.plugin).length, 1, setup.argv.join(' '));

  const nodes = calls.filter((c) => c.kind === 'node');
  assert.ok(nodes.length > 0, detail);
  assert.deepEqual(calls.slice(1, 1 + nodes.length).map((c) => c.kind), nodes.map(() => 'node'), detail);
  for (const node of nodes) {
    assert.deepEqual(values(node.argv, '--plugin-dir'), [f.plugin], node.agent);
    assert.equal(values(node.argv, '--add-dir').filter((d) => d === f.plugin).length, 1, `${node.agent}: ${node.argv.join(' ')}`);
    assert.deepEqual(values(node.argv, '--settings'), values(setup.argv, '--settings'), node.agent);
  }

  const engines = calls.filter((c) => c.kind === 'engine');
  assert.equal(engines.length, 1, detail);
  assert.equal(calls.at(-1).kind, 'engine', detail);
  assert.equal(engines[0].prompt.includes(CLAUSE), false);
  assert.ok(existsSync(join(f.dir, STATE_DIR, 'autonomous_logs', `${BRANCH}.planning`)), detail);
});

test('the hand-off archives only what the driver consumed', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.writeQuestion(
    1,
    '# Questions from task-plan-writer\n\nRaised by: task-plan-writer (script-driven planning)\n\n## Q1 — Which storage key?\n\nWhich storage key?\n',
  );
  await f.writeAnswer(1, 'Use `fixture.storage`.\n');
  await f.writeQuestion(2, '# Questions from Phase G\n\nRaised by: Phase G — Run gates (test-fix-plan-writer)\n\n## Questions\n1. Which gate?\n');
  await f.writeAnswer(2, 'The typecheck gate.\n');
  await mkdir(join(f.dir, STATE_DIR, 'story_plans'), { recursive: true });
  await writeFile(join(f.dir, STORY), '# Story plan\n\nan existing draft\n', 'utf8');
  await f.seedRecord({ status: 'parked' });

  await f.pass();
  const calls = f.calls();
  assert.equal(calls[0]?.kind, 'setup', show(f));
  const engines = calls.filter((c) => c.kind === 'engine');
  assert.equal(engines.length, 1, show(f));
  assert.deepEqual(engines[0].answered, ['answer_1.md', 'question_1.md'], show(f));
  assert.deepEqual(engines[0].topLevel, ['answer_2.md', 'question_2.md'], show(f));
  assert.deepEqual(await f.topLevel(), []);
  assert.deepEqual(await f.archived(), ['answer_1.md', 'answer_2.md', 'question_1.md', 'question_2.md']);
});

test('on a placeholder host the pilot launch records the plugin directory .mcp.json in the manifest, and a launch with the key absent records none', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.armPauseResume();
  const env = { XDG_STATE_HOME: f.stateHome };
  await f.pass({ env, placeholderHost: true });
  const manifest = await f.manifestFile(env);
  assert.ok(existsSync(manifest), `no manifest at ${manifest}:\n${show(f)}`);
  const lines = readFileSync(manifest, 'utf8').split('\n');
  assert.ok(lines.includes(`${f.plugin}/.mcp.json`), `${lines.join('\n')}\n${show(f)}`);

  const g = await pilotFixture(t, { key: null });
  if (g === null) return;
  await g.armPauseResume();
  const plainEnv = { XDG_STATE_HOME: g.stateHome };
  await g.pass({ env: plainEnv, placeholderHost: true });
  const plainManifest = await g.manifestFile(plainEnv);
  assert.ok(existsSync(plainManifest), `no manifest at ${plainManifest}:\n${show(g)}`);
  const plain = readFileSync(plainManifest, 'utf8').split('\n');
  assert.equal(plain.some((line) => line.startsWith(`${g.plugin}/`)), false, `${plain.join('\n')}\n${show(g)}`);
});
