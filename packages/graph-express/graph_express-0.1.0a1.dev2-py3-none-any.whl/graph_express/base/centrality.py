import logging as log
from abc import abstractmethod
from typing import Optional

import networkit as nk
import networkx as nx
import pandas as pd

DEFAULT_ATTRS = [
    "degree",
    "in_degree",
    "out_degree",
    "weighted_degree",
    "weighted_in_degree",
    "weighted_out_degree",
]


class Centrality():

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    @staticmethod
    def degree(G):
        """ Degree centrality. """
        return pd\
            .Series([x[1] for x in G.degree()],
                    name="degree")\
            .astype(float)

    @staticmethod
    def in_degree(G):
        """ In-degree centrality. """
        return pd\
            .Series([x[1] for x in getattr(G, "in_degree", G.degree)],
                    name="in_degree")\
            .astype(float)

    @staticmethod
    def out_degree(G):
        """ Out-degree centrality. """
        return pd\
            .Series([x[1] for x in getattr(G, "out_degree", G.degree)],
                    name="out_degree")\
            .astype(float)

    @staticmethod
    def weighted_degree(G: nx.Graph, weight: str = "weight") -> pd.Series:
        """ Weighted degree centrality. """
        try:
            E = pd.DataFrame([(e[0], e[1], e[2][weight]) for e in G.edges(data=True)])
        except KeyError:
            log.debug(f"Edge attribute '{weight}' not found.")
            return Centrality.degree(G)

        W0 = E.iloc[:, [0, 2]].groupby(0).sum(weight)
        W1 = E.iloc[:, [1, 2]].groupby(1).sum(weight)

        W = W0\
            .add(W1, fill_value=0)\
            .squeeze("columns")\
            .astype(float)\
            .loc[list(G.nodes())]

        W.name = "weighted_degree"
        W.index = range(W.shape[0])
        return W.fillna(0)

    @staticmethod
    def weighted_in_degree(G: nx.Graph, weight: str = "weight") -> pd.Series:
        """ Weighted in-degree centrality. """
        try:
            E = pd.DataFrame([(e[0], e[1], e[2][weight]) for e in G.edges(data=True)])
        except KeyError:
            log.debug(f"Edge attribute '{weight}' not found.")
            return Centrality.in_degree(G)

        W = pd.Series(
            E.iloc[:, [1, 2]].groupby(1).sum(weight).squeeze("columns"),
            index=G.nodes()
        )
        W.name = "weighted_in_degree"
        W.index = range(W.shape[0])
        return W.fillna(0)

    @staticmethod
    def weighted_out_degree(G: nx.Graph, weight: str = "weight") -> pd.Series:
        """ Weighted out-degree centrality. """
        try:
            E = pd.DataFrame([(e[0], e[1], e[2][weight]) for e in G.edges(data=True)])
        except KeyError:
            log.debug(f"Edge attribute '{weight}' not found.")
            return Centrality.out_degree(G)

        W = pd.Series(
            E.iloc[:, [0, 2]].groupby(0).sum(weight).squeeze("columns"),
            index=G.nodes()
        )
        W.name = "weighted_out_degree"
        W.index = range(W.shape[0])
        return W.fillna(0)

    @staticmethod
    def bridging_centrality(G: nx.Graph,
                            betweenness: Optional[dict] = None,
                            bridging_coef: Optional[dict] = None) -> pd.Series:
        """
        Bridging centrality:
        * [Paper](https://cse.buffalo.edu/tech-reports/2006-05.pdf)
        """
        if not betweenness:
            betweenness = nx.betweenness_centrality(G)

        if not bridging_coef:
            bridging_coef = Centrality.bridging_coef(G)
            bridging_coef.index = G.nodes()

        bridging_centrality = [betweenness[node] * bridging_coef[node] for node in G.nodes()]

        return pd.Series(
            bridging_centrality,
            name="bridging_centrality"
        )

    @staticmethod
    def bridging_coef(G: nx.Graph) -> pd.Series:
        """
        Bridging coefficient:
        * [Paper](https://cse.buffalo.edu/tech-reports/2006-05.pdf)
        """
        bridging_coef = {}
        degree = nx.degree_centrality(G)

        for node in G.nodes():
            bridging_coef[node] = 0

            if degree[node] > 0:
                neighbors_degree = dict(
                    nx.degree(G, nx.neighbors(G, node))).values()

                sum_neigh_inv_deg = sum(
                    (1.0/d) for d in neighbors_degree)

                if sum_neigh_inv_deg > 0:
                    bridging_coef[node] = (1.0/degree[node]) / sum_neigh_inv_deg

        return pd.Series(
            list(bridging_coef.values()),
            name="bridging_coef"
        )

    @staticmethod
    def brokering_centrality(G: nx.Graph, clustering: Optional[dict] = None) -> pd.Series:
        """
        Brokering centrality:
        * [Paper](https://doi.org/10.1093/gbe/evq064)
        """
        degree = nx.degree_centrality(G)

        if not clustering:
            clustering = nx.clustering(G)

        brokering_centrality = [(1 - clustering[node]) * degree[node] for node in G.nodes()]

        return pd.Series(
            brokering_centrality,
            name="brokering_centrality"
        )

    def nx_centrality(G: nx.Graph, alg: str, **kwargs) -> pd.Series:
        """
        Wrapper for centrality algorithms implemented by NetworkX.
        * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html)
        """
        alg = getattr(nx, alg)

        return pd.Series(
            alg(G, **kwargs),
            name=alg
        )

    @staticmethod
    def nk_centrality(nkG: nk.Graph, alg: str, **kwargs) -> pd.Series:
        """
        Wrapper for centrality algorithms implemented by Networkit.
        * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html)

        ___

        Examples of available algorithms (version 10.1):
        - `ApproxBetweenness`:
            * [Paper](https://doi.org/10.1145/2556195.2556224)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.ApproxBetweenness)
        - `ApproxCloseness`:
            * [Paper](https://doi.org/10.1145/2660460.2660465)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.ApproxCloseness)
        - `Closeness`:
            * [Paper](https://www.theses.fr/2015USPCD010.pdf)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.Closeness)
        - `EstimateBetweenness`:
            * [Paper](http://doi.org/10.1137/1.9781611972887.9)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.EstimateBetweenness)
        - `EigenvectorCentrality`:
            * [Paper](https://doi.org/10.1007%2FBF01449896)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.EigenvectorCentrality)
        - `KadabraBetweenness`:
            * [Paper](https://arxiv.org/abs/1903.09422)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.KadabraBetweenness)
        - `KatzCentrality`:
            * [Paper](https://doi.org/10.1007/BF02289026)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.KatzCentrality)
        - `LaplacianCentrality`:
            * [Paper](https://doi.org/10.1016/j.ins.2011.12.027)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.LaplacianCentrality)
        - `LocalClusteringCoefficient`:
            * [Paper](https://doi.org/10.1137/1.9781611973198.1)
            * [Paper (turbo mode)](https://dl.acm.org/citation.cfm?id=2790175) - aimed at graphs with skewed, high degree distribution
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.LocalClusteringCoefficient)
        - `PageRank`:
            * [Paper](http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf)
            * [Reference](https://networkit.github.io/dev-docs/python_api/centrality.html?#networkit.centrality.PageRank)
        """
        alg = getattr(nk.centrality, alg)

        return pd.Series(
            alg(nkG, **kwargs).run().scores(),
            name=alg
        )
