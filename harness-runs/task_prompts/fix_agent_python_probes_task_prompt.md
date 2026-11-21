`fix_agent_python_probes` makes Python reachable for a run's agents where it is missing today, without widening the unattended permission profile: the end-of-branch reviewers get a working route to run a Python probe inside the package's own environment, and implementers check a Python layer's lint and types per unit, not only at Run gates.

## Why

`feat_graphscene_graph_model`'s run (#414) hit both gaps (`harness-runs/improvement_observations/feat_graphscene_graph_model.md` on that branch):

**Reviewers could not run a probe.** Three reviewers graded findings without reproducing them, because every Python call they tried was refused:

- `branch-reviewer`: "couldn't run a probe because the command was refused" (code-review finding 3, `jsonschema`'s integral-float behaviour);
- `review-plan-reviewer`: "the sandbox refused the Python call";
- `skeptic-reviewer`: "the sandbox refused every attempt to execute Python". Both Must Fix findings of that run (code-review 3, skeptic 1) shipped as read-only proofs.

The refusal is the permission profile, not the OS sandbox: runs use `dontAsk`, so a bare `python3 …` or `uv run …` is refused because no allow rule matches it. A sanctioned probe route already exists, `scripts/scratch-run.sh`, and it has two gaps:

1. **Only `layer-implementer` and `layer-reviewer` are told it exists** (`plugin/agents/layer-reviewer.md` → *Run the probe that would settle it*). `branch-reviewer`, `skeptic-reviewer` and `review-plan-reviewer` are not, so they reached for an interpreter and were refused.
2. **`.py` runs the system `python3`** (`SCRATCH_INTERPRETERS` in `scripts/scratch-run.sh`), not a package's synced environment, so a probe importing `graphscene`, `jsonschema` or anything else the package declares fails even when the route is found.

**Implementers never ran the Python layer's lint and type check.** A unit runs `<typecheck_cmd>`, `commands.typecheck` (`bash scripts/typecheck.sh`), over the whole tree (`plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 2), and that command does not reach gate 13's `ruff` / `mypy` legs (13a/13b, 13e/13f). Every implementer return in that run said so. The defects surfaced only at the end-of-branch review and at Run gates: code-review findings 1 (strict `mypy`) and 2 (`ruff`), and Run gates round 1's `13e` `I001`. That cost 3 fix units and a second Run gates round, more than the probe gap did.

## Decided (2026-11-21)

- **No new allow rule.** No `Bash(python3:*)`, `Bash(uv:*)` or other interpreter-wide grant: an inline program (`-c`) cannot be audited by the script-allowlist guard's construct scan, and the profile `_README`'s package-manager paragraph already refuses grants of that breadth. Every route stays a fixed script under `<scripts_dir>` that decides **which file** runs.
- **The trust class does not change.** A probe and a lint or type check run inside the run's OS sandbox, like the test files an implementer writes and `scripts/test.sh` already runs: writes limited to the run copy and its temporary directory, no network domain allowed, the credential files masked (`sandbox.credentials.files`), and every push scanned for a credential by `push-branch.sh`. What scratch-run adds is a probe file under `<state_dir>/scratch/`, gitignored by its contents.
- **Both gaps are this branch's scope.** It runs before #434, a refactor across every `graphscene/` module, which would hit the per-unit gap hardest.
- **This repository's own copies change in the same branch.** Runs use the main checkout's `scripts/` and `plugin/` in place. A script changed under `cli/templates/scripts/` has its self-adoption copy under `scripts/` updated with it (`scripts/scratch-run.sh` and `cli/templates/scripts/scratch-run.sh` are identical today), so the next run sees the change once the main checkout pulls the merge.

## Leads

_The leads below are starting points, not requirements. The planning session decides what holds when this branch is planned._

- **Reviewer instructions.** The `layer-reviewer` paragraph is the model: the probe file under `<state_dir>/scratch/`, one path argument, the extension naming the interpreter, the command and its output recorded rather than a pointer to the file, and *a probe reads and computes; it never writes into the tree under review*. A reviewer runs no mutation check: its contract is read-only on the tree, unlike the implementer's.
- **A probe inside a package's environment.** Candidates, for planning to weigh:
  - a `python-service.sh` verb, e.g. `--package <dir> probe <scratch-file> [args]`, that applies the same path test as scratch-run (`hr_scratch_path_var` in `scripts/lib/harness-run-lib.sh`) and runs the file through the leg flags the gate legs use (`uv run --frozen --no-sync --no-cache`), so it neither reaches the network nor changes the environment, and an unprovisioned package exits `3` as the gate legs do;
  - scratch-run selecting a package's `<package>/.venv` interpreter for a `.py` file under a package-named scratch path.

  The first keeps scratch-run's single-token interpreter table as it is (its header, *WHAT THAT COSTS*, explains why that table cannot express a two-word toolchain) and reuses `python-service.sh`'s package table, which already knows each package's environment.
- **The per-unit lint and type check.** Candidates:
  - this repository's `scripts/typecheck.sh` (the `commands.typecheck` wrapper) also running each Python package's `python-service.sh --package <dir> lint` and `typecheck`, so units get them with no instruction change; an unprovisioned package is exit `3` there and must not read as a type error;
  - a per-layer check command a unit runs for the layer it touched, so a TypeScript-only unit does not pay for `mypy`. That is a configuration and instruction change across adopters, larger than the first.

  The gate legs already grade an unprovisioned environment `BLOCKED`; whichever route lands must keep that distinction for a unit too.
- **Reachability is already there; check it rather than add it.** `autonomous-script-allowlist-guard.sh` auto-allows a `.sh` under `<scripts_dir>` whose basename is not in `DENY_SCRIPT_BASENAMES`; `python-service.sh` is not on that list. If a new verb lands there, no profile change should be needed. Planning should confirm with the guard's own rules, not assume it.
- **`python-service.sh`'s network and environment verbs (`lock`, `sync`, `provision`) are reachable by an agent today** under the same rule. Inside the sandbox they fail (no network, the shared `uv` cache not writable), so nothing leaks, but they are operator verbs. Whether to refuse them when called from a run, rather than let them fail late, is worth a look while this script is open.

## Depends on

Nothing. Runs after `feat_graphscene_graph_model` (#414) merges, before #434.
