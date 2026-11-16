/**
 * One planning node session, `cli/templates/scripts/lib/planning-node-lib.sh`: the core's dispatch
 * blocks, each dispatch node's return schema, the node's prompt, the per-node flags, the launch and
 * the validated read.
 *
 * **The rule this suite enforces: a node's result is a declared outcome, `error` or
 * `undelivered`, never a guess.** `pnl_reap` decides in one fixed order — 1 no `init` event, 2 an
 * `init` tool the agent does not declare, 3 no `result` (or an API overload), 4 a failed session,
 * 5 a `result` text whose return block is missing, is not one JSON object or fails the agent's
 * `## Return schema`, 6 an outcome the graph does not declare, 7 `FAIL` (or `PASS` at a round gate)
 * without a non-blank `findings_file` — and one case pins each rule, beside the declared outcomes
 * that pass. Each `error` case also pins its `class=`: `infra` for rules 1, 4 and 5, `agent` for
 * the rest. `withheld=` reports the declared tools the `init` event lacks and refuses nothing.
 * `pnl_init` refuses a dispatch node's agent file with no usable `## Return schema`.
 *
 * Each case copies `lib/harness-run-lib.sh`, the library and the shipped planning graph from
 * `cli/templates/scripts/` into its own fixture under the system temp directory, beside a plugin
 * directory holding this checkout's planning core and fixture agent files, and sources them in one
 * `bash` process. `PD_SESSION_EXEC` names a stub function that runs
 * `$DEVSCENE_AGENT_CLI -p "$1" "${@:2}"`; the agent CLI is a stub that records its argv and prints
 * canned `stream-json` lines. The agent files — their `tools:` lines and their `## Return schema`
 * blocks — are written here rather than copied, so an assertion holds the library's comparison and
 * not the corpus's current allowlists and schemas.
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
const FENCE = '```';

const str = (extra = {}) => ({ type: 'string', minLength: 1, description: 'd', ...extra });
const outcome = (value) => ({ const: value, description: 'd' });
const variant = (value, properties, required) => ({
  type: 'object',
  description: 'd',
  properties: { outcome: outcome(value), ...properties },
  required: ['outcome', ...required],
  additionalProperties: false,
});
const schema = (variants) => ({
  $schema: 'http://json-schema.org/draft-07/schema#',
  title: 't',
  description: 'd',
  type: 'object',
  oneOf: variants,
});
const BLOCKER = variant('blocker', { blocker: str() }, ['blocker']);
const REVIEWER_SCHEMA = schema([
  variant('PASS', { findings_file: str() }, []),
  variant('FAIL', { findings_file: str(), must_fix_count: { type: 'integer', minimum: 1, description: 'd' } }, ['findings_file']),
  BLOCKER,
]);
const QUESTIONS = variant('questions', { questions: { type: 'array', minItems: 1, items: { type: 'string', minLength: 1 }, description: 'd' } }, ['questions']);
const WRITER_SCHEMA = schema([
  variant(
    'returned',
    { story_file: str(), tasks_count: { type: 'integer', minimum: 0, description: 'd' }, partial: { type: 'boolean', description: 'd' } },
    ['story_file', 'tasks_count'],
  ),
  QUESTIONS,
  BLOCKER,
]);
const UI_WRITER_SCHEMA = schema([
  variant('returned', { ui_test_index: str() }, ['ui_test_index']),
  variant('no_ui', { reason: str() }, ['reason']),
  QUESTIONS,
  BLOCKER,
]);

const AGENTS = {
  'task-plan-writer': { tools: 'Read, Write, mcp__docs__search_docs', schema: WRITER_SCHEMA },
  'business-parity-reviewer': { tools: 'Read, Grep', schema: REVIEWER_SCHEMA },
  'architecture-reviewer': { tools: 'Read, Grep', schema: REVIEWER_SCHEMA },
  'task-plan-reviewer': { tools: 'Read, Grep, Bash, mcp__docs__search_docs', schema: REVIEWER_SCHEMA },
  'ui-tests-plan-writer': { tools: 'Read, Write', schema: UI_WRITER_SCHEMA },
  'ui-tests-plan-reviewer': { tools: 'Read, Grep, mcp__docs__search_docs', schema: REVIEWER_SCHEMA },
  plain: { tools: 'Read, Bash', schema: REVIEWER_SCHEMA },
};
const WRITER_TOOLS = ['Read', 'Write'];
const REVIEWER_TOOLS = ['Read', 'Grep', 'Bash'];
const UI_REVIEWER_TOOLS = ['Read', 'Grep'];
const UI_WRITER_TOOLS = ['Read', 'Write'];

/** An agent file: frontmatter, an `## Output contract`, then `section` (a `## Return schema` by default). */
const agentFile = (name, tools, section) =>
  `---\nname: ${name}\ndescription: fixture\ntools: ${tools}\nmodel: inherit\n---\n\nBody.\n\n## Output contract\n\n${FENCE}\n# not a heading\n${FENCE}\n\n${section}\n## Next\n\n${FENCE}json\n{"not":"this"}\n${FENCE}\n`;
const schemaSection = (value) => `## Return schema\n\n${FENCE}json\n${JSON.stringify(value, null, 2)}\n${FENCE}\n`;

const PRELUDE = [
  '. "$W/s/lib/harness-run-lib.sh" || exit 99',
  '. "$W/s/lib/planning-node-lib.sh" || exit 98',
  'session() { "$DEVSCENE_AGENT_CLI" -p "$1" "${@:2}"; }',
  'PD_SESSION_EXEC=session',
  'PD_FORMATTER=cat',
].join('\n');

/**
 * A fresh fixture: a worktree carrying the shipped libraries and graph, a plugin directory, and a
 * stub agent CLI. `core` transforms the copied planning core's text; `sections` replaces an agent's
 * `## Return schema` section text by agent name.
 */
async function fixture(t, { core = (text) => text, sections = {} } = {}) {
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
  for (const [agent, { tools, schema: s }] of Object.entries(AGENTS)) {
    const section = agent in sections ? sections[agent] : schemaSection(s);
    await writeFile(join(plugin, 'agents', `${agent}.md`), agentFile(agent, tools, section));
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
/** A reply text: `prose`, then `object` in a ```` ```json ```` block, then `after`. */
const reply = (object, { prose = 'Done.\n\n', after = '\n' } = {}) =>
  `${prose}${FENCE}json\n${typeof object === 'string' ? object : JSON.stringify(object, null, 2)}\n${FENCE}${after}`;
/** A successful `result` event whose text ends with `object`'s return block. */
const returns = (object, opts) => result({ result: reply(object, opts) });

/**
 * Launch one session of <node> as <agent> whose stub prints <events>, reap it, and return the
 * reaped keys, the return and object texts, the stub's argv and the run's stream copy.
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
of=$(printf '%s\\n' "$out" | sed -n 's/^object_file=//p')
printf '%s\\n' '--- return'
[ -z "$rf" ] || cat "$rf"
printf '\\n%s\\n' '--- object'
[ -z "$of" ] || cat "$of"
pnl_cleanup
[ ! -e "$rf" ] && [ ! -e "$of" ] || exit 94
`);
  assert.equal(r.status, 0, `exit ${r.status}\n${r.stderr}\n${r.stdout}`);
  const [head, rest] = r.stdout.split('--- return\n');
  const [returnText, objectText] = rest.split('\n--- object\n');
  const keys = Object.fromEntries(
    head.trimEnd().split('\n').map((line) => [line.slice(0, line.indexOf('=')), line.slice(line.indexOf('=') + 1)]),
  );
  const argv = (await readFile(f.env.STUB_ARGV, 'utf8')).split('\n');
  const runStream = await readFile(join(f.root, 'run.stream.jsonl'), 'utf8');
  const nodeStream = await readFile(join(f.root, 'run.planning', `1-${node}.stream.jsonl`), 'utf8');
  const manifest = await readFile(join(f.root, 'run.planning', 'node-sessions.jsonl'), 'utf8').catch(() => null);
  return { keys, returnText, objectText, argv, runStream, nodeStream, manifest };
}

/** Assert `r` is `error` / `infra` with `reason` and no return read; `label` names the case. */
function infraError(r, reason, label = reason) {
  assert.equal(r.keys.kind, 'error', label);
  assert.equal(r.keys.class, 'infra', label);
  assert.equal(r.keys.reason, reason, label);
  assert.equal(r.keys.outcome, '');
  assert.equal(r.keys.return_file, '');
  assert.equal(r.keys.object_file, '');
}

test('pnl_init reads the plugin name, the dispatch cap, every block and every dispatch node\'s schema', { skip: SKIP }, async (t) => {
  const f = await fixture(t, { core: (text) => text.replace(/MAX_TOTAL_DISPATCHES = \d+/, 'MAX_TOTAL_DISPATCHES = 7') });
  const r = await f.bash(`
pnl_init "$P" "$W" || exit 97
printf '%s|%s|%s\\n' "$PNL_PLUGIN_NAME" "$PNL_MAX_DISPATCHES" "$PNL_STATE_DIR"
(cd "$PNL_TMP" && ls)
cat "$PNL_TMP/schema-plan_review.json"
[ -d "$PNL_TMP" ] || exit 93
d=$PNL_TMP; pnl_cleanup; [ ! -e "$d" ] || exit 92
`);
  assert.equal(r.status, 0, r.stderr);
  const [head, ...rest] = r.stdout.trimEnd().split('\n');
  assert.equal(head, `${PLUGIN_NAME}|7|devscene`);
  const schemaLine = rest.pop();
  assert.deepEqual(rest.sort(), [
    'schema-architecture_review.json',
    'schema-business_parity_review.json',
    'schema-plan_review.json',
    'schema-plan_writer.json',
    'schema-ui_review.json',
    'schema-ui_writer.json',
  ]);
  assert.deepEqual(JSON.parse(schemaLine), REVIEWER_SCHEMA, 'the first json block of the section, compact');
  assert.ok(!schemaLine.includes('\n  '));
});

test('pnl_init refuses an agent file with no usable ## Return schema, naming it', { skip: SKIP }, async (t) => {
  const cases = [
    ['', /carries no '## Return schema' section/],
    [`## Return schema\n\nProse only.\n\n${FENCE}\n{}\n${FENCE}\n`, /'## Return schema' section of '.*' carries no ```json block/],
    [`## Return schema\n\n${FENCE}json\n{"oneOf":[]} {}\n${FENCE}\n`, /'## Return schema' block of '.*' is not one JSON object/],
    [`## Return schema\n\n${FENCE}json\n[1]\n${FENCE}\n`, /'## Return schema' block of '.*' is not one JSON object/],
    [`## Return schema\n\n${FENCE}json\n{"type":"object"}\n${FENCE}\n`, /'## Return schema' block of '.*' carries no top-level oneOf array/],
    [`${FENCE}\n## Return schema\n${FENCE}\n`, /carries no '## Return schema' section/],
  ];
  for (const [section, pattern] of cases) {
    const f = await fixture(t, { sections: { 'architecture-reviewer': section } });
    const r = await f.bash('pnl_init "$P" "$W"; rc=$?; printf "%s" "${PNL_TMP-}"; exit $rc');
    assert.equal(r.status, 2, section);
    assert.equal(r.stdout, '', 'no temporary directory is left set');
    assert.match(r.stderr, /^planning-driver: /);
    assert.match(r.stderr, pattern);
    assert.ok(r.stderr.includes(join(f.plugin, 'agents', 'architecture-reviewer.md')), r.stderr);
    assert.equal(r.stderr.trimEnd().split('\n').length, 1);
  }
});

test('pnl_init refuses a dispatch node that names no agent, naming the node', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const graphPath = join(f.wt, 's', 'flows', 'task_plan_writing.graph.json');
  const graph = JSON.parse(await readFile(graphPath, 'utf8'));
  delete graph.nodes.plan_writer.agent;
  await writeFile(graphPath, JSON.stringify(graph));
  const r = await f.bash('pnl_init "$P" "$W"; rc=$?; printf "%s" "${PNL_TMP-}"; exit $rc');
  assert.equal(r.status, 2, r.stderr);
  assert.equal(r.stdout, '', 'no temporary directory is left set');
  assert.match(r.stderr, /^planning-driver: .*names no agent for dispatch node 'plan_writer'/);
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

test('pnl_agent_flags carries no --json-schema and splits MCP: no mcp__ tool disallows them, some keep only their servers', { skip: SKIP }, async (t) => {
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
  assert.deepEqual(plain.trimEnd().split('\n'), [
    '--agent', `${PLUGIN_NAME}:plain`, '--plugin-dir', f.plugin, '--add-dir', f.plugin, '--disallowedTools', 'mcp__*',
  ]);
  const mcpLines = withMcp.trimEnd().split('\n');
  assert.deepEqual(mcpLines.slice(0, 8), [
    '--agent', `${PLUGIN_NAME}:task-plan-reviewer`, '--plugin-dir', f.plugin, '--add-dir', f.plugin, '--strict-mcp-config', '--mcp-config',
  ]);
  assert.equal(mcpLines.length, 9);
  assert.ok(!bare.stdout.includes('--json-schema'));
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
  const events = [init(REVIEWER_TOOLS), returns({ outcome: 'PASS', findings_file: 'devscene/r/review_0.md' })];
  const r = await reap(f, 'plan_review', 'task-plan-reviewer', events);
  assert.deepEqual(r.argv.slice(0, 4), ['-p', 'the prompt', '--agent', `${PLUGIN_NAME}:task-plan-reviewer`]);
  assert.ok(!r.argv.includes('--json-schema'), 'the launch argv carries no --json-schema');
  const lines = events.map((e) => JSON.stringify(e)).join('\n') + '\n';
  assert.equal(r.nodeStream, lines);
  assert.equal(r.runStream, lines);
  assert.equal(r.manifest, '{"session_id":"s1","seq":"1","node":"plan_review"}\n');
  assert.match(r.keys.duration_secs, /^\d+$/);
  assert.equal(r.keys.cost, '0.25');
  assert.equal(r.keys.denials, '0');
  assert.equal(r.keys.withheld, '');
  assert.equal(r.keys.kind, 'returned');
  assert.ok(!('friction_file' in r.keys));
});

test('rule 1: a stub that exits 0 with empty stdout is error, no init event', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const r = await reap(f, 'plan_review', 'task-plan-reviewer', []);
  infraError(r, 'the agent did not resolve: no init event');
  assert.equal(r.keys.withheld, '');
  assert.equal(r.manifest, null, 'a session with no init event has no session id to record');
});

test('rule 2: init tools the agent does not declare are error; declared tools the init lacks are withheld, not refused', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const ok = returns({ outcome: 'PASS', findings_file: 'f.md' });
  const lacking = await reap(f, 'plan_review', 'task-plan-reviewer', [init(['Read', 'Bash']), ok]);
  assert.equal(lacking.keys.kind, 'returned');
  assert.equal(lacking.keys.class, '');
  assert.equal(lacking.keys.withheld, 'Grep');

  const extra = await reap(f, 'plan_review', 'task-plan-reviewer', [init([...REVIEWER_TOOLS, 'Edit']), ok]);
  assert.equal(extra.keys.kind, 'error');
  assert.equal(extra.keys.class, 'agent');
  assert.equal(extra.keys.reason, 'the init event grants tools the agent does not declare: [Edit]');
  assert.equal(extra.keys.withheld, '');

  const mixed = await reap(f, 'plan_review', 'task-plan-reviewer', [init(['Read', 'Bash', 'Edit']), ok]);
  assert.equal(mixed.keys.kind, 'error', 'a lacking tool does not mask an extra one');
  assert.equal(mixed.keys.class, 'agent');
  assert.equal(mixed.keys.reason, 'the init event grants tools the agent does not declare: [Edit]');
  assert.equal(mixed.keys.withheld, 'Grep');

  const withMcp = await reap(f, 'plan_review', 'task-plan-reviewer', [init([...REVIEWER_TOOLS, 'mcp__docs__search_docs']), ok]);
  assert.equal(withMcp.keys.kind, 'returned', 'an agent MCP tool present in init matches');
  assert.equal(withMcp.keys.withheld, '');

  const noMcp = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), ok]);
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
  infraError(failed, 'the session ended as success with is_error');

  const turns = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ subtype: 'error_max_turns', result: reply({ outcome: 'PASS', findings_file: 'f.md' }) }),
  ]);
  infraError(turns, 'the session ended as error_max_turns');
});

test('rule 5: structured_output is never read; a result with no return block is error, infra', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const structured = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ result: 'verdict: PASS', structured_output: { outcome: 'PASS', findings_file: 'devscene/r/review_0.md' } }),
  ]);
  infraError(structured, 'the result carries no return block');

  const bareJson = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ result: JSON.stringify({ outcome: 'PASS', findings_file: 'f.md' }) }),
  ]);
  infraError(bareJson, 'the result carries no return block');

  const ok = { outcome: 'PASS', findings_file: 'f.md' };
  for (const [label, text] of [
    ['prose after the block', reply(ok, { after: '\n\nThat is all.\n' })],
    ['a second fence after the block', reply(ok, { after: `\n${FENCE}\n` })],
    ['an unclosed block', `Done.\n${FENCE}json\n${JSON.stringify(ok)}\n`],
    ['a plain fence, not json', `${FENCE}\n${JSON.stringify(ok)}\n${FENCE}\n`],
    ['an info string beyond json', `${FENCE}jsonc\n${JSON.stringify(ok)}\n${FENCE}\n`],
  ]) {
    const r = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), result({ result: text })]);
    infraError(r, 'the result carries no return block', label);
  }
});

test('rule 5: a return block that is not one JSON object is error, infra', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  for (const body of ['{"outcome": "PASS",', '["PASS"]', '"PASS"', '']) {
    const r = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), returns(body)]);
    infraError(r, 'the return block is not one JSON object');
  }
});

test('rule 5: a return that fails its schema is error, infra, naming the first failure', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const cases = [
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { findings_file: 'f.md' }, 'missing required key outcome'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'SHIP', findings_file: 'f.md' }, 'outcome "SHIP" matches no variant'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'error' }, 'outcome "error" matches no variant'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'FAIL', must_fix_count: 1 }, 'missing required key findings_file'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'PASS', findings_file: 'f.md', return: 'x' }, 'unknown key return'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'PASS', findings_file: 'f.md', harness_friction: [] }, 'unknown key harness_friction'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'PASS', findings_file: '' }, 'findings_file is shorter than 1'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'PASS', findings_file: 3 }, 'findings_file is not a string'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'FAIL', findings_file: 'f.md', must_fix_count: 0 }, 'must_fix_count is below 1'],
    ['plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'FAIL', findings_file: 'f.md', must_fix_count: 1.5 }, 'must_fix_count is not an integer'],
    ['plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'returned', story_file: 's.md', tasks_count: '3' }, 'tasks_count is not an integer'],
    ['plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'returned', story_file: 's.md', tasks_count: 3, partial: 'no' }, 'partial is not a boolean'],
    ['plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'questions', questions: [] }, 'questions has fewer than 1 items'],
    ['plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'questions', questions: 'Which?' }, 'questions is not an array'],
    ['plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'questions', questions: ['Which?', ''] }, 'questions item 1 is shorter than 1'],
    ['plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'questions', questions: [1] }, 'questions item 0 is not a string'],
  ];
  for (const [node, agent, tools, object, failure] of cases) {
    const r = await reap(f, node, agent, [init(tools), returns(object)]);
    infraError(r, `the return fails its schema: ${failure}`);
  }
});

test('rule 5: prose above the block, an earlier json block and whitespace after it are accepted', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const object = { outcome: 'FAIL', findings_file: 'devscene/r/review_1.md', must_fix_count: 2 };
  const prose = `Two Must Fix — see below.\n\n${FENCE}json\n{"outcome":"draft"}\n${FENCE}\n\nFinal:\n`;
  const r = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), returns(object, { prose, after: '\n \t\n\n' })]);
  assert.equal(r.keys.kind, 'returned');
  assert.equal(r.keys.outcome, 'FAIL');
  assert.deepEqual(JSON.parse(r.objectText), object);

  const crlf = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    result({ result: `Done.\r\n${FENCE}json\r\n${JSON.stringify(object)}\r\n${FENCE}\r\n` }),
  ]);
  assert.equal(crlf.keys.kind, 'returned');

  const noTrailing = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), returns(object, { prose: '', after: '' })]);
  assert.equal(noTrailing.keys.kind, 'returned', 'a block opening the text and ending it with no newline');
});

test('rule 6: an outcome the schema admits and the graph does not declare is error, agent', { skip: SKIP }, async (t) => {
  const widened = schema([...REVIEWER_SCHEMA.oneOf, variant('SHIP', { findings_file: str() }, [])]);
  const f = await fixture(t, { sections: { 'task-plan-reviewer': schemaSection(widened) } });
  const r = await reap(f, 'plan_review', 'task-plan-reviewer', [
    init(REVIEWER_TOOLS),
    returns({ outcome: 'SHIP', findings_file: 'devscene/r/review_0.md' }),
  ]);
  assert.equal(r.keys.kind, 'error');
  assert.equal(r.keys.class, 'agent');
  assert.equal(r.keys.outcome, '');
  assert.equal(r.keys.reason, 'undeclared outcome SHIP');
  assert.equal(r.keys.findings, '');
  assert.equal(r.keys.return_file, '');
  assert.equal(r.keys.object_file, '');
});

test('rule 7: FAIL anywhere, or PASS at a round gate, without a non-blank findings_file is error, agent', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const pass = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), returns({ outcome: 'PASS' })]);
  assert.equal(pass.keys.kind, 'error');
  assert.equal(pass.keys.class, 'agent');
  assert.equal(pass.keys.reason, 'PASS carries no findings_file');

  const blank = await reap(f, 'plan_review', 'task-plan-reviewer', [init(REVIEWER_TOOLS), returns({ outcome: 'FAIL', findings_file: ' ' })]);
  assert.equal(blank.keys.kind, 'error');
  assert.equal(blank.keys.class, 'agent');
  assert.equal(blank.keys.reason, 'FAIL carries no findings_file');

  const uiPass = await reap(f, 'ui_review', 'ui-tests-plan-reviewer', [init(UI_REVIEWER_TOOLS), returns({ outcome: 'PASS' })]);
  assert.equal(uiPass.keys.kind, 'returned', 'ui_review is no round gate');
  assert.equal(uiPass.keys.outcome, 'PASS');
});

test('declared outcomes are returned: PASS, FAIL, blocker, returned, questions and no_ui', { skip: SKIP }, async (t) => {
  const f = await fixture(t);
  const check = async (node, agent, tools, object, extra = {}) => {
    const text = reply(object, { prose: 'Summary — prose above.\n\n' });
    const r = await reap(f, node, agent, [init(tools), result({ result: text, ...extra })]);
    assert.equal(r.keys.kind, 'returned', JSON.stringify(object));
    assert.equal(r.keys.class, '');
    assert.equal(r.keys.outcome, object.outcome);
    assert.equal(r.keys.reason, '');
    assert.equal(r.returnText, text, 'return_file holds the whole result text');
    assert.equal(r.objectText, JSON.stringify(object) + '\n', 'object_file holds the validated object, compact');
    return r;
  };
  const pass = await check('plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'PASS', findings_file: 'devscene/r/review_0.md' }, { permission_denials: [{}, {}] });
  assert.equal(pass.keys.findings, 'devscene/r/review_0.md');
  assert.equal(pass.keys.denials, '2');

  const fail = await check('plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'FAIL', findings_file: 'devscene/r/review_1.md', must_fix_count: 2 });
  assert.equal(fail.keys.findings, 'devscene/r/review_1.md');

  const blocker = await check('plan_review', 'task-plan-reviewer', REVIEWER_TOOLS, { outcome: 'blocker', blocker: 'cannot read devscene/x.md' });
  assert.equal(blocker.keys.findings, '');

  const written = await check('plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'returned', story_file: 's.md', tasks_count: 3, partial: false });
  assert.equal(written.keys.findings, '');

  await check('plan_writer', 'task-plan-writer', WRITER_TOOLS, { outcome: 'questions', questions: ['Which?', 'Why?'] });
  await check('ui_writer', 'ui-tests-plan-writer', UI_WRITER_TOOLS, { outcome: 'no_ui', reason: 'the branch ships a CLI' });
});
