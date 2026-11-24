/**
 * `init`'s offer to build the walker's Python environment, and the `init --upgrade` line naming the
 * rebuild, through the compiled CLI against throwaway fixture repositories.
 *
 * **The rule this suite enforces: only `--provision-python` (or a yes on a terminal) runs
 * `flow-host-provision.sh`, and never under `--dry-run`; a run without it names the command; a failed
 * or skipped build is a warning and `init` still exits 0; and an upgrade that changed a shipped Python file
 * names the rebuild command.** The command and the argv are spelled out here rather than read from
 * `dist/`, so a change to the producer is a change this suite sees.
 *
 * `uv` is a stub first on `PATH` appending its argv to a log, so no case reaches the network or the
 * shared `uv` cache. The `no uv` case instead runs with a `PATH` holding links to only `bash`,
 * `dirname`, `git`, `jq` and the running `node`, and is skipped where `jq` does not resolve; its
 * assertion on the script's own skip wording is what holds `provision.ts` → `SKIPPED_MARKER` equal to
 * it. `runCli` pipes stdin, so no case is a terminal and none is prompted.
 */

import assert from 'node:assert/strict';
import { appendFileSync, existsSync, readFileSync } from 'node:fs';
import { chmod, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import test from 'node:test';

import { createFixture, INIT_SCRIPTS_DIR, PACKAGE_ROOT, runBash, runCli } from './helpers/fixture.mjs';

const CLAUDE_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';
const COMMAND = `bash ${INIT_SCRIPTS_DIR}/flow-host-provision.sh`;

/** A stub `uv` appending its argv as one line to `UV_STUB_LOG`, then exiting `UV_STUB_EXIT`. */
const STUB_UV = `#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$UV_STUB_LOG"
[ "\${UV_STUB_EXIT:-0}" = 0 ] || echo "stub uv: failing on purpose" >&2
exit "\${UV_STUB_EXIT:-0}"
`;

const output = (result) => `${result.stdout}\n${result.stderr}`;

/** The binaries `init` and the script reach before the script's `uv` check; the running `node` is linked beside them. */
const SKIP_BINARIES = ['bash', 'dirname', 'git', 'jq'];

/** `command -v <name>`'s answer, or `undefined`. */
const whichOf = async (name) => {
  const result = await runBash(PACKAGE_ROOT, ['-c', 'command -v "$1"', '_', name]);
  return result.status === 0 ? result.stdout.trim() : undefined;
};
const NO_JQ = (await whichOf('jq')) === undefined ? 'jq does not resolve on this process\'s PATH' : false;

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

test('no uv on PATH is a warning carrying the script\'s SKIPPED line, never a built note', { skip: NO_JQ }, async (t) => {
  const repo = await repository(t);
  const bare = await mkdtemp(join(tmpdir(), 'provision-bare-bin-'));
  t.after(() => rm(bare, { recursive: true, force: true }));
  for (const name of SKIP_BINARIES) {
    const target = await whichOf(name);
    assert.ok(target, `${name} does not resolve`);
    await symlink(target, join(bare, name));
  }
  await symlink(process.execPath, join(bare, 'node'));
  const result = await repo.run(['init', '--provision-python'], { PATH: bare });
  assert.equal(result.status, 0, output(result));
  assert.match(result.stderr, /was not built: flow-host: provision: SKIPPED — uv is not on PATH/);
  assert.doesNotMatch(output(result), /built the Python environment the flow walker runs in at/);
  assert.deepEqual(repo.uvCalls(), []);
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
