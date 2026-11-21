"""The `model` layer: the typed flow-graph model and the one error shape every stage reports in.

The rule: this layer imports the standard library only. A `typing.Protocol` that an adapter
implements and the engine drives is declared here, so an adapter never imports the engine.
"""
