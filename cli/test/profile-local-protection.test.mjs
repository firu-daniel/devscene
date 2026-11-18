/**
 * The protection of the local permission additions file.
 *
 * **The rule this suite exists to enforce: a session cannot write
 * `.claude/settings.autonomous.local.json` in the main checkout, and git ignores that file.** Its
 * entries reach the profile every run is rendered from, so a writable copy would let a session grant
 * itself permissions. Only the main checkout's copy is protected, because a run loads no other: the
 * path stays out of the run-copy surface, and so out of the shell mirror of that surface.
 *
 * Every fixture lives under the system temp directory and is removed in process. These run against
 * the **compiled** CLI, so `npm run build` precedes `npm test`.
 */

import assert from 'node:assert/strict';
import { join } from 'node:path';
import { test } from 'node:test';

import { copySurfacePaths, jobSurfacePaths, runRegistryPath } from '../dist/generators/writeProtection.js';
import { createFixture, ignoredAmong, readJson, runCli } from './helpers/fixture.mjs';

const LOCAL_FILE = '.claude/settings.autonomous.local.json';
const PROFILE_FILE = '.claude/settings.autonomous.json';
const COMMITTED_SETTINGS_FILE = '.claude/settings.json';
const CONFIG_FILE = 'devscene.config.json';
const GITIGNORE_FILE = '.gitignore';
const REGISTRY_SEGMENTS = ['autonomous_logs', 'registry.json'];

/** A repository `init` has wired, torn down after `t`. */
async function wiredFixture(t) {
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
  const result = await runCli(fixture.dir, ['init']);
  assert.equal(result.status, 0, `init exited ${result.status}\n${result.stdout}\n${result.stderr}`);
  return { dir: fixture.dir, stdout: result.stdout };
}

test('the profile denies writes to the main checkout copy on both sides', async (t) => {
  const { dir } = await wiredFixture(t);
  const profile = readJson(join(dir, PROFILE_FILE));
  const absolute = join(dir, LOCAL_FILE);

  assert.ok(profile.sandbox.filesystem.denyWrite.includes(absolute), `${absolute} is not in denyWrite`);
  assert.ok(profile.permissions.deny.includes(`Edit(/${absolute})`), `no exact Edit deny rule for ${absolute}`);

  const { stdout, stderr } = await runCli(dir, ['doctor']);
  assert.match(stdout, /^PASS\s+profile-write-protection\s/m, `doctor did not pass the check\n${stdout}\n${stderr}`);
});

test('git ignores the file, and the rule reaches no committed neighbour', async (t) => {
  const { dir } = await wiredFixture(t);
  assert.deepEqual(await ignoredAmong(dir, [LOCAL_FILE, COMMITTED_SETTINGS_FILE]), [LOCAL_FILE]);
});

test('a second init keeps the ignore file', async (t) => {
  const { dir } = await wiredFixture(t);
  const second = await runCli(dir, ['init']);
  assert.equal(second.status, 0, `the second init exited ${second.status}\n${second.stdout}\n${second.stderr}`);
  assert.match(second.stdout, new RegExp(`^= kept +${GITIGNORE_FILE.replace('.', '\\.')}(\\s|$)`, 'm'), second.stdout);
});

test('the file is on the remote job surface and off the run-copy surface', async (t) => {
  const { dir } = await wiredFixture(t);
  const config = readJson(join(dir, CONFIG_FILE));
  assert.ok(jobSurfacePaths(config).includes(LOCAL_FILE), `${LOCAL_FILE} is not a job surface`);
  assert.ok(!copySurfacePaths(config).includes(LOCAL_FILE), `${LOCAL_FILE} is on the run-copy surface`);
});

test('runRegistryPath falls back to the default state directory', () => {
  assert.equal(runRegistryPath('/repo', {}), join('/repo', 'devscene', ...REGISTRY_SEGMENTS));
});

test('runRegistryPath normalizes a configured state directory with a trailing slash', () => {
  assert.equal(runRegistryPath('/repo', { stateDir: 'runs/' }), join('/repo', 'runs', ...REGISTRY_SEGMENTS));
});
