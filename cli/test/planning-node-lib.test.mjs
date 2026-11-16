/**
 * One planning node session, `cli/templates/scripts/lib/planning-node-lib.sh`: the core's dispatch
 * blocks, the node's prompt and schema, the per-node flags, the launch and the validated read.
 *
 * **The rule this suite enforces: a node's result is a declared outcome, `error` or
 * `undelivered`, never a guess.** `pnl_reap` decides in one fixed order — no `init` event, an
 * `init` tool the agent does not declare, no `result` (or an API overload), a failed session, no
 * decision object, an undeclared outcome, a missing `findings_file`, `questions` with a blank
 * `return` — and one case pins each rule, beside the declared outcomes that pass. Each `error` case
 * also pins its `class=`: `infra` for rules 1, 4 and 5, `agent` for the rest. `withheld=` reports
 * the declared tools the `init` event lacks and refuses nothing.
 *
 * Each case copies `lib/harness-run-lib.sh`, the library and the shipped planning graph from
 * `cli/templates/scripts/` into its own fixture under the system temp directory, beside a plugin
 * directory holding this checkout's planning core and fixture agent files, and sources them in one
 * `bash` process. `PD_SESSION_EXEC` names a stub function that runs
 * `$DEVSCENE_AGENT_CLI -p "$1" "${@:2}"`; the agent CLI is a stub that records its argv and prints
 * canned `stream-json` lines. The agent files are written here rather than copied, so a tools
 * assertion holds the library's comparison and not the corpus's current allowlists.
 */

import assert from 'node:assert/strict';
import { copyFile, mkdir, mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { PACKAGE_ROOT, WORKSPACE_ROOT, runBash } from './helpers/fixture.mjs';
import { walkerUnavailable } from './helpers/walker.mjs';

const SKIP = walkerUnavailable();
const TEMPLATES = join(PACKAGE_ROOT, 'templates', 'scripts');
const CORE_SOURCE = join(WORKSPACE_ROOT, 'plugin', 'instructions', 'task_plan_writing_instructions_core.md');
const PLUGIN_NAME = 'fixture-plugin';

const AGENTS = {
  'task-plan-writer': 'Read, Write, mcp__docs__search_docs',
  'task-plan-reviewer': 'Read, Grep, Bash, mcp__docs__search_docs',
  'ui-tests-plan-reviewer': 'Read, Grep, mcp__docs__search_docs',
  plain: 'Read, Bash',
};
const WRITER_TOOLS = ['Read', 'Write'];
const REVIEWER_TOOLS = ['Read', 'Grep', 'Bash'];
const UI_REVIEWER_TOOLS = ['Read', 'Grep'];

const PRELUDE = [
  '. "$W/s/lib/harness-run-lib.sh" || exit 99',
  '. "$W/s/lib/planning-node-lib.sh" || exit 98',
  'session() { "$DEVSCENE_AGENT_CLI" -p "$1" "${@:2}"; }',
  'PD_SESSION_EXEC=session',
  'PD_FORMATTER=cat',
].join('\n');

/**
 * A fresh fixture: a worktree carrying the shipped libraries and graph, a plugin directory, and a
 * stub agent CLI. `core` transforms the copied planning core's text.
 */
async function fixture(t, { core = (text) => text } = {}) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'planning-node-lib-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const wt = join(root, 'wt');
  const plugin = join(root, 'plugin');
  await mkdir(join(wt, 's', 'lib'), { recursive: true });
  await mkdir(join(wt, 's', 'flows'), { recursive: true });
  await writeFile(
    join(wt, 'devscene.config.json'),
    JSON.stringify({ version: 1, defaultBranch: 'main', stateDir: 'devscene/', scriptsDir: 's' }),
  );
  for (const lib of ['harness-run-lib.sh', 'planning-node-lib.sh']) {
    await copyFile(join(TEMPLATES, 'lib', lib), join(wt, 's', 'lib', lib));
  }
  await copyFile(join(TEMPLATES, 'flows', 'task_plan_writing.graph.json'), join(wt, 's', 'flows', 'task_plan_writing.graph.json'));

  await mkdir(join(plugin, '.claude-plugin'), { recursive: true });
  await mkdir(join(plugin, 'agents'), { recursive: true });
  await mkdir(join(plugin, 'instructions'), { recursive: true });
  await writeFile(join(plugin, '.claude-plugin', 'plugin.json'), JSON.stringify({ name: PLUGIN_NAME }));
  for (const [agent, tools] of Object.entries(AGENTS)) {
    await writeFile(join(plugin, 'agents', `${agent}.md`), `---\nname: ${agent}\ndescription: fixture\ntools: ${tools}\nmodel: inherit\n---\n\nBody.\n`);
  }
  await writeFile(
    join(plugin, 'instructions', 'task_plan_writing_instructions_core.md'),
    core(await readFile(CORE_SOURCE, 'utf8')),
  );

  const stub = join(root, 'agent-cli');
  await writeFile(
    stub,
    '#!/usr/bin/env bash\nprintf \'%s\\n\' "$@" > "$STUB_ARGV"\n[ ! -s "$STUB_OUT" ] || cat "$STUB_OUT"\nexit 0\n',
    { mode: 0o755 },
  );
  const env = {
    W: wt,
    P: plugin,
    DEVSCENE_AGENT_CLI: stub,
    STUB_OUT: join(root, 'stub-out.jsonl'),
    STUB_ARGV: join(root, 'stub-argv'),
  };
  /** Run `body` after the prelude, in the fixture root. */
  const bash = (body) => runBash(root, ['-c', `${PRELUDE}\n${body}`], env);
  return { root, wt, plugin, env, bash };
}

const init = (tools) => ({ type: 'system', subtype: 'init', session_id: 's1', tools });
const result = (extra = {}) => ({
  type: 'result',
  subtype: 'success',
  is_error: false,
  total_cost_usd: 0.25,
  permission_denials: [],
  ...extra,
});

/**
 * Launch one session of <node> as <agent> whose stub prints <events>, reap it, and return the
 * reaped keys, the return and friction texts, the stub's argv and the run's stream copy.
 */
async function reap(f, node, agent, events) {
  await writeFile(f.env.STUB_OUT, events.map((e) => (typeof e === 'string' ? e : JSON.stringify(e))).join('\n') + (events.length ? '\n' : ''));
  const log = join(f.root, 'run.log');
  const r = await f.bash(`
pnl_init "$P" "$W" || exit 97
pnl_launch 1 ${node} ${agent} 'the prompt' '${log}' || exit 96
h=$PNL_HANDLE
wait "\${h%%\t*}"
out=$(pnl_reap "$h") || exit 95
printf '%s\\n' "$out"
rf=$(printf '%s\\n' "$out" | sed -n 's/^return_file=//p')
ff=$(printf '%s\\n' "$out" | sed -n 's/^friction_file=//p')
printf '%s\\n' '--- return'
[ -z "$rf" ] || cat "$rf"
printf '\\n%s\\n' '--- friction'
[ -z "$ff" ] || cat "$ff"
pnl_cleanup
[ ! -e "$rf" ] && [ ! -e "$ff" ] || exit 94
`);
  assert.equal(r.status, 0, `exit ${r.status}\n${r.stderr}\n${r.stdout}`);
  const [head, rest] = r.stdout.split('--- return\n');
  const [returnText, frictionText] = rest.split('\n--- friction\n');
  const keys = Object.fromEntries(
    head.trimEnd().split('\n').map((line) => [line.slice(0, line.indexOf('=')), line.slice(line.indexOf('=') + 1)]),
  );
  const argv = (await readFile(f.env.STUB_ARGV, 'utf8')).split('\n');
  const runStream = await readFile(join(f.root, 'run.stream.jsonl'), 'utf8');
  const nodeStream = await readFile(join(f.root, 'run.planning', `1-${node}.stream.jsonl`), 'utf8');
  const manifest = await readFile(join(f.root, 'run.planning', 'node-sessions.jsonl'), 'utf8').catch(() => null);
  return { keys, returnText, frictionText, argv, runStream, nodeStream, manifest };
}

test('pnl_init reads the plugin name, the dispatch cap and every block', { skip: SKIP }, async (t) => {
  const f = await fixture(t, { core: (text) => text.replace(/MAX_TOTAL_DISPATCHES = \d+/, 'MAX_TOTAL_DISPATCHES = 7') });
  const r = await f.bash(`
pnl_init "$P" "$W" || exit 97
printf '%s|%s|%s\\n' "$PNL_PLUGIN_NAME" "$PNL_MAX_DISPATCHES" "$PNL_STATE_DIR"
[ -d "$PNL_TMP" ] || exit 93
d=$PNL_TMP; pnl_cleanup; [ ! -e "$d" ] || exit 92
`);
  assert.equal(r.status, 0, r.stderr);
  assert.equal(r.stdout, `${PLUGIN_NAME}|7|devscene\n`);
});

test('pnl_init refuses a core with one heading renamed, naming it', { skip: SKIP }, async (t) => {
  const f = await fixture(t, {
    core: (text) => text.replace('### 3. Architecture review (plan-review mode)', '### 3. Architecture review'),
  });
  const r = await f.bash('pnl_init "$P" "$W"; rc=$?; printf "%s" "${PNL_TMP-}"; exit $rc');
  assert.equal(r.status, 2);
  assert.equal(r.stdout, '', 'no temporary directory is left set');
  assert.match(r.stderr, /^planning-driver: the heading '### 3\. Architecture review \(plan-review mode\)' is not under '## Loop'/);
  assert.equal(r.stderr.trimEnd().split('\n').length, 1);
});

test('pnl_init refuses a core with no MAX_TOTAL_DISPATCHES integer', { skip: SKIP }, async (t) => {
  const f = await fixture(t, { core: (text) => text.replace(/MAX_TOTAL_DISPATCHES = \d+/, 'MAX_TOTAL_DISPATCHES = n') });
  const r = await f.bash('pnl_init "$P" "$W"');
  assert.equal(r.status, 2);
  assert.match(r.stderr, /^planning-driver: no 'MAX_TOTAL_DISPATCHES = <n>' line under '## Setup \(once per session\)'/);
});

test('pnl_init refuses a plugin manifest with no name', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  await writeFile(join(f.plugin, '.claude-plugin', 'plugin.json'), '{"name":""}');
  const r = await f.bash('pnl_init "$P" "$W"');
  assert.equal(r.status, 2);
  assert.match(r.stderr, /^planning-driver: .*plugin\.json' carries no non-empty name/);
});

test('pnl_prompt fills the walker values and leaves every other placeholder literal', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const r = await f.bash(`
pnl_init "$P" "$W" || exit 97
pnl_prompt plan_writer initial feat_x 0 '' || exit 1
echo ===
pnl_prompt plan_writer revision feat_x 2 '' devscene/a/review_1.md devscene/b/review_1.md || exit 1
echo ===
pnl_prompt plan_review '' feat_x 3 converging || exit 1
echo ===
pnl_prompt ui_writer revision feat_x 1 '' devscene/u/review_0.md || exit 1
pnl_cleanup
`);
  assert.equal(r.status, 0, r.stderr);
  const [initial, revision, gate, ui] = r.stdout.split('===\n');
  assert.equal(
    initial,
    [
      'Write the task plan.',
      'Branch: feat_x',
      'Task prompt: devscene/task_prompts/feat_x_task_prompt.md',
      'Outputs: story index at devscene/story_plans/feat_x_story_plan.md and per-task files at devscene/task_plans/feat_x/task_<N>_plan.md',
      '',
    ].join('\n'),
  );
  assert.equal(
    revision.split('\n').slice(0, 2).join('\n'),
    'Revise the task plan per findings at devscene/a/review_1.md, devscene/b/review_1.md.\n' +
      'Revision note: devscene/plan_revisions/feat_x/task_plan_revision_2.md',
  );
  assert.ok(gate.includes('findings_folder: devscene/task_plan_reviews/feat_x/\n'), gate);
  assert.ok(gate.includes('iteration: 3\nreview_mode: converging\n'), gate);
  assert.ok(gate.includes('prompt_path: devscene/task_prompts/feat_x_task_prompt.md\n'), gate);
  assert.equal(ui.split('\n')[0], 'Revise the UI-test plan per findings at devscene/u/review_0.md.');
});

test('pnl_schema enumerates exactly the node\'s declared outcomes', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const r = await f.bash(`
pnl_init "$P" "$W" || exit 97
pnl_schema plan_writer || exit 1
pnl_schema plan_review || exit 1
pnl_schema no_such_node; echo "rc=$?"
pnl_cleanup
`);
  assert.equal(r.status, 0, r.stderr);
  const [writer, reviewer, missing] = r.stdout.trimEnd().split('\n');
  const w = JSON.parse(writer);
  assert.deepEqual(w.properties.outcome.enum, ['returned', 'questions', 'error', 'blocker']);
  assert.deepEqual(w.required, ['outcome']);
  assert.equal(w.properties.findings_file.type, 'string');
  assert.equal(w.properties.return.type, 'string');
  assert.equal(w.properties.harness_friction.type, 'array');
  assert.deepEqual(w.properties.harness_friction.items, { type: 'string' });
  assert.deepEqual(JSON.parse(reviewer).properties.outcome.enum, ['PASS', 'FAIL', 'error', 'blocker']);
  assert.equal(missing, 'rc=2');
});

test('pnl_agent_flags splits MCP: no mcp__ tool disallows them, some keep only their servers', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const script = `
pnl_init "$P" "$W" || exit 97
pnl_agent_flags plan_review plain || exit 1
echo ===
pnl_agent_flags plan_review task-plan-reviewer || exit 1
echo ===
cat "$PNL_TMP/mcp-plan_review.json"
pnl_cleanup
`;
  const bare = await f.bash(script);
  assert.equal(bare.status, 0, bare.stderr);
  const [plain, withMcp, noFile] = bare.stdout.split('===\n');
  const plainLines = plain.trimEnd().split('\n');
  assert.deepEqual(plainLines.slice(0, 6), ['--agent', `${PLUGIN_NAME}:plain`, '--plugin-dir', f.plugin, '--add-dir', f.plugin]);
  assert.equal(plainLines[6], '--json-schema');
  assert.deepEqual(JSON.parse(plainLines[7]).properties.outcome.enum, ['PASS', 'FAIL', 'error', 'blocker']);
  assert.deepEqual(plainLines.slice(8), ['--disallowedTools', 'mcp__*']);
  const mcpLines = withMcp.trimEnd().split('\n');
  assert.deepEqual(mcpLines.slice(8, 10), ['--strict-mcp-config', '--mcp-config']);
  assert.equal(mcpLines.length, 11);
  assert.ok(!mcpLines.includes('--disallowedTools'));
  assert.deepEqual(JSON.parse(noFile), { mcpServers: {} });

  await writeFile(
    join(f.wt, '.mcp.json'),
    JSON.stringify({ mcpServers: { docs: { command: 'docs-server' }, playwright: { command: 'pw' } } }),
  );
  const filtered = await f.bash(script);
  assert.equal(filtered.status, 0, filtered.stderr);
  assert.deepEqual(JSON.parse(filtered.stdout.split('===\n')[2]), { mcpServers: { docs: { command: 'docs-server' } } });
});

test('pnl_launch runs the session through PD_SESSION_EXEC with the per-node flags, and pnl_reap copies its stream once', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const events = [init(REVIEWER_TOOLS), result({ structured_output: { outcome: 'PASS', findings_file: 'devscene/r/review_0.md', return: 'verdict: PASS' } })];
  const r = await reap(f, 'plan_review', 'task-plan-reviewer', events);
  assert.deepEqual(r.argv.slice(0, 4), ['-p', 'the prompt', '--agent', `${PLUGIN_NAME}:task-plan-reviewer`]);
  assert.ok(r.argv.includes('--json-schema'));
  const lines = events.map((e) => JSON.stringify(e)).join('\n') + '\n';
  assert.equal(r.nodeStream, lines);
  assert.equal(r.runStream, lines);
  assert.equal(r.manifest, '{"session_id":"s1","seq":"1","node":"plan_review"}\n');
  assert.match(r.keys.duration_secs, /^\d+$/);
  assert.equal(r.keys.cost, '0.25');
  assert.equal(r.keys.denials, '0');
  assert.equal(r.keys.withheld, '');
});

test('rule 1: a stub that exits 0 with empty stdout is error, no init event', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const r = await reap(f, 'plan_review', 'task-plan-reviewer', []);
  assert.equal(r.keys.kind, 'error');
  assert.equal(r.keys.outcome, '');
  assert.equal(r.keys.reason, 'the agent did not resolve: no init event');
  assert.equal(r.keys.class, 'infra');
  assert.equal(r.keys.return_file, '');
  assert.equal(r.keys.withheld, '');
  assert.equal(r.manifest, null, 'a session with no init event has no session id to record');
});

test('rule 2: init tools the agent does not declare are error; declared tools the init lacks are withheld, not refused', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const ok = { structured_output: { outcome: 'PASS', findings_file: 'f.md', return: 'x' } };
  const lacking = await reap(f, 'plan_review', 'task-plan-reviewer', [init(['Read', 'Bash']), result(ok)]);
  assert.equal(lacking.keys.kind, 'returned');
  assert.equal(lacking.keys.class, '');
  assert.equal(lacking.keys.withheld, 'Grep');

  const extra = await reap(f, 'plan_review', 'task-plan-reviewer', [init([...REVIEWER_TOOLS, 'Edit']), result(ok)]);
  assert.equal(extra.keys.kind, 'error');
  assert.equal(extra.keys.class, 'agent');
  assert.equal(extra.keys.reason, 'the init event grants tools the agent does not declare: [Edit]');
  assert.equal(extra.keys.withheld, '');

  const mixed = await reap(f, 'plan_review', 'task-plan-reviewer', [init(['Read', 'Bash', 'Edit']), result(ok)]);
  assert.equal(mixed.keys.kind, 'error', 'a lacking tool does not mask an extra one');
  assert.equal(mixed.keys.class, 'agent');
  assert.equal(mixed.keys.reason, 'the init event grants tools the agent does not declare: [Edit]');
  assert.equal(mixed.keys.withheld, 'Grep');

  const withMcp = await reap(f, 'plan_review', 'task-plan-reviewer', [init([...REVIEWER_TOOLS, 'mcp__docs__search_docs']), result(ok)]);
  assert.equal(withMcp.keys.kind, 'returned', 'an agent MCP tool present in init matches');
  assert.equal(withMcp.keys.withheld, '');

  const noMcp = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), result(ok)]);
  assert.equal(noMcp.keys.kind, 'returned');
  assert.equal(noMcp.keys.withheld, '', 'a declared mcp__ tool absent from init is never withheld');
});

test('rule 3: no result event, or an API overload, is undelivered', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const none = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS)]);
  assert.equal(none.keys.kind, 'undelivered');
  assert.equal(none.keys.reason, 'no result event');
  assert.equal(none.keys.class, '');

  for (const text of ['API Error: 529 {"type":"error","error":{"type":"overloaded_error","message":"Overloaded"}}', 'API Error: 500 Internal server error', 'API Error: 503 Service Unavailable']) {
    const r = await reap(f, 'plan_review', 'task-plan-reviewer', [
      init(REVIEWER_TOOLS),
      result({ subtype: 'success', is_error: true, result: text }),
    ]);
    assert.equal(r.keys.kind, 'undelivered', text);
    assert.equal(r.keys.outcome, '');
  }
});

test('rule 4: is_error, or a subtype other than success, is error', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const failed = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), result({ is_error: true, result: 'Prompt is too long' })]);
  assert.equal(failed.keys.kind, 'error');
  assert.equal(failed.keys.reason, 'the session ended as success with is_error');
  assert.equal(failed.keys.class, 'infra');

  const turns = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ subtype: 'error_max_turns', structured_output: { outcome: 'PASS', findings_file: 'f.md' } }),
  ]);
  assert.equal(turns.keys.kind, 'error');
  assert.equal(turns.keys.reason, 'the session ended as error_max_turns');
  assert.equal(turns.keys.class, 'infra');
});

test('rule 5: the decision is structured_output, else result parsed as JSON, else error', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const fallback = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ result: JSON.stringify({ outcome: 'FAIL', findings_file: 'devscene/r/review_2.md', return: 'verdict: FAIL' }) }),
  ]);
  assert.equal(fallback.keys.kind, 'returned');
  assert.equal(fallback.keys.outcome, 'FAIL');
  assert.equal(fallback.keys.findings, 'devscene/r/review_2.md');

  const none = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), result({ result: 'verdict: PASS' })]);
  assert.equal(none.keys.kind, 'error');
  assert.equal(none.keys.reason, 'the result carries no decision object');
  assert.equal(none.keys.class, 'infra');
});

test('rule 6: an undeclared outcome is error, and the rest of the decision is left unread', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const r = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ structured_output: { outcome: 'SHIP', findings_file: 'devscene/r/review_0.md', return: 'ship it', harness_friction: ['x'] } }),
  ]);
  assert.equal(r.keys.kind, 'error');
  assert.equal(r.keys.outcome, '');
  assert.equal(r.keys.reason, 'undeclared outcome SHIP');
  assert.equal(r.keys.class, 'agent');
  assert.equal(r.keys.findings, '');
  assert.equal(r.keys.return_file, '');
  assert.equal(r.keys.friction_file, '');
});

test('rule 7: FAIL anywhere, or PASS at a round gate, without findings_file is error', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const fail = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), result({ structured_output: { outcome: 'FAIL', return: 'verdict: FAIL' } })]);
  assert.equal(fail.keys.kind, 'error');
  assert.equal(fail.keys.reason, 'FAIL carries no findings_file');
  assert.equal(fail.keys.class, 'agent');

  const pass = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), result({ structured_output: { outcome: 'PASS', findings_file: ' ' } })]);
  assert.equal(pass.keys.kind, 'error');
  assert.equal(pass.keys.reason, 'PASS carries no findings_file');

  const uiFail = await reap(f, 'ui_review', 'ui-tests-plan-reviewer', [init(UI_REVIEWER_TOOLS), result({ structured_output: { outcome: 'FAIL' } })]);
  assert.equal(uiFail.keys.kind, 'error');

  const uiPass = await reap(f, 'ui_review', 'ui-tests-plan-reviewer', [init(UI_REVIEWER_TOOLS), result({ structured_output: { outcome: 'PASS' } })]);
  assert.equal(uiPass.keys.kind, 'returned', 'ui_review is no round gate');
  assert.equal(uiPass.keys.outcome, 'PASS');
});

test('rule 8: questions with a blank return is error', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const r = await reap(f, 'plan_writer', 'task-plan-writer', [init(WRITER_TOOLS), result({ structured_output: { outcome: 'questions', return: ' \n\t' } })]);
  assert.equal(r.keys.kind, 'error');
  assert.equal(r.keys.reason, 'questions with a blank return');
  assert.equal(r.keys.class, 'agent');
});

test('declared outcomes are returned: PASS, FAIL, returned and questions', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const pass = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ permission_denials: [{}, {}], structured_output: { outcome: 'PASS', findings_file: 'devscene/r/review_0.md', return: 'verdict: PASS' } }),
  ]);
  assert.deepEqual(
    { kind: pass.keys.kind, class: pass.keys.class, outcome: pass.keys.outcome, findings: pass.keys.findings, denials: pass.keys.denials, reason: pass.keys.reason },
    { kind: 'returned', class: '', outcome: 'PASS', findings: 'devscene/r/review_0.md', denials: '2', reason: '' },
  );
  assert.equal(pass.returnText, 'verdict: PASS');

  const fail = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ structured_output: { outcome: 'FAIL', findings_file: 'devscene/r/review_1.md', return: 'verdict: FAIL' } }),
  ]);
  assert.equal(fail.keys.kind, 'returned');
  assert.equal(fail.keys.outcome, 'FAIL');
  assert.equal(fail.keys.findings, 'devscene/r/review_1.md');

  const written = await reap(f, 'plan_writer', 'task-plan-writer', [
    init(WRITER_TOOLS),
    result({ structured_output: { outcome: 'returned', return: 'story_file: s.md\ntasks_count: 3', harness_friction: ['the wrapper refused a path', 'two\nlines'] } }),
  ]);
  assert.equal(written.keys.kind, 'returned');
  assert.equal(written.keys.outcome, 'returned');
  assert.equal(written.keys.findings, '');
  assert.equal(written.returnText, 'story_file: s.md\ntasks_count: 3');
  assert.equal(written.frictionText, 'the wrapper refused a path\ntwo lines\n');

  const asked = await reap(f, 'plan_writer', 'task-plan-writer', [
    init(WRITER_TOOLS),
    result({ structured_output: { outcome: 'questions', return: '## Questions\n1. Which?' } }),
  ]);
  assert.equal(asked.keys.kind, 'returned');
  assert.equal(asked.keys.outcome, 'questions');
  assert.equal(asked.returnText, '## Questions\n1. Which?');
});
