/**
 * `init`'s offer to build the walker's Python environment, and the `init --upgrade` line naming the
 * rebuild, through the compiled CLI against throwaway fixture repositories.
 *
 * **The rule this suite enforces: only `--provision-python` (or a yes on a terminal) runs
 * `flow-host-provision.sh`, and never under `--dry-run`; a run without it names the command; a failed
 * build is a warning and `init` still exits 0; and an upgrade that changed a shipped Python file
 * names the rebuild command.** The command and the argv are spelled out here rather than read from
 * `dist/`, so a change to the producer is a change this suite sees.
 *
 * `uv` is a stub first on `PATH` appending its argv to a log, so no case reaches the network or the
 * shared `uv` cache. `runCli` pipes stdin, so no case is a terminal and none is prompted.
 */

import assert from 'node:assert/strict';
import { appendFileSync, existsSync, readFileSync } from 'node:fs';
import { chmod, writeFile } from 'node:fs/promises';
import { delimiter, join } from 'node:path';
import test from 'node:test';

import { createFixture, INIT_SCRIPTS_DIR, runCli } from './helpers/fixture.mjs';

const CLAUDE_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';
const COMMAND = `bash ${INIT_SCRIPTS_DIR}/flow-host-provision.sh`;

/** A stub `uv` appending its argv as one line to `UV_STUB_LOG`, then exiting `UV_STUB_EXIT`. */
const STUB_UV = `#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$UV_STUB_LOG"
[ "\${UV_STUB_EXIT:-0}" = 0 ] || echo "stub uv: failing on purpose" >&2
exit "\${UV_STUB_EXIT:-0}"
`;

const output = (result) => `${result.stdout}\n${result.stderr}`;

/** A fixture whose detection resolves every command, with its own agent-runner home and a stub `uv`. */
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
  await writeFile(join(home.dir, 'uv'), STUB_UV);
  await chmod(join(home.dir, 'uv'), 0o755);
  const log = join(home.dir, 'uv.log');
  const run = (args, env = {}) =>
    runCli(dir, args, {
      [CLAUDE_HOME_VARIABLE]: home.dir,
      PATH: `${home.dir}${delimiter}${process.env.PATH ?? ''}`,
      UV_STUB_LOG: log,
      ...env,
    });
  /** Every recorded `uv` argv, one per call. */
  const uvCalls = () => (existsSync(log) ? readFileSync(log, 'utf8').split('\n').filter((line) => line !== '') : []);
  return { dir, run, uvCalls };
}

test('--provision-python runs the stub uv once with the provisioning argv, and init exits 0', async (t) => {
  const repo = await repository(t);
  const result = await repo.run(['init', '--provision-python']);
  assert.equal(result.status, 0, output(result));
  const project = join(repo.dir, INIT_SCRIPTS_DIR, 'python', 'devscene-flow-host');
  assert.deepEqual(repo.uvCalls(), [`sync --frozen --no-dev --no-editable --project ${project}`]);
});

test('without the flag and with stdin piped, uv never runs and the note names the command', async (t) => {
  const repo = await repository(t);
  const result = await repo.run(['init']);
  assert.equal(result.status, 0, output(result));
  assert.deepEqual(repo.uvCalls(), []);
  assert.match(output(result), new RegExp(`is not built: run ${COMMAND} outside the sandbox`));
});

test('--dry-run --provision-python runs nothing', async (t) => {
  const repo = await repository(t);
  const result = await repo.run(['init', '--dry-run', '--provision-python']);
  assert.equal(result.status, 0, output(result));
  assert.deepEqual(repo.uvCalls(), []);
  assert.match(output(result), new RegExp(`would build .* by running ${COMMAND}`));
});

test('a failing uv leaves init exiting 0 with a warning naming the command', async (t) => {
  const repo = await repository(t);
  const result = await repo.run(['init', '--provision-python'], { UV_STUB_EXIT: '1' });
  assert.equal(result.status, 0, output(result));
  assert.equal(repo.uvCalls().length, 1);
  assert.match(result.stderr, new RegExp(`was not built: ${COMMAND} ended with exit status 1: .*run ${COMMAND} outside the sandbox`));
});

test('--upgrade refuses --provision-python and writes nothing', async (t) => {
  const repo = await repository(t);
  const result = await repo.run(['init', '--upgrade', '--provision-python']);
  assert.notEqual(result.status, 0, output(result));
  assert.match(result.stderr, /--upgrade cannot be combined with --provision-python/);
  assert.equal(existsSync(join(repo.dir, 'devscene.config.json')), false);
});

test('init --upgrade after an edit under <scriptsDir>/python/ names the rebuild command', async (t) => {
  const repo = await repository(t);
  const wired = await repo.run(['init']);
  assert.equal(wired.status, 0, output(wired));
  appendFileSync(join(repo.dir, INIT_SCRIPTS_DIR, 'python', 'devscene-flow-host', 'pyproject.toml'), '# edited\n');

  const upgraded = await repo.run(['init', '--upgrade']);
  assert.equal(upgraded.status, 0, output(upgraded));
  assert.match(output(upgraded), new RegExp(`rebuild it with uv by running ${COMMAND} outside the sandbox`));

  const current = await repo.run(['init', '--upgrade']);
  assert.doesNotMatch(output(current), /rebuild it with uv/);
  assert.deepEqual(repo.uvCalls(), []);
});
