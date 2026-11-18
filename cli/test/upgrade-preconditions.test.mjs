/**
 * The repository refusals of `init --upgrade`: `cli/src/upgrade/preconditions.ts`.
 *
 * **The rule this suite enforces: a refused repository is byte-identical afterwards, and a dry run
 * softens only the two run-registry refusals.** The module runs in this process against throwaway
 * fixtures. The two git probes that do not fail in an ordinary repository are made to fail by a
 * `git` placed first on this process's `PATH`.
 */

import assert from 'node:assert/strict';
import { chmodSync, mkdirSync, writeFileSync } from 'node:fs';
import { delimiter, dirname, join } from 'node:path';
import { test } from 'node:test';

import { HarnessError } from '../dist/core/errors.js';
import { probeRepoRoot } from '../dist/core/git.js';
import { resolveUpgradeTarget } from '../dist/upgrade/preconditions.js';
import { createFixture, runGit, snapshotTree } from './helpers/fixture.mjs';

const CONFIG_FILE = 'devscene.config.json';
const REGISTRY_SEGMENTS = ['autonomous_logs', 'registry.json'];
const STATE_DIR = 'runs';
const DEFAULT_STATE_DIR = 'devscene';

const CONFIG = Object.freeze({
  version: 1,
  defaultBranch: 'main',
  stateDir: STATE_DIR,
  layers: [{ name: 'general', path: '.', conventions: 'conventions.md' }],
  commands: { typecheck: 'echo typecheck', test: 'echo test' },
});

const WITHOUT_STATE_DIR = Object.freeze(
  Object.fromEntries(Object.entries(CONFIG).filter(([key]) => key !== 'stateDir')),
);

const ACTIVE_REGISTRY = JSON.stringify({
  runs: { feat_live: { status: 'running', pid: String(process.pid) }, feat_done: { status: 'completed' } },
});
const MALFORMED_REGISTRY = '{"runs":';

const registryFile = (stateDir) => join(stateDir, ...REGISTRY_SEGMENTS);

async function repository(t, files = { [CONFIG_FILE]: CONFIG }) {
  const fixture = await createFixture({ remote: false, files });
  t.after(fixture.cleanup);
  return fixture.dir;
}

async function plainDirectory(t) {
  const fixture = await createFixture({ git: false });
  t.after(fixture.cleanup);
  return fixture.dir;
}

function resolveIn(cwd, overrides = {}) {
  return resolveUpgradeTarget({ cwd, dryRun: false, assertRepositoryAllowed: () => undefined, ...overrides });
}

/** Asserts `call` refuses with a message matching every pattern and leaves `dir` byte-identical. */
async function assertRefused(dir, call, patterns, snapshotOptions) {
  const before = await snapshotTree(dir, snapshotOptions);
  assert.throws(call, (error) => {
    assert.ok(error instanceof HarnessError, `expected a HarnessError, got ${error}`);
    for (const pattern of patterns) assert.match(error.message, pattern);
    return true;
  });
  assert.deepEqual(await snapshotTree(dir, snapshotOptions), before);
}

/** A linked worktree of a fresh repository, carrying `files`. */
async function linkedWorktree(t, files) {
  const main = await repository(t);
  await runGit(main, ['commit', '--quiet', '--allow-empty', '-m', 'seed']);
  const linked = join(await plainDirectory(t), 'linked');
  await runGit(main, ['worktree', 'add', '--quiet', '-b', 'linked', linked]);
  for (const [name, content] of Object.entries(files)) writeFileSync(join(linked, name), content);
  return { main, linked };
}

/**
 * A repository whose alternates file borrows from a second fixture holding `registryText`, the
 * shape a run copy has. Takes `registryText` as a function of the repository's root, which the
 * registry has to name.
 */
async function borrowingRepository(t, registryText) {
  const copy = await repository(t);
  const main = await repository(t);
  const registryPath = join(main, registryFile(STATE_DIR));
  mkdirSync(dirname(registryPath), { recursive: true });
  writeFileSync(registryPath, registryText(copy));
  const info = join(copy, '.git', 'objects', 'info');
  mkdirSync(info, { recursive: true });
  writeFileSync(join(info, 'alternates'), `${join(main, '.git', 'objects')}\n`);
  return { copy, main };
}

/** Puts first on `PATH` a `git` that fails when any argument is `failingArgument`. */
async function failGitOn(t, failingArgument) {
  const bin = await plainDirectory(t);
  const originalPath = process.env.PATH;
  const shim = join(bin, 'git');
  writeFileSync(
    shim,
    [
      '#!/bin/sh',
      'for argument in "$@"; do',
      `  if [ "$argument" = '${failingArgument}' ]; then exit 1; fi`,
      'done',
      `PATH='${originalPath}'`,
      'export PATH',
      'exec git "$@"',
      '',
    ].join('\n'),
  );
  chmodSync(shim, 0o755);
  process.env.PATH = `${bin}${delimiter}${originalPath}`;
  t.after(() => {
    process.env.PATH = originalPath;
  });
}

test('a directory outside any repository is refused and stays one', async (t) => {
  const dir = await plainDirectory(t);
  let asked = false;
  const assertRepositoryAllowed = () => {
    asked = true;
  };
  await assertRefused(dir, () => resolveIn(dir, { assertRepositoryAllowed }), [/not inside a git repository/], {
    exclude: [],
  });
  assert.equal(asked, false);
  assert.equal(probeRepoRoot(dir).kind, 'not-a-repository');
});

test('a repository with no configuration is told to run init', async (t) => {
  const dir = await repository(t, {});
  await assertRefused(dir, () => resolveIn(dir), [/not found/, /npx devscene init/]);
});

test('a configuration that cannot be used is refused with its problems listed', async (t) => {
  const cases = {
    unparsable: { text: '{"version":', patterns: [/not valid JSON/, /correct devscene\.config\.json/] },
    'missing keys': {
      text: JSON.stringify({ version: 1, stateDir: STATE_DIR }),
      patterns: [/defaultBranch: is required/, /layers: is required/, /commands: is required/],
    },
    'a stateDir that is not a string': {
      text: JSON.stringify({ ...CONFIG, stateDir: 5 }),
      patterns: [/stateDir: /],
    },
    'stateDir absent with no active run': {
      text: JSON.stringify(WITHOUT_STATE_DIR),
      patterns: [/stateDir: is required/],
    },
  };
  for (const [name, { text, patterns }] of Object.entries(cases)) {
    await t.test(name, async (t) => {
      const dir = await repository(t, { [CONFIG_FILE]: text });
      await assertRefused(dir, () => resolveIn(dir), patterns);
      await assertRefused(dir, () => resolveIn(dir, { dryRun: true }), patterns);
    });
  }
});

test('a linked worktree is refused with the main checkout named', async (t) => {
  const cases = {
    configured: { [CONFIG_FILE]: JSON.stringify(CONFIG) },
    unconfigured: {},
  };
  for (const [name, files] of Object.entries(cases)) {
    await t.test(name, async (t) => {
      const { main, linked } = await linkedWorktree(t, files);
      const patterns = [/linked worktree/, new RegExp(`main checkout at ${main}$`)];
      await assertRefused(linked, () => resolveIn(linked), patterns);
      await assertRefused(linked, () => resolveIn(linked, { dryRun: true }), patterns);
    });
  }
});

test('a run copy the borrowed registry records is refused with the main checkout named', async (t) => {
  const { copy, main } = await borrowingRepository(t, (root) =>
    JSON.stringify({ runs: { feat_copy: { worktree: root, copy_kind: 'clone' } } }),
  );
  const patterns = [new RegExp(`${copy} is a run copy`), new RegExp(`main checkout at ${main}$`)];
  await assertRefused(copy, () => resolveIn(copy), patterns);
  await assertRefused(copy, () => resolveIn(copy, { dryRun: true }), patterns);
});

test('a clone the borrowed registry does not record as a run copy is not refused', async (t) => {
  const { copy } = await borrowingRepository(t, (root) =>
    JSON.stringify({
      runs: {
        feat_elsewhere: { worktree: `${root}-elsewhere`, copy_kind: 'clone' },
        feat_not_a_clone: { worktree: root, copy_kind: 'worktree' },
      },
    }),
  );
  const before = await snapshotTree(copy);
  assert.deepEqual(resolveIn(copy).notes, []);
  assert.deepEqual(await snapshotTree(copy), before);
});

test('a borrowed registry that cannot be read refuses, and is a note under a dry run', async (t) => {
  const { copy, main } = await borrowingRepository(t, () => MALFORMED_REGISTRY);
  await assertRefused(copy, () => resolveIn(copy), [new RegExp(join(main, registryFile(STATE_DIR))), /not valid JSON/]);

  const before = await snapshotTree(copy);
  const { notes } = resolveIn(copy, { dryRun: true });
  assert.equal(notes.length, 1);
  assert.match(notes[0], /would refuse: .*not valid JSON/);
  assert.deepEqual(await snapshotTree(copy), before);
});

test('git not answering for the main checkout or the common directory refuses', async (t) => {
  const cases = { '--porcelain': /main checkout/, '--git-common-dir': /common directory/ };
  for (const [argument, pattern] of Object.entries(cases)) {
    await t.test(argument, async (t) => {
      const dir = await repository(t);
      await failGitOn(t, argument);
      await assertRefused(dir, () => resolveIn(dir), [pattern]);
    });
  }
});

test('an active run refuses, naming only the active branch and the remedy', async (t) => {
  const dir = await repository(t, { [CONFIG_FILE]: CONFIG, [registryFile(STATE_DIR)]: ACTIVE_REGISTRY });
  await assertRefused(dir, () => resolveIn(dir), [/runs are active on feat_live \(/, /wait for them to finish or stop them/]);
});

test('an active run is found at the default path when stateDir is absent', async (t) => {
  const dir = await repository(t, {
    [CONFIG_FILE]: WITHOUT_STATE_DIR,
    [registryFile(DEFAULT_STATE_DIR)]: ACTIVE_REGISTRY,
  });
  await assertRefused(dir, () => resolveIn(dir), [/feat_live/, new RegExp(registryFile(DEFAULT_STATE_DIR))]);
});

test('an unreadable registry refuses, naming the path and the detail', async (t) => {
  const dir = await repository(t, { [CONFIG_FILE]: CONFIG, [registryFile(STATE_DIR)]: MALFORMED_REGISTRY });
  await assertRefused(dir, () => resolveIn(dir), [new RegExp(join(dir, registryFile(STATE_DIR))), /not valid JSON/]);
});

test('what the callback throws reaches the caller before the repository is read further', async (t) => {
  const dir = await repository(t, {});
  const refusal = new Error('the harness itself');
  const before = await snapshotTree(dir);
  let received;
  assert.throws(
    () =>
      resolveIn(dir, {
        assertRepositoryAllowed: (root) => {
          received = root;
          throw refusal;
        },
      }),
    (error) => error === refusal,
  );
  assert.equal(received, dir);
  assert.deepEqual(await snapshotTree(dir), before);
});

test('a dry run turns each registry refusal into a note', async (t) => {
  const cases = {
    active: { text: ACTIVE_REGISTRY, pattern: /would refuse: .*feat_live/ },
    unreadable: { text: MALFORMED_REGISTRY, pattern: /would refuse: .*not valid JSON/ },
  };
  for (const [name, { text, pattern }] of Object.entries(cases)) {
    await t.test(name, async (t) => {
      const dir = await repository(t, { [CONFIG_FILE]: CONFIG, [registryFile(STATE_DIR)]: text });
      const before = await snapshotTree(dir);
      const { notes } = resolveIn(dir, { dryRun: true });
      assert.equal(notes.length, 1);
      assert.match(notes[0], pattern);
      assert.deepEqual(await snapshotTree(dir), before);
    });
  }
});

test('a dry run still refuses a configuration with stateDir absent', async (t) => {
  const dir = await repository(t, {
    [CONFIG_FILE]: WITHOUT_STATE_DIR,
    [registryFile(DEFAULT_STATE_DIR)]: ACTIVE_REGISTRY,
  });
  await assertRefused(dir, () => resolveIn(dir, { dryRun: true }), [/stateDir: is required/]);
});

test('an accepted repository resolves from a subdirectory, reading the configured registry', async (t) => {
  // An active registry at the default path is not the configured one, so it must not refuse.
  const dir = await repository(t, {
    [CONFIG_FILE]: CONFIG,
    [registryFile(DEFAULT_STATE_DIR)]: ACTIVE_REGISTRY,
    [registryFile(STATE_DIR)]: JSON.stringify({ runs: { feat_done: { status: 'completed' } } }),
  });
  const cwd = join(dir, 'nested', 'deeper');
  mkdirSync(cwd, { recursive: true });
  const before = await snapshotTree(dir);
  const allowed = [];

  for (const dryRun of [false, true]) {
    const target = resolveIn(cwd, { dryRun, assertRepositoryAllowed: (root) => allowed.push(root) });
    assert.deepEqual(target, { repoRoot: dir, config: { ...CONFIG }, gitCommonDir: join(dir, '.git'), notes: [] });
  }
  assert.deepEqual(allowed, [dir, dir]);
  assert.deepEqual(await snapshotTree(dir), before);
});
