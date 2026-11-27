/**
 * The watcher's half of the script-driven planning hand-off, end to end through the
 * `autonomous-watcher.sh` that `init` writes: the `execution.scriptDrivenPlanning` key,
 * `planning_driver_ready`, and the setup → driver → engine sequence in `spawn_engine`'s launch
 * subshell, locally and in job mode.
 *
 * **The rule this suite enforces: with the key off or absent a launch is one engine session; with
 * it on and the launch ready, a task launch is a setup session carrying the
 * `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH` clause, then one `uv run … devscene-planning-driver`
 * call, then — only on the driver's hand-off — one engine session without the clause, in local and
 * job mode alike; and the hand-off archives exactly the answered pairs the driver's `consumed:` line
 * names.**
 *
 * The driver is a stub `uv` placed first on the watcher's `PATH` (`createWatcherFixture`'s
 * `pathPrefix`), beside an environment planted at `<scripts_dir>/python/.venv` in place of the
 * borrowed one: a `pyvenv.cfg` marker and an executable `bin/devscene-planning-driver` that nothing
 * runs. The stub records its argv and four environment values to the calls log, then plays the
 * case's scripted answer — an exit status, a stdout line and the files the driver would have left
 * on disk. No case runs Python: the driver's own walk, parks and stops are `devscene-flow-host`'s
 * `pytest` suites'.
 *
 * The runtime root is planted in the agent runner's records under a `CLAUDE_CONFIG_DIR` each case
 * creates under the system temp directory: an `installed_plugins.json` `user` row by default, and a
 * `directory`-sourced marketplace — the job's own install shape — for the job case. The stub agent
 * CLI tells the setup session from the engine session by the clause and records each argv. Every
 * literal this suite asserts on is spelled in this file.
 */

import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { copyFile, mkdir, mkdtemp, realpath, rm, unlink, writeFile } from 'node:fs/promises';
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
const DRIVER = 'devscene-planning-driver';
const FORMATTER = 'autonomous-format-stream.sh';
const LEDGER = `${STATE_DIR}/flow_progress/${BRANCH}_progress.md`;
const TASK_PROMPT = `${STATE_DIR}/task_prompts/${BRANCH}_task_prompt.md`;
const CLAR = `${STATE_DIR}/clarifications/${BRANCH}`;
const RUN_LOG = `${STATE_DIR}/autonomous_logs/${BRANCH}.log`;
const UNDELIVERED_DETAIL = 'paused itself on API overload: three consecutive planning dispatches undelivered — ';

/** One pass that launches a setup session, the driver and an engine session. */
const PASS_TIMEOUT_MS = scaleBound(180_000);

/**
 * The agent CLI stub. argv[2] is its own directory; the rest is the watcher's argv. A setup session
 * (the clause in its `-p` prompt) writes the task ledger with only `P0` closed; any other session is
 * the engine, which records the channel's top level and closes every ledger entry.
 */
const AGENT_STUB_SOURCE = String.raw`
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const dir = process.argv[2];
const argv = process.argv.slice(3);
const at = argv.indexOf('-p');
const prompt = at === -1 ? '' : argv[at + 1];
const cwd = process.cwd();
const record = (entry) => appendFileSync(join(dir, 'calls.log'), JSON.stringify({ ...entry, argv }) + '\n');
const put = (rel, text) => { mkdirSync(dirname(join(cwd, rel)), { recursive: true }); writeFileSync(join(cwd, rel), text); };
const names = (rel) => (existsSync(join(cwd, rel)) ? readdirSync(join(cwd, rel)).filter((n) => n !== 'answered').sort() : []);
// helpers/watcher.mjs → choice 1: a session launched in a pass stays running for the rest of it.
const linger = () => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 300);

if (prompt.includes('${CLAUSE}')) {
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

/**
 * The `uv` stub. argv[2] is its own directory; the rest is the watcher's argv. Every call is
 * recorded with the four environment values; a `run` call then plays `mode.json`'s `driver` answer:
 * `files` (paths relative to the working copy) written, `stdout` printed as one line, `status`
 * returned. Any other call exits 0.
 */
const UV_STUB_SOURCE = String.raw`
import { appendFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const dir = process.argv[2];
const argv = process.argv.slice(3);
const env = {};
for (const name of ['DEVSCENE_MAIN_REPO', 'CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS', 'UV_PROJECT_ENVIRONMENT', 'PYTHONPATH']) {
  env[name] = process.env[name] ?? null;
}
appendFileSync(join(dir, 'calls.log'), JSON.stringify({ kind: 'uv', argv, env }) + '\n');
if (argv[0] !== 'run') process.exit(0);
const { driver } = JSON.parse(readFileSync(join(dir, 'mode.json'), 'utf8'));
for (const [rel, text] of Object.entries(driver.files ?? {})) {
  mkdirSync(dirname(join(process.cwd(), rel)), { recursive: true });
  writeFileSync(join(process.cwd(), rel), text);
}
if (driver.stdout !== '') process.stdout.write(driver.stdout + '\n');
process.exit(driver.status);
`;

/** The hand-off with nothing consumed: the default answer. */
const HANDOFF = { status: 0, stdout: 'consumed:' };

/**
 * A watcher fixture on `feat_x`, a plugin directory under the system temp directory holding
 * `plugin.json` and the planning core, the agent runner's records naming it under a temp
 * `CLAUDE_CONFIG_DIR`, the two stubs, and the flow host's environment replaced by a planted one.
 *
 * `key` is `execution.scriptDrivenPlanning`, committed with the fixture; `null` leaves it out.
 * `layout` is how the records name the plugin: `installed`, an `installed_plugins.json` `user` row
 * whose `installPath` is the plugin; `directory`, a `directory`-sourced marketplace whose manifest's
 * `./plugin` source is the plugin, beside an install row naming a cache directory that does not
 * exist; `none`, no records at all.
 *
 * @param {import('node:test').TestContext} t
 * @param {{ pluginJson?: boolean, key?: boolean | null, layout?: 'installed' | 'directory' | 'none', qa?: boolean, driverScript?: boolean }} [options]
 *   `pluginJson: false` leaves `plugin.json` out; `qa: true` turns `phases.qa` on;
 *   `driverScript: false` leaves `bin/devscene-planning-driver` out of the planted environment.
 */
async function pilotFixture(t, { pluginJson = true, key = true, layout = 'installed', qa = false, driverScript = true } = {}) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'watcher-planning-driver-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const stubDir = join(root, 'stub');
  const uvBin = join(root, 'uv-bin');
  await mkdir(stubDir);
  await mkdir(uvBin);

  const f = await createWatcherFixture(t, { branch: BRANCH, pathPrefix: uvBin });
  if (f === null) return null;

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

  // The fixture's environment is a link to this checkout's real one; the planted one replaces it.
  const scripts = join(f.dir, INIT_SCRIPTS_DIR);
  const venv = join(scripts, 'python', '.venv');
  await unlink(venv);
  await mkdir(join(venv, 'bin'), { recursive: true });
  await writeFile(join(venv, 'pyvenv.cfg'), 'home = /nonexistent\n', 'utf8');
  if (driverScript) {
    await writeFile(join(venv, 'bin', DRIVER), '#!/usr/bin/env bash\nexit 99\n', { mode: 0o755 });
  }

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
  await mkdir(join(plugin, 'instructions'));
  if (pluginJson) await copyFile(join(source, '.claude-plugin', 'plugin.json'), join(plugin, '.claude-plugin', 'plugin.json'));
  await copyFile(join(source, 'instructions', CORE), join(plugin, 'instructions', CORE));

  await writeFile(join(stubDir, 'agent-stub.mjs'), AGENT_STUB_SOURCE, 'utf8');
  await writeFile(join(stubDir, 'uv-stub.mjs'), UV_STUB_SOURCE, 'utf8');
  await writeFile(join(stubDir, 'mode.json'), JSON.stringify({ driver: HANDOFF }), 'utf8');
  const cli = join(stubDir, 'agent-cli');
  await writeFile(cli, `#!/usr/bin/env bash\nexec '${process.execPath}' '${join(stubDir, 'agent-stub.mjs')}' '${stubDir}' "$@"\n`, {
    mode: 0o755,
  });
  await writeFile(
    join(uvBin, 'uv'),
    `#!/usr/bin/env bash\nexec '${process.execPath}' '${join(stubDir, 'uv-stub.mjs')}' '${stubDir}' "$@"\n`,
    { mode: 0o755 },
  );

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
    cli,
    plugin,
    scripts,
    venv,
    /**
     * A machine state directory outside `f.dir`: the pilot runs in place, so the default one under
     * `f.dir` lies under the session-writable worktree and the watcher writes no manifest there.
     */
    stateHome: join(root, 'state'),
    /** The `uv` stub's answer to a `run` call: `{ status, stdout, files? }`. */
    setDriver: (driver) => writeFile(join(stubDir, 'mode.json'), JSON.stringify({ driver }), 'utf8'),
    /** Each call the stubs saw, in order: `{ kind: 'setup' | 'engine' | 'uv', argv, prompt?, env?, topLevel?, answered? }`. */
    calls: () =>
      existsSync(callsPath)
        ? readFileSync(callsPath, 'utf8')
            .split('\n')
            .filter(Boolean)
            .map((line) => JSON.parse(line))
        : [],
    passStderr: '',
    /** One pass with the stub as the agent CLI and the fixture's own `CLAUDE_CONFIG_DIR`. */
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
        ['-c', '. "$1"; hr_run_profile_absent_file "$(hr_repo_slug "$2")" "$3"', '_', join(scripts, 'lib', 'harness-run-lib.sh'), f.dir, BRANCH],
        f.watcherEnv(env),
        { timeoutMs: TICK_TIMEOUT_MS, signal: t.signal },
      );
      assert.equal(printed.status, 0, printed.stderr);
      return printed.stdout.trim();
    },
  };
}

/** `argv` without `-p <prompt>`, `--output-format <format>` and `--verbose`. */
function sharedFlags(argv) {
  const out = [];
  for (let at = 0; at < argv.length; at += 1) {
    if (argv[at] === '-p' || argv[at] === '--output-format') {
      at += 1;
    } else if (argv[at] !== '--verbose') {
      out.push(argv[at]);
    }
  }
  return out;
}

/**
 * The `uv` argv the watcher owes the driver, by the story index's contract, for the engine session
 * `engine` launched after it; `pluginDirAdded` when the shared flags already carry the plugin root.
 */
function expectedUvArgv(f, engine, { pluginDirAdded = false } = {}) {
  const py = join(f.scripts, 'python');
  return [
    'run', '--frozen', '--no-sync', '--no-cache', '--project', join(py, 'devscene-flow-host'),
    DRIVER,
    '--branch', BRANCH,
    '--worktree', f.dir,
    '--main-repo', f.dir,
    '--plugin-dir', f.plugin,
    '--flows', join(f.scripts, 'flows'),
    '--log', join(f.dir, RUN_LOG),
    '--formatter', join(f.scripts, FORMATTER),
    ...(pluginDirAdded ? ['--plugin-dir-added'] : []),
    '--',
    f.cli,
    ...sharedFlags(engine.argv),
  ];
}

/** The environment the `uv` stub must have seen. */
function expectedUvEnv(f) {
  const py = join(f.scripts, 'python');
  return {
    DEVSCENE_MAIN_REPO: f.dir,
    CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS: '0',
    UV_PROJECT_ENVIRONMENT: join(py, '.venv'),
    PYTHONPATH: `${join(py, 'devscene-flow-host', 'src')}:${join(py, 'graphscene', 'src')}`,
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

/** The lines of the watcher log carrying `text`. */
function watcherLines(f, text) {
  return f.watcherLog().split('\n').filter((l) => l.includes(text));
}

function show(f) {
  const runLog = join(f.dir, RUN_LOG);
  return [
    `--- calls\n${f.calls().map((c) => `${c.kind} ${c.kind === 'uv' ? c.argv.join(' ') : ''}`).join('\n')}`,
    `--- watcher log\n${f.watcherLog().split('\n').filter((l) => !l.includes('session environment for')).join('\n')}`,
    `--- run log tail\n${(existsSync(runLog) ? readFileSync(runLog, 'utf8') : '').split('\n').slice(-12).join('\n')}`,
    `--- pass stderr\n${f.passStderr}`,
  ].join('\n');
}

for (const [name, key] of [
  ['key absent', null],
  ['key false', false],
]) {
  test(`${name}: no uv call and one engine session, with no clause, though the launch would be ready`, async (t) => {
    const f = await pilotFixture(t, { key });
    if (f === null) return;
    await f.armPauseResume();
    await f.pass();
    const calls = f.calls();
    assert.deepEqual(calls.map((c) => c.kind), ['engine'], show(f));
    assert.equal(calls[0].prompt.includes(CLAUSE), false);
    assert.equal(f.watcherLog().includes('planning driver'), false, f.watcherLog());
  });
}

test('key on and ready: the setup session, one uv call on the contract argv, then the engine session; the hand-off archives only the consumed pair', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.writeQuestion(
    1,
    '# Questions from task-plan-writer\n\nRaised by: task-plan-writer (script-driven planning)\n\n## Q1 — Which storage key?\n\nWhich storage key?\n',
  );
  await f.writeAnswer(1, 'Use `fixture.storage`.\n');
  await f.writeQuestion(2, '# Questions from Phase G\n\nRaised by: Phase G — Run gates (test-fix-plan-writer)\n\n## Questions\n1. Which gate?\n');
  await f.writeAnswer(2, 'The typecheck gate.\n');
  await f.seedRecord({ status: 'parked' });
  await f.setDriver({ status: 0, stdout: 'consumed: 1' });

  await f.pass();
  const calls = f.calls();
  assert.deepEqual(calls.map((c) => c.kind), ['setup', 'uv', 'engine'], show(f));
  const [setup, uv, engine] = calls;
  assert.ok(setup.prompt.includes(CLAUSE), show(f));
  assert.equal(engine.prompt.includes(CLAUSE), false);
  assert.deepEqual(sharedFlags(setup.argv), sharedFlags(engine.argv));
  assert.deepEqual(uv.argv, expectedUvArgv(f, engine), show(f));
  assert.deepEqual(uv.env, expectedUvEnv(f));

  assert.deepEqual(engine.answered, ['answer_1.md', 'question_1.md'], show(f));
  assert.deepEqual(engine.topLevel, ['answer_2.md', 'question_2.md'], show(f));
  assert.equal(watcherLines(f, `planning driver handed off '${BRANCH}' (archived the answered pair(s) it consumed: 1)`).length, 1, show(f));
  assert.equal(f.record().status, 'completed', show(f));
});

test('the driver stops on a park: no engine session, and the run is parked from the question on disk', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.setDriver({
    status: 3,
    stdout: 'stopped: park',
    files: { [`${CLAR}/question_1.md`]: '# Questions from task-plan-writer\n\n## Q1 — Which storage key does the feature use?\n' },
  });
  await f.armPauseResume();
  await f.pass();
  assert.deepEqual(f.calls().map((c) => c.kind), ['setup', 'uv'], show(f));
  assert.equal(f.record().status, 'parked', show(f));
});

test('the driver stops undelivered: the run pauses and its one paused notification names the overload', async (t) => {
  const f = await pilotFixture(t);
  if (f === null) return;
  await f.setDriver({ status: 3, stdout: 'stopped: undelivered', files: { [`${STATE_DIR}/PAUSE_ACK`]: '' } });
  await f.armPauseResume();
  await f.pass();
  assert.deepEqual(f.calls().map((c) => c.kind), ['setup', 'uv'], show(f));
  assert.equal(f.record().status, 'paused', show(f));
  const paused = f.notifications().filter((n) => n.event === 'paused' && n.branch === BRANCH);
  assert.equal(paused.length, 1, `${JSON.stringify(f.notifications())}\n${show(f)}`);
  assert.ok(paused[0].detail.startsWith(UNDELIVERED_DETAIL), `${paused[0].detail}\n${show(f)}`);
});

for (const [name, driver, code] of [
  ['exits 2', { status: 2, stdout: '' }, 2],
  ['exits 0 with no consumed: line', { status: 0, stdout: '' }, 0],
]) {
  test(`the driver ${name}: no engine session, the run is failed, and the log names the exit`, async (t) => {
    const f = await pilotFixture(t);
    if (f === null) return;
    await f.setDriver(driver);
    await f.armPauseResume();
    await f.pass();
    assert.deepEqual(f.calls().map((c) => c.kind), ['setup', 'uv'], show(f));
    assert.equal(f.record().status, 'failed', show(f));
    assert.equal(watcherLines(f, `planning driver failed for '${BRANCH}' (${DRIVER} exit ${code})`).length, 1, show(f));
  });
}

test('key on, and the environment has no devscene-planning-driver: no uv run, one engine session, and the off line with its cause', async (t) => {
  const f = await pilotFixture(t, { driverScript: false });
  if (f === null) return;
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.deepEqual(calls.map((c) => c.kind), ['engine'], show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  const off = watcherLines(f, `planning driver off for '${BRANCH}': `);
  assert.equal(off.length, 1, f.watcherLog());
  assert.ok(
    off[0].includes(`planning driver off for '${BRANCH}': the flow host cannot run ${DRIVER} (${f.venv} has no ${DRIVER})`),
    off[0],
  );
});

test('key on, and the runtime root has no plugin.json: one engine session, no clause, and the off line', async (t) => {
  const f = await pilotFixture(t, { pluginJson: false });
  if (f === null) return;
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.deepEqual(calls.map((c) => c.kind), ['engine'], show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  const off = watcherLines(f, `planning driver off for '${BRANCH}': `);
  assert.equal(off.length, 1, f.watcherLog());
  assert.ok(off[0].includes(`'${f.plugin}/.claude-plugin/plugin.json' is not readable`), off[0]);
});

test('key on, and no runtime root resolves from the records: one engine session, no clause, and one off line naming it', async (t) => {
  const f = await pilotFixture(t, { layout: 'none' });
  if (f === null) return;
  await f.armPauseResume();
  await f.pass();
  const calls = f.calls();
  assert.deepEqual(calls.map((c) => c.kind), ['engine'], show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  const off = watcherLines(f, `planning driver off for '${BRANCH}': `);
  assert.equal(off.length, 1, f.watcherLog());
  assert.ok(
    off[0].endsWith(`planning driver off for '${BRANCH}': the plugin's runtime root could not be resolved from the agent runner's records`),
    off[0],
  );
});

test('key not a boolean: one engine session, no clause, and one off line naming the key', async (t) => {
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
  assert.deepEqual(calls.map((c) => c.kind), ['engine'], show(f));
  assert.equal(calls[0].prompt.includes(CLAUSE), false);
  const off = watcherLines(f, `planning driver off for '${BRANCH}': `);
  assert.equal(off.length, 1, f.watcherLog());
  assert.ok(off[0].includes('execution.scriptDrivenPlanning is not a boolean'), off[0]);
});

test('a job with the key on: the setup session, one uv call on the contract argv, then the engine session', async (t) => {
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
  assert.deepEqual(calls.map((c) => c.kind), ['setup', 'uv', 'engine'], detail);
  const [setup, uv, engine] = calls;
  assert.ok(setup.prompt.includes(CLAUSE), detail);
  assert.match(setup.prompt, /executes in a GitHub Actions job \(execution: github-actions\), where the interactive-test phase is unsupported/);
  assert.equal(values(setup.argv, '--add-dir').filter((d) => d === f.plugin).length, 1, setup.argv.join(' '));
  assert.equal(engine.prompt.includes(CLAUSE), false);
  assert.deepEqual(uv.argv, expectedUvArgv(f, engine, { pluginDirAdded: true }), detail);
  assert.deepEqual(uv.env, expectedUvEnv(f));
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
