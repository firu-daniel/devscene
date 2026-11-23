`feat_graphscene_cli` adds GraphScene's thin command line, a wrapper over the library for hosts not written in Python. Part of #376.

## Why

A host in another language, or a shell script, should be able to load and check a graph and walk it step by step without writing Python. Split out of #418 on 2026-11-22, so #418 holds only DevScene's side.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- **A thin wrapper over the library, with no DevScene names:** no `devscene.config.json`, no `stateDir`, no plugin path. `graphscene/tests/test_boundary.py` already refuses `devscene*` imports.
- **It lives in the `facade` layer,** which `.claude/context/graphscene.md` and `graphscene/README.md` → `## The layers` name as the home of a thin command-line entry point.
- **Commands to weigh:** `check <graph>` (load and report every violation), and `start` / `next` / `current` over a state file the caller names, with predicate answers passed in (flags, or a file) since the CLI reads no configuration. "Cannot answer" refuses, as the walk does.
- **Output for a rejection:** a static `Violation` reads `<path>: <check-id>: <detail>`, with the check id at the start of the reason (`graphscene.engine.static_check`, `graphscene.engine.references`), not in a field. How the CLI prints findings, and whether it exposes the check id separately, is this branch's. #459's checker comparison (moved there from #419 on 2026-11-23) may want the id as its own field.
- **Output for a step:** JSON is the natural form for a caller in another language. The `key: value` lines `flow-walker.sh` prints are DevScene's wire format and belong to #418, not here.
- **An entry point** declared in `pyproject.toml`'s `[project.scripts]`, run through `uv run --frozen --no-sync`.
- #425's adopter-integration milestone names this CLI as the route for hosts not written in Python.

## Depends on

None open. `Walker` (#416) and `load_graph` are on `dev`.
