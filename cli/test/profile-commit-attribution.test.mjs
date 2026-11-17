/**
 * **The rule this suite enforces: the unattended profile switches off Claude Code's commit
 * attribution in its object form, grants no raw `git commit` and denies the amend.**
 *
 * The object form is asserted literally because `attribution: false` needs a newer Claude Code than
 * the object does, and an older one skips the whole settings file - sandbox block and `deny` rules
 * with it - silently in a `-p` session. The raw-commit grant is asserted absent under any spelling,
 * because every commit a run makes goes through the excluded commit wrapper.
 *
 * The profile is read from a fixture `init` wired, against the compiled CLI at `dist/cli.js`.
 */

import assert from 'node:assert/strict';
import { join } from 'node:path';
import test from 'node:test';

import { createFixture, readJson, runCli } from './helpers/fixture.mjs';

const PROFILE_FILE = '.claude/settings.autonomous.json';

/** A minimal Node project, so detection resolves its commands without a placeholder warning. */
const PROJECT_FILES = {
  'package.json': {
    name: 'fixture-project',
    private: true,
    version: '0.0.0',
    scripts: { typecheck: 'echo typecheck', test: 'echo test', build: 'echo build' },
  },
  'README.md': '# fixture project\n',
};

test('the unattended profile switches off commit attribution and grants no raw commit', async (t) => {
  const fixture = await createFixture({ files: PROJECT_FILES });
  t.after(fixture.cleanup);

  const result = await runCli(fixture.dir, ['init']);
  assert.equal(result.status, 0, `init exited ${result.status}\n${result.stdout}\n${result.stderr}`);

  const profile = readJson(join(fixture.dir, PROFILE_FILE));
  const allow = profile.permissions.allow ?? [];
  const deny = profile.permissions.deny ?? [];

  await t.test('attribution is the object form with both strings empty', () => {
    assert.deepEqual(profile.attribution, { commit: '', pr: '' });
  });

  await t.test('allow carries no raw git commit entry under any spelling', () => {
    assert.ok(!allow.includes('Bash(git commit:*)'), JSON.stringify(allow));
    const commitEntries = allow.filter((entry) => typeof entry === 'string' && entry.startsWith('Bash(git commit'));
    assert.deepEqual(commitEntries, []);
  });

  await t.test('deny carries the amend', () => {
    assert.ok(deny.includes('Bash(git commit --amend:*)'), JSON.stringify(deny));
  });

  await t.test('the _README states the attribution and commit rule', () => {
    const lines = profile._README.filter((line) => line.startsWith('COMMIT ATTRIBUTION IS OFF'));
    assert.equal(lines.length, 1, JSON.stringify(profile._README.map((line) => line.slice(0, 40))));
  });
});
