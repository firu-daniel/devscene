# devscene-flow-host

**Who reads this:** a contributor changing this package. It owns what the package is, what it may depend on, how its lock follows GraphScene's, and how its toolchain is run here.

## What it is

`devscene-flow-host` is the harness's GraphScene host, imported as `devscene_flow_host`. It holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it, and no behaviour yet. Any other DevScene Python integration gets its own `devscene`-prefixed package rather than a place here. Anything useful without DevScene goes in GraphScene (`graphscene/`), not here.

It stays in this repository: it is not part of the npm package (`cli/package.json` → `files`), and adopters never import it.

## What it may depend on

- **The package imports only the standard library, itself and its declared runtime dependencies.** It reaches `graphscene` through its public surface only — `import graphscene` or `from graphscene import <name in graphscene.__all__>`, never a submodule such as `graphscene.engine` — and GraphScene never imports it.
- **`graphscene` is an editable path dependency on `../graphscene`** (`pyproject.toml` → `[tool.uv.sources]`), so one sync provisions both packages, this package's environment imports the checkout's current `graphscene/src/graphscene/`, and no release is needed.

`tests/test_boundary.py` enforces the rule.

## The lock follows GraphScene

This package's `uv.lock` pins GraphScene's own runtime dependencies as resolved through the path source. A change to `graphscene/pyproject.toml` → `[project] dependencies` re-locks this package too:

```
bash scripts/python-service.sh --package devscene-flow-host lock
```

`tests/test_graphscene_dependency.py` fails until it is done.

## Running the toolchain

Every command goes through `scripts/python-service.sh`, run from the repository root.

Lint:

```
bash scripts/python-service.sh --package devscene-flow-host lint
```

Typecheck:

```
bash scripts/python-service.sh --package devscene-flow-host typecheck
```

Test:

```
bash scripts/python-service.sh --package devscene-flow-host test
```

`test` forwards paths to `pytest`, relative to `devscene-flow-host/`:

```
bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py
```

Provision every package's environment, outside any sandbox:

```
bash scripts/python-service.sh provision
```

## Gating

The package is gated by gate 13's legs 13h–13j ([`docs/development.md`](../docs/development.md) → `## 5. Verifying a change`).
