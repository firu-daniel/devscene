/**
 * Whether this repository may be upgraded, decided before anything is planned.
 *
 * **The rule this module exists to enforce: every refusal comes before the first generator**, so a
 * refused `init --upgrade` leaves the repository byte-identical. Everything here only reads, and no
 * path creates or offers a repository.
 *
 * The check refusing the harness's own repository lives in `commands/init.ts`, which imports this
 * module, so it arrives as a callback. Flag combinations are that command's to refuse.
 */

import { hasErrors, formatProblem } from '../config/check.js';
import { configExists, loadConfig, type LoadedConfig } from '../config/io.js';
import { CONFIG_FILENAME, type HarnessConfig } from '../config/model.js';
import { HarnessError } from '../core/errors.js';
import { gitCommonDir, mainWorktreeRoot, probeRepoRoot } from '../core/git.js';
import { nameList } from '../core/nameList.js';
import { pidIsAlive, pidNumber, readRegistryRecords, RUNNING_STATUS } from '../core/runRegistry.js';
import { runRegistryPath } from '../generators/writeProtection.js';

/** The repository an upgrade may proceed in. */
export interface UpgradeTarget {
  readonly repoRoot: string;
  readonly config: HarnessConfig;
  readonly gitCommonDir: string;
  /** What a `--dry-run` found that a real run would have refused on. */
  readonly notes: readonly string[];
}

/** What {@link resolveUpgradeTarget} is asked. */
export interface UpgradeTargetRequest {
  readonly cwd: string;
  /** Turns the two run-registry refusals into {@link UpgradeTarget.notes}, and no other refusal. */
  readonly dryRun: boolean;
  /** Refuses by throwing; what it throws reaches the caller unchanged. */
  readonly assertRepositoryAllowed: (repoRoot: string) => unknown;
}

/** Whether a run may be executing, as the refusal has to read it. */
export type ActiveRuns =
  | { state: 'none' }
  | { state: 'active'; branches: readonly string[] }
  | { state: 'unreadable'; detail: string };

const REFUSAL_PREFIX = 'refusing to upgrade';

/** The root of the repository around `cwd`, or the refusal saying why there is none. */
function upgradeRoot(cwd: string): string {
  const probe = probeRepoRoot(cwd);
  if (probe.kind === 'repository') return probe.root;
  if (probe.kind === 'not-a-repository') {
    throw new HarnessError(`${REFUSAL_PREFIX}: ${probe.message}; run --upgrade inside a repository \`init\` has wired`);
  }
  throw new HarnessError(`${REFUSAL_PREFIX}: ${probe.message}`);
}

/**
 * Refuses anywhere but the main checkout, whose profile is the one a run loads. A probe with no
 * answer refuses too, because it cannot show this is the main checkout.
 */
function assertMainCheckout(root: string): void {
  const main = mainWorktreeRoot(root);
  if (main === undefined) {
    throw new HarnessError(
      `${REFUSAL_PREFIX}: git did not report the main checkout of ${root}; make \`git worktree list --porcelain\` work there, then run --upgrade again`,
    );
  }
  if (main !== root) {
    throw new HarnessError(
      `${REFUSAL_PREFIX}: ${root} is a linked worktree; run --upgrade in the main checkout at ${main}`,
    );
  }
}

/** The shared git directory, or the refusal when git does not name one. */
function requireCommonDir(root: string): string {
  const commonDir = gitCommonDir(root);
  if (commonDir !== undefined) return commonDir;
  throw new HarnessError(
    `${REFUSAL_PREFIX}: git did not report the common directory of ${root}; make \`git rev-parse --git-common-dir\` work there, then run --upgrade again`,
  );
}

/** The refusal for a configuration that is absent or carries an error. */
function configRefusal(root: string, loaded: LoadedConfig): HarnessError {
  const problems = loaded.problems.filter((problem) => problem.severity === 'error').map(formatProblem);
  // An absent file's problem already names `init` as its remedy.
  const remedy = configExists(root) ? `; correct ${CONFIG_FILENAME}, then run --upgrade again` : '';
  return new HarnessError(`${REFUSAL_PREFIX}: ${problems.join('; ')}${remedy}`);
}

/**
 * The branches whose runs may be executing.
 *
 * A malformed record is `unreadable`, because the refusal cannot prove it is not a run. A record is
 * active when its `status` is `running` and its pid is alive or holds no number yet: at launch the
 * watcher writes `running`, clears any earlier pid to `""`, and writes the new pid after it spawns
 * the run.
 */
export function readActiveRuns(registryPath: string): ActiveRuns {
  const read = readRegistryRecords(registryPath);
  if (read.state === 'unreadable') return read;
  if (read.malformedKeys.length > 0) {
    return {
      state: 'unreadable',
      detail: `${registryPath} holds run records that are not objects: ${nameList(read.malformedKeys)}`,
    };
  }

  const branches = read.records
    .filter(({ record }) => {
      if (record['status'] !== RUNNING_STATUS) return false;
      const pid = record['pid'];
      return pidNumber(pid) === undefined || pidIsAlive(pid);
    })
    .map(({ key }) => key);
  return branches.length > 0 ? { state: 'active', branches } : { state: 'none' };
}

/** Why the run registry stops an upgrade, or `undefined` when it does not. */
function runRegistryRefusal(registryPath: string): string | undefined {
  const runs = readActiveRuns(registryPath);
  switch (runs.state) {
    case 'none':
      return undefined;
    case 'active':
      return `runs are active on ${nameList(runs.branches)} (${registryPath}); wait for them to finish or stop them, then run --upgrade again`;
    case 'unreadable':
      return `the run registry ${registryPath} cannot be read, so no run can be ruled out: ${runs.detail}; repair it, or remove it once no run is executing, then run --upgrade again`;
  }
}

/** The dry-run notes the registry yields; a real run throws instead. */
function runRegistryNotes(registryPath: string, dryRun: boolean): readonly string[] {
  const refusal = runRegistryRefusal(registryPath);
  if (refusal === undefined) return [];
  if (!dryRun) throw new HarnessError(`${REFUSAL_PREFIX}: ${refusal}`);
  return [`a real --upgrade run would refuse: ${refusal}`];
}

/**
 * Whether `config` names a state directory the registry path can be built from. Absent falls back
 * to the default; any other non-string is a shape error, so {@link resolveUpgradeTarget} refuses it.
 */
function registryLocatable(config: HarnessConfig): boolean {
  const stateDir: unknown = config.stateDir;
  return stateDir === undefined || typeof stateDir === 'string';
}

/**
 * The repository `cwd` belongs to, once every repository-level refusal has passed.
 *
 * The worktree check precedes the configuration's, so a linked worktree without the file is sent to
 * the main checkout rather than told to run `init` there.
 *
 * The registry is read **before** the configuration's shape errors refuse: the check reports an
 * absent `stateDir` as an error, and an active run is the refusal an operator must act on first.
 * A configuration with a shape error is still refused, dry run included.
 */
export function resolveUpgradeTarget(request: UpgradeTargetRequest): UpgradeTarget {
  const repoRoot = upgradeRoot(request.cwd);
  request.assertRepositoryAllowed(repoRoot);
  assertMainCheckout(repoRoot);
  const commonDir = requireCommonDir(repoRoot);

  const loaded = loadConfig(repoRoot);
  const { config } = loaded;
  if (config === undefined) throw configRefusal(repoRoot, loaded);
  const notes = registryLocatable(config)
    ? runRegistryNotes(runRegistryPath(repoRoot, config), request.dryRun)
    : [];
  if (hasErrors(loaded.problems)) throw configRefusal(repoRoot, loaded);

  return { repoRoot, config, gitCommonDir: commonDir, notes };
}
