/**
 * The `init --upgrade` run: it orders the upgrade's steps and reports their outcome.
 *
 * **The rule this module exists to enforce: only the outer-loop scripts and the permission profile
 * are planned, and all refusals and planning finish before one `plan.apply`, so a refused run writes
 * nothing.** What each step decides belongs to the module it calls.
 */

import { existsSync } from 'node:fs';
import { join } from 'node:path';

import type { CommandContext } from '../commands/registry.js';
import { EXIT } from '../core/errors.js';
import { pathIsIgnored } from '../core/git.js';
import { ownManifestString } from '../core/paths.js';
import { WritePlan } from '../core/writer.js';
import { pinnedCliCommand } from '../generators/githubWorkflows.js';
import { daemonLoadedScriptPaths, planOuterLoopScriptUpgrade } from '../generators/outerLoopScripts.js';
import { PROFILE_LOCAL_PATH } from '../generators/profileEntries.js';
import { planProfileUpgrade } from '../generators/profileUpgrade.js';
import { pluginCliMismatch, pluginCliMismatchWarning } from '../machine/pluginCliVersion.js';
import { installedPluginVersion } from '../machine/plugins.js';
import { pluginVersionNotes, resolveUpgradeTarget } from './preconditions.js';
import { upgradeReport } from './report.js';

/** Where backups live under the git common directory, which every checkout shares and git never lists. */
const BACKUP_ROOT_SEGMENTS: readonly string[] = Object.freeze(['devscene', 'upgrade-backups']);

/** What `commands/init.ts` hands the run. */
export interface InitUpgradeOptions {
  readonly referenceToolchainPath: string | undefined;
  /**
   * Refuses by throwing; `init`'s check for the harness's own repository. Returns `true` only for
   * that repository's deliberate self-adoption.
   */
  readonly assertRepositoryAllowed: (repoRoot: string) => boolean;
}

/** This run's backup directory, named for its start time in UTC, to the millisecond. */
function backupDirectory(gitCommonDir: string): string {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  return join(gitCommonDir, ...BACKUP_ROOT_SEGMENTS, timestamp);
}

/** Upgrade the repository around `ctx.cwd`, or under `--dry-run` report what that would change. */
export function runInitUpgrade(
  ctx: CommandContext,
  { referenceToolchainPath, assertRepositoryAllowed }: InitUpgradeOptions,
): number {
  const { dryRun } = ctx.flags;
  const { report } = ctx;

  const target = resolveUpgradeTarget({ cwd: ctx.cwd, dryRun, assertRepositoryAllowed });
  const { repoRoot, config } = target;

  const pluginVersion = installedPluginVersion(repoRoot);
  const cliVersion = ownManifestString('version');
  const mismatch = pluginCliMismatch(pluginVersion, cliVersion);
  const versionNotes = pluginVersionNotes({ mismatch, dryRun, selfAdopted: target.selfAdopted });

  const plan = new WritePlan();
  const scripts = planOuterLoopScriptUpgrade({ repoRoot, config, plan });
  const profile = planProfileUpgrade({ repoRoot, config, plan, referenceToolchainPath, dryRun });

  const backupDir = backupDirectory(target.gitCommonDir);
  const applied = plan.apply({ repoRoot, report, dryRun, force: false, backupDir });

  const outcome = upgradeReport({
    dryRun,
    daemonLoadedPaths: daemonLoadedScriptPaths(repoRoot, config),
    scriptsDir: scripts.scriptsDir,
    applied,
    delta: profile.delta,
    settingChanges: profile.settingChanges,
    startedMcpServers: profile.startedMcpServers,
    browserMcpServers: profile.browserMcpServers,
    previousUnreadable: profile.previousUnreadable,
    localAdditionCount: profile.localAdditionCount,
    backupDir,
    localFileIgnored: existsSync(join(repoRoot, PROFILE_LOCAL_PATH))
      ? pathIsIgnored(repoRoot, PROFILE_LOCAL_PATH)
      : undefined,
    cliCommand: pinnedCliCommand(cliVersion),
    // Any other run's mismatch has already refused or become a note; the report's warning would contradict it.
    pluginMismatchWarning: target.selfAdopted && mismatch !== undefined ? pluginCliMismatchWarning(mismatch) : undefined,
  });

  for (const note of [...target.notes, ...versionNotes, ...profile.notes]) report.info(note);
  for (const warning of profile.warnings) report.warn(warning);
  for (const note of outcome.notes) report.info(note);
  for (const warning of outcome.warnings) report.warn(warning);
  report.result(outcome.result);
  return EXIT.OK;
}
