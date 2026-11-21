/**
 * The reader of the local permission additions file.
 *
 * **The rule this suite exists to enforce: the file reaches a profile only as entries added to the
 * four permitted lists, and every other content is refused with the key or entry named.** A device
 * cannot be created at the file's own path without privilege, so the device cases aim the path-level
 * reader at `/dev/null` and `/dev/zero`.
 */

import assert from 'node:assert/strict';
import { mkdirSync, symlinkSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import test from 'node:test';

import { HarnessError } from '../dist/core/errors.js';
import { FORBIDDEN_IN_ENTRY, PROFILE_LOCAL_PATH } from '../dist/generators/profileEntries.js';
import { LOCAL_ADDITION_LISTS, readLocalAdditions, readLocalFileText } from '../dist/generators/profileLocal.js';
import { createFixture, runBash, runGit, snapshotTree } from './helpers/fixture.mjs';

async function repository(t) {
  const fixture = await createFixture({ remote: false });
  t.after(fixture.cleanup);
  return fixture.dir;
}

function localPath(dir) {
  return join(dir, PROFILE_LOCAL_PATH);
}

function writeLocal(dir, content) {
  const path = localPath(dir);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, typeof content === 'string' ? content : JSON.stringify(content));
  return path;
}

/** Assert a refusal that names the file and each of `named`, and that nothing on disk moved. */
async function assertRefused(dir, named) {
  const before = await snapshotTree(dir);
  assert.throws(
    () => readLocalAdditions(dir),
    (error) => {
      assert.ok(error instanceof HarnessError, `expected a HarnessError, got ${error}`);
      for (const text of [PROFILE_LOCAL_PATH, ...named]) {
        assert.ok(error.message.includes(text), `${JSON.stringify(text)} is not in: ${error.message}`);
      }
      return true;
    },
  );
  assert.deepEqual(await snapshotTree(dir), before);
}

test('the permitted lists are exactly the four', () => {
  assert.deepEqual(
    LOCAL_ADDITION_LISTS.map((list) => list.join('.')),
    ['permissions.allow', 'permissions.ask', 'permissions.deny', 'sandbox.filesystem.denyWrite'],
  );
  assert.equal(PROFILE_LOCAL_PATH, '.claude/settings.autonomous.local.json');
});

test('absent shapes read as no additions', async (t) => {
  await t.test('no file and no .claude directory', async (t) => {
    assert.equal(readLocalAdditions(await repository(t)), undefined);
  });

  await t.test('.claude is a file, so the path cannot exist', async (t) => {
    const dir = await repository(t);
    writeFileSync(join(dir, '.claude'), 'not a directory');
    assert.equal(readLocalAdditions(dir), undefined);
  });

  await t.test('a 0-byte regular file', async (t) => {
    const dir = await repository(t);
    writeLocal(dir, '');
    assert.equal(readLocalAdditions(dir), undefined);
  });

  await t.test('a character device that reads empty', () => {
    assert.equal(readLocalFileText('/dev/null'), undefined);
  });
});

test('other file shapes are refused with the path named', async (t) => {
  await t.test('a character device with content', () => {
    assert.throws(() => readLocalFileText('/dev/zero'), (error) => {
      assert.ok(error instanceof HarnessError);
      assert.match(error.message, /\/dev\/zero/);
      return true;
    });
  });

  await t.test('a symlink to a valid file', async (t) => {
    const dir = await repository(t);
    const target = join(dir, 'elsewhere.json');
    writeFileSync(target, JSON.stringify({ permissions: { allow: ['Read'] } }));
    mkdirSync(join(dir, '.claude'));
    symlinkSync(target, localPath(dir));
    await assertRefused(dir, ['symbolic link']);
  });

  await t.test('a dangling symlink', async (t) => {
    const dir = await repository(t);
    mkdirSync(join(dir, '.claude'));
    symlinkSync(join(dir, 'missing.json'), localPath(dir));
    await assertRefused(dir, ['symbolic link']);
  });

  await t.test('a directory', async (t) => {
    const dir = await repository(t);
    mkdirSync(localPath(dir), { recursive: true });
    await assertRefused(dir, ['not a regular file']);
  });

  await t.test('a FIFO, without blocking on it', async (t) => {
    const dir = await repository(t);
    mkdirSync(join(dir, '.claude'));
    const made = await runBash(dir, ['-c', 'mkfifo "$1"', 'mkfifo', localPath(dir)]);
    assert.equal(made.status, 0, made.stderr);
    assert.throws(() => readLocalAdditions(dir), /not a regular file/);
  });
});

test('a valid file yields its lists and counts its entries', async (t) => {
  await t.test('all four lists', async (t) => {
    const dir = await repository(t);
    const content = {
      permissions: {
        allow: ['Bash(make lint)', 'WebFetch(domain:example.com)'],
        ask: ['Bash(make deploy)'],
        deny: ['Read(//srv/secrets/**)'],
      },
      sandbox: { filesystem: { denyWrite: ['/srv/shared'] } },
    };
    writeLocal(dir, content);
    assert.deepEqual(readLocalAdditions(dir), { fragment: content, count: 5 });
  });

  await t.test('duplicates are kept and counted', async (t) => {
    const dir = await repository(t);
    const content = { permissions: { allow: ['Read', 'Read'], deny: ['Read'] } };
    writeLocal(dir, content);
    assert.deepEqual(readLocalAdditions(dir), { fragment: content, count: 3 });
  });

  await t.test('an object with no lists adds nothing', async (t) => {
    const dir = await repository(t);
    writeLocal(dir, {});
    assert.deepEqual(readLocalAdditions(dir), { fragment: {}, count: 0 });
  });

  await t.test('an untracked file in a repository with commits', async (t) => {
    const dir = await repository(t);
    writeFileSync(join(dir, 'README'), 'seed');
    await runGit(dir, ['add', 'README']);
    await runGit(dir, ['commit', '--quiet', '-m', 'seed']);
    writeLocal(dir, { permissions: { allow: ['Read'] } });
    assert.equal(readLocalAdditions(dir)?.count, 1);
  });
});

test('a file tracked at HEAD is refused, whatever it holds', async (t) => {
  const dir = await repository(t);
  writeLocal(dir, { permissions: { allow: ['Read'] } });
  await runGit(dir, ['add', '--', PROFILE_LOCAL_PATH]);
  await runGit(dir, ['commit', '--quiet', '-m', 'track it']);
  await assertRefused(dir, ['tracked at HEAD', 'machine-local', 'remote job must never merge']);

  writeLocal(dir, 'not json');
  await assertRefused(dir, ['tracked at HEAD']);
});

test('content outside the four lists is refused with the key named', async (t) => {
  const cases = [
    ['sandbox.enabled', { sandbox: { enabled: false } }],
    ['permissions.defaultMode', { permissions: { defaultMode: 'bypassPermissions' } }],
    ['_README', { _README: ['a note'] }],
    ['sandbox.filesystem.allowWrite', { sandbox: { filesystem: { allowWrite: ['/'] } } }],
    ['sandbox.network', { sandbox: { network: {} } }],
    ['permissions.allow', { 'permissions.allow': ['Read'] }],
    ['constructor', '{"constructor":{}}'],
    ['__proto__', '{"__proto__":{"allow":["Read"]}}'],
  ];

  for (const [key, content] of cases) {
    await t.test(key, async (t) => {
      const dir = await repository(t);
      writeLocal(dir, content);
      await assertRefused(dir, [`${key} is not allowed`]);
    });
  }
});

test('malformed structure is refused with the key named', async (t) => {
  const cases = [
    ['invalid JSON', '{ nope', ['not valid JSON']],
    ['an array root', [], ['top level']],
    ['a scalar root', '3', ['top level']],
    ['a null root', 'null', ['top level']],
    ['permissions not an object', { permissions: ['Read'] }, ['permissions must be an object']],
    ['sandbox not an object', { sandbox: true }, ['sandbox must be an object']],
    ['filesystem not an object', { sandbox: { filesystem: null } }, ['sandbox.filesystem must be an object']],
    ['allow not a list', { permissions: { allow: 'Read' } }, ['permissions.allow must be a list']],
    ['ask an object', { permissions: { ask: {} } }, ['permissions.ask must be a list']],
    ['deny null', { permissions: { deny: null } }, ['permissions.deny must be a list']],
    ['denyWrite not a list', { sandbox: { filesystem: { denyWrite: '/x' } } }, ['sandbox.filesystem.denyWrite must be a list']],
  ];
  for (const [name, content, named] of cases) {
    await t.test(name, async (t) => {
      const dir = await repository(t);
      writeLocal(dir, content);
      await assertRefused(dir, named);
    });
  }
});

test('an unusable entry is refused with its list position named', async (t) => {
  const withEntry = (entry) => ({ permissions: { allow: ['Read', entry] } });
  const where = 'permissions.allow[1]';

  for (const [name, entry] of [['a number', 7], ['null', null], ['an object', {}], ['an empty string', ''], ['spaces', '   ']]) {
    await t.test(name, async (t) => {
      const dir = await repository(t);
      writeLocal(dir, withEntry(entry));
      await assertRefused(dir, [where]);
    });
  }

  for (const [needle, described] of FORBIDDEN_IN_ENTRY) {
    await t.test(`carrying ${JSON.stringify(needle)}`, async (t) => {
      const dir = await repository(t);
      writeLocal(dir, withEntry(`Bash(a${needle}b)`));
      await assertRefused(dir, [where, described]);
    });
  }

  await t.test('an unsubstituted token', async (t) => {
    const dir = await repository(t);
    writeLocal(dir, withEntry('Read({{repoRoot}}/x)'));
    await assertRefused(dir, [where, '{{repoRoot}}']);
  });

  await t.test('in the sandbox list too', async (t) => {
    const dir = await repository(t);
    writeLocal(dir, { sandbox: { filesystem: { denyWrite: ['/ok', ' '] } } });
    await assertRefused(dir, ['sandbox.filesystem.denyWrite[1]']);
  });
});
