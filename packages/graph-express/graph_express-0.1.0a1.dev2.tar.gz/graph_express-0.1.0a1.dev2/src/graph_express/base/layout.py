import igraph as ig
import logging as log
from abc import abstractmethod
from typing import Optional, Union

import networkx as nx
import pandas as pd
from datashader.layout import forceatlas2_layout

DEFAULT_LAYOUT = "forceatlas2"


class Layout():

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    @staticmethod
    def layout(G: Union[nx.Graph, list], layout: Optional[str] = DEFAULT_LAYOUT, **kwargs) -> pd.DataFrame:
        return getattr(Layout, f"{layout or DEFAULT_LAYOUT}_layout")(G, **kwargs)

    @staticmethod
    def circular_layout(G: Union[nx.Graph, list]) -> pd.DataFrame:
        """
        Circular algorithm implementation from `networkx`.
        """
        if G is None:
            raise TypeError(
                f"Circular layout requires either a graph object "
                f"or a list of nodes, received '{type(G).__str__}'."
            )

        return pd.DataFrame.from_dict(
            nx.circular_layout(G),
            orient="index",
            columns=["x", "y"],
        )

    @staticmethod
    def forceatlas2_layout(
        G: nx.Graph,
        pos: Union[list, dict, pd.DataFrame] = None,
        iterations: int = 100,
        linlog: bool = False,
        nohubs: bool = False,
        seed: int = None,
    ) -> pd.DataFrame:
        """
        ForceAtlas2 algorithm implementation from `datashader`.
        * [Paper](https://doi.org/10.1371/journal.pone.0098679)
        * [Reference](https://datashader.org/user_guide/Networks.html)
        """
        if pos is None:
            pos = Layout.random_layout(G)

        elif type(pos) == list:
            pos = Layout.circular_layout(pos)

        elif type(pos) == dict:
            pos = pd.DataFrame.from_dict(
                pos,
                orient="index",
                columns=["x", "y"],
            )

        edges = pd.DataFrame(
            G.edges(),
            columns=["source", "target"]
        )

        try:
            pos = forceatlas2_layout(
                nodes=pos,
                edges=edges,
                iterations=iterations,
                linlog=linlog,
                nohubs=nohubs,
                seed=seed,
            )
        except ValueError as e:
            log.warning(
                f"{e}: Failed to compute attraction (n={G.order()}, E={G.size()})."
            )

        return pos

    @staticmethod
    def kamada_kawai_layout(
        G: Union[nx.Graph, ig.Graph],
        dim: int = 2,
        index: str = "name",
    ) -> pd.DataFrame:
        """
        Kamada-Kawai algorithm implementation from `networkx`.
        * [Paper](https://doi.org/10.1016%2F0020-0190%2889%2990102-6)
        """
        if type(G) is not ig.Graph:
            iG = ig.Graph.from_networkx(G)
            index = "_nx_name"

        return pd.DataFrame(
            list(iG.layout("kk", dim=dim)),
            columns=["x", "y", "z"][:dim],
            index=iG.vs()[index]
        )

    @staticmethod
    def random_layout(G: nx.Graph, seed: int = None) -> pd.DataFrame:
        """
        Random algorithm implementation from `networkx`.
        """
        return pd.DataFrame.from_dict(
            nx.random_layout(G, seed=seed),
            orient="index",
            columns=["x", "y"],
        )
