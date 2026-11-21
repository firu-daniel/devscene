"""The `adapters` layer: what touches a format or the outside world — the shipped schema, the
mapping from parsed JSON to the typed model, and reading a file from disk.

The rule: this layer imports `graphscene.model`, `jsonschema` and the standard library, and never
imports `graphscene.engine`.
"""
