/**
 * Whether the plugin installed on this machine and this CLI are the same version, which of them is
 * behind when they are not, and what an operator is told to do about it.
 *
 * **The rule this module exists to enforce: one comparison and one wording serve the `--upgrade`
 * refusal, the dry-run note, the upgrade report and `doctor`; the complete warning sentence has one
 * producer, {@link pluginCliMismatchWarning}; and no remedy pins the CLI to an older plugin.** The two
 * halves are released together, so the way out of a mismatch is always forward, to the latest of both.
 *
 * Order is semantic-version precedence. A version that does not parse, or two different strings of
 * equal precedence, cannot say which half is behind, so `older` is `'unknown'`.
 */

import { pinnedCliCommand } from '../generators/githubWorkflows.js';
import { PLUGIN_KEY } from '../generators/projectSettings.js';

/** Two different versions, and which of them is behind. */
export interface PluginCliMismatch {
  readonly pluginVersion: string;
  readonly cliVersion: string;
  readonly older: 'plugin' | 'cli' | 'unknown';
}

/** A version reduced to the parts that decide precedence; build metadata decides nothing. */
interface ParsedVersion {
  readonly release: readonly bigint[];
  readonly prerelease: readonly string[];
}

const NUMBER = '0|[1-9]\\d*';
const PRERELEASE_IDENTIFIER = `(?:${NUMBER}|\\d*[A-Za-z-][0-9A-Za-z-]*)`;
const BUILD_IDENTIFIER = '[0-9A-Za-z-]+';
const VERSION_SHAPE = new RegExp(
  `^(${NUMBER})\\.(${NUMBER})\\.(${NUMBER})` +
    `(?:-(${PRERELEASE_IDENTIFIER}(?:\\.${PRERELEASE_IDENTIFIER})*))?` +
    `(?:\\+${BUILD_IDENTIFIER}(?:\\.${BUILD_IDENTIFIER})*)?$`,
);
const NUMERIC_IDENTIFIER = /^\d+$/;

function parseVersion(version: string): ParsedVersion | undefined {
  const match = VERSION_SHAPE.exec(version);
  if (match === null) return undefined;
  return {
    release: match.slice(1, 4).map((part) => BigInt(part)),
    prerelease: match[4]?.split('.') ?? [],
  };
}

function compareValues<T extends bigint | string>(left: T, right: T): number {
  if (left < right) return -1;
  return left > right ? 1 : 0;
}

/** Element by element; a list that is a prefix of the other sorts first. */
function compareLists<T>(left: readonly T[], right: readonly T[], compare: (a: T, b: T) => number): number {
  for (const [index, item] of left.entries()) {
    const other = right[index];
    if (other === undefined) return 1;
    const order = compare(item, other);
    if (order !== 0) return order;
  }
  return left.length === right.length ? 0 : -1;
}

function comparePrereleaseIdentifiers(left: string, right: string): number {
  const leftNumeric = NUMERIC_IDENTIFIER.test(left);
  const rightNumeric = NUMERIC_IDENTIFIER.test(right);
  if (leftNumeric && rightNumeric) return compareValues(BigInt(left), BigInt(right));
  if (leftNumeric !== rightNumeric) return leftNumeric ? -1 : 1;
  return compareValues(left, right);
}

function comparePrecedence(left: ParsedVersion, right: ParsedVersion): number {
  const release = compareLists(left.release, right.release, compareValues);
  if (release !== 0) return release;
  // A release outranks its prereleases, the reverse of the prefix rule compareLists applies.
  const leftIsRelease = left.prerelease.length === 0;
  const rightIsRelease = right.prerelease.length === 0;
  if (leftIsRelease || rightIsRelease) return Number(leftIsRelease) - Number(rightIsRelease);
  return compareLists(left.prerelease, right.prerelease, comparePrereleaseIdentifiers);
}

function olderHalf(pluginVersion: string, cliVersion: string): PluginCliMismatch['older'] {
  const plugin = parseVersion(pluginVersion);
  const cli = parseVersion(cliVersion);
  if (plugin === undefined || cli === undefined) return 'unknown';
  const order = comparePrecedence(plugin, cli);
  if (order === 0) return 'unknown';
  return order < 0 ? 'plugin' : 'cli';
}

/** The mismatch between the two versions; `undefined` when they match or the plugin's is unreadable. */
export function pluginCliMismatch(pluginVersion: string | undefined, cliVersion: string): PluginCliMismatch | undefined {
  if (pluginVersion === undefined || pluginVersion === cliVersion) return undefined;
  return { pluginVersion, cliVersion, older: olderHalf(pluginVersion, cliVersion) };
}

/** What differs, as a clause a caller places inside its own sentence. */
export function pluginCliMismatchSummary({ pluginVersion, cliVersion }: PluginCliMismatch): string {
  return `the installed plugin is version ${pluginVersion} and this CLI is version ${cliVersion}`;
}

/** What to do, as a clause. `'unknown'` takes the longer route: it is right whichever half is behind. */
export function pluginCliMismatchRemedy({ older }: PluginCliMismatch): string {
  const upgrade = `run \`${pinnedCliCommand('latest')} init --upgrade\``;
  if (older === 'cli') return upgrade;
  return `update the plugin with \`claude plugin update ${PLUGIN_KEY}\`, restart any open session, then ${upgrade}`;
}

function capitalized(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/** The complete warning `doctor` and the upgrade report print. */
export function pluginCliMismatchWarning(mismatch: PluginCliMismatch): string {
  return `${capitalized(pluginCliMismatchSummary(mismatch))}. ${capitalized(pluginCliMismatchRemedy(mismatch))}.`;
}
