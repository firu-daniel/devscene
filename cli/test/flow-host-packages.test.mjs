/**
 * The shipped Python packages `init` writes under `<scriptsDir>/python/`, through the compiled CLI
 * against throwaway fixture repositories.
 *
 * **The rule this suite exists to enforce: `init` copies the staged `dist/python/` tree byte for
 * byte, keeps an edited copy on a plain re-run, replaces it after a `.bak` under `--force`, and
 * `init --upgrade` restores the shipped bytes after a backup.** Expected bytes are read from
 * `cli/dist/python/`, because "copied verbatim" is the contract.
 *
 * `flowHostPackageDrift` is reached through no command yet; its missing and changed cases are
 * asserted through `doctor` by the task that adds that check.
 */

import assert from 'node:assert/strict';
import { appendFileSync, existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';

import { stagedPythonDir } from '../dist/flowHost/layout.js';
import { createFixture, INIT_SCRIPTS_DIR, runCli, snapshotTree } from './helpers/fixture.mjs';

const RELOCATED_SCRIPTS_DIR = 'tools/harness';
const CLAUDE_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';
const BACKUP_ROOT = ['.git', 'devscene', 'upgrade-backups'];
const EDIT = '# This line was added by hand.\n';

/** Two shipped files, by their path under `dist/python/`. */
const PYPROJECT = 'devscene-flow-host/pyproject.toml';
const GRAPHSCENE_INIT = 'graphscene/src/graphscene/__init__.py';

const staged = (relative) => readFileSync(join(stagedPythonDir(), ...relative.split('/')));
const written = (dir, scriptsDir, relative) => join(dir, ...scriptsDir.split('/'), 'python', ...relative.split('/'));

/** A fixture whose detection resolves every command, with its own agent-runner home. */
async function repository(t) {
  const home = await createFixture({ git: false });
  t.after(home.cleanup);
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
  const run = async (args) => {
    const result = await runCli(dir, args, { [CLAUDE_HOME_VARIABLE]: home.dir });
    assert.equal(result.status, 0, `${args.join(' ')} exited ${result.status}\n${result.stdout}\n${result.stderr}`);
    return result;
  };
  return { dir, run };
}

for (const [label, scriptsDir, flags] of [
  ['the default scriptsDir', INIT_SCRIPTS_DIR, []],
  [`--scripts-dir ${RELOCATED_SCRIPTS_DIR}`, RELOCATED_SCRIPTS_DIR, ['--scripts-dir', RELOCATED_SCRIPTS_DIR]],
]) {
  test(`init writes the shipped packages byte for byte under ${label}, and a second init changes nothing`, async (t) => {
    const repo = await repository(t);
    await repo.run(['init', ...flags]);

    for (const relative of [PYPROJECT, GRAPHSCENE_INIT]) {
      const path = written(repo.dir, scriptsDir, relative);
      assert.ok(existsSync(path), `${relative} was not written under ${scriptsDir}/python`);
      assert.ok(readFileSync(path).equals(staged(relative)), `${relative} differs from dist/python`);
    }

    const before = await snapshotTree(repo.dir);
    await repo.run(['init', ...flags]);
    assert.deepEqual(await snapshotTree(repo.dir), before);
  });
}

test('an edited copy survives a plain re-run, and --force replaces it after a .bak', async (t) => {
  const repo = await repository(t);
  await repo.run(['init']);
  const path = written(repo.dir, INIT_SCRIPTS_DIR, PYPROJECT);
  appendFileSync(path, EDIT);
  const edited = readFileSync(path);

  await repo.run(['init']);
  assert.ok(readFileSync(path).equals(edited), 'a plain re-run rewrote the edited copy');

  await repo.run(['init', '--force']);
  assert.ok(readFileSync(path).equals(staged(PYPROJECT)), '--force did not restore the shipped bytes');
  assert.ok(readFileSync(`${path}.bak`).equals(edited), '--force left no .bak of the edited copy');
});

test('init --upgrade restores the shipped bytes after a backup', async (t) => {
  const repo = await repository(t);
  await repo.run(['init']);
  const path = written(repo.dir, INIT_SCRIPTS_DIR, GRAPHSCENE_INIT);
  appendFileSync(path, EDIT);
  const edited = readFileSync(path);

  await repo.run(['init', '--upgrade']);
  assert.ok(readFileSync(path).equals(staged(GRAPHSCENE_INIT)), 'the upgrade did not restore the shipped bytes');

  const backupRoot = join(repo.dir, ...BACKUP_ROOT);
  const runs = readdirSync(backupRoot);
  assert.equal(runs.length, 1, `expected one backup run, found ${runs.join(', ')}`);
  const backup = join(backupRoot, runs[0], ...INIT_SCRIPTS_DIR.split('/'), 'python', ...GRAPHSCENE_INIT.split('/'));
  assert.ok(readFileSync(backup).equals(edited), 'the backup does not hold the edited copy');
});
