/**
 * The plugin and CLI version comparison and its wording: `cli/src/machine/pluginCliVersion.ts`, and
 * the dry-run note `cli/src/upgrade/preconditions.ts` builds from them.
 *
 * **The rule this suite exists to enforce: a readable difference is ordered by semantic-version
 * precedence, every remedy moves forward to the latest release, and none pins the CLI to the older
 * version.** The functions are pure, so every case passes plain values.
 */

import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
  pluginCliMismatch,
  pluginCliMismatchRemedy,
  pluginCliMismatchSummary,
  pluginCliMismatchWarning,
} from '../dist/machine/pluginCliVersion.js';
import { pluginVersionNotes } from '../dist/upgrade/preconditions.js';

const UPGRADE_REMEDY = 'run `npx devscene@latest init --upgrade`';
const UPDATE_REMEDY =
  'update the plugin with `claude plugin update devscene@devscene`, restart any open session, then run `npx devscene@latest init --upgrade`';

const olderOf = (pluginVersion, cliVersion) => pluginCliMismatch(pluginVersion, cliVersion)?.older;

test('an unreadable plugin version or two identical versions are no mismatch', () => {
  assert.equal(pluginCliMismatch(undefined, '1.2.3'), undefined);
  assert.equal(pluginCliMismatch('1.2.3', '1.2.3'), undefined);
  assert.equal(pluginCliMismatch('not-a-version', 'not-a-version'), undefined);
});

test('a mismatch carries both versions and the older half', () => {
  assert.deepEqual(pluginCliMismatch('1.2.3', '1.3.0'), { pluginVersion: '1.2.3', cliVersion: '1.3.0', older: 'plugin' });
  assert.deepEqual(pluginCliMismatch('2.0.0', '1.3.0'), { pluginVersion: '2.0.0', cliVersion: '1.3.0', older: 'cli' });
});

test('release numbers compare numerically', () => {
  assert.equal(olderOf('0.9.0', '0.10.0'), 'plugin');
  assert.equal(olderOf('0.10.0', '0.9.0'), 'cli');
  assert.equal(olderOf('1.0.9', '1.0.10'), 'plugin');
  assert.equal(olderOf('9007199254740993.0.0', '9007199254740992.0.0'), 'cli');
});

test('a prerelease sorts below its release', () => {
  assert.equal(olderOf('1.0.0-rc.1', '1.0.0'), 'plugin');
  assert.equal(olderOf('1.0.0', '1.0.0-rc.1'), 'cli');
  assert.equal(olderOf('1.0.0-rc.1', '0.9.0'), 'cli');
});

test('prerelease identifiers compare left to right', async (t) => {
  for (const [lower, higher] of [
    ['1.0.0-alpha', '1.0.0-alpha.1'],
    ['1.0.0-alpha.1', '1.0.0-alpha.beta'],
    ['1.0.0-alpha.beta', '1.0.0-beta'],
    ['1.0.0-beta.2', '1.0.0-beta.11'],
    ['1.0.0-rc.1', '1.0.0-rc.1.0'],
    ['1.0.0-9', '1.0.0-a'],
  ]) {
    await t.test(`${lower} is below ${higher}`, () => {
      assert.equal(olderOf(lower, higher), 'plugin');
      assert.equal(olderOf(higher, lower), 'cli');
    });
  }
});

test('a version that does not parse gives unknown', async (t) => {
  for (const version of ['latest', '1.2', '1.2.3.4', 'v1.2.3', '01.2.3', '1.2.3-', '1.2.3-01', '1.2.3+', '1.2.3\n']) {
    await t.test(JSON.stringify(version), () => {
      assert.equal(olderOf(version, '1.2.3'), 'unknown');
      assert.equal(olderOf('1.2.3', version), 'unknown');
    });
  }
});

test('two different strings of equal precedence give unknown', () => {
  assert.equal(olderOf('1.2.3+a', '1.2.3+b'), 'unknown');
  assert.equal(olderOf('1.2.3+a', '1.2.3'), 'unknown');
  assert.equal(olderOf('1.2.3-rc.1+a', '1.2.3-rc.1+b'), 'unknown');
});

test('build metadata does not hide a difference in precedence', () => {
  assert.equal(olderOf('1.2.3+z', '1.2.4+a'), 'plugin');
});

const WORDING = [
  {
    older: 'plugin',
    pluginVersion: '1.2.0',
    cliVersion: '1.3.0',
    remedy: UPDATE_REMEDY,
    warning:
      'The installed plugin is version 1.2.0 and this CLI is version 1.3.0. Update the plugin with `claude plugin update devscene@devscene`, restart any open session, then run `npx devscene@latest init --upgrade`.',
  },
  {
    older: 'cli',
    pluginVersion: '1.3.0',
    cliVersion: '1.2.0',
    remedy: UPGRADE_REMEDY,
    warning:
      'The installed plugin is version 1.3.0 and this CLI is version 1.2.0. Run `npx devscene@latest init --upgrade`.',
  },
  {
    older: 'unknown',
    pluginVersion: '1.2.0+a',
    cliVersion: '1.2.0+b',
    remedy: UPDATE_REMEDY,
    warning:
      'The installed plugin is version 1.2.0+a and this CLI is version 1.2.0+b. Update the plugin with `claude plugin update devscene@devscene`, restart any open session, then run `npx devscene@latest init --upgrade`.',
  },
];

for (const { older, pluginVersion, cliVersion, remedy, warning } of WORDING) {
  test(`the wording when the older half is ${older}`, () => {
    const mismatch = pluginCliMismatch(pluginVersion, cliVersion);
    assert.equal(mismatch.older, older);
    assert.equal(
      pluginCliMismatchSummary(mismatch),
      `the installed plugin is version ${pluginVersion} and this CLI is version ${cliVersion}`,
    );
    assert.equal(pluginCliMismatchRemedy(mismatch), remedy);
    assert.equal(pluginCliMismatchWarning(mismatch), warning);
  });

  test(`no remedy pins either version when the older half is ${older}`, () => {
    const text = pluginCliMismatchRemedy(pluginCliMismatch(pluginVersion, cliVersion));
    assert.ok(!text.includes(`@${pluginVersion}`), text);
    assert.ok(!text.includes(`@${cliVersion}`), text);
  });

  test(`a dry run notes the refusal when the older half is ${older}`, () => {
    const mismatch = pluginCliMismatch(pluginVersion, cliVersion);
    assert.deepEqual(pluginVersionNotes({ mismatch, dryRun: true }), [
      `a real --upgrade run would refuse: the installed plugin is version ${pluginVersion} and this CLI is version ${cliVersion}; ${remedy}`,
    ]);
  });
}

test('a dry run with no mismatch has no version note', () => {
  assert.deepEqual(pluginVersionNotes({ mismatch: undefined, dryRun: true }), []);
});
