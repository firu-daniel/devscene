"""The `records` layer: reads the repository's records — `devscene.config.json`, the
flow-progress ledger, and the round and reviewer files — into plain values.

The rule: this layer imports the standard library and `devscene_flow_host.records` only, never
`graphscene`. It answers no GraphScene protocol.
"""
