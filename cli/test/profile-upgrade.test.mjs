/**
 * The profile upgrade planner, its entry delta and the drift comparison.
 *
 * **The rule this suite exists to enforce: `init --upgrade` and `doctor` compare a profile against
 * one render, every list the render can produce is compared, and a profile never vouches for its own
 * entries when it is graded.**
 *
 * The functions run in this process against repositories wired by the **compiled** CLI, so each case
 * points `CLAUDE_CONFIG_DIR` at its own agent-runner home for the CLI and for this process alike: the
 * plugin roots are resolved from a file outside every repository.
 */

import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { test } from 'node:test';

import { requireConfig } from '../dist/config/io.js';
import { HarnessError } from '../dist/core/errors.js';
import { formatJson } from '../dist/core/json.js';
import { Reporter } from '../dist/core/report.js';
import { WritePlan } from '../dist/core/writer.js';
import { PLUGIN_KEY } from '../dist/generators/projectSettings.js';
import {
  PROFILE_ENTRY_LISTS,
  planProfileUpgrade,
  profileDrift,
  profileEntryDelta,
  renderCurrentProfile,
} from '../dist/generators/profileUpgrade.js';
import { createFixture, readJson, runCli, snapshotTree } from './helpers/fixture.mjs';

const LOCAL_FILE = '.claude/settings.autonomous.local.json';
const PROFILE_FILE = '.claude/settings.autonomous.json';
const CONFIG_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';

const ALLOW = 'permissions.allow';
const RETIRED = 'Bash(retired-command:*)';
const LOCAL_ENTRY = 'Bash(local-command:*)';
const STRAY_SCRIPT = 'Bash(bash /tmp/x/scripts/evil.sh:*)';
const STRAY_READ = 'Read(//tmp/x/**)';
const TOOLCHAIN_ENTRY = 'Bash(/opt/reference/reference-analyze:*)';

async function temporaryDir(t) {
  const fixture = await createFixture({ git: false });
  t.after(fixture.cleanup);
  return fixture.dir;
}

/** Point this process at `home` for the rest of the case. */
function useMachine(t, home) {
  const before = process.env[CONFIG_HOME_VARIABLE];
  process.env[CONFIG_HOME_VARIABLE] = home;
  t.after(() => {
    if (before === undefined) delete process.env[CONFIG_HOME_VARIABLE];
    else process.env[CONFIG_HOME_VARIABLE] = before;
  });
}

/** An agent-runner home resolving no plugin root. */
async function machineWithoutPlugin(t) {
  const home = await temporaryDir(t);
  useMachine(t, home);
  return { home };
}

/** An agent-runner home recording one plugin install root. */
async function machineWithPlugin(t) {
  const root = await temporaryDir(t);
  const home = await temporaryDir(t);
  mkdirSync(join(home, 'plugins'), { recursive: true });
  writeFileSync(
    join(home, 'plugins', 'installed_plugins.json'),
    formatJson({ version: 2, plugins: { [PLUGIN_KEY]: [{ scope: 'user', installPath: root }] } }),
  );
  useMachine(t, home);
  return { home, root };
}

/** A repository wired by `init` on `machine`. */
async function adopted(t, machine, args = []) {
  const fixture = await createFixture({
    files: {
      'package.json': {
        name: 'fixture-project',
        private: true,
        version: '0.0.0',
        scripts: { typecheck: 'echo typecheck', test: 'echo test', build: 'echo build', dev: 'echo dev' },
      },
      'README.md': '# fixture project\n',
    },
  });
  t.after(fixture.cleanup);
  const { dir } = fixture;
  const result = await runCli(dir, ['init', ...args], { [CONFIG_HOME_VARIABLE]: machine.home });
  assert.equal(result.status, 0, `init exited ${result.status}\n${result.stdout}\n${result.stderr}`);
  return { dir, config: requireConfig(dir) };
}

const profilePath = (dir) => join(dir, PROFILE_FILE);
const profileOf = (dir) => readJson(profilePath(dir));
const writeProfile = (dir, profile) => writeFileSync(profilePath(dir), formatJson(profile));

function writeLocal(dir, content) {
  writeFileSync(join(dir, LOCAL_FILE), formatJson(content));
}

/** The on-disk profile after `edit`. */
function editProfile(dir, edit) {
  const profile = profileOf(dir);
  edit(profile);
  writeProfile(dir, profile);
  return profile;
}

function planned({ dir, config }, options = {}) {
  const plan = new WritePlan();
  return { plan, result: planProfileUpgrade({ repoRoot: dir, config, plan, dryRun: false, ...options }) };
}

const drift = ({ dir, config }, onDisk = profileOf(dir)) => profileDrift({ repoRoot: dir, config, onDisk });
const entriesOf = (found, list) => found.filter((item) => item.list === list).map((item) => item.entry);
const deltaOf = (delta, list) => delta.find((row) => row.list === list);

test('PROFILE_ENTRY_LISTS has one row per list, and a credential row names its field', () => {
  assert.deepEqual(PROFILE_ENTRY_LISTS, [
    { path: 'permissions.allow' },
    { path: 'permissions.deny' },
    { path: 'permissions.ask' },
    { path: 'permissions.additionalDirectories' },
    { path: 'sandbox.excludedCommands' },
    { path: 'sandbox.filesystem.allowWrite' },
    { path: 'sandbox.filesystem.denyWrite' },
    { path: 'sandbox.network.allowedDomains' },
    { path: 'sandbox.credentials.files', field: 'path' },
    { path: 'sandbox.credentials.envVars', field: 'name' },
    { path: 'enabledMcpjsonServers' },
  ]);
});

test('an unchanged profile plans an empty delta and the same bytes, and nothing is written', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  const before = await snapshotTree(repo.dir);

  const first = planned(repo);
  const second = planned(repo);

  assert.deepEqual(first.result.delta, []);
  assert.equal(first.result.previousUnreadable, false);
  assert.equal(first.result.localAdditionCount, 0);
  assert.equal(first.result.path, profilePath(repo.dir));
  assert.equal(first.result.repoPath, PROFILE_FILE);
  assert.deepEqual(first.result.previous, profileOf(repo.dir));

  const [request, ...others] = first.plan.requests;
  assert.deepEqual(others, []);
  assert.equal(request.path, profilePath(repo.dir));
  assert.equal(request.policy, 'replace-if-changed');
  assert.equal(request.label, 'unattended permission profile');

  const bytes = formatJson(request.content);
  assert.equal(bytes, formatJson(second.plan.requests[0].content));
  assert.equal(bytes, readFileSync(profilePath(repo.dir), 'utf8'));
  assert.deepEqual(await snapshotTree(repo.dir), before, 'planning changed the tree');
});

test('a retired entry is removed and a missing script entry is added', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  let dropped;
  editProfile(repo.dir, (profile) => {
    const { allow } = profile.permissions;
    dropped = allow.find((entry) => entry.startsWith('Bash(bash ') && entry.includes('.sh'));
    allow.splice(allow.indexOf(dropped), 1);
    allow.push(RETIRED);
  });

  const { delta, rendered } = planned(repo).result;
  assert.deepEqual(delta, [{ list: ALLOW, added: [dropped], removed: [RETIRED] }]);
  assert.ok(rendered.permissions.allow.includes(dropped));
  assert.ok(!rendered.permissions.allow.includes(RETIRED));
});

test('a local entry is counted, lands once, and survives a second render', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  writeLocal(repo.dir, { permissions: { allow: [LOCAL_ENTRY] } });

  const first = planned(repo);
  assert.equal(first.result.localAdditionCount, 1);
  assert.deepEqual(first.result.delta, [{ list: ALLOW, added: [LOCAL_ENTRY], removed: [] }]);

  const context = {
    repoRoot: repo.dir,
    report: new Reporter({ quiet: true }),
    dryRun: false,
    force: false,
    backupDir: await temporaryDir(t),
  };
  assert.equal(first.plan.apply(context)[0].effect, 'backed-up-and-replaced');

  const second = planned(repo);
  assert.deepEqual(second.result.delta, []);
  assert.equal(second.result.rendered.permissions.allow.filter((entry) => entry === LOCAL_ENTRY).length, 1);
  assert.equal(second.plan.apply(context)[0].effect, 'kept');
});

test('carried plugin-root entries stay, and renderCurrentProfile can leave them out', async (t) => {
  const machine = await machineWithPlugin(t);
  const repo = await adopted(t, machine);
  const entries = [`Read(/${machine.root}/**)`, `Bash(bash ${machine.root}/scripts/helper.sh:*)`];
  editProfile(repo.dir, (profile) => profile.permissions.allow.push(...entries));

  const { delta, rendered, notes } = planned(repo).result;
  assert.deepEqual(delta, []);
  for (const entry of entries) assert.ok(rendered.permissions.allow.includes(entry), entry);
  assert.equal(notes.length, 1, 'the carry-forward was not reported');

  const { allow } = renderCurrentProfile({ repoRoot: repo.dir, config: repo.config, carryForward: false }).permissions;
  for (const entry of entries) assert.ok(!allow.includes(entry), entry);
});

for (const [name, content] of [
  ['text that does not parse', '{ not json'],
  ['JSON that is not an object', '[]\n'],
]) {
  test(`a profile holding ${name} is planned as a replacement`, async (t) => {
    const repo = await adopted(t, await machineWithoutPlugin(t));
    writeFileSync(profilePath(repo.dir), content);

    const { plan, result } = planned(repo);
    assert.equal(result.previousUnreadable, true);
    assert.equal(result.previous, undefined);
    assert.equal(plan.size, 1);
    assert.ok(deltaOf(result.delta, ALLOW).added.length > 0);
    assert.ok(result.delta.every((row) => row.removed.length === 0));
  });
}

test('an absent profile is planned as new and is not called unreadable', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  rmSync(profilePath(repo.dir));

  const { result } = planned(repo);
  assert.equal(result.previousUnreadable, false);
  assert.equal(result.previous, undefined);
  assert.ok(deltaOf(result.delta, ALLOW).added.length > 0);
});

test('profileDrift is clean after init, and reports both directions', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  assert.deepEqual(drift(repo), { missing: [], unaccounted: [] });

  let dropped;
  const onDisk = editProfile(repo.dir, (profile) => {
    dropped = profile.permissions.deny.pop();
    profile.permissions.allow.push(RETIRED);
  });
  assert.deepEqual(drift(repo, onDisk), {
    missing: [{ list: 'permissions.deny', entry: dropped }],
    unaccounted: [{ list: ALLOW, entry: RETIRED }],
  });
});

test('a local entry the profile has not picked up is missing, and accounted for once it has', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  writeLocal(repo.dir, { permissions: { allow: [LOCAL_ENTRY] } });
  assert.deepEqual(drift(repo), { missing: [{ list: ALLOW, entry: LOCAL_ENTRY }], unaccounted: [] });

  editProfile(repo.dir, (profile) => profile.permissions.allow.push(LOCAL_ENTRY));
  assert.deepEqual(drift(repo), { missing: [], unaccounted: [] });
});

test('a toolchain-shaped entry is accounted for only with the parity phase on', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  const onDisk = editProfile(repo.dir, (profile) => profile.permissions.allow.push(TOOLCHAIN_ENTRY));
  const parityOff = { ...repo.config, parity: { toolchainCommands: ['reference-analyze'] } };
  const parityOn = { ...parityOff, phases: { ...repo.config.phases, parity: true } };

  assert.deepEqual(drift({ ...repo, config: parityOff }, onDisk).unaccounted, [{ list: ALLOW, entry: TOOLCHAIN_ENTRY }]);
  assert.deepEqual(drift({ ...repo, config: parityOn }, onDisk).unaccounted, []);
});

test('a hand-added sandbox entry or credential is in the delta and is unaccounted', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  const onDisk = editProfile(repo.dir, ({ sandbox }) => {
    sandbox.filesystem.allowWrite.push('/opt/hand-added');
    sandbox.excludedCommands.push('bash /opt/hand-added.sh:*');
    sandbox.network.allowedDomains.push('hand-added.example');
    sandbox.credentials.files.push({ path: '~/.hand-added', mode: 'deny' });
    sandbox.credentials.envVars.push({ name: 'HAND_ADDED', mode: 'deny' });
  });
  const expected = [
    ['sandbox.excludedCommands', 'bash /opt/hand-added.sh:*'],
    ['sandbox.filesystem.allowWrite', '/opt/hand-added'],
    ['sandbox.network.allowedDomains', 'hand-added.example'],
    ['sandbox.credentials.files[].path', '~/.hand-added'],
    ['sandbox.credentials.envVars[].name', 'HAND_ADDED'],
  ];

  const next = renderCurrentProfile({ repoRoot: repo.dir, config: repo.config, carryForward: false });
  assert.deepEqual(
    profileEntryDelta(onDisk, next),
    expected.map(([list, entry]) => ({ list, added: [], removed: [entry] })),
  );
  assert.deepEqual(drift(repo, onDisk), {
    missing: [],
    unaccounted: expected.map(([list, entry]) => ({ list, entry })),
  });
});

test('an element with no usable string is compared by its JSON form', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  const onDisk = editProfile(repo.dir, (profile) => {
    profile.permissions.allow.push(42, '');
    profile.sandbox.credentials.files.push({ mode: 'deny' }, { path: 7 });
    profile.enabledMcpjsonServers = 'not-a-list';
  });

  const { unaccounted } = drift(repo, onDisk);
  assert.deepEqual(entriesOf(unaccounted, ALLOW), ['42', '""']);
  assert.deepEqual(entriesOf(unaccounted, 'sandbox.credentials.files[].path'), ['{"mode":"deny"}', '{"path":7}']);
  assert.deepEqual(entriesOf(unaccounted, 'enabledMcpjsonServers'), ['not-a-list']);
  assert.deepEqual(deltaOf(planned(repo).result.delta, 'sandbox.credentials.files[].path').removed, [
    '{"mode":"deny"}',
    '{"path":7}',
  ]);
});

test('with no plugin root resolved, plugin-root shapes are unaccounted', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  const onDisk = editProfile(repo.dir, (profile) => profile.permissions.allow.push(STRAY_SCRIPT, STRAY_READ));

  assert.deepEqual(entriesOf(drift(repo, onDisk).unaccounted, ALLOW), [STRAY_SCRIPT, STRAY_READ]);
});

test('with a plugin root resolved, only entries really under it are accounted for', async (t) => {
  const machine = await machineWithPlugin(t);
  const repo = await adopted(t, machine);
  const escaping = `Read(/${machine.root}/../../etc/**)`;
  const sibling = `Read(/${machine.root}-sibling/**)`;
  const onDisk = editProfile(repo.dir, (profile) => {
    profile.permissions.allow.push(
      `Bash(bash ${machine.root}/scripts/helper.sh:*)`,
      `Read(/${machine.root}/**)`,
      STRAY_SCRIPT,
      STRAY_READ,
      escaping,
      sibling,
    );
    // The plugin-root shape is accepted in `allow` only.
    profile.permissions.ask.push(`Read(/${machine.root}/**)`);
  });

  const { unaccounted } = drift(repo, onDisk);
  assert.deepEqual(entriesOf(unaccounted, ALLOW), [STRAY_SCRIPT, STRAY_READ, escaping, sibling]);
  assert.deepEqual(entriesOf(unaccounted, 'permissions.ask'), [`Read(/${machine.root}/**)`]);
});

test('a plugin root in additionalDirectories is accounted for only while it resolves', async (t) => {
  const machine = await machineWithPlugin(t);
  const repo = await adopted(t, machine);
  const onDisk = editProfile(repo.dir, (profile) => profile.permissions.additionalDirectories.push(machine.root));
  assert.deepEqual(drift(repo, onDisk).unaccounted, []);

  await machineWithoutPlugin(t);
  assert.deepEqual(drift(repo, onDisk).unaccounted, [{ list: 'permissions.additionalDirectories', entry: machine.root }]);
});

test('a refused local file propagates, and nothing is enqueued', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t));
  writeLocal(repo.dir, { permissions: { defaultMode: 'bypassPermissions' } });

  const plan = new WritePlan();
  assert.throws(() => planProfileUpgrade({ repoRoot: repo.dir, config: repo.config, plan, dryRun: true }), HarnessError);
  assert.equal(plan.size, 0);
  assert.throws(() => drift(repo), HarnessError);
});

/** The dotted path of every array under `value`. */
function arrayPaths(value, prefix = '') {
  return Object.entries(value).flatMap(([key, nested]) => {
    const path = prefix === '' ? key : `${prefix}.${key}`;
    if (Array.isArray(nested)) return [path];
    return nested !== null && typeof nested === 'object' ? arrayPaths(nested, path) : [];
  });
}

test('with the browser fragment on, every array in the render has a row', async (t) => {
  const repo = await adopted(t, await machineWithoutPlugin(t), ['--qa']);
  const rendered = renderCurrentProfile({ repoRoot: repo.dir, config: repo.config });
  assert.ok(Array.isArray(rendered.enabledMcpjsonServers), 'the browser fragment is not on');

  const rows = new Set(PROFILE_ENTRY_LISTS.map(({ path }) => path));
  const uncovered = arrayPaths(rendered).filter((path) => path !== '_README' && !rows.has(path));
  assert.deepEqual(uncovered, []);
  assert.deepEqual(planned(repo).result.delta, []);
});
