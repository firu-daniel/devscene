/**
 * `flow-host-provision.sh` and the library function it calls, `hr_flow_host_provision` in
 * `cli/templates/scripts/lib/harness-run-lib.sh`.
 *
 * **The rule this suite enforces: the script builds exactly one environment, its own checkout's
 * `<scriptsDir>/python/.venv`, from exactly one project, `<scriptsDir>/python/devscene-flow-host`,
 * through one `uv sync --frozen --no-dev --no-editable` call; a missing `uv`, a missing flow host
 * and a failed sync are each a `failed` line and exit 1, and any argument is exit 2.** The library's
 * six `HR_FLOW_HOST_*` names are a declared mirror of `cli/src/flowHost/layout.ts` and of
 * `cli/src/flowHost/provision.ts` → `ENV_MARKER_FILE`, and the expected paths below are built from
 * those modules' compiled exports, so a rename on either side fails here.
 *
 * `uv` is a stub on `PATH` that records its argv and `UV_PROJECT_ENVIRONMENT` — the stub-binary
 * pattern `cli/test/job-layout-root.test.mjs` uses — so no case reaches the network or the shared
 * `uv` cache. The fixture is a throwaway repository under the system temp directory with the script
 * and `lib/` copied in from the template tree; `init` is not run, because the subject is the script,
 * not the writer. The `no uv` case builds a `PATH` holding links to only `bash`, `dirname`, `git`
 * and `jq`, and is skipped where `jq` does not resolve, since the script cannot read its
 * configuration without it.
 */

import assert from 'node:assert/strict';
import { chmod, cp, mkdir, mkdtemp, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import test from 'node:test';

import {
  FLOW_HOST_DIRNAME,
  FLOW_HOST_ENV_DIRNAME,
  FLOW_HOST_PACKAGES,
  FLOW_HOST_PROJECT,
  FLOW_HOST_SOURCE_DIRNAME,
} from '../dist/flowHost/layout.js';
import { ENV_MARKER_FILE } from '../dist/flowHost/provision.js';
import { PACKAGE_ROOT, runBash, runGit } from './helpers/fixture.mjs';

const TEMPLATE_SCRIPTS = join(PACKAGE_ROOT, 'templates', 'scripts');
const SCRIPT = 'flow-host-provision.sh';
const LIBRARY = 'lib/harness-run-lib.sh';
/** Not the schema default, so a script reading the default instead of the key fails. */
const SCRIPTS_DIR = 'tools/harness';
const ARGS_FILE = 'uv.args';

/** The binaries the script reaches before its `uv` check, by name. */
const NEEDED_BINARIES = ['bash', 'dirname', 'git', 'jq'];

const whichOf = async (name) => {
  const result = await runBash(PACKAGE_ROOT, ['-c', 'command -v "$1"', '_', name]);
  return result.status === 0 ? result.stdout.trim() : undefined;
};
const NO_JQ = (await whichOf('jq')) === undefined ? 'jq does not resolve on this process\'s PATH' : false;

/** A stub `uv` writing `<UV_PROJECT_ENVIRONMENT>\n<argv>\n` to `argsFile`, then exiting `status`. */
const stubUv = (argsFile, status) =>
  `#!/usr/bin/env bash\nprintf '%s\\n%s\\n' "$UV_PROJECT_ENVIRONMENT" "$*" > '${argsFile}'\nexit ${status}\n`;

/**
 * A repository with the script, its library, a flow-host `pyproject.toml` and a stub `uv`; every
 * directory is torn down in `t.after`.
 *
 * @param {import('node:test').TestContext} t
 * @param {{ uvStatus?: number }} [options]
 */
async function fixture(t, { uvStatus = 0 } = {}) {
  const w = await realpath(await mkdtemp(join(tmpdir(), 'flow-host-provision-')));
  t.after(() => rm(w, { recursive: true, force: true }));
  const d = join(w, 'demo');
  const scripts = join(d, ...SCRIPTS_DIR.split('/'));
  const bin = join(w, 'bin');
  await mkdir(join(scripts, 'lib'), { recursive: true });
  await mkdir(bin);
  await runGit(w, ['init', '--quiet', '-b', 'trunk', d]);
  await writeFile(
    join(d, 'devscene.config.json'),
    JSON.stringify({ version: 1, defaultBranch: 'trunk', scriptsDir: SCRIPTS_DIR, layers: [] }),
    'utf8',
  );
  for (const name of [SCRIPT, LIBRARY]) await cp(join(TEMPLATE_SCRIPTS, name), join(scripts, name));
  const project = join(scripts, FLOW_HOST_DIRNAME, FLOW_HOST_PROJECT);
  await mkdir(project, { recursive: true });
  await writeFile(join(project, 'pyproject.toml'), '', 'utf8');
  const argsFile = join(w, ARGS_FILE);
  await writeFile(join(bin, 'uv'), stubUv(argsFile, uvStatus), 'utf8');
  await chmod(join(bin, 'uv'), 0o755);
  return {
    w,
    d,
    scripts,
    project,
    argsFile,
    environment: join(scripts, FLOW_HOST_DIRNAME, FLOW_HOST_ENV_DIRNAME),
    env: { PATH: `${bin}${delimiter}${process.env.PATH ?? ''}` },
    run: (args = [], env) => runBash(w, [join(scripts, SCRIPT), ...args], env),
  };
}

test('a sync runs uv with the exact argv and environment, and prints the provisioned line', { skip: NO_JQ }, async (t) => {
  const f = await fixture(t);
  const result = await f.run([], f.env);
  assert.deepEqual(
    { status: result.status, stdout: result.stdout, stderr: result.stderr },
    { status: 0, stdout: `flow-host: provisioned ${f.environment}\n`, stderr: '' },
  );
  assert.equal(
    readFileSync(f.argsFile, 'utf8'),
    `${f.environment}\nsync --frozen --no-dev --no-editable --project ${f.project}\n`,
  );
});

test('a failed sync prints the failure line and exits 1', { skip: NO_JQ }, async (t) => {
  const f = await fixture(t, { uvStatus: 3 });
  const result = await f.run([], f.env);
  assert.deepEqual(
    { status: result.status, stdout: result.stdout, stderr: result.stderr },
    { status: 1, stdout: '', stderr: 'flow-host: provision: failed (exit 3)\n' },
  );
});

test('no flow host is a failed line and exit 1, with uv never run', { skip: NO_JQ }, async (t) => {
  const f = await fixture(t);
  await rm(join(f.scripts, FLOW_HOST_DIRNAME), { recursive: true, force: true });
  const result = await f.run([], f.env);
  assert.deepEqual(
    { status: result.status, stdout: result.stdout, stderr: result.stderr },
    {
      status: 1,
      stdout: '',
      stderr: `flow-host: provision: failed — no flow host at ${f.project}; run npx devscene init --upgrade\n`,
    },
  );
  assert.equal(existsSync(f.argsFile), false, 'uv ran with no flow host');
});

test('no uv on PATH is a failed line naming this script, and exit 1', { skip: NO_JQ }, async (t) => {
  const f = await fixture(t);
  const bare = join(f.w, 'bare-bin');
  await mkdir(bare);
  for (const name of NEEDED_BINARIES) {
    const target = await whichOf(name);
    assert.ok(target, `${name} does not resolve`);
    await symlink(target, join(bare, name));
  }
  const result = await runBash(f.w, [join(f.scripts, SCRIPT)], { PATH: bare });
  assert.deepEqual(
    { status: result.status, stdout: result.stdout, stderr: result.stderr },
    {
      status: 1,
      stdout: '',
      stderr: `flow-host: provision: failed — uv is not on PATH; install uv, then run bash ${f.scripts}/${SCRIPT} outside the sandbox\n`,
    },
  );
});

test('any argument is usage, exit 2, with uv never run', async (t) => {
  const f = await fixture(t);
  for (const args of [['x'], ['--target', f.d], ['']]) {
    const result = await f.run(args, f.env);
    assert.equal(result.status, 2, `${JSON.stringify(args)}: ${result.stderr}`);
    assert.equal(result.stdout, '');
  }
  assert.equal(existsSync(f.argsFile), false, 'uv ran on a usage error');
});

test('the library sets the six HR_FLOW_HOST_* names as cli/src/flowHost/layout.ts and provision.ts export them', async () => {
  const names = [
    'HR_FLOW_HOST_DIRNAME',
    'HR_FLOW_HOST_PROJECT',
    'HR_FLOW_HOST_GRAPHSCENE',
    'HR_FLOW_HOST_ENV_DIRNAME',
    'HR_FLOW_HOST_SOURCE_DIRNAME',
    'HR_FLOW_HOST_ENV_MARKER',
  ];
  const result = await runBash(PACKAGE_ROOT, [
    '-c',
    '. "$1" || exit 99; shift; for name in "$@"; do printf "%s=%s\\n" "$name" "${!name-<unset>}"; done',
    'hr',
    join(TEMPLATE_SCRIPTS, LIBRARY),
    ...names,
  ]);
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  const sourced = Object.fromEntries(
    result.stdout
      .split('\n')
      .filter((line) => line !== '')
      .map((line) => [line.slice(0, line.indexOf('=')), line.slice(line.indexOf('=') + 1)]),
  );
  const others = FLOW_HOST_PACKAGES.filter((name) => name !== FLOW_HOST_PROJECT);
  assert.equal(others.length, 1, `FLOW_HOST_PACKAGES holds ${JSON.stringify(FLOW_HOST_PACKAGES)}`);
  assert.deepEqual(sourced, {
    HR_FLOW_HOST_DIRNAME: FLOW_HOST_DIRNAME,
    HR_FLOW_HOST_PROJECT: FLOW_HOST_PROJECT,
    HR_FLOW_HOST_GRAPHSCENE: others[0],
    HR_FLOW_HOST_ENV_DIRNAME: FLOW_HOST_ENV_DIRNAME,
    HR_FLOW_HOST_SOURCE_DIRNAME: FLOW_HOST_SOURCE_DIRNAME,
    HR_FLOW_HOST_ENV_MARKER: ENV_MARKER_FILE,
  });
});
