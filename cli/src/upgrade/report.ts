/**
 * The wording of the `init --upgrade` report.
 *
 * **The rule this module exists to enforce: {@link upgradeReport} is a pure function that reads no
 * file and prints nothing.** The command gathers every input and sends the returned lines through
 * its `Reporter`, so each line can be tested from plain values.
 *
 * `Reporter.info` is silenced by `--quiet` and `Reporter.warn` is not, so what an adopter must act on
 * after a real run is a warning, and is complete without the notes.
 */

import { nameList } from '../core/nameList.js';
import type { WriteEffect, WriteResult } from '../core/writer.js';
import { RESTART_WATCHER_SCRIPT_NAME } from '../generators/outerLoopScripts.js';
import { namesUnstartedMcpServer } from '../generators/permissionProfile.js';
import { PROFILE_LOCAL_PATH, PROFILE_PATH } from '../generators/profileEntries.js';
import { LOCAL_ADDITION_LISTS } from '../generators/profileLocal.js';
import { ALLOW_LIST_PATH, type ProfileEntryDelta } from '../generators/profileUpgrade.js';
import { scriptInvocation } from '../generators/scripts.js';

/** What {@link upgradeReport} is told about the run. */
export interface UpgradeReportInput {
  readonly dryRun: boolean;
  /** The `daemonLoadedScriptPaths(repoRoot, config)` value. */
  readonly daemonLoadedPaths: ReadonlySet<string>;
  /** The `outerLoopScriptsDir(config)` value. */
  readonly scriptsDir: string;
  readonly applied: readonly WriteResult[];
  readonly delta: readonly ProfileEntryDelta[];
  /** The `ProfileUpgradePlan.settingChanges` value. */
  readonly settingChanges: readonly string[];
  /** The `ProfileUpgradePlan.startedMcpServers` value. */
  readonly startedMcpServers: readonly string[];
  readonly previousUnreadable: boolean;
  readonly localAdditionCount: number;
  readonly backupDir: string;
  /** `undefined` when there is no local file to ask about. */
  readonly localFileIgnored: boolean | undefined;
  readonly cliVersion: string;
  /** The `pinnedCliCommand(cliVersion)` value: what the restart script runs the daemon verbs through. */
  readonly cliCommand: string;
  readonly pluginVersion: string | undefined;
  /** The `pinnedCliCommand(pluginVersion)` value; `undefined` when `pluginVersion` is. */
  readonly pluginCliCommand: string | undefined;
}

/** The lines of one report, for `Reporter.info`, `Reporter.warn` and `Reporter.result`. */
export interface UpgradeReport {
  readonly notes: readonly string[];
  readonly warnings: readonly string[];
  readonly result: string;
}

const CLI = 'npx devscene';
const UPGRADE_COMMAND = `${CLI} init --upgrade`;

const CHANGED_EFFECTS: ReadonlySet<WriteEffect> = new Set<WriteEffect>(['created', 'backed-up-and-replaced']);

function counted(count: number, singular: string, plural = `${singular}s`): string {
  return `${count} ${count === 1 ? singular : plural}`;
}

/** One line per entry, because an entry such as `Bash(a, b)` can itself contain the separator. */
function profileLines(delta: readonly ProfileEntryDelta[], dryRun: boolean): readonly string[] {
  const addedVerb = dryRun ? 'would add' : 'added';
  const removedVerb = dryRun ? 'would remove' : 'removed';
  return delta.flatMap(({ list, added, removed }) => [
    ...added.map((entry) => `Profile ${list}: ${addedVerb} ${entry}`),
    ...removed.map((entry) => `Profile ${list}: ${removedVerb} ${entry}`),
  ]);
}

/** Names only the lists the local file accepts: it refuses a key outside them. */
function movableEntriesAdvice(movable: readonly string[], anyRefused: boolean, dryRun: boolean): string {
  const outcome = dryRun ? 'they would be removed and would not be moved' : 'they were removed and were not moved';
  const lists = LOCAL_ADDITION_LISTS.map((list) => list.join('.')).join(', ');
  const wanted = anyRefused ? 'Any of these' : 'Anything';
  return (
    `The generator does not produce ${counted(movable.length, 'profile entry', 'profile entries')}, so ${outcome} ` +
    `automatically: ${nameList(movable)}. ${wanted} still wanted in ${lists} belongs in ${PROFILE_LOCAL_PATH}, ` +
    `followed by another ${UPGRADE_COMMAND}.`
  );
}

/** Every entry is spelled out, past `nameList`'s cap: the notes naming them do not survive `--quiet`. */
function refusedEntriesNotice(refused: readonly string[], dryRun: boolean): string {
  const one = refused.length === 1;
  const entries = counted(refused.length, `${ALLOW_LIST_PATH} entry`, `${ALLOW_LIST_PATH} entries`);
  const verb = dryRun ? 'would be' : one ? 'was' : 'were';
  const servers = one ? 'its MCP server' : 'their MCP servers';
  return (
    `${entries} ${verb} removed and cannot be moved to ${PROFILE_LOCAL_PATH}, because this profile does not start ` +
    `${servers}: ${refused.join(', ')}.`
  );
}

function removedEntriesWarning(
  delta: readonly ProfileEntryDelta[],
  startedMcpServers: readonly string[],
  dryRun: boolean,
): string {
  const refusedIn = (list: string, entry: string): boolean =>
    list === ALLOW_LIST_PATH && namesUnstartedMcpServer(entry, startedMcpServers);
  const refused = delta.flatMap(({ list, removed }) => removed.filter((entry) => refusedIn(list, entry)));
  const movable = delta.flatMap(({ list, removed }) => removed.filter((entry) => !refusedIn(list, entry)));

  const parts: string[] = [];
  if (movable.length > 0) parts.push(movableEntriesAdvice(movable, refused.length > 0, dryRun));
  if (refused.length > 0) parts.push(refusedEntriesNotice(refused, dryRun));
  return parts.join(' ');
}

/** Turn the outcome of an upgrade or a dry run into the lines the command reports. */
export function upgradeReport(input: UpgradeReportInput): UpgradeReport {
  const { dryRun, daemonLoadedPaths, scriptsDir, applied, delta, settingChanges, localAdditionCount, backupDir } = input;
  const { previousUnreadable, localFileIgnored, cliVersion, cliCommand, pluginVersion, pluginCliCommand } = input;
  const { startedMcpServers } = input;

  const notes: string[] = [...profileLines(delta, dryRun)];
  const warnings: string[] = [];

  if (delta.some(({ removed }) => removed.length > 0)) {
    warnings.push(removedEntriesWarning(delta, startedMcpServers, dryRun));
  }
  if (settingChanges.length > 0) {
    const names = settingChanges.join(', ');
    warnings.push(
      dryRun
        ? `${counted(settingChanges.length, 'profile setting')} outside the entry lists would be reset to what this CLI renders: ${names}. ${PROFILE_LOCAL_PATH} cannot hold them; the replaced file would be backed up first.`
        : `${counted(settingChanges.length, 'profile setting')} outside the entry lists ${settingChanges.length === 1 ? 'was' : 'were'} reset to what this CLI renders: ${names}. ${PROFILE_LOCAL_PATH} cannot hold them; the replaced file is under ${backupDir}.`,
    );
  }

  if (localAdditionCount > 0) {
    const additions = counted(localAdditionCount, 'local addition');
    notes.push(`Profile ${dryRun ? 'would include' : 'includes'} ${additions} from ${PROFILE_LOCAL_PATH}.`);
  }

  const changed = applied.filter(({ effect }) => CHANGED_EFFECTS.has(effect));

  const backups = changed.filter(({ backupPath }) => backupPath !== undefined).length;
  if (backups > 0) {
    const files = counted(backups, 'replaced file');
    // A dry run creates no directory, and a real run's is named for its own start time.
    notes.push(dryRun ? `Would back up ${files} first.` : `Backed up ${files} under ${backupDir}.`);
  }

  // A replacement with no backup corrected permission bits only, which a running daemon does not load.
  const contentChanged = changed.filter(({ effect, backupPath }) => effect === 'created' || backupPath !== undefined);
  if (contentChanged.some(({ path }) => daemonLoadedPaths.has(path))) {
    const restart = `DEVSCENE_CLI="${cliCommand}" ${scriptInvocation(scriptsDir, RESTART_WATCHER_SCRIPT_NAME)}`;
    if (dryRun) {
      notes.push(`Would change the watcher or its libraries: restart the daemon afterwards with ${restart}`);
    } else {
      warnings.push(`A running daemon keeps the code it already loaded: restart it with ${restart}`);
    }
  }

  if (localFileIgnored === false) {
    warnings.push(`${PROFILE_LOCAL_PATH} is not ignored by git: a plain ${CLI} init merges the ignore rule.`);
  }
  if (pluginVersion !== undefined && pluginCliCommand !== undefined && pluginVersion !== cliVersion) {
    warnings.push(
      `The installed plugin is version ${pluginVersion} and this CLI is version ${cliVersion}: ` +
        `run ${pluginCliCommand} init --upgrade, from the CLI of the plugin's version.`,
    );
  }
  if (previousUnreadable) {
    warnings.push(
      `The previous ${PROFILE_PATH} could not be read, so the old profile could not be compared: ` +
        'every entry is reported as added, and nothing it held is reported as removed.',
    );
  }

  const files = counted(changed.length, 'file');
  let result: string;
  if (dryRun) {
    result = changed.length === 0 ? 'Dry run: already current, no file would change.' : `Dry run: ${files} would change.`;
  } else {
    result = changed.length === 0 ? 'Already current: no file changed.' : `Upgrade complete: ${files} changed.`;
  }

  return { notes, warnings, result };
}
