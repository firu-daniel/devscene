/**
 * What `flow-walker.sh` itself does before it hands off to `devscene-flow-walker`, driven against
 * the copy `init` shipped into a throwaway fixture (`cli/templates/scripts/flow-walker.sh` →
 * `# HAND-OFF`).
 *
 * **The rule this suite enforces: the hand-off refuses an unprovisioned checkout with the
 * provisioning remedy and runs nothing; what it executes is chosen by its own directory alone, never
 * by an environment variable (`<state_dir>/lessons.md` → `## Trust checks`); it passes `--flows`
 * only to the walk verbs; and it removes a leftover bash state file so the walk starts fresh.**
 *
 * Not covered here, deliberately: the command's own routing, which the other `flow-walker*` suites
 * and `devscene-flow-host/tests/` cover; and `--no-cache` inside a real sandbox, which no suite can
 * reach.
 *
 * Every fixture repository is built under the system temp directory and torn down in process.
 */

import assert from 'node:assert/strict';
import { accessSync, constants as fsConstants, existsSync, lstatSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import test from 'node:test';

import { flowHostEnvDir } from '../dist/flowHost/layout.js';
import { INIT_SCRIPTS_DIR, runBash } from './helpers/fixture.mjs';
import { plantReview, stateDirOf, walk, walkerFixture, walkerStatePath, walkerUnavailable, WALKER_FLOW } from './helpers/walker.mjs';

const SKIP = walkerUnavailable();
const BRANCH = 'feat_x';

const REFUSAL = /^flow-walker: .*bash .*flow-host-provision\.sh.*outside the sandbox/;

/**
 * The binaries the hand-off needs to reach its provisioning check, linked into the `PATH` that
 * leaves `uv` out — the way `cli/test/doctor-flow-host.test.mjs` → `pathWithoutUv` builds one.
 */
const NEEDED_BINARIES = ['bash', 'git', 'jq', 'dirname', 'rm', 'sed', 'cat', 'tr', 'awk', 'grep', 'head', 'env', 'sh'];

const startArgs = ['start', '--flow', WALKER_FLOW, '--branch', BRANCH, '--skipped', 'none'];
const currentArgs = ['current', '--flow', WALKER_FLOW, '--branch', BRANCH];

async function fixture(t) {
  const fx = await walkerFixture({ parity: false, qa: false, branch: BRANCH });
  t.after(fx.cleanup);
  return fx.dir;
}

async function tempDir(t, prefix) {
  const dir = await mkdtemp(join(tmpdir(), prefix));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}

/** The shipped walker, called with `env` applied over the fixture helpers' isolated environment. */
function walkWith(dir, args, env) {
  return runBash(dir, [join(dir, INIT_SCRIPTS_DIR, 'flow-walker.sh'), ...args], env);
}

function resolveOnPath(name) {
  for (const entry of (process.env.PATH ?? '').split(delimiter)) {
    if (entry === '') continue;
    const candidate = join(entry, name);
    try {
      accessSync(candidate, fsConstants.X_OK);
      return candidate;
    } catch {
      // Not here; keep looking.
    }
  }
  return undefined;
}

async function pathWithoutUv(t) {
  const dir = await tempDir(t, 'harness-nouv-');
  for (const name of NEEDED_BINARIES) {
    const target = resolveOnPath(name);
    assert.ok(target, `${name} does not resolve on PATH, so an environment without uv cannot be built for this test`);
    symlinkSync(target, join(dir, name));
  }
  return dir;
}

function assertRefused(dir, result) {
  assert.equal(result.status, 2, `${result.stdout}\n${result.stderr}`);
  assert.equal(result.stdout, '');
  const lines = result.stderr.split('\n').filter((line) => line !== '');
  assert.equal(lines.length, 1, result.stderr);
  assert.match(lines[0], REFUSAL);
  assert.equal(existsSync(walkerStatePath(dir, BRANCH)), false, 'a refused hand-off wrote walker state');
}

function assertDispatch(result) {
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  assert.deepEqual(result.action[0], ['action', 'dispatch'], result.stdout);
}

/** `<stateDir>/.flow_walker_state`, its parent created when `init` left none. */
async function flatStatePath(dir) {
  const parent = join(dir, stateDirOf(dir));
  await mkdir(parent, { recursive: true });
  return join(parent, '.flow_walker_state');
}

test('an absent environment is refused with the provisioning remedy, and nothing runs', { skip: SKIP }, async (t) => {
  const dir = await fixture(t);
  const config = JSON.parse(readFileSync(join(dir, 'devscene.config.json'), 'utf8'));
  rmSync(join(dir, flowHostEnvDir(config)));

  assertRefused(dir, await walk(dir, startArgs));
});

test('a PATH without uv is refused with the provisioning remedy, and nothing runs', { skip: SKIP }, async (t) => {
  const dir = await fixture(t);
  const path = await pathWithoutUv(t);

  assertRefused(dir, await walkWith(dir, startArgs, { PATH: path }));
});

test('no environment variable chooses what the hand-off runs', { skip: SKIP }, async (t) => {
  const dir = await fixture(t);
  const planted = await tempDir(t, 'harness-planted-pythonpath-');
  await mkdir(join(planted, 'devscene_flow_host'));
  await writeFile(join(planted, 'devscene_flow_host', '__init__.py'), 'raise ImportError("planted PYTHONPATH was imported")\n', 'utf8');
  const empty = await tempDir(t, 'harness-empty-flow-host-');

  const result = await walkWith(dir, startArgs, {
    PYTHONPATH: planted,
    DEVSCENE_FLOW_HOST_ENV: empty,
    DEVSCENE_FLOW_HOST_PROJECT: empty,
    UV_PROJECT_ENVIRONMENT: empty,
    VIRTUAL_ENV: empty,
  });
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  assert.match(result.stdout, /^action: dispatch\n/);
});

test('check-round-file reaches the command without --flows', { skip: SKIP }, async (t) => {
  const dir = await fixture(t);

  const absent = await walk(dir, ['check-round-file', '--findings', join(dir, 'absent.md')]);
  assert.equal(absent.status, 3, absent.stderr);
  assert.equal(absent.stdout, '');
  assert.match(absent.stderr, /^flow-walker: /);

  const valid = await plantReview(dir, `task_plan_reviews/${BRANCH}`, 0, 'PASS');
  const passed = await walk(dir, ['check-round-file', '--findings', valid]);
  assert.equal(passed.status, 0, passed.stderr);
  assert.equal(passed.stdout, '');

  for (const result of [absent, passed]) assert.doesNotMatch(result.stderr, /--flows/);
});

test('a leftover flat state file is removed so the walk starts fresh', { skip: SKIP }, async (t) => {
  const dir = await fixture(t);
  const flat = await flatStatePath(dir);
  writeFileSync(flat, 'step=3\n', 'utf8');

  const current = await walk(dir, currentArgs);
  assert.equal(current.status, 1, current.stderr);
  assert.match(current.stderr, /^flow-walker: no walk in progress at /);
  assert.equal(existsSync(flat), false, 'the flat state file survived `current`');

  assertDispatch(await walk(dir, startArgs));
  assert.ok(lstatSync(flat).isDirectory(), `${flat} is not a directory after \`start\``);
  assert.ok(existsSync(walkerStatePath(dir, BRANCH)), 'start saved no walk state');
});

test('a symbolic link at the flat state path is not removed', { skip: SKIP }, async (t) => {
  const dir = await fixture(t);
  const flat = await flatStatePath(dir);
  const target = join(dir, 'flat-state-target');
  writeFileSync(target, 'step=3\n', 'utf8');
  symlinkSync(target, flat);

  await walk(dir, currentArgs);
  assert.ok(lstatSync(flat).isSymbolicLink(), `${flat} was removed by \`current\``);
  assert.equal(readFileSync(target, 'utf8'), 'step=3\n');
});
