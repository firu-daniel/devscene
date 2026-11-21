/**
 * The profile `init --upgrade` writes, put through the written watcher's own per-run functions.
 *
 * **The rule this suite exists to enforce: a profile upgraded with local additions is one the watcher
 * launches a run with, on a macOS-style host and on a bubblewrap-style host alike, and a placeholder
 * left at the local file's path changes nothing.** `HR_PLACEHOLDER_HOST` selects the host arm, so
 * neither arm needs its host. No session starts here: real Seatbelt and bubblewrap sessions are the
 * hand-run Gate 15 (`docs/development.md`).
 *
 * Every per-run profile lands under the fixture's own `XDG_STATE_HOME` (`watcherEnv`), which the first
 * case asserts, so the fixture's teardown removes it.
 */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { rm, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import test from 'node:test';

import { runBash, runCli, snapshotTree } from './helpers/fixture.mjs';
import { TICK_TIMEOUT_MS, createWatcherFixture } from './helpers/watcher.mjs';

const UPGRADE = ['init', '--upgrade'];
const BASE_PROFILE = '.claude/settings.autonomous.json';
const LOCAL_FILE = '.claude/settings.autonomous.local.json';
const CLAUDE_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';
const ALREADY_CURRENT = /^Already current: no file changed\.$/m;

/** A trio path the render re-roots on a bubblewrap host, dropping the base's sibling glob for it. */
const TRIO_PATH = '/.git/commondir';

const LOCAL_ALLOW = 'Bash(local-allow-command:*)';
const LOCAL_ASK = 'Bash(local-ask-command:*)';
const LOCAL_DENY = 'Bash(local-deny-command:*)';

/** A fixture `init` wired, with `upgrade` and `watcherCall` bound to it, or `null` when skipped. */
async function wiredFixture(t) {
  const w = await createWatcherFixture(t);
  if (w === null) return null;

  // The agent-runner home is the fixture's, so no plugin installed on the host reaches the upgrade.
  const cliEnv = { ...w.watcherEnv(), [CLAUDE_HOME_VARIABLE]: join(w.dir, 'home', '.claude') };
  const basePath = join(w.dir, BASE_PROFILE);

  return {
    ...w,
    basePath,
    localPath: join(w.dir, LOCAL_FILE),
    async upgrade() {
      const result = await runCli(w.dir, UPGRADE, cliEnv);
      assert.equal(result.status, 0, `init --upgrade exited ${result.status}\n${result.stdout}\n${result.stderr}`);
      return result;
    },
    /** `script` run in a shell that sourced the written watcher; `$1`… are `args`. */
    async watcherCall(script, args = []) {
      const result = await runBash(
        w.dir,
        ['-c', `. "$1" status >/dev/null; shift; ${script}`, '_', w.watcherPath, ...args],
        w.watcherEnv(),
        { timeoutMs: TICK_TIMEOUT_MS, signal: t.signal },
      );
      assert.equal(result.status, 0, `the watcher call exited ${result.status}\n${result.stdout}\n${result.stderr}`);
      return result.stdout;
    },
  };
}

/** Assert `profile` carries one local entry in each of the four lists. */
function assertLocalEntries(profile, localDenyWrite, label) {
  assert.ok(profile.permissions.allow.includes(LOCAL_ALLOW), `${label}: permissions.allow lost ${LOCAL_ALLOW}`);
  assert.ok(profile.permissions.ask.includes(LOCAL_ASK), `${label}: permissions.ask lost ${LOCAL_ASK}`);
  assert.ok(profile.permissions.deny.includes(LOCAL_DENY), `${label}: permissions.deny lost ${LOCAL_DENY}`);
  assert.ok(profile.sandbox.filesystem.denyWrite.includes(localDenyWrite), `${label}: denyWrite lost ${localDenyWrite}`);
}

/** Assert `profile` protects the local file at `localPath` on both the sandbox and file-tool sides. */
function assertLocalFileProtected(profile, localPath, label) {
  assert.ok(profile.sandbox.filesystem.denyWrite.includes(localPath), `${label}: ${localPath} is not in denyWrite`);
  assert.ok(profile.permissions.deny.includes(`Edit(/${localPath})`), `${label}: no Edit deny rule for ${localPath}`);
}

const hasTrioGlob = (profile) =>
  profile.sandbox.filesystem.denyWrite.some((entry) => entry.includes('*') && entry.endsWith(TRIO_PATH));

test('an upgraded profile with local additions passes the per-run check on both host kinds', async (t) => {
  const f = await wiredFixture(t);
  if (f === null) return;

  const localDenyWrite = join(f.dir, 'local-deny-write');
  await writeFile(
    f.localPath,
    `${JSON.stringify(
      {
        permissions: { allow: [LOCAL_ALLOW], ask: [LOCAL_ASK], deny: [LOCAL_DENY] },
        sandbox: { filesystem: { denyWrite: [localDenyWrite] } },
      },
      null,
      2,
    )}\n`,
    'utf8',
  );
  await f.upgrade();

  const base = JSON.parse(readFileSync(f.basePath, 'utf8'));
  assertLocalEntries(base, localDenyWrite, 'the base profile');
  assertLocalFileProtected(base, f.localPath, 'the base profile');

  for (const host of [0, 1]) {
    const label = `HR_PLACEHOLDER_HOST=${host}`;
    const copy = `${f.dir}-upgrade-copy-${host}`;
    t.after(() => rm(copy, { recursive: true, force: true }));

    const rendered = await f.watcherCall(
      `HR_PLACEHOLDER_HOST=${host}; run_profile_render "$1" "$2" clone; printf "%s|%s|%s" "$?" "$RUN_PROFILE_REFUSAL" "$RUN_PROFILE_FILE"`,
      [`feat_upgrade_${host}`, copy],
    );
    const [status, refusal, file] = rendered.split('|');
    assert.deepEqual([status, refusal], ['0', ''], `${label}: render said ${rendered}`);
    assert.ok(file.startsWith(`${f.dir}/`), `${label}: ${file} is outside the fixture, so teardown would miss it`);

    const check = await f.watcherCall(
      `HR_PLACEHOLDER_HOST=${host}; run_profile_check "$1" "$2"; printf "%s|%s" "$?" "$RUN_PROFILE_REFUSAL"`,
      [file, copy],
    );
    assert.equal(check, '0|', `${label}: the per-run check said ${check}`);

    const jobCheck = await f.watcherCall(
      `HR_PLACEHOLDER_HOST=${host}; run_profile_check "$1"; printf "%s|%s" "$?" "$RUN_PROFILE_REFUSAL"`,
      [f.basePath],
    );
    assert.equal(jobCheck, '0|', `${label}: the job-mode check said ${jobCheck}`);

    const perRun = JSON.parse(readFileSync(file, 'utf8'));
    assertLocalEntries(perRun, localDenyWrite, `${label}: the per-run copy`);
    assertLocalFileProtected(perRun, f.localPath, `${label}: the per-run copy`);
    // Without this, a host value the watcher ignored would pass as two runs of one arm.
    assert.equal(hasTrioGlob(perRun), host === 0, `${label}: the wrong host arm rendered the copy`);
  }
});

test('a 0-byte read-only file at the local path leaves a further upgrade unchanged', async (t) => {
  const f = await wiredFixture(t);
  if (f === null) return;

  await f.upgrade();
  await writeFile(f.localPath, '', { mode: 0o444 });
  const before = await snapshotTree(f.dir);

  const result = await f.upgrade();

  assert.match(result.stdout, ALREADY_CURRENT);
  assert.deepEqual(await snapshotTree(f.dir), before);
});
