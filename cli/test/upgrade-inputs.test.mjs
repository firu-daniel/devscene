/**
 * The two read-only facts `--upgrade` and `doctor` share: `cli/src/core/runRegistry.ts` and
 * `cli/src/machine/plugins.ts` → `installedPluginVersion`.
 *
 * **The rule this suite enforces: the registry reader reports what the file holds, the active-run
 * reading stops on whatever it cannot prove idle, and the version reader answers `undefined` for
 * every failure.** Registry cases cover both pid spellings: the number a hand-written record carries
 * and the string `hr_registry_set` stores. Every file lives under the system temp directory, and the
 * agent runner's home is a scratch `CLAUDE_CONFIG_DIR`, never the real account's.
 */

import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';

import { PLUGIN_NAME } from '../dist/core/pluginIdentity.js';
import { pidIsAlive, readActiveRuns, readRegistryRecords, RUNNING_STATUS } from '../dist/core/runRegistry.js';
import { MARKETPLACE_NAME, PLUGIN_KEY } from '../dist/generators/projectSettings.js';
import { installedPluginVersion } from '../dist/machine/plugins.js';

const DEAD_PID = spawnSync(process.execPath, ['-e', '']).pid;

function tempDir(t, prefix) {
  const dir = mkdtempSync(join(tmpdir(), prefix));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function writeJson(path, value) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(value));
}

/** A registry file holding `text` verbatim, and its path. */
function registryWithText(t, text) {
  const path = join(tempDir(t, 'run-registry-'), 'registry.json');
  writeFileSync(path, text);
  return path;
}

const registryWithRuns = (t, runs) => registryWithText(t, JSON.stringify({ runs }));

function killFailsWith(t, code) {
  t.mock.method(process, 'kill', () => {
    throw Object.assign(new Error(code), { code });
  });
}

test('pidIsAlive answers for a live pid in either spelling and for no other value', () => {
  assert.equal(RUNNING_STATUS, 'running');
  assert.equal(pidIsAlive(process.pid), true);
  assert.equal(pidIsAlive(String(process.pid)), true);
  for (const pid of [DEAD_PID, String(DEAD_PID), 0, -1, '0', '-1', 1.5, '', 'abc', null, true, undefined]) {
    assert.equal(pidIsAlive(pid), false, `pid ${JSON.stringify(pid)}`);
  }
});

test('pidIsAlive reads EPERM as alive and any other failure as dead', async (t) => {
  await t.test('EPERM', (t) => {
    killFailsWith(t, 'EPERM');
    assert.equal(pidIsAlive(4242), true);
  });
  await t.test('ESRCH', (t) => {
    killFailsWith(t, 'ESRCH');
    assert.equal(pidIsAlive(4242), false);
  });
});

test('pidIsAlive never reaches the syscall for a non-positive pid', (t) => {
  const kill = t.mock.method(process, 'kill', () => true);
  for (const pid of [0, -1, '0', '-1']) pidIsAlive(pid);
  assert.equal(kill.mock.callCount(), 0);
});

test('readRegistryRecords answers a missing file with no records and creates nothing', (t) => {
  const path = join(tempDir(t, 'run-registry-'), 'absent', 'registry.json');
  assert.deepEqual(readRegistryRecords(path), { state: 'read', records: [], malformedKeys: [] });
  assert.equal(existsSync(dirname(path)), false);
});

test('readRegistryRecords reports malformed JSON and a path it cannot read as unreadable', (t) => {
  const malformed = registryWithText(t, '{"runs":');
  const parsed = readRegistryRecords(malformed);
  assert.equal(parsed.state, 'unreadable');
  assert.match(parsed.detail, /is not valid JSON/);
  assert.ok(parsed.detail.includes(malformed));

  const directory = tempDir(t, 'run-registry-');
  const unread = readRegistryRecords(directory);
  assert.equal(unread.state, 'unreadable');
  assert.match(unread.detail, /EISDIR/);
});

test('readRegistryRecords reports every shape other than {"runs": {…}} as unreadable', async (t) => {
  for (const text of ['[]', '{}', '"runs"', 'null', '{"runs":[]}', '{"runs":null}', '{"runs":"x"}']) {
    await t.test(text, (t) => {
      const path = registryWithText(t, text);
      const result = readRegistryRecords(path);
      assert.equal(result.state, 'unreadable');
      assert.ok(result.detail.includes(path));
    });
  }
});

test('readRegistryRecords lists a non-object record by key and keeps the others', (t) => {
  const good = { status: 'completed' };
  const path = registryWithRuns(t, { good, nothing: null, list: [], text: 'x', count: 1 });
  assert.deepEqual(readRegistryRecords(path), {
    state: 'read',
    records: [{ key: 'good', record: good }],
    malformedKeys: ['nothing', 'list', 'text', 'count'],
  });
});

test('readActiveRuns is none for a missing file and for an empty registry', (t) => {
  assert.deepEqual(readActiveRuns(join(tempDir(t, 'run-registry-'), 'registry.json')), { state: 'none' });
  assert.deepEqual(readActiveRuns(registryWithRuns(t, {})), { state: 'none' });
});

test('readActiveRuns grades one record by its status and its pid', async (t) => {
  const running = (fields) => ({ status: 'running', ...fields });
  const cases = [
    ['a live numeric pid', running({ pid: process.pid }), true],
    ['a live pid as the watcher stores it', running({ pid: String(process.pid) }), true],
    ['no pid yet', running({}), true],
    ['a null pid', running({ pid: null }), true],
    ['a pid the watcher cleared', running({ pid: '' }), true],
    ['a pid field holding no number', running({ pid: 'pending' }), true],
    ['a dead numeric pid', running({ pid: DEAD_PID }), false],
    ['a dead pid as the watcher stores it', running({ pid: String(DEAD_PID) }), false],
    ['a non-positive pid', running({ pid: 0 }), false],
    ['a finished record with a live pid', { status: 'completed', pid: process.pid }, false],
    ['a parked record with a live stored pid', { status: 'parked', pid: String(process.pid) }, false],
    ['a record with no status', { pid: process.pid }, false],
  ];
  for (const [label, record, active] of cases) {
    await t.test(label, (t) => {
      const expected = active ? { state: 'active', branches: ['feat_x'] } : { state: 'none' };
      assert.deepEqual(readActiveRuns(registryWithRuns(t, { feat_x: record })), expected);
    });
  }
});

test('readActiveRuns names only the active branches', (t) => {
  const path = registryWithRuns(t, {
    feat_a: { status: 'running', pid: String(process.pid) },
    feat_b: { status: 'completed', pid: '' },
    feat_c: { status: 'running' },
    feat_d: { status: 'running', pid: String(DEAD_PID) },
  });
  assert.deepEqual(readActiveRuns(path), { state: 'active', branches: ['feat_a', 'feat_c'] });
});

test('readActiveRuns is unreadable for a non-object record, even beside an active run', (t) => {
  const path = registryWithRuns(t, { feat_a: { status: 'running', pid: process.pid }, feat_b: 'corrupt' });
  const result = readActiveRuns(path);
  assert.equal(result.state, 'unreadable');
  assert.ok(result.detail.includes(path));
  assert.ok(result.detail.includes('feat_b'));
  assert.ok(!result.detail.includes('feat_a'));
});

test('readActiveRuns passes on an unreadable registry', (t) => {
  const path = registryWithText(t, 'not json');
  assert.deepEqual(readActiveRuns(path), readRegistryRecords(path));
  assert.equal(readActiveRuns(path).state, 'unreadable');
});

/** Point the agent runner's home at a scratch directory for this test, and return it. */
function scratchHome(t) {
  const home = tempDir(t, 'plugin-version-');
  const previous = process.env.CLAUDE_CONFIG_DIR;
  process.env.CLAUDE_CONFIG_DIR = home;
  t.after(() => {
    if (previous === undefined) delete process.env.CLAUDE_CONFIG_DIR;
    else process.env.CLAUDE_CONFIG_DIR = previous;
  });
  return home;
}

/** Record `installRoot` as this plugin's install, on a row of `row`'s scope. */
function recordInstall(home, installRoot, row = { scope: 'user' }) {
  writeJson(join(home, 'plugins', 'installed_plugins.json'), {
    version: 2,
    plugins: { [PLUGIN_KEY]: [{ ...row, installPath: installRoot }] },
  });
}

/** Record a directory-sourced marketplace at `<home>/source` and return the runtime root it yields. */
function recordDirectoryMarketplace(home) {
  const location = join(home, 'source');
  writeJson(join(home, 'plugins', 'known_marketplaces.json'), {
    [MARKETPLACE_NAME]: { source: { source: 'directory' }, installLocation: location },
  });
  writeJson(join(location, '.claude-plugin', 'marketplace.json'), {
    plugins: [{ name: PLUGIN_NAME, source: './plugin' }],
  });
  return join(location, 'plugin');
}

const writeManifest = (root, manifest) => writeJson(join(root, '.claude-plugin', 'plugin.json'), manifest);

test('installedPluginVersion reads the manifest at the install root', (t) => {
  const home = scratchHome(t);
  const root = join(home, 'cache', '1.2.3');
  recordInstall(home, root);
  writeManifest(root, { name: PLUGIN_NAME, version: '1.2.3' });
  assert.equal(installedPluginVersion(), '1.2.3');
});

test('installedPluginVersion passes the repository to the install-row selection', (t) => {
  const home = scratchHome(t);
  const root = join(home, 'cache', '2.0.0');
  recordInstall(home, root, { scope: 'project', projectPath: '/repo/here' });
  writeManifest(root, { version: '2.0.0' });
  assert.equal(installedPluginVersion('/repo/here'), '2.0.0');
});

test('installedPluginVersion prefers the runtime root over the install root', (t) => {
  const home = scratchHome(t);
  const installRoot = join(home, 'cache', '1.0.0');
  recordInstall(home, installRoot);
  writeManifest(installRoot, { version: '1.0.0' });
  writeManifest(recordDirectoryMarketplace(home), { version: '1.1.0' });
  assert.equal(installedPluginVersion(), '1.1.0');
});

test('installedPluginVersion falls back to the install root when the runtime root answers nothing', async (t) => {
  const cases = [
    ['a missing manifest', undefined],
    ['a non-string version', { version: 3 }],
    ['an empty version', { version: '' }],
  ];
  for (const [label, runtimeManifest] of cases) {
    await t.test(label, (t) => {
      const home = scratchHome(t);
      const installRoot = join(home, 'cache', '1.0.0');
      recordInstall(home, installRoot);
      writeManifest(installRoot, { version: '1.0.0' });
      const runtimeRoot = recordDirectoryMarketplace(home);
      if (runtimeManifest !== undefined) writeManifest(runtimeRoot, runtimeManifest);
      assert.equal(installedPluginVersion(), '1.0.0');
    });
  }
});

test('installedPluginVersion answers undefined for every failure', async (t) => {
  await t.test('no records at all', (t) => {
    scratchHome(t);
    assert.equal(installedPluginVersion(), undefined);
  });

  const atInstallRoot = [
    ['a missing manifest', () => {}],
    ['a non-string version', (root) => writeManifest(root, { version: 1 })],
    ['no version', (root) => writeManifest(root, { name: PLUGIN_NAME })],
    ['a manifest that is not an object', (root) => writeManifest(root, ['1.0.0'])],
    [
      'an unparsable manifest',
      (root) => {
        mkdirSync(join(root, '.claude-plugin'), { recursive: true });
        writeFileSync(join(root, '.claude-plugin', 'plugin.json'), '{');
      },
    ],
  ];
  for (const [label, arrange] of atInstallRoot) {
    await t.test(label, (t) => {
      const home = scratchHome(t);
      const root = join(home, 'cache', '1.0.0');
      recordInstall(home, root);
      arrange(root);
      assert.equal(installedPluginVersion(), undefined);
    });
  }
});
