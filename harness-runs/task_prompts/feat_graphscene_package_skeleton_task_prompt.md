`feat_graphscene_package_skeleton` creates GraphScene as an isolated Python library inside this repository, with its toolchain and gates, before any engine code. Part of #376.

## Why

Building it here avoids a release cycle on every change while the harness depends on it. Extraction later stays cheap only if the boundary between the generic library and the harness is enforced from the first commit.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- Its own directory and `pyproject.toml`, set up like `docs-retrieval-service/` (ruff, strict mypy, pytest), Python >= 3.11 (#376).
- The harness-specific side (config reading, the `claude` executor, the planning hooks) kept apart from the library, with the dependency pointing one way only.
- A test or check that catches the library importing harness code or reading `devscene.config.json`.
- A layer in `devscene.config.json` and its `CLAUDE.md` row, so the architecture reviewer sees the boundary - leave this as a manual action owed after the branch merges, if it can't be done during the run.
- Wired into the gates, through #411.

## Depends on

#411
