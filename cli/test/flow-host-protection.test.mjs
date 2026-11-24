/**
 * The write protection of the main checkout's `<scriptsDir>/python/`.
 *
 * **The rule this suite enforces: anything that runs outside the sandbox must not be writable from
 * inside it.** The flow walker's environment is provisioned outside the sandbox from the main
 * checkout's `<scriptsDir>/python/`, which builds those packages, so the profile denies writes to
 * that directory on both sides and a remote job refuses a branch whose own commits changed it. A run
 * copy's directory is not protected: no unsandboxed step builds from it, so the directory stays off
 * the run-copy surface.
 *
 * Every fixture lives under the system temp directory and is removed in process; no case reaches the
 * network. These run against the **compiled** CLI, so `npm run build` precedes `npm test`.
 */

import assert from 'node:assert/strict';
import { realpathSync } from 'node:fs';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';

import { flowHostDir, flowHostProjectDir } from '../dist/flowHost/layout.js';
import { copySurfacePaths, fileToolDenyRules } from '../dist/generators/writeProtection.js';
import { createFixture, readJson, runCli, runGit } from './helpers/fixture.mjs';

const PROFILE_FILE = '.claude/settings.autonomous.json';
const CONFIG_FILE = 'devscene.config.json';
const DEFAULT_BRANCH = 'main';
const RUN_BRANCH = 'harness/run-1';

/** A repository `init` has wired, torn down after `t`, with its written configuration. */
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
  return { dir: fixture.dir, config: readJson(join(fixture.dir, CONFIG_FILE)) };
}

test("the profile denies writes to the main checkout's <scriptsDir>/python on both sides", async (t) => {
  const { dir, config } = await wiredFixture(t);
  const profile = readJson(join(dir, PROFILE_FILE));
  const absolute = join(dir, flowHostDir(config));

  assert.ok(profile.sandbox.filesystem.denyWrite.includes(absolute), `${absolute} is not in denyWrite`);
  const [rule] = fileToolDenyRules({ path: absolute, kind: 'directory', reason: '' });
  assert.ok(profile.permissions.deny.includes(rule), `no ${rule} in permissions.deny`);
});

test('the directory is off the run-copy surface', async (t) => {
  const { config } = await wiredFixture(t);
  const dir = flowHostDir(config);
  const carried = copySurfacePaths(config).filter((rel) => rel === dir || rel.startsWith(`${dir}/`));
  assert.deepEqual(carried, [], `the run-copy surface carries ${carried.join(', ')}`);
});

/** Write `files` (relative path → text) under `dir`. */
async function writeFiles(dir, files) {
  for (const [relative, text] of Object.entries(files)) {
    const path = join(dir, relative);
    await mkdir(dirname(path), { recursive: true });
    await writeFile(path, text, 'utf8');
  }
}

/** Stage everything in `dir` and commit it. */
async function commit(dir, message) {
  await runGit(dir, ['add', '-A']);
  await runGit(dir, ['commit', '--quiet', '-m', message]);
}

test("doctor --job-surfaces fails a branch whose own commit changed the shipped project's pyproject.toml, naming it", async (t) => {
  const config = {
    version: 1,
    projectName: 'demo',
    defaultBranch: DEFAULT_BRANCH,
    stateDir: 'devscene/',
    scriptsDir: 'scripts',
    githooksDir: 'githooks',
    layers: [{ name: 'general', path: '.', conventions: '.claude/context/conventions.md' }],
    commands: { typecheck: 'true', test: 'true' },
  };
  const changed = `${flowHostProjectDir(config)}/pyproject.toml`;

  const root = realpathSync(await mkdtemp(join(tmpdir(), 'flow-host-protection-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const origin = join(root, 'origin.git');
  const work = join(root, 'work');
  const clone = join(root, 'clone');
  await mkdir(origin);
  await runGit(origin, ['init', '--quiet', '--bare']);
  await mkdir(work);
  await runGit(work, ['init', '--quiet', '-b', DEFAULT_BRANCH]);
  await runGit(work, ['config', 'user.email', 'fixture@example.invalid']);
  await runGit(work, ['config', 'user.name', 'fixture']);
  await runGit(work, ['remote', 'add', 'origin', origin]);
  await writeFiles(work, {
    [CONFIG_FILE]: `${JSON.stringify(config, null, 2)}\n`,
    [changed]: '[project]\nname = "devscene-flow-host"\n',
  });
  await commit(work, 'seed');
  await runGit(work, ['checkout', '--quiet', '-b', RUN_BRANCH]);
  await writeFiles(work, { [changed]: '[project]\nname = "devscene-flow-host"\n# changed on the run branch\n' });
  await commit(work, `change ${changed}`);
  await runGit(work, ['push', '--quiet', 'origin', DEFAULT_BRANCH, RUN_BRANCH]);
  await runGit(root, ['clone', '--quiet', origin, clone]);
  await runGit(clone, ['checkout', '--quiet', '-b', RUN_BRANCH, `origin/${RUN_BRANCH}`]);

  const result = await runCli(clone, ['doctor', `--job-surfaces=${DEFAULT_BRANCH}`]);
  const text = `${result.stdout}\n${result.stderr}`;
  assert.equal(result.status, 1, `expected exit 1, got ${result.status}\n${text}`);
  assert.match(text, /FAIL\s+job-surfaces/);
  assert.ok(text.includes(changed), `expected ${changed} in\n${text}`);
});
