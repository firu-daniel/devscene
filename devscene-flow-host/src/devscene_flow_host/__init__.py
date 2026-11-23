"""The harness's GraphScene host.

It holds only the code that feeds GraphScene the harness's configuration, records, predicates,
executor configuration and hooks, and the commands over it; anything useful without DevScene
belongs in GraphScene; another DevScene Python integration gets its own `devscene`-prefixed
package.

The rule: this package imports only the standard library, itself and its declared runtime
dependencies. It reaches `graphscene` through its public surface only — `import graphscene` or
`from graphscene import <name in graphscene.__all__>`, never a submodule such as
`graphscene.engine` — and GraphScene never imports it (`tests/test_boundary.py`).
"""

__all__: list[str] = []
