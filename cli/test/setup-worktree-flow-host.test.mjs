/**
 * The shipped `setup-worktree.sh`'s step 6: the flow walker's environment.
 *
 * **The rule these tests exist to enforce: with no argument the bootstrap builds its own checkout's
 * `<scriptsDir>/python/.venv` from its own `<scriptsDir>/python/devscene-flow-host`; with `--target
 * <clone>` it builds `<clone>/<scriptsDir>/python/.venv` from the MAIN checkout's project, never the
 * clone's; a missing `uv`, a missing project and a failed sync each fail the bootstrap with exit 1
 * naming step 6.**
 *
 * The fixture is `cli/test/setup-worktree-clone-target.test.mjs`'s: a hand-built main checkout and
 * the clone `hr_clone_create_var` makes, with `commands.depInstall` and `commands.build` unset. The
 * flow-host project is committed, so the clone carries its own copy and a `--target` run reading it
 * would show the clone's path. `uv` is a stub on `PATH` recording `UV_PROJECT_ENVIRONMENT` and its
 * argv, so no case reaches the network or the shared `uv` cache. The `no uv` case rebuilds the
 * process's `PATH` with every entry holding a `uv` replaced by links to its other executables.
 */

import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { chmod, cp, mkdir, mkdtemp, readdir, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import test from 'node:test';

import { FLOW_HOST_DIRNAME, FLOW_HOST_ENV_DIRNAME, FLOW_HOST_PROJECT } from '../dist/flowHost/layout.js';
import { PACKAGE_ROOT, runBash, runGit } from './helpers/fixture.mjs';

const TEMPLATE_SCRIPTS = join(PACKAGE_ROOT, 'templates', 'scripts');
const LIB = join(TEMPLATE_SCRIPTS, 'lib', 'harness-run-lib.sh');
const SCRIPTS_DIR = 'scripts';
const CONFIG = {
  version: 1,
  defaultBranch: 'trunk',
  protectedBranches: ['trunk'],
  stateDir: 'devscene/',
  scriptsDir: SCRIPTS_DIR,
  githooksDir: 'githooks',
  layers: [],
  commands: {},
};
const BRANCH = 'feat_c';

const output = (result) => `${result.stdout}\n${result.stderr}`;

/** `<root>/<scriptsDir>/python/devscene-flow-host`. */
const projectOf = (root) => join(root, SCRIPTS_DIR, FLOW_HOST_DIRNAME, FLOW_HOST_PROJECT);
/** `<root>/<scriptsDir>/python/.venv`. */
const environmentOf = (root) => join(root, SCRIPTS_DIR, FLOW_HOST_DIRNAME, FLOW_HOST_ENV_DIRNAME);

/** A stub `uv` writing `<UV_PROJECT_ENVIRONMENT>\n<argv>\n` to `UV_STUB_LOG`, then exiting `UV_STUB_EXIT`. */
const STUB_UV = `#!/usr/bin/env bash
printf '%s\\n%s\\n' "\${UV_PROJECT_ENVIRONMENT-}" "$*" > "$UV_STUB_LOG"
exit "\${UV_STUB_EXIT:-0}"
`;

/**
 * A main checkout on `trunk` carrying the configuration, a pre-push hook, the script with its `lib/`
 * and a committed flow-host `pyproject.toml`, and the clone of {@link BRANCH} at `<root>/main-feat_c`.
 *
 * @param {import('node:test').TestContext} t
 */
async function fixture(t) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'setup-flow-host-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const main = join(root, 'main');
  await mkdir(join(main, 'githooks'), { recursive: true });
  await runGit(main, ['init', '--quiet', '-b', 'trunk']);
  await runGit(main, ['config', 'user.email', 'fixture@example.invalid']);
  await runGit(main, ['config', 'user.name', 'Harness Fixture']);
  await writeFile(join(main, 'devscene.config.json'), `${JSON.stringify(CONFIG)}\n`);
  await writeFile(join(main, 'githooks', 'pre-push'), '#!/usr/bin/env bash\nexit 0\n', { mode: 0o755 });
  await mkdir(join(main, SCRIPTS_DIR));
  await cp(join(TEMPLATE_SCRIPTS, 'setup-worktree.sh'), join(main, SCRIPTS_DIR, 'setup-worktree.sh'));
  await cp(join(TEMPLATE_SCRIPTS, 'lib'), join(main, SCRIPTS_DIR, 'lib'), { recursive: true });
  await mkdir(projectOf(main), { recursive: true });
  await writeFile(join(projectOf(main), 'pyproject.toml'), '');
  await runGit(main, ['add', 'devscene.config.json', 'githooks', SCRIPTS_DIR]);
  await runGit(main, ['commit', '--quiet', '-m', 'fixture: seed']);
  await mkdir(join(main, 'devscene', 'autonomous_logs'), { recursive: true });

  const created = await runBash(root, [
    '-c',
    '. "$1" || exit 99; hr_clone_create_var "$2" "$3" trunk || { printf "%s\\n" "$HR_CLONE_REFUSAL" >&2; exit 1; }',
    'hr',
    LIB,
    main,
    BRANCH,
  ]);
  assert.equal(created.status, 0, output(created));

  const bin = join(root, 'bin');
  await mkdir(bin);
  await writeFile(join(bin, 'uv'), STUB_UV);
  await chmod(join(bin, 'uv'), 0o755);
  const log = join(root, 'uv.log');
  const script = join(main, SCRIPTS_DIR, 'setup-worktree.sh');

  return {
    root,
    main,
    clone: join(root, `main-${BRANCH}`),
    log,
    /** Run the bootstrap with the stub `uv` first on `PATH`; `env` is laid over that. */
    setup: (args = [], env = {}) =>
      runBash(root, [script, ...args], {
        PATH: `${bin}${delimiter}${process.env.PATH ?? ''}`,
        UV_STUB_LOG: log,
        ...env,
      }),
    /** The stub's record: `{ environment, argv }`, or `null` when `uv` never ran. */
    uvCall: () => {
      if (!existsSync(log)) return null;
      const [environment, argv] = readFileSync(log, 'utf8').split('\n');
      return { environment, argv };
    },
  };
}

/**
 * The process's `PATH` with every entry holding a `uv` replaced by a directory of links to that
 * entry's other names, so `command -v uv` fails and every other tool still resolves.
 *
 * @param {string} root a directory the test owns.
 */
async function pathWithoutUv(root) {
  const entries = (process.env.PATH ?? '').split(delimiter).filter((entry) => entry !== '');
  const out = [];
  for (const [i, entry] of entries.entries()) {
    if (!existsSync(join(entry, 'uv'))) {
      out.push(entry);
      continue;
    }
    const shadow = join(root, `no-uv-${i}`);
    await mkdir(shadow);
    for (const name of await readdir(entry)) {
      if (name !== 'uv') await symlink(join(entry, name), join(shadow, name));
    }
    out.push(shadow);
  }
  return out.join(delimiter);
}

test('(a) With no argument, the checkout’s own project is synced into its own environment', async (t) => {
  const f = await fixture(t);
  const result = await f.setup();
  assert.equal(result.status, 0, output(result));
  assert.deepEqual(f.uvCall(), {
    environment: environmentOf(f.main),
    argv: `sync --frozen --no-dev --no-editable --project ${projectOf(f.main)}`,
  });
  assert.ok(result.stdout.includes(`flow-host: provisioned ${environmentOf(f.main)}\n`), output(result));
});

test('(b) With --target <clone>, the main checkout’s project is synced into the clone’s environment', async (t) => {
  const f = await fixture(t);
  assert.ok(existsSync(join(projectOf(f.clone), 'pyproject.toml')), 'the clone carries no flow host of its own');
  const result = await f.setup(['--target', f.clone]);
  assert.equal(result.status, 0, output(result));
  assert.deepEqual(f.uvCall(), {
    environment: environmentOf(f.clone),
    argv: `sync --frozen --no-dev --no-editable --project ${projectOf(f.main)}`,
  });
});

test('(c) No uv on PATH fails the bootstrap with exit 1, naming step 6', async (t) => {
  const f = await fixture(t);
  const result = await f.setup([], { PATH: await pathWithoutUv(f.root) });
  assert.equal(result.status, 1, output(result));
  assert.ok(
    result.stderr.includes(
      `flow-host: provision: failed — uv is not on PATH; install uv, then run bash ${join(f.main, SCRIPTS_DIR)}/flow-host-provision.sh outside the sandbox\n`,
    ),
    output(result),
  );
  assert.ok(result.stderr.includes('setup-worktree.sh: step 6 (flow-host provision) failed\n'), output(result));
  assert.equal(f.uvCall(), null, 'the stub uv ran');
});

test('(d) No flow-host project fails the bootstrap with exit 1, naming step 6, with uv never run', async (t) => {
  const f = await fixture(t);
  await rm(join(f.main, SCRIPTS_DIR, FLOW_HOST_DIRNAME), { recursive: true, force: true });
  const result = await f.setup();
  assert.equal(result.status, 1, output(result));
  assert.ok(
    result.stderr.includes(
      `flow-host: provision: failed — no flow host at ${projectOf(f.main)}; run npx devscene init --upgrade\n`,
    ),
    output(result),
  );
  assert.ok(result.stderr.includes('setup-worktree.sh: step 6 (flow-host provision) failed\n'), output(result));
  assert.equal(f.uvCall(), null, 'uv ran with no flow host');
});

test('(e) A failed sync fails the bootstrap with exit 1, naming step 6', async (t) => {
  const f = await fixture(t);
  const result = await f.setup([], { UV_STUB_EXIT: '3' });
  assert.equal(result.status, 1, output(result));
  assert.ok(result.stderr.includes('flow-host: provision: failed (exit 3)\n'), output(result));
  assert.ok(result.stderr.includes('setup-worktree.sh: step 6 (flow-host provision) failed\n'), output(result));
});
