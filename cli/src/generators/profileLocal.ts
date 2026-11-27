/**
 * The reader and validator of the adopter's local permission additions,
 * {@link PROFILE_LOCAL_PATH}.
 *
 * **The rule this module exists to enforce: the file may only add entries, and only to the four
 * {@link LOCAL_ADDITION_LISTS}.** Its contents reach the profile every unattended run is rendered
 * from, so a key that could switch the sandbox off or change the permission mode is refused here,
 * before any caller sees it. Everything is refused by default: a key is accepted only because it is
 * on the path to one of the four lists.
 *
 * It reads and decides; merging the result into a profile is `permissionProfile.ts`'s, which is why
 * this module imports neither that file nor `writeProtection.ts`.
 *
 * **Absent has three shapes.** No file; a 0-byte regular file; a character device that reads empty.
 * The last two are what a bubblewrap host leaves at, and shows inside a sandboxed call for, a
 * `denyWrite` path that does not exist (`docs/sandbox-verification.md` → F9), and this path is one.
 * Every other shape is refused, a symlink included: following one would take grants from a file
 * outside the protected path.
 *
 * **A tracked file is refused in every execution mode.** The file is safe for a remote job only
 * because it never travels with the repository.
 */

import { closeSync, constants, fstatSync, openSync, readFileSync, readSync } from 'node:fs';
import { join } from 'node:path';

import { HarnessError } from '../core/errors.js';
import { pathAtRef } from '../core/git.js';
import { isJsonObject, parseJsonText, type JsonObject, type JsonValue } from '../core/json.js';
import { containsToken } from '../core/templating.js';
import { FORBIDDEN_IN_ENTRY, PROFILE_LOCAL_PATH } from './profileEntries.js';
import { SANDBOX_KEY } from './sandboxProfile.js';

/** The only lists the local file may add to, each as its key path from the file's root. */
export const LOCAL_ADDITION_LISTS: ReadonlyArray<readonly string[]> = Object.freeze([
  Object.freeze(['permissions', 'allow']),
  Object.freeze(['permissions', 'ask']),
  Object.freeze(['permissions', 'deny']),
  Object.freeze([SANDBOX_KEY, 'filesystem', 'denyWrite']),
]);

/** A validated local file. */
export interface LocalAdditions {
  /** The file's contents: only {@link LOCAL_ADDITION_LISTS}, with duplicates kept for the merge. */
  readonly fragment: JsonObject;
  /** How many entries the file lists, duplicates included. */
  readonly count: number;
}

/**
 * `O_NOFOLLOW` makes the shape test and the read one operation on one file; `O_NONBLOCK` keeps a
 * FIFO from hanging the open before it can be refused.
 */
const OPEN_FLAGS = constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK;

function errorCode(error: unknown): string | undefined {
  return (error as NodeJS.ErrnoException | null)?.code;
}

/** Reads one byte, never to the end: a device such as `/dev/zero` has none. */
function deviceReadsEmpty(fd: number): boolean {
  try {
    return readSync(fd, Buffer.alloc(1), 0, 1, null) === 0;
  } catch {
    return false;
  }
}

/**
 * The text at `path`, or `undefined` for an absent shape (module header); any other shape throws.
 *
 * Exported apart from {@link readLocalAdditions} because no unprivileged test can create a device
 * at the local file's path, and this form can be aimed at `/dev/null`.
 */
export function readLocalFileText(path: string): string | undefined {
  let fd: number;
  try {
    fd = openSync(path, OPEN_FLAGS);
  } catch (error) {
    const code = errorCode(error);
    if (code === 'ENOENT' || code === 'ENOTDIR') return undefined;
    if (code === 'ELOOP') {
      throw new HarnessError(`${path} is a symbolic link; it must be a regular file. Replace the link with the file itself.`);
    }
    throw new HarnessError(`${path} could not be opened (${code ?? String(error)}); it must be a readable regular file.`);
  }
  try {
    const stats = fstatSync(fd);
    if (stats.isCharacterDevice() && deviceReadsEmpty(fd)) return undefined;
    if (!stats.isFile()) {
      throw new HarnessError(`${path} is not a regular file; remove it, or replace it with one.`);
    }
    return stats.size === 0 ? undefined : readFileSync(fd, 'utf8');
  } finally {
    closeSync(fd);
  }
}

function refusal(detail: string): HarnessError {
  return new HarnessError(`${PROFILE_LOCAL_PATH}: ${detail}`);
}

function samePath(a: readonly string[], b: readonly string[]): boolean {
  return a.length === b.length && a.every((segment, index) => segment === b[index]);
}

/** Compared by segment, so a single key spelled `permissions.allow` is not taken for the list. */
function isAdditionList(path: readonly string[]): boolean {
  return LOCAL_ADDITION_LISTS.some((list) => samePath(list, path));
}

function leadsToAdditionList(path: readonly string[]): boolean {
  return LOCAL_ADDITION_LISTS.some((list) => list.length > path.length && samePath(list.slice(0, path.length), path));
}

function assertUsableEntry(entry: JsonValue, where: string): void {
  if (typeof entry !== 'string') {
    throw refusal(`${where} is ${JSON.stringify(entry)}; every entry must be a string.`);
  }
  if (entry.trim() === '') throw refusal(`${where} is blank; remove it or give it a value.`);
  for (const [needle, why] of FORBIDDEN_IN_ENTRY) {
    if (entry.includes(needle)) {
      throw refusal(`${where} (${JSON.stringify(entry)}) contains ${why}, so it would not match as written.`);
    }
  }
  if (containsToken(entry)) {
    throw refusal(`${where} (${JSON.stringify(entry)}) carries an unsubstituted {{token}}; write the literal value.`);
  }
}

/** Refuse whatever under `node` is not on the way to an addition list; returns the entries seen. */
function validatedEntryCount(node: JsonObject, parent: readonly string[]): number {
  let count = 0;
  for (const [key, value] of Object.entries(node)) {
    const path = [...parent, key];
    const dotted = path.join('.');
    if (isAdditionList(path)) {
      if (!Array.isArray(value)) throw refusal(`${dotted} must be a list.`);
      value.forEach((entry, index) => assertUsableEntry(entry, `${dotted}[${index}]`));
      count += value.length;
    } else if (!leadsToAdditionList(path)) {
      throw refusal(
        `${dotted} is not allowed; this file may only add entries to ${LOCAL_ADDITION_LISTS.map((list) => list.join('.')).join(', ')}.`,
      );
    } else if (isJsonObject(value)) {
      count += validatedEntryCount(value, path);
    } else {
      throw refusal(`${dotted} must be an object.`);
    }
  }
  return count;
}

/**
 * The validated additions in `repoRoot`, or `undefined` when the file is absent (module header).
 * Every refusal is a `HarnessError` naming the file and the offending key or entry.
 */
export function readLocalAdditions(repoRoot: string): LocalAdditions | undefined {
  const text = readLocalFileText(join(repoRoot, PROFILE_LOCAL_PATH));
  if (text === undefined) return undefined;
  if (pathAtRef(repoRoot, 'HEAD', PROFILE_LOCAL_PATH)) {
    throw refusal(
      'the file is tracked at HEAD. It is machine-local, and a remote job must never merge one: remove it from the repository with `git rm --cached` and commit that.',
    );
  }
  const parsed = parseJsonText(text, PROFILE_LOCAL_PATH);
  if (!isJsonObject(parsed)) throw refusal('the top level must be a JSON object.');
  return { fragment: parsed, count: validatedEntryCount(parsed, []) };
}
