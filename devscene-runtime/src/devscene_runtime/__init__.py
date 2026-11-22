"""DevScene's own Python runtime.

It holds only DevScene's meanings; anything useful without DevScene belongs in GraphScene.

The rule: this package imports only the standard library, itself and its declared runtime
dependencies. It reaches `graphscene` through its public surface only — `import graphscene` or
`from graphscene import <name in graphscene.__all__>`, never a submodule such as
`graphscene.engine` — and GraphScene never imports it (`tests/test_boundary.py`).
"""

__all__: list[str] = []
