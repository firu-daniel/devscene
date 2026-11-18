/**
 * The `replace-if-changed` write policy and the git common-directory probe.
 *
 * **The rule this suite exists to enforce: a `replace-if-changed` target is either left alone or
 * swapped whole, and changed bytes are recoverable from the backup directory.** Every refusal is
 * asserted on the tree, not on the message alone.
 */

import assert from 'node:assert/strict';
import {
  closeSync,
  existsSync,
  fstatSync,
  lstatSync,
  mkdirSync,
  openSync,
  readdirSync,
  readFileSync,
  readlinkSync,
  readSync,
  statSync,
  symlinkSync,
  chmodSync,
  writeFileSync,
} from 'node:fs';
import { mkdtemp, realpath, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import test from 'node:test';

import { gitCommonDir } from '../dist/core/git.js';
import { Reporter } from '../dist/core/report.js';
import { WritePlan } from '../dist/core/writer.js';
import { createFixture, runGit, snapshotTree } from './helpers/fixture.mjs';

/** A repository directory and a backup directory beside it, which starts absent. */
async function workspace(t) {
  const fixture = await createFixture({ git: false, dirs: ['repo'] });
  t.after(fixture.cleanup);
  return { base: fixture.dir, repoRoot: join(fixture.dir, 'repo'), backupDir: join(fixture.dir, 'backups') };
}

/** Write a file below `root`, creating its parents, and optionally set its mode. */
function seed(root, relativePath, content, mode) {
  const path = join(root, relativePath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, content);
  if (mode !== undefined) chmodSync(path, mode);
  return path;
}

function modeOf(path) {
  return statSync(path).mode & 0o777;
}

function replaceRequest(path, content, extra = {}) {
  return { path, policy: 'replace-if-changed', content, label: 'target', ...extra };
}

/** Apply `requests` as one plan and return the results with the captured output lines. */
function apply(space, requests, options = {}) {
  const lines = [];
  const report = new Reporter({ out: (line) => lines.push(line), err: (line) => lines.push(line) });
  const plan = new WritePlan();
  for (const request of requests) plan.add(request);
  const results = plan.apply({
    repoRoot: space.repoRoot,
    report,
    dryRun: false,
    force: false,
    backupDir: space.backupDir,
    ...options,
  });
  return { results, lines };
}

/** Names in `directory` that are neither the target nor expected: the leftover temporary files. */
function temporaryFiles(directory) {
  return readdirSync(directory).filter((name) => name.endsWith('.tmp'));
}

test('an absent target is created, with its parents and the default mode', async (t) => {
  const space = await workspace(t);
  const path = join(space.repoRoot, 'nested/dir/file.txt');

  const { results } = apply(space, [replaceRequest(path, 'new\n')]);

  assert.equal(results[0].effect, 'created');
  assert.equal(results[0].outcome, 'created');
  assert.equal(results[0].backupPath, undefined);
  assert.equal(readFileSync(path, 'utf8'), 'new\n');
  assert.equal(modeOf(path), 0o644);
  assert.equal(existsSync(space.backupDir), false);
});

test('a created target takes the mode its request names', async (t) => {
  const space = await workspace(t);
  const path = join(space.repoRoot, 'run.sh');

  apply(space, [replaceRequest(path, '#!/bin/sh\n', { mode: 0o755 })]);

  assert.equal(modeOf(path), 0o755);
});

test('matching bytes and mode are kept, with no backup directory', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'file.txt', 'same\n', 0o640);
  const before = lstatSync(path);

  const { results } = apply(space, [replaceRequest(path, 'same\n', { mode: 0o640 })]);

  assert.equal(results[0].effect, 'kept');
  assert.equal(lstatSync(path).ino, before.ino);
  assert.equal(existsSync(space.backupDir), false);
});

test('--force is not consulted: a current file stays kept', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'file.txt', 'same\n');

  const { results } = apply(space, [replaceRequest(path, 'same\n')], { force: true });

  assert.equal(results[0].effect, 'kept');
  assert.equal(existsSync(`${path}.bak`), false);
  assert.equal(existsSync(space.backupDir), false);
});

test('changed bytes are backed up at the repo-relative path and then replaced', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'nested/file.txt', 'old\n');
  const expectedBackup = join(space.backupDir, 'nested/file.txt');

  const { results, lines } = apply(space, [replaceRequest(path, 'new\n')]);

  assert.equal(results[0].effect, 'backed-up-and-replaced');
  assert.equal(results[0].backupPath, expectedBackup);
  assert.equal(readFileSync(path, 'utf8'), 'new\n');
  assert.equal(readFileSync(expectedBackup, 'utf8'), 'old\n');
  assert.equal(existsSync(`${path}.bak`), false);
  assert.equal(modeOf(space.backupDir), 0o700);
  assert.equal(modeOf(dirname(expectedBackup)), 0o700);
  assert.ok(lines.some((line) => line.includes(expectedBackup)));
});

test('bytes that are not valid UTF-8 are compared as bytes and backed up intact', async (t) => {
  const space = await workspace(t);
  const original = Buffer.from([0xff, 0x0a]);
  const path = seed(space.repoRoot, 'binary', original);

  // U+FFFD followed by a newline is what decoding `original` as UTF-8 yields.
  const { results } = apply(space, [replaceRequest(path, '�\n')]);

  assert.equal(results[0].effect, 'backed-up-and-replaced');
  assert.deepEqual(readFileSync(results[0].backupPath), original);
});

test('a second apply of the same plan reports only kept and creates no backup directory', async (t) => {
  const space = await workspace(t);
  const changed = seed(space.repoRoot, 'changed.txt', 'old\n');
  const absent = join(space.repoRoot, 'absent.txt');
  const requests = [replaceRequest(changed, 'new\n'), replaceRequest(absent, 'made\n', { mode: 0o755 })];
  apply(space, requests);

  const secondBackupDir = join(space.base, 'second-backups');
  const { results } = apply({ ...space, backupDir: secondBackupDir }, requests);

  assert.deepEqual(results.map((result) => result.effect), ['kept', 'kept']);
  assert.equal(existsSync(secondBackupDir), false);
});

test('a mode-only difference replaces the file with no backup', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'run.sh', 'body\n', 0o644);
  const before = lstatSync(path);

  const { results } = apply(space, [replaceRequest(path, 'body\n', { mode: 0o755 })], { backupDir: undefined });

  assert.equal(results[0].effect, 'backed-up-and-replaced');
  assert.equal(results[0].backupPath, undefined);
  assert.equal(modeOf(path), 0o755);
  assert.equal(readFileSync(path, 'utf8'), 'body\n');
  assert.notEqual(lstatSync(path).ino, before.ino);
  assert.equal(existsSync(space.backupDir), false);
});

test('a replacement keeps the existing mode when the request names none', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'run.sh', 'old\n', 0o750);

  const { results } = apply(space, [replaceRequest(path, 'new\n')]);

  assert.equal(modeOf(path), 0o750);
  assert.equal(modeOf(results[0].backupPath), 0o750);
});

test('--dry-run leaves the tree and the backup directory byte-identical', async (t) => {
  const space = await workspace(t);
  const changed = seed(space.repoRoot, 'changed.txt', 'old\n', 0o640);
  const modeOnly = seed(space.repoRoot, 'mode.sh', 'body\n', 0o644);
  const absent = join(space.repoRoot, 'sub/absent.txt');
  const before = await snapshotTree(space.base);

  const { results, lines } = apply(
    space,
    [
      replaceRequest(changed, 'new\n'),
      replaceRequest(modeOnly, 'body\n', { mode: 0o755 }),
      replaceRequest(absent, 'made\n'),
    ],
    { dryRun: true },
  );

  assert.deepEqual(await snapshotTree(space.base), before);
  assert.equal(modeOf(changed), 0o640);
  assert.equal(modeOf(modeOnly), 0o644);
  assert.equal(existsSync(space.backupDir), false);
  assert.deepEqual(results.map((result) => result.outcome), ['skipped', 'skipped', 'skipped']);
  assert.deepEqual(
    results.map((result) => result.effect),
    ['backed-up-and-replaced', 'backed-up-and-replaced', 'created'],
  );
  assert.equal(results[0].backupPath, join(space.backupDir, 'changed.txt'));
  assert.ok(lines.length > 0);
});

test('a symlink at the target is refused and left in place', async (t) => {
  const space = await workspace(t);
  const outside = seed(space.base, 'outside.txt', 'outside\n');
  const path = join(space.repoRoot, 'link.txt');
  symlinkSync(outside, path);

  assert.throws(() => apply(space, [replaceRequest(path, 'new\n')]), /symlink/);

  assert.equal(readlinkSync(path), outside);
  assert.equal(readFileSync(outside, 'utf8'), 'outside\n');
  assert.equal(existsSync(space.backupDir), false);
});

test('a symlink on the backup path refuses the whole plan before anything is written', async (t) => {
  const space = await workspace(t);
  const first = seed(space.repoRoot, 'first.txt', 'old\n');
  const second = seed(space.repoRoot, 'nested/second.txt', 'old\n');
  const elsewhere = join(space.base, 'elsewhere');
  mkdirSync(elsewhere);
  mkdirSync(space.backupDir);
  symlinkSync(elsewhere, join(space.backupDir, 'nested'));

  assert.throws(
    () => apply(space, [replaceRequest(first, 'new\n'), replaceRequest(second, 'new\n')]),
    /symlink/,
  );

  assert.equal(readFileSync(first, 'utf8'), 'old\n');
  assert.equal(readFileSync(second, 'utf8'), 'old\n');
  assert.deepEqual(readdirSync(elsewhere), []);
  assert.deepEqual(readdirSync(space.backupDir), ['nested']);
});

test('a symlink at the backup file itself, or the backup directory, is refused', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'file.txt', 'old\n');
  const elsewhere = join(space.base, 'elsewhere');
  mkdirSync(elsewhere);
  mkdirSync(space.backupDir);
  symlinkSync(join(elsewhere, 'landing'), join(space.backupDir, 'file.txt'));
  const linkedRoot = join(space.base, 'linked-backups');
  symlinkSync(elsewhere, linkedRoot);

  assert.throws(() => apply(space, [replaceRequest(path, 'new\n')]), /symlink/);
  assert.throws(() => apply({ ...space, backupDir: linkedRoot }, [replaceRequest(path, 'new\n')]), /symlink/);

  assert.equal(readFileSync(path, 'utf8'), 'old\n');
  assert.deepEqual(readdirSync(elsewhere), []);
});

test('an existing backup file is refused rather than overwritten', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'file.txt', 'old\n');
  const backup = seed(space.backupDir, 'file.txt', 'earlier\n');

  assert.throws(() => apply(space, [replaceRequest(path, 'new\n')]), /already exists/);

  assert.equal(readFileSync(path, 'utf8'), 'old\n');
  assert.equal(readFileSync(backup, 'utf8'), 'earlier\n');
});

test('a backup owed with no backup directory is an internal fault', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'file.txt', 'old\n');

  assert.throws(() => apply(space, [replaceRequest(path, 'new\n')], { backupDir: undefined }), /backupDir/);

  assert.equal(readFileSync(path, 'utf8'), 'old\n');
});

test('a target outside the repository is refused even with allowOutsideRepo', async (t) => {
  const space = await workspace(t);
  const path = seed(space.base, 'outside.txt', 'old\n');

  assert.throws(() => apply(space, [replaceRequest(path, 'new\n', { allowOutsideRepo: true })]), /outside/);

  assert.equal(readFileSync(path, 'utf8'), 'old\n');
  assert.equal(existsSync(space.backupDir), false);
});

test('no temporary file survives a successful replacement', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'file.txt', 'old\n');

  apply(space, [replaceRequest(path, 'new\n')]);

  assert.deepEqual(readdirSync(space.repoRoot), ['file.txt']);
});

test('a failure during the commit removes the temporary file and keeps the target', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'file.txt', 'old\n');
  // Absent while the plan is checked, then a regular file by the time the backup is written.
  const blocker = {
    path: space.backupDir,
    policy: 'create-if-absent',
    content: 'in the way\n',
    label: 'blocker',
    allowOutsideRepo: true,
  };

  assert.throws(() => apply(space, [blocker, replaceRequest(path, 'new\n')]), /not a directory/);

  assert.equal(readFileSync(path, 'utf8'), 'old\n');
  assert.deepEqual(temporaryFiles(space.repoRoot), []);
  assert.deepEqual(readdirSync(space.repoRoot), ['file.txt']);
});

test('a reader holding the old file open keeps its inode and its bytes', async (t) => {
  const space = await workspace(t);
  const path = seed(space.repoRoot, 'running.sh', 'old contents\n');
  const descriptor = openSync(path, 'r');
  t.after(() => closeSync(descriptor));
  const openInode = fstatSync(descriptor).ino;

  apply(space, [replaceRequest(path, 'new contents\n')]);

  assert.equal(fstatSync(descriptor).ino, openInode);
  assert.notEqual(lstatSync(path).ino, openInode);
  const buffer = Buffer.alloc(64);
  const length = readSync(descriptor, buffer, 0, buffer.length, 0);
  assert.equal(buffer.subarray(0, length).toString('utf8'), 'old contents\n');
  assert.equal(readFileSync(path, 'utf8'), 'new contents\n');
});

test('gitCommonDir answers from a main checkout and from a linked worktree', async (t) => {
  const fixture = await createFixture();
  t.after(fixture.cleanup);
  const parent = await realpath(await mkdtemp(join(tmpdir(), 'write-plan-worktree-')));
  t.after(() => rm(parent, { recursive: true, force: true }));
  const worktree = join(parent, 'linked');
  await runGit(fixture.dir, ['worktree', 'add', '-b', 'linked-branch', worktree]);

  const expected = join(fixture.dir, '.git');
  assert.equal(gitCommonDir(fixture.dir), expected);
  assert.equal(gitCommonDir(worktree), expected);
});

test('gitCommonDir is undefined where git does not answer', async (t) => {
  const fixture = await createFixture({ git: false });
  t.after(fixture.cleanup);

  assert.equal(gitCommonDir(fixture.dir), undefined);
});
