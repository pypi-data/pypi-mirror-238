import logging as log
from inspect import signature
from typing import Literal, Optional

import networkx as nx
import pandas as pd

from .base import (
    Centrality,
    Community,
    Convert,
    DEFAULT_ATTRS,
    DEFAULT_LAYOUT,
    Graph,
    Layout,
    Plot,
)
from .utils import (
    method_class,
    method_input,
)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = Literal["critical", "error", "warning", "info", "debug", "notset"]

AVAILABLE_ATTRS = method_class([Centrality, Community])
AVAILABLE_LAYOUTS = method_class([Layout])


class GraphExpress(Graph, Centrality, Community, Convert, Layout, Plot):

    def __init__(self, log_level: Optional[LOG_LEVEL] = "info"):
        super().__init__()
        self.log_level = log_level

        if log_level is not None:
            log.basicConfig(format=LOG_FORMAT, level=getattr(log, log_level.upper()))

    @staticmethod
    def compute(G: nx.Graph,
                attrs: Optional[list] = DEFAULT_ATTRS,
                fillna: Optional[None] = 0,
                normalize: bool = False,
                **kwargs) -> pd.DataFrame:
        """
        Returns centralities and communities in a single data frame indexed by node label.

        Centrality algorithms implemented:
            * `degree`
            * `in_degree`
            * `out_degree`
            * `weighted_degree`
            * `weighted_in_degree`
            * `weighted_out_degree`
            * `bridging_centrality`
            * `bridging_coef`
            * `brokering_centrality`

        Centrality algorithm wrappers:
            * `nx_centrality` ([networkx](https://networkx.org/documentation/stable/reference/algorithms/centrality.html))
            * `nk_centrality` ([networkit](https://networkit.github.io/dev-docs/python_api/centrality.html))

        Community algorithm wrappers:
            * `louvain `([python-louvain](https://python-louvain.readthedocs.io/en/latest/))
            * `leiden` ([leidenalg](https://leidenalg.readthedocs.io/en/stable/))
            * `cdlib_community` ([cdlib](https://cdlib.readthedocs.io/en/latest/reference/algorithms.html))
            * `nk_community` ([networkit](https://networkit.github.io/dev-docs/python_api/community.html))
        """
        df = pd.DataFrame()
        attrs = [attrs] if type(attrs) == str else attrs
        attr_input = method_input(globals(), AVAILABLE_ATTRS)

        if not G.order():
            raise RuntimeError(
                f"Graph is empty (nodes: {G.order()}, edges: {G.size()}")

        for attr in attrs:
            if attr not in AVAILABLE_ATTRS:
                raise RuntimeError(
                    f"Invalid node attribute ('{attr}'). " +
                    f"Available choices: {list(AVAILABLE_ATTRS.keys())}.")

        nkG = None
        if any("nkG" in attr_input[attr] for attr in attrs):
            log.debug("Converting NetworkX graph to Networkit format...")
            nkG = Convert.nx2nk(G)

        iG = None
        if any("iG" in attr_input[attr] for attr in attrs):
            log.debug("Converting NetworkX graph to igraph format...")
            iG = Convert.nx2ig(G)

        for attr in attrs:
            if attr not in df.columns:
                log.info(f"Computing '{attr}' attribute...")
                # Get function to compute attribute.
                method = getattr(globals()[AVAILABLE_ATTRS[attr]], attr)
                # Get graph required by function (NetworkX, Networkit, or igraph).
                graph = locals()[attr_input[attr]]
                # Pass keyword arguments or dictionary with attribute name.
                params = kwargs.get(attr, {arg: kwargs[arg] for arg in signature(method).parameters if arg in kwargs})
                # Compute attribute and assign to new data frame column.
                df[attr] = method(graph, **params) if G.order() else ()

        if normalize:
            # All attributes, except partitions (dtype=int).
            columns = df.select_dtypes(float).columns
            df[columns] = df[columns].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

        df.index = G.nodes()
        df.index.name = "id"

        return df.fillna(fillna)
