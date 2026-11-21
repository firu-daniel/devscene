# The probe route

## Resolved values

| Token | Class | How to resolve it |
|---|---|---|
| `<state_dir>` | config value | `stateDir` — the run-artifact tree every artifact path in this file sits under. Default `devscene/`; no path segment of it begins with a dot. |
| `<scripts_dir>` | config value | `scriptsDir` — the repo-relative directory the outer-loop scripts live in. |

## The route

A probe is one file under `<state_dir>/scratch/`, run with `bash <scripts_dir>/scratch-run.sh <state_dir>/scratch/<name>.<ext>` — one path argument, further arguments forwarded to the file, the interpreter taken from the extension (`.py`, `.js`, `.mjs`, `.cjs`, `.rb`, `.dart`, `.php`; never `.sh`), and any path outside that directory refused.

**The package-environment form.** `scratch-run.sh` runs a `.py` file under the `python3` on `PATH`, which sees none of a package's declared dependencies. Where the owning layer's conventions document routes that language's commands through a wrapper under `<scripts_dir>`, and that wrapper's usage states a probe form taking one file under `<state_dir>/scratch/`, a probe that imports what the package declares runs through that form instead; every other rule in this section holds unchanged. A wrapper's own refusal, such as an unprovisioned environment, is a probe you could not run.

Record the command and what the probe showed, never a pointer to the file: nothing under `<state_dir>/scratch/` is committed. A refusal the tool layer or the sandbox gives a command stays a refusal from inside a probe.

## A reviewer's probe

A reviewer's probe reads and computes; it never writes into the tree under review. Its probe file under `<state_dir>/scratch/` is the one file a citing reviewer writes beyond those its own definition names: every sentence in a citing reviewer's definition that bounds what it writes, or that has a `PASS` touch no disk, excepts that file, whether or not the sentence carries a citation to this heading. Nothing under that directory is committed, so the clean tree a `PASS` leaves still holds.

A probe the tool layer moves to the background is not waited on (`${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 6), and a finding resting on it is disclosed under `## A confirmation you did not execute`.

## A confirmation you did not execute

A finding confirmed only by reading — documented behaviour taken on trust, an interpreter not on `PATH`, a probe you could not run — says so in its own entry, naming what was read. An undisclosed one is a false report. Disclosure never changes a grade: the citer's own grading rules alone set severity.

## Who may cite this

These documents point at a section of this file:

- `${CLAUDE_PLUGIN_ROOT}/agents/branch-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/layer-implementer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/layer-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/review-plan-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/skeptic-reviewer.md`

A citer **points and never restates**, and no plugin asset beyond this list points at this file. A new citer joins this list. An edit that rewords or moves a heading updates every roster member in the same change. A document outside the plugin cites this file by its repo-relative path and is not a roster member.
