/**
 * The wording of the `init --upgrade` report: `cli/src/upgrade/report.ts` → `upgradeReport`.
 *
 * **The rule this suite enforces: the report says what the run did or would do, in the matching tense,
 * and prints an instruction only when the run's own results call for it.** The function is pure, so
 * every case passes plain values and no repository is built. The end-to-end printing belongs to the
 * `init --upgrade` command's suite.
 */

import assert from 'node:assert/strict';
import { join } from 'node:path';
import { test } from 'node:test';

import { upgradeReport } from '../dist/upgrade/report.js';

const REPO = '/work/repo';
const BACKUP_DIR = '/work/repo/.git/devscene/upgrade-backups/stamp';
const LOCAL_FILE = '.claude/settings.autonomous.local.json';
const PROFILE_FILE = '.claude/settings.autonomous.json';

const loadedPaths = (...relativePaths) => new Set(relativePaths.map((relativePath) => join(REPO, relativePath)));
const DAEMON_LOADED = loadedPaths(
  'scripts/autonomous-watcher.sh',
  'scripts/lib/harness-run-lib.sh',
  'scripts/lib/unit-commit-lib.sh',
);

const report = (overrides = {}) =>
  upgradeReport({
    dryRun: false,
    daemonLoadedPaths: DAEMON_LOADED,
    scriptsDir: 'scripts',
    applied: [],
    delta: [],
    settingChanges: [],
    startedMcpServers: [],
    browserMcpServers: ['playwright'],
    previousUnreadable: false,
    localAdditionCount: 0,
    backupDir: BACKUP_DIR,
    localFileIgnored: undefined,
    cliCommand: 'npx devscene@1.2.3',
    pluginMismatchWarning: undefined,
    ...overrides,
  });

const write = (relativePath, effect, extra = {}) => ({
  label: relativePath,
  path: join(REPO, relativePath),
  policy: 'replace-if-changed',
  outcome: effect,
  effect,
  ...extra,
});

const replaced = (relativePath) =>
  write(relativePath, 'backed-up-and-replaced', { backupPath: join(BACKUP_DIR, relativePath) });

const allLines = ({ notes, warnings, result }) => [...notes, ...warnings, result];
const restartLines = (lines) => lines.filter((line) => line.includes('restart-watcher.sh'));

const DELTA = [
  { list: 'permissions.allow', added: ['Bash(a, b)', 'Bash(c)'], removed: ['Bash(old)'] },
  { list: 'sandbox.network.allowedDomains', added: [], removed: ['old.example'] },
];

test('a run that changed nothing says the repository is current and adds nothing else', () => {
  const applied = [
    { ...write('scripts', 'ensured'), policy: 'ensure-dir' },
    write('scripts/autonomous-watcher.sh', 'kept'),
    write(PROFILE_FILE, 'kept'),
  ];
  assert.deepEqual(report({ applied }), { notes: [], warnings: [], result: 'Already current: no file changed.' });
  assert.deepEqual(report({ applied, dryRun: true }), {
    notes: [],
    warnings: [],
    result: 'Dry run: already current, no file would change.',
  });
});

test('the result counts created and replaced files, and never a kept file or a directory', () => {
  const applied = [
    { ...write('scripts', 'ensured'), policy: 'ensure-dir' },
    write('scripts/new.sh', 'created'),
    replaced(PROFILE_FILE),
    write('scripts/kept.sh', 'kept'),
  ];
  assert.equal(report({ applied }).result, 'Upgrade complete: 2 files changed.');
  assert.equal(report({ applied, dryRun: true }).result, 'Dry run: 2 files would change.');
  assert.equal(report({ applied: [replaced(PROFILE_FILE)] }).result, 'Upgrade complete: 1 file changed.');
});

test('every added and removed entry is named under its list, in the tense of the run', () => {
  assert.deepEqual(report({ delta: DELTA }).notes, [
    'Profile permissions.allow: added Bash(a, b)',
    'Profile permissions.allow: added Bash(c)',
    'Profile permissions.allow: removed Bash(old)',
    'Profile sandbox.network.allowedDomains: removed old.example',
  ]);
  assert.deepEqual(report({ delta: DELTA, dryRun: true }).notes, [
    'Profile permissions.allow: would add Bash(a, b)',
    'Profile permissions.allow: would add Bash(c)',
    'Profile permissions.allow: would remove Bash(old)',
    'Profile sandbox.network.allowedDomains: would remove old.example',
  ]);
});

test('every entry is named however many a list changes', () => {
  const added = Array.from({ length: 9 }, (_, index) => `Bash(entry-${index})`);
  const { notes } = report({ delta: [{ list: 'permissions.allow', added, removed: [] }] });
  assert.equal(notes.length, added.length);
  for (const entry of added) assert.ok(notes.some((line) => line.endsWith(entry)), entry);
});

test('removed entries get one warning, naming the local file and only the lists it accepts', () => {
  const real = report({ delta: DELTA }).warnings;
  assert.equal(real.length, 1);
  assert.match(real[0], /^The generator does not produce 2 profile entries, so they were removed and were not moved automatically: Bash\(old\), old\.example\./);
  assert.ok(real[0].includes(LOCAL_FILE));
  assert.ok(real[0].endsWith('followed by another npx devscene init --upgrade.'));
  for (const list of ['permissions.allow', 'permissions.ask', 'permissions.deny', 'sandbox.filesystem.denyWrite']) {
    assert.ok(real[0].includes(list), list);
  }
  assert.ok(!real[0].includes('sandbox.network.allowedDomains'));

  const dry = report({ delta: DELTA, dryRun: true }).warnings;
  assert.equal(dry.length, 1);
  assert.match(dry[0], /so they would be removed and would not be moved automatically: /);
});

const LOCAL_LISTS = 'permissions.allow, permissions.ask, permissions.deny, sandbox.filesystem.denyWrite';
const UNSTARTED_TOOL = 'mcp__gone__click';
const STARTED_TOOL = 'mcp__playwright__click';
const allowRemoved = (...removed) => ({ list: 'permissions.allow', added: [], removed });
const removedWarning = (delta, overrides = {}) => {
  const { warnings } = report({ delta, startedMcpServers: ['playwright'], ...overrides });
  assert.equal(warnings.length, 1);
  return warnings[0];
};

test('with no refused entry the removed-entries warning keeps its exact wording, in either mode', () => {
  const delta = [allowRemoved('Bash(old)'), { list: 'sandbox.network.allowedDomains', added: [], removed: ['old.example'] }];
  assert.equal(
    removedWarning(delta),
    `The generator does not produce 2 profile entries, so they were removed and were not moved automatically: Bash(old), old.example. Anything still wanted in ${LOCAL_LISTS} belongs in ${LOCAL_FILE}, followed by another npx devscene init --upgrade.`,
  );
  assert.equal(
    removedWarning(delta, { dryRun: true }),
    `The generator does not produce 2 profile entries, so they would be removed and would not be moved automatically: Bash(old), old.example. Anything still wanted in ${LOCAL_LISTS} belongs in ${LOCAL_FILE}, followed by another npx devscene init --upgrade.`,
  );
});

test('an entry for a server the profile starts keeps the advice to use the local file', () => {
  assert.equal(
    removedWarning([allowRemoved(STARTED_TOOL)]),
    `The generator does not produce 1 profile entry, so they were removed and were not moved automatically: ${STARTED_TOOL}. Anything still wanted in ${LOCAL_LISTS} belongs in ${LOCAL_FILE}, followed by another npx devscene init --upgrade.`,
  );
});

test('an entry the local file would refuse is told it cannot move there, and gets no advice to', () => {
  assert.equal(
    removedWarning([allowRemoved(UNSTARTED_TOOL)]),
    `1 permissions.allow entry was removed and cannot be moved to ${LOCAL_FILE}, because this profile does not start its MCP server: ${UNSTARTED_TOOL}.`,
  );
  assert.equal(
    removedWarning([allowRemoved(UNSTARTED_TOOL, 'mcp__other__read')], { dryRun: true }),
    `2 permissions.allow entries would be removed and cannot be moved to ${LOCAL_FILE}, because this profile does not start their MCP servers: ${UNSTARTED_TOOL}, mcp__other__read.`,
  );
});

test('refused and movable entries are named apart, and the advice covers only the movable ones', () => {
  assert.equal(
    removedWarning([allowRemoved('Bash(old)', UNSTARTED_TOOL, STARTED_TOOL)]),
    `The generator does not produce 2 profile entries, so they were removed and were not moved automatically: Bash(old), ${STARTED_TOOL}. Any of these still wanted in ${LOCAL_LISTS} belongs in ${LOCAL_FILE}, followed by another npx devscene init --upgrade. ` +
      `1 permissions.allow entry was removed and cannot be moved to ${LOCAL_FILE}, because this profile does not start its MCP server: ${UNSTARTED_TOOL}.`,
  );
});

test('only permissions.allow is refused for an unstarted server', () => {
  const warning = removedWarning([{ list: 'permissions.ask', added: [], removed: [UNSTARTED_TOOL] }]);
  assert.ok(warning.startsWith('The generator does not produce 1 profile entry'), warning);
  assert.ok(!warning.includes('cannot be moved'), warning);
});

test('every refused entry is named, however many there are', () => {
  const entries = Array.from({ length: 9 }, (_, index) => `mcp__gone__tool_${index}`);
  const warning = removedWarning([allowRemoved(...entries)]);
  for (const entry of entries) assert.ok(warning.includes(entry), entry);
  assert.ok(!warning.includes('more'), warning);
});

const BROWSER_TOOL = 'mcp__playwright__browser_click';
const BROWSER_SERVER = 'mcp__playwright';
const noToolReason = (subject) => `because ${subject} an MCP server and no tool`;
const BROWSER_REASON = "because a deny naming a browser tool would revoke the interactive-test agent's own grant";
const denyRemoved = (...removed) => ({ list: 'permissions.deny', added: [], removed });

test('an allow entry naming a server and no tool is told it cannot move, singular and plural, in either mode', () => {
  assert.equal(
    removedWarning([allowRemoved('mcp__foo')]),
    `1 permissions.allow entry was removed and cannot be moved to ${LOCAL_FILE}, ${noToolReason('it names')}: mcp__foo.`,
  );
  assert.equal(
    removedWarning([allowRemoved('mcp__foo')], { dryRun: true }),
    `1 permissions.allow entry would be removed and cannot be moved to ${LOCAL_FILE}, ${noToolReason('it names')}: mcp__foo.`,
  );
  assert.equal(
    removedWarning([allowRemoved('mcp__foo', 'mcp__bar')]),
    `2 permissions.allow entries were removed and cannot be moved to ${LOCAL_FILE}, ${noToolReason('they name')}: mcp__foo, mcp__bar.`,
  );
  assert.equal(
    removedWarning([allowRemoved('mcp__foo', 'mcp__bar')], { dryRun: true }),
    `2 permissions.allow entries would be removed and cannot be moved to ${LOCAL_FILE}, ${noToolReason('they name')}: mcp__foo, mcp__bar.`,
  );
});

test('a deny entry naming a browser tool is told it cannot move, singular and plural, in either mode', () => {
  assert.equal(
    removedWarning([denyRemoved(BROWSER_TOOL)]),
    `1 permissions.deny entry was removed and cannot be moved to ${LOCAL_FILE}, ${BROWSER_REASON}: ${BROWSER_TOOL}.`,
  );
  assert.equal(
    removedWarning([denyRemoved(BROWSER_TOOL)], { dryRun: true }),
    `1 permissions.deny entry would be removed and cannot be moved to ${LOCAL_FILE}, ${BROWSER_REASON}: ${BROWSER_TOOL}.`,
  );
  assert.equal(
    removedWarning([denyRemoved(BROWSER_TOOL, BROWSER_SERVER)]),
    `2 permissions.deny entries were removed and cannot be moved to ${LOCAL_FILE}, ${BROWSER_REASON}: ${BROWSER_TOOL}, ${BROWSER_SERVER}.`,
  );
  assert.equal(
    removedWarning([denyRemoved(BROWSER_TOOL, BROWSER_SERVER)], { dryRun: true }),
    `2 permissions.deny entries would be removed and cannot be moved to ${LOCAL_FILE}, ${BROWSER_REASON}: ${BROWSER_TOOL}, ${BROWSER_SERVER}.`,
  );
});

test('all three refused groups and a movable entry are each named once, under their own sentence', () => {
  assert.equal(
    removedWarning([allowRemoved('Bash(old)', UNSTARTED_TOOL, 'mcp__foo'), denyRemoved(BROWSER_TOOL)]),
    `The generator does not produce 1 profile entry, so they were removed and were not moved automatically: Bash(old). Any of these still wanted in ${LOCAL_LISTS} belongs in ${LOCAL_FILE}, followed by another npx devscene init --upgrade. ` +
      `1 permissions.allow entry was removed and cannot be moved to ${LOCAL_FILE}, because this profile does not start its MCP server: ${UNSTARTED_TOOL}. ` +
      `1 permissions.allow entry was removed and cannot be moved to ${LOCAL_FILE}, ${noToolReason('it names')}: mcp__foo. ` +
      `1 permissions.deny entry was removed and cannot be moved to ${LOCAL_FILE}, ${BROWSER_REASON}: ${BROWSER_TOOL}.`,
  );
});

test('a bare allow entry is refused even when the profile starts that server', () => {
  assert.equal(
    removedWarning([allowRemoved(BROWSER_SERVER)]),
    `1 permissions.allow entry was removed and cannot be moved to ${LOCAL_FILE}, ${noToolReason('it names')}: ${BROWSER_SERVER}.`,
  );
});

test('a deny of a non-browser server stays movable', () => {
  assert.equal(
    removedWarning([denyRemoved('mcp__other__read')]),
    `The generator does not produce 1 profile entry, so they were removed and were not moved automatically: mcp__other__read. Anything still wanted in ${LOCAL_LISTS} belongs in ${LOCAL_FILE}, followed by another npx devscene init --upgrade.`,
  );
});

test('the browser servers are the ones the report is given', () => {
  const warning = removedWarning([denyRemoved(BROWSER_TOOL)], { browserMcpServers: ['other-browser'] });
  assert.ok(warning.startsWith('The generator does not produce 1 profile entry'), warning);
  assert.ok(!warning.includes('cannot be moved'), warning);
});

test('a browser-named entry in permissions.ask stays movable', () => {
  const warning = removedWarning([{ list: 'permissions.ask', added: [], removed: [BROWSER_TOOL] }]);
  assert.ok(warning.startsWith('The generator does not produce 1 profile entry'), warning);
  assert.ok(warning.includes('Anything still wanted'), warning);
  assert.ok(!warning.includes('cannot be moved'), warning);
});

test('entries that were only added raise no warning', () => {
  const delta = [{ list: 'permissions.allow', added: ['Bash(a)'], removed: [] }];
  assert.deepEqual(report({ delta }).warnings, []);
});

test('a real run warns about each setting it reset, and where the old file went', () => {
  const [one, ...others] = report({ settingChanges: ['hooks'] }).warnings;
  assert.deepEqual(others, []);
  assert.equal(
    one,
    `1 profile setting outside the entry lists was reset to what this CLI renders: hooks. ${LOCAL_FILE} cannot hold them; the replaced file is under ${BACKUP_DIR}.`,
  );
  assert.match(report({ settingChanges: ['hooks', 'env'] }).warnings[0], /^2 profile settings outside the entry lists were reset to what this CLI renders: hooks, env\. /);
});

test('a dry run warns about each setting it would reset, and names no backup directory', () => {
  const [one, ...others] = report({ settingChanges: ['permissions.defaultMode'], dryRun: true }).warnings;
  assert.deepEqual(others, []);
  assert.equal(
    one,
    `1 profile setting outside the entry lists would be reset to what this CLI renders: permissions.defaultMode. ${LOCAL_FILE} cannot hold them; the replaced file would be backed up first.`,
  );
});

test('local additions are counted in the tense of the run, and absent when there are none', () => {
  assert.deepEqual(report({ localAdditionCount: 2 }).notes, [`Profile includes 2 local additions from ${LOCAL_FILE}.`]);
  assert.deepEqual(report({ localAdditionCount: 1, dryRun: true }).notes, [
    `Profile would include 1 local addition from ${LOCAL_FILE}.`,
  ]);
  assert.deepEqual(report({ localAdditionCount: 0 }).notes, []);
});

test('a real run names the backup directory when a backup was taken', () => {
  const { notes } = report({ applied: [replaced(PROFILE_FILE)] });
  assert.deepEqual(notes, [`Backed up 1 replaced file under ${BACKUP_DIR}.`]);
});

test('a dry run says a backup would be taken and names no directory, because none exists', () => {
  const { notes } = report({ applied: [replaced(PROFILE_FILE), replaced('scripts/a.sh')], dryRun: true });
  assert.deepEqual(notes, ['Would back up 2 replaced files first.']);
});

test('no backup line when nothing was backed up: created files and a permission-bits repair', () => {
  const applied = [write('scripts/new.sh', 'created'), write('scripts/mode.sh', 'backed-up-and-replaced')];
  for (const dryRun of [false, true]) {
    const lines = allLines(report({ applied, dryRun }));
    assert.ok(!lines.some((line) => /back(ed)? up/i.test(line)), lines.join('\n'));
    assert.ok(!lines.some((line) => line.includes(BACKUP_DIR)), lines.join('\n'));
  }
});

for (const [name, entry] of [
  ['a replaced watcher', replaced('scripts/autonomous-watcher.sh')],
  ['a created watcher', write('scripts/autonomous-watcher.sh', 'created')],
  ['a replaced lib row', replaced('scripts/lib/harness-run-lib.sh')],
  ['a created lib row', write('scripts/lib/unit-commit-lib.sh', 'created')],
]) {
  test(`${name} prints the restart instruction, in the tense of the run`, () => {
    const real = report({ applied: [entry] });
    assert.deepEqual(restartLines(real.warnings), [
      'A running daemon keeps the code it already loaded: restart it with DEVSCENE_CLI="npx devscene@1.2.3" bash scripts/restart-watcher.sh',
    ]);
    assert.deepEqual(restartLines(real.notes), []);

    const dry = report({ applied: [entry], dryRun: true });
    assert.deepEqual(restartLines(dry.notes), [
      'Would change the watcher or its libraries: restart the daemon afterwards with DEVSCENE_CLI="npx devscene@1.2.3" bash scripts/restart-watcher.sh',
    ]);
    assert.deepEqual(restartLines(dry.warnings), []);
  });
}

test('the restart line follows scriptsDir, including the repository root', () => {
  const rootLoaded = loadedPaths('autonomous-watcher.sh', 'lib/harness-run-lib.sh');
  const atRoot = report({
    scriptsDir: '.',
    daemonLoadedPaths: rootLoaded,
    applied: [replaced('autonomous-watcher.sh')],
  });
  assert.ok(atRoot.warnings.some((line) => line.endsWith(' bash restart-watcher.sh')), atRoot.warnings.join('\n'));
  const libAtRoot = report({
    scriptsDir: '.',
    daemonLoadedPaths: rootLoaded,
    applied: [replaced('lib/harness-run-lib.sh')],
  });
  assert.equal(restartLines(libAtRoot.warnings).length, 1);
  const nested = report({
    scriptsDir: 'tools/ci',
    daemonLoadedPaths: loadedPaths('tools/ci/autonomous-watcher.sh'),
    applied: [replaced('tools/ci/autonomous-watcher.sh')],
  });
  assert.ok(nested.warnings.some((line) => line.endsWith(' bash tools/ci/restart-watcher.sh')), nested.warnings.join('\n'));
});

test('no restart line when the watcher and lib rows are untouched', () => {
  const cases = {
    'only the profile changed': [replaced(PROFILE_FILE)],
    'another script changed': [replaced('scripts/commit-on-branch.sh')],
    'a non-lib subdirectory changed': [replaced('scripts/flows/task_plan_writing.graph.json')],
    'the watcher was kept': [write('scripts/autonomous-watcher.sh', 'kept')],
    'the lib row was kept': [write('scripts/lib/harness-run-lib.sh', 'kept')],
    'the watcher only had its permission bits corrected': [write('scripts/autonomous-watcher.sh', 'backed-up-and-replaced')],
  };
  for (const [name, applied] of Object.entries(cases)) {
    for (const dryRun of [false, true]) {
      assert.deepEqual(restartLines(allLines(report({ applied, dryRun }))), [], name);
    }
  }
});

test('a local file git does not ignore is named, in either mode, and only then', () => {
  for (const dryRun of [false, true]) {
    assert.deepEqual(report({ localFileIgnored: false, dryRun }).warnings, [
      `${LOCAL_FILE} is not ignored by git: a plain npx devscene init merges the ignore rule.`,
    ]);
    assert.deepEqual(report({ localFileIgnored: true, dryRun }).warnings, []);
    assert.deepEqual(report({ localFileIgnored: undefined, dryRun }).warnings, []);
  }
});

test('a supplied plugin mismatch warning appears unchanged and once, in either mode', () => {
  const pluginMismatchWarning = 'the supplied mismatch sentence';
  for (const dryRun of [false, true]) {
    assert.deepEqual(report({ pluginMismatchWarning, dryRun }).warnings, [pluginMismatchWarning]);
  }
});

test('no version line when no plugin mismatch warning is supplied, in either mode', () => {
  for (const dryRun of [false, true]) {
    assert.deepEqual(report({ pluginMismatchWarning: undefined, dryRun }).warnings, []);
  }
});

test('an unreadable previous profile is reported as not compared, in either mode', () => {
  for (const dryRun of [false, true]) {
    const { warnings } = report({ previousUnreadable: true, dryRun });
    assert.equal(warnings.length, 1);
    assert.ok(warnings[0].includes(PROFILE_FILE));
    assert.match(warnings[0], /could not be compared/);
  }
});

test('all of the wording is plain ASCII', () => {
  const everything = {
    applied: [replaced('scripts/autonomous-watcher.sh'), replaced(PROFILE_FILE)],
    delta: DELTA,
    settingChanges: ['hooks'],
    previousUnreadable: true,
    localAdditionCount: 3,
    localFileIgnored: false,
    pluginMismatchWarning: 'The installed plugin is version 9.9.9 and this CLI is version 1.2.3.',
  };
  for (const dryRun of [false, true]) {
    for (const line of allLines(report({ ...everything, dryRun }))) {
      assert.match(line, /^[\x20-\x7e]+$/, line);
    }
  }
});

test('the same input yields the same report and is left unmodified', () => {
  const input = Object.freeze({ applied: Object.freeze([replaced(PROFILE_FILE)]), delta: Object.freeze([...DELTA]) });
  assert.deepEqual(report(input), report(input));
});
