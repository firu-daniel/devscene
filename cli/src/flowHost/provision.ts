/**
 * `init`'s post-plan provisioning of the walker's environment, `<scriptsDir>/python/.venv`.
 *
 * **The rule this module exists to enforce: it is `init`'s one caller of the provisioning script.**
 * It runs `bash <scriptsDir>/flow-host-provision.sh` and never re-implements the sync, so `init`, a
 * person and `doctor`'s remedy build the environment through one implementation
 * (`cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_provision`). The environment is
 * written into the adopting repository by `uv`, in that child, outside `cli/src/core/writer.ts`'s
 * engine; that header records the exception.
 *
 * - **It never fails `init`.** A failed sync — `uv` missing and no flow host included — or a child that
 *   could not run is a warning carrying the child's last stderr line and naming the command to re-run
 *   outside the sandbox; the packages the plan wrote stay valid.
 * - **`--dry-run` spawns nothing** and says what would run.
 * - **`spawnSync` rather than `execFileSync`**, for the reason `cli/src/commands/doctor.ts` →
 *   `runNotifier` gives: the warning quotes the child's stderr, which `execFileSync` would fold into
 *   its thrown error.
 */

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

import type { HarnessConfig } from '../config/model.js';
import { FLOW_HOST_PROVISION_SCRIPT_NAME, outerLoopScriptPath, outerLoopScriptsDir } from '../generators/outerLoopScripts.js';
import { scriptInvocation } from '../generators/scripts.js';
import { flowHostEnvDir } from './layout.js';

/** A cold `uv` cache downloads every dependency, which may take minutes. */
const PROVISION_TIMEOUT_MS = 900000;

/**
 * The file `uv` writes into every environment it creates: present means already provisioned.
 *
 * MIRRORS. `cli/templates/scripts/lib/harness-run-lib.sh` → `HR_FLOW_HOST_ENV_MARKER` spells it for
 * the shell; `cli/test/flow-host-provision.test.mjs` holds the two equal.
 */
export const ENV_MARKER_FILE = 'pyvenv.cfg';

/**
 * The environment variable that turns `init`'s default build of the walker's environment off; this
 * constant is its only spelling in `cli/src`, and it is read through this constant alone. It exists
 * for the test suite alone, so no fixture `init` reaches the network unasked
 * (`.claude/context/cli.md` → `## What "done" means here`). **No shipped path ever sets it.** `off`
 * makes `init` skip the build exactly as `--no-provision-python` does.
 */
export const FLOW_HOST_PROVISION_PROBE_ENV = 'DEVSCENE_FLOW_HOST_PROVISION_PROBE';

/** What {@link provisionFlowHost} takes. */
export interface ProvisionFlowHostOptions {
  readonly repoRoot: string;
  readonly config: HarnessConfig;
  readonly dryRun: boolean;
}

/** Lines for `init`'s notes and warnings blocks. */
export interface ProvisionFlowHostResult {
  readonly notes: readonly string[];
  readonly warnings: readonly string[];
}

/** The repo-relative command that provisions the environment: `bash <scriptsDir>/flow-host-provision.sh`. */
export function flowHostProvisionInvocation(config: HarnessConfig): string {
  return scriptInvocation(outerLoopScriptsDir(config), FLOW_HOST_PROVISION_SCRIPT_NAME);
}

/** Whether the walker's environment already exists in `repoRoot`. */
export function flowHostProvisioned(repoRoot: string, config: HarnessConfig): boolean {
  return existsSync(join(repoRoot, ...flowHostEnvDir(config).split('/'), ENV_MARKER_FILE));
}

/** The non-empty, right-trimmed lines of a captured stream. */
function lines(stream: string | null | undefined): string[] {
  return typeof stream === 'string'
    ? stream
        .split('\n')
        .map((line) => line.trimEnd())
        .filter((line) => line !== '')
    : [];
}

/** Build the Python environment the flow walker runs in, or under `dryRun` say what would. */
export function provisionFlowHost({ repoRoot, config, dryRun }: ProvisionFlowHostOptions): ProvisionFlowHostResult {
  const command = flowHostProvisionInvocation(config);
  const environment = flowHostEnvDir(config);
  if (dryRun) {
    return {
      notes: [`would build the Python environment the flow walker runs in at ${environment}/ with uv, by running ${command}`],
      warnings: [],
    };
  }

  const script = outerLoopScriptPath(repoRoot, config, FLOW_HOST_PROVISION_SCRIPT_NAME);
  const result = spawnSync('bash', [script], {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: PROVISION_TIMEOUT_MS,
    windowsHide: true,
  });
  const stderr = lines(result.stderr);
  const rerun = `the packages init wrote stay valid; run ${command} outside the sandbox to build it`;

  if (result.error !== undefined || result.signal !== null) {
    const failure = result.error as NodeJS.ErrnoException | undefined;
    const why =
      failure?.code === 'ENOENT'
        ? 'bash is not on PATH'
        : result.signal !== null
          ? `it was stopped by ${result.signal}; the bound on this call is ${PROVISION_TIMEOUT_MS / 1000}s`
          : `it could not be run to completion: ${failure?.message ?? 'unknown error'}`;
    return { notes: [], warnings: [`the Python environment the flow walker runs in was not built: ${why}. ${rerun}`] };
  }

  if (result.status === 0) {
    return { notes: [`built the Python environment the flow walker runs in at ${environment}/ with uv`], warnings: [] };
  }

  const lastLine = stderr.at(-1);
  return {
    notes: [],
    warnings: [
      `the Python environment the flow walker runs in was not built: ${command} ended with exit status ${String(result.status)}${
        lastLine === undefined ? '' : `: ${lastLine}`
      }. ${rerun}`,
    ],
  };
}
