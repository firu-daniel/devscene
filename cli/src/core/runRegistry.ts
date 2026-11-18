/**
 * The run registry's read side: `<stateDir>/autonomous_logs/registry.json`, the file the watcher
 * keeps as `{"runs": {"<branch>": {…}}}`.
 *
 * **The rule this module exists to enforce: the registry file's parsing and record walk live here
 * once, and each caller keeps its own grading.** {@link readRegistryRecords} says what the file holds
 * and grades nothing. {@link readActiveRuns} is the grading a refusal needs, which treats what it
 * cannot prove idle as a reason to stop; a report is free to grade the same records differently.
 *
 * The caller supplies the path, so this module knows neither the configuration nor where the state
 * directory is. Nothing here writes. The registry's shape, field set and status vocabulary are the
 * watcher's: `cli/templates/scripts/autonomous-watcher.sh` states them and
 * `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_registry_set` writes them.
 */

import { isJsonObject, readJsonFile, type JsonObject, type JsonValue } from './json.js';
import { nameList } from './nameList.js';

/** The record status of a run the watcher considers in flight. */
export const RUNNING_STATUS = 'running';

/** The top-level key holding every run record, by branch. */
const RUNS_KEY = 'runs';

/** A pid as `hr_registry_set` stores it: that writer turns every value into a JSON string. */
const PID_TEXT = /^-?\d+$/;

/** What the registry file holds, before anyone grades it. */
export type RegistryRecords =
  | { state: 'read'; records: readonly { key: string; record: JsonObject }[]; malformedKeys: readonly string[] }
  | { state: 'unreadable'; detail: string };

/** Whether a run may be executing, as a refusal has to read it. */
export type ActiveRuns =
  | { state: 'none' }
  | { state: 'active'; branches: readonly string[] }
  | { state: 'unreadable'; detail: string };

/** The number a pid field carries, stored as a number or as the watcher's text; otherwise `undefined`. */
function pidNumber(pid: JsonValue | undefined): number | undefined {
  if (typeof pid === 'number') return pid;
  return typeof pid === 'string' && PID_TEXT.test(pid) ? Number(pid) : undefined;
}

/**
 * Is this pid a process that exists, from this account's point of view?
 *
 * `process.kill(pid, 0)` sends no signal. `EPERM` is `true`: the process exists and belongs to another
 * account. A pid of `0` or below is rejected before the call, because those values address a process
 * group and a garbage record must not reach the syscall.
 */
export function pidIsAlive(pid: JsonValue | undefined): boolean {
  const value = pidNumber(pid);
  if (value === undefined || !Number.isInteger(value) || value <= 0) return false;
  try {
    process.kill(value, 0);
    return true;
  } catch (error) {
    return (error as NodeJS.ErrnoException).code === 'EPERM';
  }
}

/**
 * Every record in the registry at `registryPath`.
 *
 * A missing file is `read` with no records, because a repository that has never started a run has
 * none. A file that cannot be read or parsed, or that is not `{"runs": {…}}`, is `unreadable`. A
 * `runs` value that is not an object is left out of `records` and listed in `malformedKeys`.
 */
export function readRegistryRecords(registryPath: string): RegistryRecords {
  let parsed: JsonValue | undefined;
  try {
    parsed = readJsonFile(registryPath);
  } catch (error) {
    return { state: 'unreadable', detail: error instanceof Error ? error.message : String(error) };
  }
  if (parsed === undefined) return { state: 'read', records: [], malformedKeys: [] };

  const runs = isJsonObject(parsed) ? parsed[RUNS_KEY] : undefined;
  if (!isJsonObject(runs)) {
    return { state: 'unreadable', detail: `${registryPath} is not a {"${RUNS_KEY}": {…}} object` };
  }

  const records: { key: string; record: JsonObject }[] = [];
  const malformedKeys: string[] = [];
  for (const key of Object.keys(runs)) {
    const record = runs[key];
    if (isJsonObject(record)) records.push({ key, record });
    else malformedKeys.push(key);
  }
  return { state: 'read', records, malformedKeys };
}

/**
 * The branches whose runs may be executing.
 *
 * A malformed record is `unreadable`, because a refusal cannot prove it is not a run. A record is
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
