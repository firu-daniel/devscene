`feat_flow_walker_uv_shipping` brings `graphscene/`, `devscene-flow-host/` and their `uv` requirement to adopters, so that #419's cutover finds the Python walker installed and provisioned in an adopting repository. Part of #376. Split out of #419 on 2026-11-24.

## Why

Today the Python packages run only in this repository. After #419, every flow that walks a graph runs `devscene-flow-walker` through `uv`, so an adopter without the packages, a provisioned environment and `uv` would have no walker. None of the shipping work depends on what #419 changes. #419 depends on it: its `flow-walker.sh` hand-off has to know where the package sits in an adopting repository, and how that environment gets provisioned. So this branch goes first. Shipping it before the cutover means adopters get `uv` as a requirement one release before anything uses it.

## Decided (2026-11-23, moved from #419)

- **DevScene requires `uv`.** Every flow that walks a graph needs it, which widens #376's "`uv` required where the engine runs". `graphscene/` and `devscene-flow-host/` ship in the npm package and run through `uv`, with no PyPI release before extraction (#425). Adopters never import the package (#418). They reach it only through the scripts `init` writes.
- **`devscene-flow-host` is DevScene's own package and stays in this repository** _(decided 2026-11-22)_. It ships inside the npm package, beside `graphscene/`.

## Decided (2026-11-24)

- **A change under `.github/workflows/` is pushed by hand.** If this branch changes a file under the repository's `.github/workflows/`, the run parks **before** the push that would carry it. The park's question asks for that push. The user pushes by hand, then drops an answer acknowledging it, and the run resumes. The unattended push guard refuses such a push, and a refused push fails the run.

## Leads

_Starting points from #419's leads and the 2026-11-24 status review, not requirements. The planning session decides what holds._

- **What ships:** the npm package carrying both Python packages' sources (`cli/package.json` → `files` carries `dist`, `scripts`, `templates` today); `init` provisioning once; a `doctor` check for `uv`; a `setup-uv` step in `devscene-run.yml`; the README requirement.
- **Where the packages live in an adopting repository**, and the path `flow-walker.sh` will pass as `--project`, is this branch's choice. #419 uses it.
- **Provisioning.** In this repository, `bash scripts/python-service.sh provision` installs the console script, outside the sandbox, and a run copy's bootstrap runs it. `python-service.sh` is not among the scripts `init` writes (`cli/src/generators/outerLoopScripts.ts`), so an adopter's run copy has no route to a provisioned environment yet.
- **The `setup-uv` step.** The shipped workflow is the template `cli/templates/github/workflows/devscene-run.yml`, not a file under this repository's `.github/workflows/`. Whether the push guard covers it is for planning to check. The rule above applies only if a file under `.github/workflows/` changes.
- **Whether `doctor` warns or fails** on a missing `uv` before #419 makes the walker need it.
- **Measured (2026-11-24, macOS, under a run's per-run profile):** inside the sandbox, `uv` runs, and `uv run --frozen --no-sync` without `--no-cache` exits `2` (`Failed to initialize cache at ~/.cache/uv`, refused by the sandbox). Anything this branch runs through `uv` inside a session needs `--no-cache`. The Linux leg is owed in #317.

## Depends on

#465. Ordered before #419.
