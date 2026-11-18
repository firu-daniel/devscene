/**
 * The local permission additions, merged into the rendered profile.
 *
 * **The rule this suite exists to enforce: the profile a run writes is the generated profile plus
 * the validated `.claude/settings.autonomous.local.json`, and an entry that file supplied leaves the
 * profile when the file stops supplying it.** A plain re-run that keeps the profile never reads the
 * local file, and a refused run leaves the tree byte-identical.
 *
 * Every case passes its own `CLAUDE_CONFIG_DIR`, because the plugin roots are resolved from a file
 * outside every repository. These run against the **compiled** CLI.
 */

import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { test } from 'node:test';

import { EXIT } from '../dist/core/errors.js';
import { isToolchainEntry } from '../dist/generators/permissionProfile.js';
import { PLUGIN_KEY } from '../dist/generators/projectSettings.js';
import { createFixture, readJson, runCli, snapshotTree } from './helpers/fixture.mjs';

const LOCAL_FILE = '.claude/settings.autonomous.local.json';
const PROFILE_FILE = '.claude/settings.autonomous.json';
const RECORD_PREFIX = 'LOCAL ALLOW ENTRY: ';

const LOCAL_ALLOW = 'Bash(local-allow:*)';
const LOCAL_ASK = 'Bash(local-ask:*)';
const LOCAL_DENY = 'Bash(local-deny:*)';
const LOCAL_DENY_WRITE = '/opt/local-deny-write';
const LOCAL_READ = 'Read(//opt/tools/**)';
const PLAIN_ALLOW = 'Bash(foo:*)';

const EVERY_LIST = {
  permissions: { allow: [LOCAL_ALLOW, LOCAL_ALLOW], ask: [LOCAL_ASK], deny: [LOCAL_DENY] },
  sandbox: { filesystem: { denyWrite: [LOCAL_DENY_WRITE] } },
};
const CARRY_SHAPED = { permissions: { allow: [PLAIN_ALLOW, LOCAL_READ] } };

async function temporaryDir(t) {
  const fixture = await createFixture({ git: false });
  t.after(fixture.cleanup);
  return fixture.dir;
}

/** A repository with detectable commands, not yet wired. */
async function repository(t) {
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
  return fixture.dir;
}

/** An agent-runner home that resolves no plugin root. */
async function machineWithoutPlugin(t) {
  return { CLAUDE_CONFIG_DIR: await temporaryDir(t) };
}

/** An agent-runner home recording one plugin install root. */
async function machineWithPlugin(t) {
  const root = await temporaryDir(t);
  const home = await temporaryDir(t);
  mkdirSync(join(home, 'plugins'), { recursive: true });
  writeFileSync(
    join(home, 'plugins', 'installed_plugins.json'),
    `${JSON.stringify({ version: 2, plugins: { [PLUGIN_KEY]: [{ scope: 'user', installPath: root }] } }, null, 2)}\n`,
  );
  return { CLAUDE_CONFIG_DIR: home };
}

function writeLocal(dir, content) {
  mkdirSync(join(dir, '.claude'), { recursive: true });
  writeFileSync(join(dir, LOCAL_FILE), typeof content === 'string' ? content : `${JSON.stringify(content, null, 2)}\n`);
}

async function initOk(dir, args, env) {
  const result = await runCli(dir, ['init', ...args], env);
  assert.equal(result.status, 0, `init ${args.join(' ')} exited ${result.status}\n${result.stdout}\n${result.stderr}`);
  return result;
}

const profileOf = (dir) => readJson(join(dir, PROFILE_FILE));
const profileBytes = (dir) => readFileSync(join(dir, PROFILE_FILE));
const records = (profile) => profile._README.filter((line) => line.startsWith(RECORD_PREFIX));

/** Each local entry is present once, and after every entry the same list had without it. */
function assertMergedLast(list, entry, generated) {
  assert.equal(list.filter((item) => item === entry).length, 1, `${entry} is not listed exactly once`);
  assert.equal(list.indexOf(entry), generated.length, `${entry} does not follow every generated entry`);
  assert.deepEqual(list.slice(0, generated.length), generated, 'the generated entries changed');
}

function assertEveryListMerged(profile, baseline) {
  assertMergedLast(profile.permissions.allow, LOCAL_ALLOW, baseline.permissions.allow);
  assertMergedLast(profile.permissions.ask, LOCAL_ASK, baseline.permissions.ask);
  assertMergedLast(profile.permissions.deny, LOCAL_DENY, baseline.permissions.deny);
  assertMergedLast(profile.sandbox.filesystem.denyWrite, LOCAL_DENY_WRITE, baseline.sandbox.filesystem.denyWrite);
}

/** A value with every list removed, so only its non-list settings are compared. */
function withoutLists(value) {
  if (Array.isArray(value)) return undefined;
  if (value === null || typeof value !== 'object') return value;
  return Object.fromEntries(
    Object.entries(value)
      .filter(([, nested]) => !Array.isArray(nested))
      .map(([key, nested]) => [key, withoutLists(nested)]),
  );
}

/** A forced run that must be refused for the adopter's input, leaving every byte where it was. */
async function assertForcedRunRefused(dir, env, expected) {
  const before = await snapshotTree(dir);
  const result = await runCli(dir, ['init', '--force'], env);
  assert.notEqual(result.status, 0, `the run was not refused\n${result.stdout}`);
  assert.notEqual(result.status, EXIT.INTERNAL, `an adopter's input was billed to this CLI\n${result.stderr}`);
  assert.ok(result.stderr.includes(LOCAL_FILE), `the refusal does not name the file\n${result.stderr}`);
  assert.ok(result.stderr.includes(expected), `the refusal does not name ${expected}\n${result.stderr}`);
  assert.deepEqual(await snapshotTree(dir), before, 'the refused run changed the tree');
}

test('a fresh init merges a local entry from each list, after the generated ones and once', async (t) => {
  const env = await machineWithoutPlugin(t);
  const baselineDir = await repository(t);
  await initOk(baselineDir, [], env);
  const dir = await repository(t);
  writeLocal(dir, EVERY_LIST);
  await initOk(dir, [], env);

  const profile = profileOf(dir);
  const rebased = JSON.parse(JSON.stringify(profileOf(baselineDir)).replaceAll(baselineDir, dir));
  assertEveryListMerged(profile, rebased);
});

test('init --force merges a local entry from each list, and the sandbox settings do not move', async (t) => {
  const env = await machineWithoutPlugin(t);
  const dir = await repository(t);
  await initOk(dir, [], env);
  const baseline = profileOf(dir);
  assert.deepEqual(records(baseline), [], 'a profile with no local file carries a local record');

  writeLocal(dir, EVERY_LIST);
  await initOk(dir, ['--force'], env);
  const profile = profileOf(dir);
  assertEveryListMerged(profile, baseline);
  assert.deepEqual(withoutLists(profile.sandbox), withoutLists(baseline.sandbox));
});

test('a plain re-run keeps the profile and never reads an invalid local file', async (t) => {
  const env = await machineWithoutPlugin(t);
  const dir = await repository(t);
  await initOk(dir, [], env);
  const before = profileBytes(dir);
  writeLocal(dir, '{ not json');

  await initOk(dir, [], env);
  assert.deepEqual(profileBytes(dir), before);
});

test('a first init is refused by an invalid local file, because it would write the profile', async (t) => {
  const env = await machineWithoutPlugin(t);
  const dir = await repository(t);
  writeLocal(dir, { model: 'not-allowed' });

  const result = await runCli(dir, ['init'], env);
  assert.notEqual(result.status, 0, result.stdout);
  assert.ok(result.stderr.includes(LOCAL_FILE), result.stderr);
  assert.equal(existsSync(join(dir, PROFILE_FILE)), false, 'the refused run wrote the profile');
});

test('a forced run with an invalid local file is refused and changes nothing', async (t) => {
  const env = await machineWithoutPlugin(t);
  const dir = await repository(t);
  await initOk(dir, [], env);
  writeLocal(dir, { permissions: { defaultMode: 'bypassPermissions' } });

  await assertForcedRunRefused(dir, env, 'permissions.defaultMode');
  assert.equal(existsSync(join(dir, `${PROFILE_FILE}.bak`)), false, 'the refused run took a backup');
});

for (const [name, additions, expected] of [
  ['a deny entry naming a browser tool', { permissions: { deny: ['mcp__playwright__browser_click'] } }, 'mcp__playwright__browser_click'],
  ['an allow entry for a server the profile does not start', { permissions: { allow: ['mcp__nowhere__tool'] } }, 'mcp__nowhere__tool'],
  ['an allow entry naming no tool', { permissions: { allow: ['mcp__nowhere'] } }, 'mcp__nowhere'],
]) {
  test(`${name} is refused as the adopter's to fix`, async (t) => {
    const env = await machineWithoutPlugin(t);
    const dir = await repository(t);
    await initOk(dir, [], env);
    writeLocal(dir, additions);
    await assertForcedRunRefused(dir, env, expected);
  });
}

test('an allow entry for a server the profile starts is accepted', async (t) => {
  const env = await machineWithoutPlugin(t);
  const dir = await repository(t);
  writeLocal(dir, { permissions: { allow: ['mcp__playwright__browser_route'] } });
  await initOk(dir, ['--qa'], env);
  assert.ok(profileOf(dir).permissions.allow.includes('mcp__playwright__browser_route'));
});

test('with no plugin root, forced renders of carry-shaped local entries are byte-identical', async (t) => {
  const env = await machineWithoutPlugin(t);
  const dir = await repository(t);
  writeLocal(dir, { permissions: { allow: [PLAIN_ALLOW, LOCAL_READ, LOCAL_READ] } });
  await initOk(dir, [], env);
  await initOk(dir, ['--force'], env);
  const first = profileBytes(dir);
  await initOk(dir, ['--force'], env);
  assert.deepEqual(profileBytes(dir), first);

  const profile = profileOf(dir);
  assert.deepEqual(profile.permissions.allow.slice(-2), [PLAIN_ALLOW, LOCAL_READ]);
  assert.deepEqual(records(profile), [`${RECORD_PREFIX}${LOCAL_READ}`], 'only the carry-shaped entry is recorded, once');
});

test('with a plugin root resolved, no left-behind warning names a local entry', async (t) => {
  const env = await machineWithPlugin(t);
  const dir = await repository(t);
  writeLocal(dir, CARRY_SHAPED);
  await initOk(dir, [], env);

  const { stdout, stderr } = await initOk(dir, ['--force'], env);
  assert.ok(!`${stdout}\n${stderr}`.includes(LOCAL_READ), `the run reported a local entry:\n${stdout}\n${stderr}`);
  assert.ok(profileOf(dir).permissions.allow.includes(LOCAL_READ));
});

for (const [name, machine] of [
  ['no plugin root', machineWithoutPlugin],
  ['a plugin root', machineWithPlugin],
]) {
  test(`with ${name}, an entry deleted from the local file leaves on the next forced render`, async (t) => {
    const env = await machine(t);
    const dir = await repository(t);
    writeLocal(dir, CARRY_SHAPED);
    await initOk(dir, [], env);

    writeLocal(dir, { permissions: { allow: [PLAIN_ALLOW] } });
    const { stdout, stderr } = await initOk(dir, ['--force'], env);
    const profile = profileOf(dir);
    assert.ok(!profile.permissions.allow.includes(LOCAL_READ), 'the deleted entry was carried forward');
    assert.deepEqual(records(profile), [], 'the deleted entry is still recorded');
    assert.ok(!`${stdout}\n${stderr}`.includes(LOCAL_READ), 'the run reported the deleted entry');
  });

  test(`with ${name}, deleting the whole local file removes its entries`, async (t) => {
    const env = await machine(t);
    const dir = await repository(t);
    writeLocal(dir, CARRY_SHAPED);
    await initOk(dir, [], env);

    rmSync(join(dir, LOCAL_FILE));
    const { stdout, stderr } = await initOk(dir, ['--force'], env);
    assert.ok(!profileOf(dir).permissions.allow.includes(LOCAL_READ), 'the entry was carried forward');
    assert.ok(!`${stdout}\n${stderr}`.includes(LOCAL_READ), 'the run reported the deleted entry');
  });
}

test('with no plugin root, a pasted entry that was never local is still carried', async (t) => {
  const env = await machineWithoutPlugin(t);
  const dir = await repository(t);
  await initOk(dir, [], env);
  const profile = profileOf(dir);
  profile.permissions.allow.push(LOCAL_READ);
  writeFileSync(join(dir, PROFILE_FILE), `${JSON.stringify(profile, null, 2)}\n`);

  await initOk(dir, ['--force'], env);
  assert.ok(profileOf(dir).permissions.allow.includes(LOCAL_READ), 'the pasted entry was not carried');
});

test('isToolchainEntry recognises only a configured command under an absolute directory', () => {
  const config = { phases: { parity: true }, parity: { toolchainCommands: ['reference-analyze', ' bin/format '] } };
  assert.equal(isToolchainEntry('Bash(/opt/ref/reference-analyze:*)', config), true);
  assert.equal(isToolchainEntry('Bash(/opt/ref/bin/format:*)', config), true);
  assert.equal(isToolchainEntry('Bash(/reference-analyze:*)', config), true);
  assert.equal(isToolchainEntry('Bash(/opt/ref/other:*)', config), false);
  assert.equal(isToolchainEntry('Bash(/opt/ref/not-reference-analyze:*)', config), false);
  assert.equal(isToolchainEntry('Bash(reference-analyze:*)', config), false);
  assert.equal(isToolchainEntry('Read(//opt/ref/reference-analyze/**)', config), false);
  assert.equal(isToolchainEntry('Bash(/opt/ref/reference-analyze:*)', { ...config, phases: { parity: false } }), false);
});
