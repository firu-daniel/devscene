/**
 * The fixture and stub agent CLI the planning-driver suites share: `pd_drive` from the copies
 * `init` wrote, run against a fixture repository with a stub standing in for every node session.
 *
 * **The rule this module exists to enforce: the driver under test is the set of libraries `init`
 * shipped into the fixture — `lib/harness-run-lib.sh` and the three planning libraries — never the
 * templates in this checkout, and the plugin it reads is a copy under the system temp directory.**
 * A case that sourced the templates would pass on libraries `init` had failed to write, and a case
 * aimed at this checkout's plugin could not edit its core.
 *
 * `node --test test` loads this file as a test file of its own, so nothing here runs at import time.
 *
 * The fixture is one repository on `feat_x`, both the main checkout and the worktree `pd_drive`
 * runs in, with `phases.parity` `true` (a round's set is three gates) and `phases.qa` `false`. Its
 * bare `origin` is the one `createFixture` seeds, so `push-branch.sh` has a remote.
 *
 * The stub reads `--agent`, `-p`, `--plugin-dir` and `--json-schema` from its argv and acts on the
 * entry the case's script holds for that agent at that call index — the index counts the agent's
 * calls across every `pd_drive` of one fixture. An entry is
 * `{ outcome?, findings?, sleepMs?, mode?, friction?, touch?, return? }`: `mode` is `no-init`, `no-result`,
 * `undeclared` (outcome `SHIP`), `not-success` (a `result` of subtype `error_max_turns` with
 * `is_error`), `no-decision` (a `success` result whose text is no JSON object) or `withhold` (the
 * `init` event drops `Glob` and `Grep` from the declared tools when they include `Bash`, as Claude
 * Code 2.1.325 does); `findings`, on a
 * gate, is the verdict (`PASS` or `FAIL`) of the findings file it writes whatever its outcome, so
 * `{ outcome: 'blocker', findings: 'PASS' }` leaves a PASS file and then fails; with `outcome`
 * `PASS` or `FAIL` and a different `findings`, the decision carries no `findings_file`, which the
 * driver records as `error`; `touch` names a
 * file it creates under `<stateDir>/` before its sleep, such as `STOP` or `PAUSE`. A `sleepMs` past
 * `drive`'s `stallSecs` is a stall the driver kills. With no entry a gate returns `PASS` and a
 * writer `returned`.
 */

import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { copyFile, mkdir, mkdtemp, readdir, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';

import { INIT_SCRIPTS_DIR, WORKSPACE_ROOT, runBash, runGit } from './fixture.mjs';
import { stateDirOf, walkerFixture, walkerUnavailable } from './walker.mjs';

export const BRANCH = 'feat_x';

/** The six agents the planning graph dispatches. */
const PLANNING_AGENTS = [
  'task-plan-writer',
  'business-parity-reviewer',
  'architecture-reviewer',
  'task-plan-reviewer',
  'ui-tests-plan-writer',
  'ui-tests-plan-reviewer',
];

const LIBRARIES = ['harness-run-lib', 'planning-node-lib', 'planning-record-lib', 'planning-driver-lib'];

/** Bounds one `pd_drive`; its group is killed past it (`fixture.mjs` → choice 6). */
const DRIVE_TIMEOUT_MS = 180_000;

/** The reason a driver case cannot run on this host, or `false`. */
export function driverUnavailable() {
  return walkerUnavailable();
}

const STUB_SOURCE = String.raw`
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const argv = process.argv.slice(2);
const flag = (name) => { const at = argv.indexOf(name); return at === -1 ? '' : argv[at + 1]; };
const prompt = flag('-p');
const qualified = flag('--agent');
const agent = qualified.slice(qualified.indexOf(':') + 1);
const pluginDir = flag('--plugin-dir');
JSON.parse(flag('--json-schema'));
const dir = process.env.STUB_DIR;
const cwd = process.cwd();

const countFile = join(dir, 'count-' + agent);
const index = existsSync(countFile) ? Number(readFileSync(countFile, 'utf8')) : 0;
writeFileSync(countFile, String(index + 1));
const script = JSON.parse(readFileSync(join(dir, 'script.json'), 'utf8'));
const entry = (script[agent] ?? [])[index] ?? {};
writeFileSync(join(dir, 'prompts', agent + '-' + index + '.txt'), prompt);
appendFileSync(join(dir, 'calls.log'), agent + ' ' + index + ' start ' + Date.now() + '\n');

if (entry.touch) writeFileSync(join(process.env.STUB_STATE, entry.touch), 'stub\n');
if (entry.sleepMs) Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, entry.sleepMs);

const lines = prompt.split('\n');
const value = (key) => { const line = lines.find((l) => l.startsWith(key)); return line === undefined ? '' : line.slice(key.length); };
const put = (rel, text) => { mkdirSync(dirname(join(cwd, rel)), { recursive: true }); writeFileSync(join(cwd, rel), text); };

const decision = {};
const folder = value('findings_folder: ');
if (folder !== '') {
  decision.outcome = entry.outcome ?? 'PASS';
  const verdict = entry.findings ?? decision.outcome;
  if (verdict === 'PASS' || verdict === 'FAIL') {
    const findings = folder + 'review_' + value('iteration: ') + '.md';
    put(findings, '# review\nverdict: ' + verdict + '\nreview_mode: ' + value('review_mode: ') + '\n');
    if (verdict === decision.outcome) decision.findings_file = findings;
  }
  decision.return = entry.return ?? 'verdict: ' + decision.outcome;
} else {
  decision.outcome = entry.outcome ?? 'returned';
  if (decision.outcome === 'returned') {
    let story = value('Story index: ');
    let tasks = value('Per-task files: ');
    const initial = /^Outputs: story index at (\S+) and per-task files at (\S+)task_<N>_plan\.md$/m.exec(prompt);
    if (initial !== null) [, story, tasks] = initial;
    put(story, '# Story plan\n\nwritten by call ' + index + '\n');
    put(tasks + 'task_1_plan.md', '### Task 1\n\nwritten by call ' + index + '\n');
    const note = value('Revision note: ');
    if (note !== '') put(note, '# Revision\n\nwritten by call ' + index + '\n');
    decision.return = 'story_file: ' + story + '\ntask_files_dir: ' + tasks + '\ntasks_count: 1';
  } else {
    decision.return = entry.return ?? 'stub ' + decision.outcome;
  }
}
if (entry.return !== undefined) decision.return = entry.return;
if (entry.mode === 'undeclared') decision.outcome = 'SHIP';
decision.harness_friction = entry.friction === undefined ? [] : [entry.friction];

const tools = (() => {
  const text = readFileSync(join(pluginDir, 'agents', agent + '.md'), 'utf8');
  const line = text.split('\n').find((l) => l.startsWith('tools:'));
  return line.slice('tools:'.length).split(',').map((t) => t.trim()).filter(Boolean);
})();
appendFileSync(join(dir, 'calls.log'), agent + ' ' + index + ' end ' + Date.now() + '\n');
const events = [];
const initTools = entry.mode === 'withhold' && tools.includes('Bash') ? tools.filter((t) => t !== 'Glob' && t !== 'Grep') : tools;
if (entry.mode !== 'no-init') events.push({ type: 'system', subtype: 'init', session_id: 'stub', tools: initTools });
if (entry.mode === 'not-success') {
  events.push({ type: 'result', subtype: 'error_max_turns', is_error: true, total_cost_usd: 0.01, permission_denials: [] });
} else if (entry.mode === 'no-decision') {
  events.push({ type: 'result', subtype: 'success', is_error: false, total_cost_usd: 0.01, permission_denials: [], result: 'verdict: PASS' });
} else if (entry.mode !== 'no-result') {
  events.push({ type: 'result', subtype: 'success', is_error: false, total_cost_usd: 0.01, permission_denials: [], structured_output: decision });
}
process.stdout.write(events.map((e) => JSON.stringify(e)).join('\n') + (events.length ? '\n' : ''));
`;

/**
 * A fixture `init` wired, on `feat_x`, seeded with a task prompt and a task-engine ledger, beside a
 * plugin copy and the stub.
 *
 * @param {import('node:test').TestContext} t
 * @param {{ script?: Record<string, object[]>, core?: (text: string) => string }} [options]
 *   `script` maps an agent to its entries by call index; `core` transforms the copied planning core.
 */
export async function driverFixture(t, { script = {}, core = (text) => text } = {}) {
  const { dir, cleanup } = await walkerFixture({ parity: true, qa: false, branch: BRANCH });
  t.after(cleanup);
  const root = await realpath(await mkdtemp(join(tmpdir(), 'planning-driver-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const sd = stateDirOf(dir);

  const ledger = `${sd}/flow_progress/${BRANCH}_progress.md`;
  const prompt = `${sd}/task_prompts/${BRANCH}_task_prompt.md`;
  const seed = {
    [ledger]: [
      `# Flow progress — ${BRANCH}   (engine: task)`,
      '',
      '## Run mode',
      `Source: ${prompt} → \`### Run mode\``,
      '- skipped: none',
      '- phases: parity=true, qa=false, docs=false',
      '- remote-skipped: none',
      '',
      '## Planning',
      '- [x] P0. Untrusted input screened (prompt-injection-reviewer SAFE)',
      '- [ ] P1. Task plan converged (business_parity + architecture + task-plan-reviewer all PASS)',
      '- [ ] P2. UI-test plan converged (ui-tests-plan-reviewer PASS) — or no_ui',
      '- [ ] P3. Plans committed & pushed (story index + per-task dir + UI-test plan)',
      '',
      '## Implementation',
      '- [ ] A.      Tasks implemented (story-index readiness all [x])',
      '',
    ].join('\n'),
    [prompt]: '# Task prompt\n\nAdd a fixture feature.\n',
  };
  for (const [rel, text] of Object.entries(seed)) {
    await mkdir(dirname(join(dir, rel)), { recursive: true });
    await writeFile(join(dir, rel), text, 'utf8');
  }
  await runGit(dir, ['checkout', '--quiet', '-b', BRANCH]);
  await runGit(dir, ['add', '--', 'devscene.config.json', ...Object.keys(seed)]);
  await runGit(dir, ['commit', '--quiet', '-m', 'fixture: seed']);

  const plugin = join(root, 'plugin');
  await mkdir(join(plugin, '.claude-plugin'), { recursive: true });
  await mkdir(join(plugin, 'agents'));
  await mkdir(join(plugin, 'instructions'));
  const source = join(WORKSPACE_ROOT, 'plugin');
  await copyFile(join(source, '.claude-plugin', 'plugin.json'), join(plugin, '.claude-plugin', 'plugin.json'));
  for (const agent of PLANNING_AGENTS) {
    await copyFile(join(source, 'agents', `${agent}.md`), join(plugin, 'agents', `${agent}.md`));
  }
  const coreName = 'task_plan_writing_instructions_core.md';
  await writeFile(join(plugin, 'instructions', coreName), core(await readFile(join(source, 'instructions', coreName), 'utf8')));

  const stubDir = join(root, 'stub');
  await mkdir(join(stubDir, 'prompts'), { recursive: true });
  await writeFile(join(stubDir, 'stub.mjs'), STUB_SOURCE);
  const stub = join(stubDir, 'agent-cli');
  await writeFile(stub, `#!/usr/bin/env bash\nexec '${process.execPath}' '${join(stubDir, 'stub.mjs')}' "$@"\n`, { mode: 0o755 });
  const home = join(root, 'home');
  await mkdir(home);

  const f = {
    dir,
    root,
    sd,
    plugin,
    log: join(root, 'run.log'),
    stubDir,
    env: {
      W: dir,
      P: plugin,
      LOG: join(root, 'run.log'),
      STUB: stub,
      STUB_DIR: stubDir,
      STUB_STATE: join(dir, sd),
      HOME: home,
      XDG_CONFIG_HOME: join(home, '.config'),
      GH_TOKEN: '',
      GITHUB_TOKEN: '',
      HARNESS_PR_TOKEN: '',
      DEVSCENE_GIT_TOKEN: '',
      GITHUB_ACTIONS: '',
      PUSH_RETRY_DELAY_SECS: '0',
    },
    /** Replace the stub's script; call indices keep counting. */
    setScript: (next) => writeFile(join(stubDir, 'script.json'), JSON.stringify(next)),
    write: async (rel, text) => {
      await mkdir(dirname(join(dir, rel)), { recursive: true });
      await writeFile(join(dir, rel), text, 'utf8');
    },
    read: (rel) => readFile(join(dir, rel), 'utf8'),
    exists: (rel) => existsSync(join(dir, rel)),
  };
  await f.setScript(script);
  return f;
}

/** The calls log as one record per call, in start order, each with its prompt. */
async function readCalls(f) {
  const path = join(f.stubDir, 'calls.log');
  if (!existsSync(path)) return [];
  const byKey = new Map();
  for (const line of (await readFile(path, 'utf8')).split('\n').filter(Boolean)) {
    const [agent, index, edge, ms] = line.split(' ');
    const key = `${agent}-${index}`;
    if (!byKey.has(key)) byKey.set(key, { agent, index: Number(index), start: NaN, end: NaN, prompt: '' });
    byKey.get(key)[edge] = Number(ms);
  }
  const calls = [...byKey.values()].sort((a, b) => a.start - b.start);
  for (const call of calls) call.prompt = await readFile(join(f.stubDir, 'prompts', `${call.agent}-${call.index}.txt`), 'utf8');
  return calls;
}

/**
 * Run `pd_drive feat_x <dir> <log>` once, from the shipped libraries, with the stub as every
 * session, `PD_BACKOFF_SECS` 0 and `PD_NODE_STALL_SECS` `stallSecs` (0, off, by default).
 *
 * @param {{ stallSecs?: number }} [options]
 * @returns {Promise<{ status: number, stderr: string, log: string, calls: Array<{ agent: string,
 *   index: number, start: number, end: number, prompt: string }>, subjects: string[],
 *   clarifications: Record<string, string> }>} `subjects` oldest first.
 */
export async function drive(t, f, { stallSecs = 0 } = {}) {
  const body = [
    'cd "$W" || exit 90',
    ...LIBRARIES.map((lib) => `. "$W/${INIT_SCRIPTS_DIR}/lib/${lib}.sh" || exit 91`),
    'session_exec() { exec "$STUB" -p "$1" "${@:2}"; }',
    'PD_PLUGIN_DIR=$P PD_MAIN_REPO=$W PD_SESSION_EXEC=session_exec PD_FORMATTER=cat',
    `PD_NODE_STALL_SECS=${Number(stallSecs)} PD_BACKOFF_SECS=0`,
    `pd_drive ${BRANCH} "$W" "$LOG"`,
  ].join('\n');
  const r = await runBash(f.dir, ['-c', body], f.env, { timeoutMs: DRIVE_TIMEOUT_MS, signal: t.signal });
  const subjects = (await runGit(f.dir, ['log', '--reverse', '--format=%s', `refs/heads/${BRANCH}`])).stdout
    .split('\n')
    .filter(Boolean);
  const clarDir = join(f.dir, f.sd, 'clarifications', BRANCH);
  const clarifications = {};
  if (existsSync(clarDir)) {
    for (const entry of await readdir(clarDir, { withFileTypes: true })) {
      if (entry.isFile()) clarifications[entry.name] = await readFile(join(clarDir, entry.name), 'utf8');
    }
  }
  return {
    status: r.status,
    stderr: r.stderr,
    log: existsSync(f.log) ? await readFile(f.log, 'utf8') : '',
    calls: await readCalls(f),
    subjects,
    clarifications,
  };
}

/** One drive's outcome, printed whole when an assertion on it fails. */
export function show(r) {
  return `status ${r.status}\n--- stderr\n${r.stderr}\n--- log\n${r.log}\n--- subjects\n${r.subjects.join('\n')}`;
}

/** Assert `expected` appears in `actual` as a subsequence, in order. */
export function assertInOrder(actual, expected, message) {
  let at = 0;
  for (const item of actual) if (item === expected[at]) at += 1;
  assert.equal(at, expected.length, `${message}\nexpected in order: ${JSON.stringify(expected)}\nactual: ${JSON.stringify(actual)}`);
}
