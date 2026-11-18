/**
 * What the unattended permission profile should be, and how the file on disk differs from it.
 *
 * **The rule this module exists to enforce: `init --upgrade` and `doctor` compare against one
 * render.** Both reach {@link renderProfile} through this module, with the selection taken from the
 * configuration and the validated local additions merged, so the file one writes is the file the
 * other grades.
 *
 * The two differ in one input. An upgrade carries forward the plugin-root entries of the profile it
 * replaces. {@link profileDrift} never does, because a profile being graded must not vouch for its
 * own entries; it accepts a plugin-root shape only under a root this machine resolves.
 *
 * It reads and plans. The one write is the request {@link planProfileUpgrade} enqueues.
 */

import { join, resolve } from 'node:path';

import type { HarnessConfig } from '../config/model.js';
import { isJsonObject, readJsonFile, valueAt, type JsonObject, type JsonValue } from '../core/json.js';
import { workRoot } from '../core/paths.js';
import type { WritePlan } from '../core/writer.js';
import {
  CREDENTIAL_LISTS,
  ENABLED_SERVERS_KEY,
  isToolchainEntry,
  isUnderDirectory,
  PERMISSION_LISTS,
  pluginRootEntryTarget,
  renderProfile,
  resolvedPluginRoots,
  SANDBOX_LISTS,
} from './permissionProfile.js';
import { PROFILE_PATH, README_KEY } from './profileEntries.js';
import { readLocalAdditions, type LocalAdditions } from './profileLocal.js';
import { SANDBOX_KEY } from './sandboxProfile.js';

/** The one list whose plugin-root shapes {@link profileDrift} accepts. */
const ALLOW_LIST_PATH = 'permissions.allow';

/** One list the render can produce. */
export interface ProfileEntryList {
  /** Dotted key path from the profile's root. */
  readonly path: string;
  /** The field naming an element, for a list of objects. */
  readonly field?: string;
}

/** Every list the render can produce, built from the declarations `assertRunnable` reads. */
export const PROFILE_ENTRY_LISTS: readonly ProfileEntryList[] = Object.freeze([
  ...PERMISSION_LISTS.map((list) => ({ path: `permissions.${list}` })),
  { path: 'permissions.additionalDirectories' },
  ...SANDBOX_LISTS.map((dotted) => ({ path: `${SANDBOX_KEY}.${dotted}` })),
  ...CREDENTIAL_LISTS.map(([list, field]) => ({ path: `${SANDBOX_KEY}.credentials.${list}`, field })),
  { path: ENABLED_SERVERS_KEY },
]);

const ENTRY_LIST_PATHS: ReadonlySet<string> = new Set(PROFILE_ENTRY_LISTS.map(({ path }) => path));

/** How one list changes between two profiles. */
export interface ProfileEntryDelta {
  readonly list: string;
  readonly added: readonly string[];
  readonly removed: readonly string[];
}

/** One entry of one list. */
export interface ProfileEntry {
  readonly list: string;
  readonly entry: string;
}

/** What {@link renderWith} takes, beyond the local additions. */
interface RenderCurrentProfileOptions {
  readonly repoRoot: string;
  readonly config: HarnessConfig;
  readonly referenceToolchainPath?: string;
  readonly pluginRootEntries?: boolean;
  /** Carry the on-disk profile's plugin-root entries forward. `false` does not read that profile. */
  readonly carryForward?: boolean;
  readonly dryRun?: boolean;
  readonly warn?: (message: string) => void;
  readonly note?: (message: string) => void;
}

/** What {@link planProfileUpgrade} takes. */
export interface PlanProfileUpgradeOptions {
  readonly repoRoot: string;
  readonly config: HarnessConfig;
  readonly plan: WritePlan;
  readonly referenceToolchainPath?: string;
  readonly dryRun: boolean;
}

/** What {@link planProfileUpgrade} planned, and how it differs from the file it replaces. */
export interface ProfileUpgradePlan {
  readonly path: string;
  readonly repoPath: string;
  readonly previous: JsonObject | undefined;
  readonly rendered: JsonObject;
  /** Only the lists that change. */
  readonly delta: readonly ProfileEntryDelta[];
  /** {@link profileSettingChanges} from the file it replaces; empty when there is none to compare. */
  readonly settingChanges: readonly string[];
  readonly localAdditionCount: number;
  /** A file exists at {@link path} and is not a readable JSON object. */
  readonly previousUnreadable: boolean;
  readonly warnings: readonly string[];
  readonly notes: readonly string[];
}

/** What {@link profileDrift} takes. */
export interface ProfileDriftOptions {
  readonly repoRoot: string;
  readonly config: HarnessConfig;
  readonly onDisk: JsonObject;
}

/** How a profile on disk differs from the render, in both directions. */
export interface ProfileDrift {
  readonly missing: readonly ProfileEntry[];
  readonly unaccounted: readonly ProfileEntry[];
  /** Settings outside the entry lists that differ from the render. */
  readonly settings: readonly string[];
}

function renderWith(
  localAdditions: LocalAdditions | undefined,
  { repoRoot, config, referenceToolchainPath, pluginRootEntries, carryForward = true, dryRun, warn, note }: RenderCurrentProfileOptions,
): JsonObject {
  return renderProfile({
    repoRoot,
    config,
    workRoot: workRoot(repoRoot),
    referenceToolchainPath,
    pluginRootEntries,
    force: carryForward,
    localAdditions,
    dryRun,
    warn,
    note,
  });
}

/** The name a row's entries are reported under: `assertRunnable`'s spelling. */
function listLabel({ path, field }: ProfileEntryList): string {
  return field === undefined ? path : `${path}[].${field}`;
}

/** An element's comparable string; one with no usable string is compared, and so reported, as JSON. */
function entryName(element: JsonValue, field: string | undefined): string {
  const name = field === undefined ? element : isJsonObject(element) ? element[field] : undefined;
  return typeof name === 'string' && name.trim() !== '' ? name : JSON.stringify(element);
}

/** A row's distinct entries in file order. A non-list value there counts as one malformed element. */
function entriesIn(profile: JsonObject, { path, field }: ProfileEntryList): readonly string[] {
  const value = valueAt(profile, path.split('.'));
  if (value === undefined) return [];
  const elements = Array.isArray(value) ? value : [value];
  return [...new Set(elements.map((element) => entryName(element, field)))];
}

/** A row's entries in `profile` that `other` lacks. */
function entriesOnlyIn(profile: JsonObject, other: JsonObject, row: ProfileEntryList): readonly string[] {
  const excluded = new Set(entriesIn(other, row));
  return entriesIn(profile, row).filter((entry) => !excluded.has(entry));
}

/** What moving from `current` to `next` adds and removes, for each list that changes. */
export function profileEntryDelta(current: JsonObject | undefined, next: JsonObject): readonly ProfileEntryDelta[] {
  const before = current ?? {};
  return PROFILE_ENTRY_LISTS.flatMap((row) => {
    const added = entriesOnlyIn(next, before, row);
    const removed = entriesOnlyIn(before, next, row);
    return added.length === 0 && removed.length === 0 ? [] : [{ list: listLabel(row), added, removed }];
  });
}

/**
 * The dotted keys outside the entry lists and the rationale block whose value differs between two
 * profiles: a key on one side only, or a different value. Objects are compared key by key, so key
 * order is not a difference.
 */
export function profileSettingChanges(current: JsonObject, next: JsonObject, parent: readonly string[] = []): readonly string[] {
  const keys = [...new Set([...Object.keys(current), ...Object.keys(next)])];
  return keys.flatMap((key) => {
    if (parent.length === 0 && key === README_KEY) return [];
    const path = [...parent, key];
    const dotted = path.join('.');
    if (ENTRY_LIST_PATHS.has(dotted)) return [];
    const before = current[key];
    const after = next[key];
    if (isJsonObject(before) && isJsonObject(after)) return profileSettingChanges(before, after, path);
    return JSON.stringify(before) === JSON.stringify(after) ? [] : [dotted];
  });
}

/** The profile at `path`: absent and unreadable are different answers, and neither refuses the run. */
function readPreviousProfile(path: string): { readonly previous?: JsonObject; readonly unreadable: boolean } {
  let parsed: JsonValue | undefined;
  try {
    parsed = readJsonFile(path);
  } catch {
    return { unreadable: true };
  }
  if (parsed === undefined) return { unreadable: false };
  return isJsonObject(parsed) ? { previous: parsed, unreadable: false } : { unreadable: true };
}

/** Render the profile and enqueue it under `replace-if-changed`. A refused local file throws. */
export function planProfileUpgrade({
  repoRoot,
  config,
  plan,
  referenceToolchainPath,
  dryRun,
}: PlanProfileUpgradeOptions): ProfileUpgradePlan {
  const warnings: string[] = [];
  const notes: string[] = [];
  const localAdditions = readLocalAdditions(repoRoot);
  const rendered = renderWith(localAdditions, {
    repoRoot,
    config,
    referenceToolchainPath,
    dryRun,
    warn: (message) => warnings.push(message),
    note: (message) => notes.push(message),
  });

  const path = join(repoRoot, PROFILE_PATH);
  const { previous, unreadable } = readPreviousProfile(path);
  plan.add({ path, policy: 'replace-if-changed', content: rendered, label: 'unattended permission profile' });

  return {
    path,
    repoPath: PROFILE_PATH,
    previous,
    rendered,
    delta: profileEntryDelta(previous, rendered),
    settingChanges: previous === undefined ? [] : profileSettingChanges(previous, rendered),
    localAdditionCount: localAdditions?.count ?? 0,
    previousUnreadable: unreadable,
    warnings,
    notes,
  };
}

/**
 * Grade `onDisk` against the render. `missing` is what the render has and the disk lacks;
 * `unaccounted` is what the disk has and nothing here can answer for. A refused local file or render
 * throws.
 */
export function profileDrift({ repoRoot, config, onDisk }: ProfileDriftOptions): ProfileDrift {
  const localAdditions = readLocalAdditions(repoRoot);
  const expected = renderWith(localAdditions, { repoRoot, config, carryForward: false });
  const withPluginRoots = renderWith(localAdditions, { repoRoot, config, carryForward: false, pluginRootEntries: true });
  const roots = resolvedPluginRoots(repoRoot);

  // Resolved first: the target is the entry's raw text, so `<root>/../..` would otherwise pass as under `<root>`.
  const namesResolvedRoot = (entry: string): boolean => {
    const target = pluginRootEntryTarget(entry);
    return target !== undefined && roots.some((root) => isUnderDirectory(resolve(target), root));
  };

  const missing: ProfileEntry[] = [];
  const unaccounted: ProfileEntry[] = [];
  for (const row of PROFILE_ENTRY_LISTS) {
    const list = listLabel(row);
    for (const entry of entriesOnlyIn(expected, onDisk, row)) missing.push({ list, entry });

    const pluginRootGrants = new Set(entriesIn(withPluginRoots, row));
    for (const entry of entriesOnlyIn(onDisk, expected, row)) {
      if (pluginRootGrants.has(entry) || isToolchainEntry(entry, config)) continue;
      if (row.path === ALLOW_LIST_PATH && namesResolvedRoot(entry)) continue;
      unaccounted.push({ list, entry });
    }
  }
  return { missing, unaccounted, settings: profileSettingChanges(onDisk, expected) };
}
