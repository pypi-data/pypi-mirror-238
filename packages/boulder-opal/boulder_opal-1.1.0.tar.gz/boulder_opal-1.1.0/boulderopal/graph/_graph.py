# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""
Functionality related to the computational-flow graph object.

The Graph object and its associated data types (Tensor, Pwc, ...) are re-imported here to
allow their access directly from the client package.
"""
from typing import Any

from numpydoc.docscrape import NumpyDocString
from qctrlcommons.graph import Graph as BaseGraph

from boulderopal._nodes.composite.registry import (
    COMPOSITE_NAMESPACE_REGISTRY,
    COMPOSITE_NODE_REGISTRY,
)
from boulderopal._nodes.registry import (
    PRIMARY_NAMESPACE_REGISTRY,
    PRIMARY_NODE_REGISTRY,
)

# Nodes that shouldn't be exposed at the Graph root (as they are in a namespace).
_IGNORED_NODES = [  # graph.random nodes
    "random_choices",
    "random_colored_noise_stf_signal",
    "random_normal",
    "random_uniform",
]
_IGNORED_NODES += [  # graph.ions nodes
    "ms_dephasing_robust_cost",
    "ms_displacements",
    "ms_infidelity",
    "ms_phases",
    "ms_phases_multitone",
]


def _extend_method(
    obj: Any, method: str, method_name: str, check_exists: bool = True
) -> None:
    """
    Extend the specified object by adding methods as attributes.

    Parameters
    ----------
    obj : Any
        The object to which the node should be added.
    method : Any
        Method to be added to the object.
    method_name : str
        Name of the method to be added.
    check_exists : bool
        Whether to check if the method already exists as an
        attribute on the object.
    """
    if check_exists and hasattr(obj, method_name):
        raise AttributeError(f"existing attr {method_name} on namespace: {obj}")
    setattr(obj, method_name, method)


def _clean_doc(doc: str) -> str:
    """
    Remove the graph parameter from the doc.
    """
    doc_obj = NumpyDocString(doc)

    doc_obj["Parameters"] = [
        item for item in doc_obj["Parameters"] if item.name != "graph"
    ]

    return str(doc_obj)


class Graph(BaseGraph):  # pylint: disable=too-few-public-methods
    """
    A class for representing and building a Boulder Opal data flow graph.

    The graph object is the main entry point to the Boulder Opal graph ecosystem.
    You can call methods to add nodes to the graph, and use the `operations` attribute to get a
    dictionary representation of the graph.
    """

    def __init__(self) -> None:
        self._add_namespaces()
        super().__init__()

    def _add_namespaces(self) -> None:
        # We initialize the node namespaces to the graph in this way since they need access
        # to the initialized class object.
        for _composite_ns in COMPOSITE_NAMESPACE_REGISTRY:
            _extend_method(self, _composite_ns(self), _composite_ns.namespace_name)

        for _primary_ns in PRIMARY_NAMESPACE_REGISTRY:
            _ns = _primary_ns(self)
            _extend_method(self, _ns, _ns.__name__)  # type: ignore


# Set nodes to Graph.
for node_cls in PRIMARY_NODE_REGISTRY.legacy_registry.as_list():
    node = node_cls.create_graph_method()
    if node.__name__ not in _IGNORED_NODES:
        _extend_method(Graph, node, node.__name__)

# Set composite nodes to Graph.
for composite_node in COMPOSITE_NODE_REGISTRY:
    composite_node.__doc__ = _clean_doc(composite_node.__doc__)
    _extend_method(Graph, composite_node, composite_node.__name__)
