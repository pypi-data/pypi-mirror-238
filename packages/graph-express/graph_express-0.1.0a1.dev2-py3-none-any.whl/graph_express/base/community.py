import logging as log
from abc import abstractmethod
from typing import Optional

import community
import igraph as ig
import leidenalg
import networkx as nx
import networkit as nk
import pandas as pd
from cdlib import algorithms as cdlib_algorithms
from cdlib import evaluation as cdlib_evaluation


class Community():

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    '''
    @staticmethod
    def label(G) -> None:
        raise NotImplementedError("Method not implemented.")
    '''

    @staticmethod
    def louvain(G: nx.Graph, **kwargs) -> pd.Series:
        """
        Louvain method for community detection.
        * [Paper](https://doi.org/10.1088/1742-5468/2008/10/P10008)
        * [Reference](https://python-louvain.readthedocs.io/en/latest/)
        """
        G = G.to_undirected() if G.is_directed() else G

        mod = community.best_partition(G, **kwargs)

        series = pd.Series(
            pd.to_numeric(list(mod.values()), downcast="integer"),
            index=range(G.order()),
            name="louvain",
        )

        modularity = community.modularity(mod, G)
        log.info(f"Modules (louvain): {series.unique().shape[0]+1} (Q={modularity:.3f})")
        return series

    @staticmethod
    def leiden(iG: ig.Graph, **kwargs) -> pd.Series:
        """
        Wrapper for the Leiden algorithm.
        * [Paper](https://doi.org/10.1038/s41598-019-41695-z)
        * [Reference](https://leidenalg.readthedocs.io/en/stable/)
        """
        mod = leidenalg.find_partition(
            iG,
            leidenalg.ModularityVertexPartition,
            **kwargs,
        )

        series = pd.Series(
            pd.to_numeric(mod.membership, downcast="integer"),
            name="leiden",
        )

        log.info(f"Modules (leiden): {max(mod.membership)+1} (Q={mod.quality():.3f})")
        return series

    @staticmethod
    def cdlib_community(G: nx.Graph,
                        alg: str,
                        evaluation: str = "newman_girvan_modularity",
                        to_undirected: Optional[bool] = False,
                        **kwargs) -> pd.Series:
        """
        Wrapper for community detection algorithms implemented by cdlib.
        * [Reference](https://cdlib.readthedocs.io/en/latest/reference/algorithms.html)
        """
        if G.is_directed() and to_undirected:
            log.debug("Converting directed graph to undirected...")
            G = G.to_undirected()

        mod = getattr(cdlib_algorithms, alg)(G, **kwargs)
        com = {x: i for i, x in enumerate(mod.communities) for x in x}

        series = pd.Series(
            pd.to_numeric(
                list(com.values()),
                downcast="integer"),
            index=list(com.keys()),
            name=f"cdlib_{alg}",
        )

        modularity = getattr(cdlib_evaluation, evaluation)(G, mod)
        log.info(f"Modules ({alg}): {series.unique().shape[0]+1} (Q={modularity.score:.3f})")
        return series

    @staticmethod
    def nk_community(nkG: nk.Graph,
                     alg: str,
                     to_undirected: Optional[bool] = False,
                     **kwargs) -> pd.Series:
        """
        Wrapper for community detection algorithms implemented by Networkit.
        * [Reference](https://networkit.github.io/dev-docs/python_api/community.html)
        """
        if nkG.isDirected() and to_undirected:
            log.debug("Converting directed graph to undirected...")
            nkG = nk.graphtools.toUndirected(nkG)

        mod = getattr(nk.community, alg)(nkG, **kwargs).run().getPartition()

        series = pd.Series(
            pd.to_numeric(mod.getVector(), downcast="integer"),
            name=f"nk_{alg}",
        )

        modularity = nk.community.Modularity().getQuality(mod, nkG)
        log.info(f"Modules ({alg}): {series.unique().shape[0]+1} (Q={modularity:.3f})")
        return series
