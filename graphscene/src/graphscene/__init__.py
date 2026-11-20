"""GraphScene, a generic flow-graph navigation library.

The boundary: this package imports only the standard library, itself and its declared runtime
dependencies, and it never reads the harness's configuration file. Harness integration lives in a
separate distribution that depends on this one, never the reverse (`tests/test_boundary.py`).
"""

from graphscene.vocabulary import vocabulary_violations

__all__: list[str] = ["vocabulary_violations"]
