import logging as log
from abc import abstractmethod
from typing import Optional, Union

import igraph as ig
import networkx as nx
import networkit as nk
import pandas as pd


class Convert():

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    @staticmethod
    def ig2nk(iG: ig.Graph) -> nk.Graph:
        """ Returns igraph graph as NetworkX object. """
        return Convert.nx2nk(iG.to_networkx())

    @staticmethod
    def ig2nx(iG: ig.Graph) -> nx.Graph:
        """ Returns igraph graph as NetworkX object. """
        return iG.to_networkx()

    @staticmethod
    def nk2ig(nkG: nk.Graph, index=[]) -> ig.Graph:
        """ Returns Networkit graph as igraph object. """
        iG = ig.Graph(directed=nkG.isDirected())
        iG.add_vertices(list(nkG.iterNodes()) if not index else index)
        iG.add_edges(list(nkG.iterEdges()))
        iG.es["weight"] = list(nkG.iterEdgesWeights())
        return iG

    @staticmethod
    def nk2nx(nkG: nk.Graph, index={}) -> nx.Graph:
        """ Returns Networkit graph as NetworkX object. """
        G = nk.nxadapter.nk2nx(nkG)
        G = nx.relabel.relabel_nodes(G, index)
        return G

    @staticmethod
    def nx2ig(G: nx.Graph) -> ig.Graph:
        """ Returns NetworkX graph as igraph object. """
        iG = ig.Graph.from_networkx(G)
        # edgelist = nx.to_pandas_edgelist(G)
        # for attr in edgelist.columns[2:]:
        #     iG.es[attr] = edgelist[attr]
        return iG

    @staticmethod
    def nx2nk(G: nx.Graph) -> nk.Graph:
        """ Returns NetworkX graph as Networkit object. """
        return nk.nxadapter.nx2nk(G) if G.order() > 0 else nk.Graph()

    @staticmethod
    def pd2nx(
        edges: pd.DataFrame,
        nodes: Optional[pd.DataFrame] = None,
        source: Optional[str] = None,
        target: Optional[str] = None,
        edge_attr: Optional[Union[list, bool]] = True,
        node_attr: Optional[Union[list, bool]] = True,
        directed: Optional[bool] = True,
        multigraph: Optional[bool] = False,
    ) -> nx.Graph:
        """ Returns NetworkX graph object from Pandas data frames. """

        if not (source and target):
            if edges.shape[1] == 2:
                source, target = edges.columns.tolist()
            else:
                raise RuntimeError(f"Missing 'source' and/or 'target' attributes.")

        if any(_ not in edges.columns for _ in (source, target)):
            raise RuntimeError("Missing 'source' and/or 'target' attributes. "
                               f"Received: {[source, target]}, available: {edges.columns.tolist()}.")

        # Allow multiple edges among nodes if found.
        if multigraph is None:
            multigraph = 1 != edges[[source, target]].value_counts(ascending=True).unique()[-1]

        # Object type to build graph with.
        if multigraph:
            create_using = nx.MultiDiGraph() if directed else nx.MultiGraph()
        create_using = nx.DiGraph() if directed else nx.Graph()

        # List of edge attributes.
        if edge_attr is True:
            edge_attr = [_ for _ in edges.columns.tolist() if _ not in (source, target)]

        # Remove null and empty values.
        edges[source] = edges[source].apply(lambda x: None if x == "" else x)
        edges[target] = edges[target].apply(lambda x: None if x == "" else x)
        edges.dropna(subset=[source, target], how="any", inplace=True)

        # Consider edge weights.
        if not multigraph and "weight" not in edges.columns:
            edge_attr = ["weight"] + (edge_attr if edge_attr else [])
            weights = edges[[source, target]].value_counts()

            with pd.option_context("mode.chained_assignment", None):
                edges["weight"] = [weights.loc[x, y] for x, y in zip(edges[source], edges[target])]

        # Convert edge list to graph.
        G = nx\
            .convert_matrix\
            .from_pandas_edgelist(edges,
                                  source=source,
                                  target=target,
                                  edge_attr=edge_attr or None,
                                  create_using=create_using)

        # Assign attributes to nodes in graph.
        if type(nodes) != type(None):
            for attr in (list(nodes.columns) if node_attr == True else (node_attr or [])):
                nx.set_node_attributes(G, nodes[attr], attr)

        return G