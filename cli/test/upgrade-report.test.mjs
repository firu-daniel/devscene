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
    previousUnreadable: false,
    localAdditionCount: 0,
    backupDir: BACKUP_DIR,
    localFileIgnored: undefined,
    cliVersion: '1.2.3',
    cliCommand: 'npx devscene@1.2.3',
    pluginVersion: undefined,
    pluginCliCommand: undefined,
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

test('entries that were only added raise no warning', () => {
  const delta = [{ list: 'permissions.allow', added: ['Bash(a)'], removed: [] }];
  assert.deepEqual(report({ delta }).warnings, []);
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

test('a differing plugin version names both versions, in either mode', () => {
  for (const dryRun of [false, true]) {
    assert.deepEqual(report({ pluginVersion: '1.2.0', pluginCliCommand: 'npx devscene@1.2.0', dryRun }).warnings, [
      "The installed plugin is version 1.2.0 and this CLI is version 1.2.3: run npx devscene@1.2.0 init --upgrade, from the CLI of the plugin's version.",
    ]);
  }
});

test('no version line when the versions match or the plugin version is unreadable', () => {
  assert.deepEqual(report({ pluginVersion: '1.2.3', pluginCliCommand: 'npx devscene@1.2.3' }).warnings, []);
  assert.deepEqual(report({ pluginVersion: undefined }).warnings, []);
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
    previousUnreadable: true,
    localAdditionCount: 3,
    localFileIgnored: false,
    pluginVersion: '9.9.9',
    pluginCliCommand: 'npx devscene@9.9.9',
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
