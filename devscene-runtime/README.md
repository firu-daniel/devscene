# devscene-runtime

**Who reads this:** a contributor changing this package. It owns what the package is, what it may depend on, how its lock follows GraphScene's, and how its toolchain is run here.

## What it is

`devscene-runtime` is DevScene's own Python runtime, imported as `devscene_runtime`. It holds only DevScene's meanings, and no behaviour yet. Anything useful without DevScene goes in GraphScene (`graphscene/`), not here.

It stays in this repository: it is not part of the npm package (`cli/package.json` → `files`), and adopters never import it.

## What it may depend on

- **The package imports only the standard library, itself and its declared runtime dependencies.** It reaches `graphscene` through its public surface only — `import graphscene` or `from graphscene import <name in graphscene.__all__>`, never a submodule such as `graphscene.engine` — and GraphScene never imports it.
- **`graphscene` is an editable path dependency on `../graphscene`** (`pyproject.toml` → `[tool.uv.sources]`), so one sync provisions both packages, this package's environment imports the checkout's current `graphscene/src/graphscene/`, and no release is needed.

`tests/test_boundary.py` enforces the rule.

## The lock follows GraphScene

This package's `uv.lock` pins GraphScene's own runtime dependencies as resolved through the path source. A change to `graphscene/pyproject.toml` → `[project] dependencies` re-locks this package too:

```
bash scripts/python-service.sh --package devscene-runtime lock
```

`tests/test_graphscene_dependency.py` fails until it is done.

## Running the toolchain

Every command goes through `scripts/python-service.sh`, run from the repository root.

Lint:

```
bash scripts/python-service.sh --package devscene-runtime lint
```

Typecheck:

```
bash scripts/python-service.sh --package devscene-runtime typecheck
```

Test:

```
bash scripts/python-service.sh --package devscene-runtime test
```

`test` forwards paths to `pytest`, relative to `devscene-runtime/`:

```
bash scripts/python-service.sh --package devscene-runtime test tests/test_boundary.py
```

Provision every package's environment, outside any sandbox:

```
bash scripts/python-service.sh provision
```

## Gating

The package is gated by gate 13's legs 13h–13j ([`docs/development.md`](../docs/development.md) → `## 5. Verifying a change`).
