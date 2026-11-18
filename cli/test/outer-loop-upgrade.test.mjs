/**
 * The outer-loop script upgrade planner and drift reader, against repositories wired by the compiled
 * CLI.
 *
 * **The rule this suite exists to enforce: `init --upgrade` brings every row of `OUTER_LOOP_SCRIPTS`
 * to its shipped bytes and mode and touches no wrapper, `doctor`'s reader reports exactly the rows
 * that upgrade would change, and a plain `init` still keeps an edited script.**
 *
 * Expected bytes come from the shipped template because "copied verbatim" is the contract, as
 * `outer-loop-scripts.test.mjs` argues in its header.
 */

import assert from 'node:assert/strict';
import { appendFileSync, chmodSync, readFileSync, rmSync, statSync, symlinkSync } from 'node:fs';
import { basename, join } from 'node:path';
import { test } from 'node:test';

import { requireConfig } from '../dist/config/io.js';
import { readTemplate } from '../dist/core/paths.js';
import { Reporter } from '../dist/core/report.js';
import { WritePlan } from '../dist/core/writer.js';
import {
  OUTER_LOOP_SCRIPTS,
  RESTART_WATCHER_SCRIPT_NAME,
  WATCHER_SCRIPT_NAME,
  outerLoopRelativePath,
  outerLoopScriptDrift,
  outerLoopScriptPath,
  planOuterLoopScriptUpgrade,
  writeOuterLoopScripts,
} from '../dist/generators/outerLoopScripts.js';
import { WRAPPER_SCRIPTS } from '../dist/generators/scripts.js';
import { createFixture, runCli, snapshotTree } from './helpers/fixture.mjs';

const EDIT = '\n# This line was added by hand.\n';
const PERMISSION_BITS = 0o777;

const rowNamed = (file) => {
  const row = OUTER_LOOP_SCRIPTS.find((script) => script.file === file);
  assert.ok(row, `${file} has no row`);
  return row;
};
const WATCHER = outerLoopRelativePath(rowNamed(WATCHER_SCRIPT_NAME));
const RESTART = outerLoopRelativePath(rowNamed(RESTART_WATCHER_SCRIPT_NAME));
const LIB_ROW = OUTER_LOOP_SCRIPTS.find((script) => script.subdir === 'lib');
const LIB = outerLoopRelativePath(LIB_ROW);

/** A repository wired by the compiled `init`. */
async function adopted(t) {
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
  await initOk(dir);
  const config = requireConfig(dir);
  return { dir, config, pathOf: (relative) => outerLoopScriptPath(dir, config, relative) };
}

async function initOk(dir) {
  const result = await runCli(dir, ['init']);
  assert.equal(result.status, 0, `init exited ${result.status}\n${result.stdout}\n${result.stderr}`);
  return result;
}

const fileRequests = (plan) => plan.requests.filter((request) => request.policy !== 'ensure-dir');
const modeOf = (path) => statSync(path).mode & PERMISSION_BITS;
const shipped = (relative) => readFileSync(templatePath(relative));
const templatePath = (relative) => join(import.meta.dirname, '..', 'templates', 'scripts', ...relative.split('/'));

test('the restart script has one spelling, and its row is built from it', () => {
  assert.equal(RESTART_WATCHER_SCRIPT_NAME, 'restart-watcher.sh');
  assert.equal(RESTART, RESTART_WATCHER_SCRIPT_NAME);
  assert.equal(rowNamed(RESTART_WATCHER_SCRIPT_NAME).mode, 0o755);
});

test('the planner enqueues every table row under replace-if-changed and no wrapper', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  const before = await snapshotTree(dir);
  const plan = new WritePlan();

  const result = planOuterLoopScriptUpgrade({ repoRoot: dir, config, plan });

  const requests = fileRequests(plan);
  assert.deepEqual(
    requests.map((request) => request.path),
    OUTER_LOOP_SCRIPTS.map((script) => pathOf(outerLoopRelativePath(script))),
  );
  OUTER_LOOP_SCRIPTS.forEach((script, index) => {
    const relative = outerLoopRelativePath(script);
    const request = requests[index];
    assert.equal(request.policy, 'replace-if-changed', relative);
    assert.equal(request.mode, script.mode, relative);
    assert.equal(request.content, readTemplate(`scripts/${relative}`), relative);
  });

  assert.ok(WRAPPER_SCRIPTS.length > 0);
  const targets = new Set(requests.map((request) => basename(request.path)));
  for (const wrapper of WRAPPER_SCRIPTS) assert.equal(targets.has(wrapper.file), false, wrapper.file);

  assert.deepEqual(result.written.map(outerLoopRelativePath), OUTER_LOOP_SCRIPTS.map(outerLoopRelativePath));
  assert.deepEqual(result.notes, []);
  assert.deepEqual(await snapshotTree(dir), before, 'planning changed the tree');
});

test('the planner ensures the same directories as the plain writer', async (t) => {
  const { dir, config } = await adopted(t);
  const directories = (plan) => plan.requests.filter((request) => request.policy === 'ensure-dir');
  const upgrade = new WritePlan();
  const plain = new WritePlan();

  planOuterLoopScriptUpgrade({ repoRoot: dir, config, plan: upgrade });
  const written = writeOuterLoopScripts({ repoRoot: dir, config, plan: plain });

  assert.ok(directories(upgrade).length > 1);
  assert.deepEqual(directories(upgrade), directories(plain));
  assert.ok(fileRequests(plain).every((request) => request.policy === 'create-if-absent'));
  assert.equal(written.notes.length, 1, 'the plain writer lost its note');
});

test('an applied upgrade restores every kind of drift, and leaves a wrapper alone', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  const backups = await createFixture({ git: false });
  t.after(backups.cleanup);
  const wrapper = pathOf(WRAPPER_SCRIPTS[0].file);
  const editedWrapper = `${readFileSync(wrapper, 'utf8')}${EDIT}`;
  appendFileSync(wrapper, EDIT);
  appendFileSync(pathOf(LIB), EDIT);
  const editedLib = readFileSync(pathOf(LIB));
  chmodSync(pathOf(WATCHER), 0o644);
  rmSync(pathOf(RESTART));

  const apply = () => {
    const plan = new WritePlan();
    planOuterLoopScriptUpgrade({ repoRoot: dir, config, plan });
    return plan.apply({
      repoRoot: dir,
      report: new Reporter({ quiet: true }),
      dryRun: false,
      force: false,
      backupDir: backups.dir,
    });
  };
  const results = apply();

  const resultFor = (relative) => results.find((result) => result.path === pathOf(relative));
  assert.equal(resultFor(RESTART).effect, 'created');
  assert.equal(resultFor(LIB).effect, 'backed-up-and-replaced');
  assert.deepEqual(readFileSync(resultFor(LIB).backupPath), editedLib);
  assert.equal(resultFor(WATCHER).effect, 'backed-up-and-replaced');
  assert.equal(resultFor(WATCHER).backupPath, undefined);

  for (const script of OUTER_LOOP_SCRIPTS) {
    const relative = outerLoopRelativePath(script);
    assert.deepEqual(readFileSync(pathOf(relative)), shipped(relative), relative);
    assert.equal(modeOf(pathOf(relative)), script.mode, relative);
  }
  assert.equal(readFileSync(wrapper, 'utf8'), editedWrapper, 'the upgrade rewrote a wrapper');
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [] });

  const second = apply().filter((result) => result.policy === 'replace-if-changed');
  assert.ok(second.every((result) => result.effect === 'kept'), 'a second upgrade changed a current script');
});

test('the drift reader reports nothing on a fresh repository, and writes nothing', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [] });

  appendFileSync(pathOf(LIB), EDIT);
  rmSync(pathOf(WATCHER));
  const before = await snapshotTree(dir);
  outerLoopScriptDrift(dir, config);
  assert.deepEqual(await snapshotTree(dir), before, 'the drift reader changed the tree');
});

test('the drift reader reports a deleted row as missing', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  rmSync(pathOf(WATCHER));
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [WATCHER], changed: [] });
});

test('the drift reader reports an edited row, and a row in lib/, as changed', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  appendFileSync(pathOf(WATCHER), EDIT);
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [WATCHER] });

  appendFileSync(pathOf(LIB), EDIT);
  assert.ok(LIB.startsWith('lib/'));
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [LIB, WATCHER] });
});

test('the drift reader compares the executable bit in both directions, and no other mode bit', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  assert.equal(LIB_ROW.mode & 0o100, 0);
  assert.equal(rowNamed(WATCHER_SCRIPT_NAME).mode & 0o100, 0o100);

  chmodSync(pathOf(WATCHER), 0o644);
  chmodSync(pathOf(LIB), 0o755);
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [LIB, WATCHER] });

  chmodSync(pathOf(WATCHER), 0o700);
  chmodSync(pathOf(LIB), 0o600);
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [] });
});

test('the drift reader reports a symlink as changed even when it resolves to the shipped bytes', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  rmSync(pathOf(WATCHER));
  symlinkSync(templatePath(WATCHER), pathOf(WATCHER));
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [WATCHER] });
});

test('the drift reader does not report an edited wrapper', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  appendFileSync(pathOf(WRAPPER_SCRIPTS[0].file), EDIT);
  assert.deepEqual(outerLoopScriptDrift(dir, config), { missing: [], changed: [] });
});

test('the planner and the drift reader follow a configured scriptsDir', async (t) => {
  const { dir, config } = await adopted(t);
  const relocated = { ...config, scriptsDir: 'tools/loop/' };
  const plan = new WritePlan();

  const result = planOuterLoopScriptUpgrade({ repoRoot: dir, config: relocated, plan });

  assert.equal(result.scriptsDir, 'tools/loop');
  assert.equal(fileRequests(plan)[0].path, join(dir, 'tools', 'loop', ...LIB.split('/')));
  assert.deepEqual(outerLoopScriptDrift(dir, relocated), {
    missing: OUTER_LOOP_SCRIPTS.map(outerLoopRelativePath),
    changed: [],
  });
});

test('a plain init over an edited script keeps it and reports it as kept', async (t) => {
  const { dir, config, pathOf } = await adopted(t);
  appendFileSync(pathOf(WATCHER), EDIT);
  const edited = readFileSync(pathOf(WATCHER));

  const { stdout } = await initOk(dir);

  const repoPath = `${config.scriptsDir}/${WATCHER}`;
  const line = stdout.split('\n').find((candidate) => candidate.endsWith(` ${repoPath}`));
  assert.match(line ?? '', /^= kept\s/, `no kept line for ${repoPath}\n${stdout}`);
  assert.deepEqual(readFileSync(pathOf(WATCHER)), edited);
});
