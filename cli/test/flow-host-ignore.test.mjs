/**
 * The managed `.gitignore` block's rule for the flow walker's environment, through the compiled CLI
 * against throwaway fixture repositories.
 *
 * **The rule this suite enforces: every checkout that provisions the walker's environment ignores
 * `<scriptsDir>/python/.venv/`, under whichever `scriptsDir` is configured, and a re-run adds no
 * second copy of the line.** The expected rules are spelled out here rather than read from
 * `cli/src/flowHost/layout.ts`, so a change to the producer is a change this suite sees.
 *
 * Every fixture lives under the system temp directory and is removed in process; no case reaches the
 * network. These run against the **compiled** CLI, so `npm run build` precedes `npm test`.
 */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import test from 'node:test';

import { createFixture, runCli, runGit } from './helpers/fixture.mjs';

const RELOCATED_SCRIPTS_DIR = 'tools/harness';
const CLAUDE_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';

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

const ignoreLines = (dir) => readFileSync(join(dir, '.gitignore'), 'utf8').split('\n');

for (const [label, rule, flags] of [
  ['the default scriptsDir', 'devscene-scripts/python/.venv/', []],
  [`--scripts-dir ${RELOCATED_SCRIPTS_DIR}`, `${RELOCATED_SCRIPTS_DIR}/python/.venv/`, ['--scripts-dir', RELOCATED_SCRIPTS_DIR]],
]) {
  test(`init ignores ${rule} under ${label}, once, and git then reports the environment as nothing`, async (t) => {
    const repo = await repository(t);
    await repo.run(['init', ...flags]);
    assert.deepEqual(
      ignoreLines(repo.dir).filter((line) => line === rule),
      [rule],
      `.gitignore does not carry ${rule} exactly once after the first init`,
    );

    const before = readFileSync(join(repo.dir, '.gitignore'), 'utf8');
    await repo.run(['init', ...flags]);
    assert.equal(readFileSync(join(repo.dir, '.gitignore'), 'utf8'), before, 'a second init changed .gitignore');

    // Compared before and after rather than against empty: the fixture commits nothing, so the files
    // init wrote are untracked entries of their own.
    const porcelain = async () =>
      (await runGit(repo.dir, ['status', '--porcelain', '--untracked-files=all'])).stdout;
    const wired = await porcelain();
    const environment = join(repo.dir, ...rule.split('/'));
    await mkdir(environment, { recursive: true });
    await writeFile(join(environment, 'pyvenv.cfg'), 'home = /usr/bin\n', 'utf8');
    assert.equal(await porcelain(), wired, 'git status reports the environment');
  });
}
