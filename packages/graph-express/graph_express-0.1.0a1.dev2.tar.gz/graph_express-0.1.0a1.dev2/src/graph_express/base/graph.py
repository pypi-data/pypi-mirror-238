from abc import abstractmethod
from os.path import isfile, splitext
from typing import Optional

import igraph as ig
import networkit as nk
import networkx as nx
import pandas as pd
from networkx_gdf import GDF

READERS = [
    "gexf",
    "gml",
    "graphml",
    "leda",
    "pajek",
    "pickle",
    "shp",
    # "yaml",
]

WRITERS = [
    "gexf",
    "gml",
    "graphml",
    "pajek",
    "shp",
    # "yaml,
]


class Graph(GDF):

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    @staticmethod
    def graph(
        directed: bool = False,
        multigraph: bool = False,
    ) -> nx.Graph:
        """ Returns NetworkX graph object. """
        if multigraph:
            return nx.MultiDiGraph() if directed else nx.MultiGraph()
        return nx.DiGraph() if directed else nx.Graph()

    @staticmethod
    def adjacency(G: nx.Graph):
        """ Returns Pandas adjacency matrix from graph. """
        return nx.to_pandas_adjacency(G).astype(int, errors="ignore")

    @staticmethod
    def compose(list_of_graphs: list) -> nx.Graph:
        """ Returns a NetworkX graph composed from a list of graphs. """
        C = list_of_graphs[0]

        for G in list_of_graphs[1:]:
            C = nx.compose(C, G)

        return C

    @staticmethod
    def density(G: nx.Graph, str=False) -> float:
        """ Returns graph density, measure of its completeness. """
        return f"{100*nx.density(G):.2f}%" if str else nx.density(G)

    @staticmethod
    def diameter(G: nx.Graph) -> float:
        """ Returns graph diameter, measure of its extension. """
        return nx.diameter(G)

    @staticmethod
    def edges(G: nx.Graph) -> pd.DataFrame:
        """ Returns Pandas edge list from graph. """
        return nx.to_pandas_edgelist(G)

    @staticmethod
    def info(G: nx.Graph) -> None:
        """ Quickly describes graph object. """
        print(f"Graph ({'directed' if G.is_directed() else 'undirected'}) "
              f"has {G.order()} nodes and {G.size()} edges (density: {Graph.density(G, True)}).")

    @staticmethod
    def is_graph(object, instances=[nx.Graph, nx.DiGraph, nx.MultiGraph, nk.Graph, ig.Graph]) -> bool:
        """ Returns True if object is a known graph instance. """
        return any(isinstance(object, graph) for graph in instances)

    @staticmethod
    def is_graph_supported(filepath: str) -> bool:
        """ Returns True if file format is supported. """
        return splitext(filepath)[-1].lower().lstrip(".") in READERS

    @staticmethod
    def isolates(G: nx.Graph) -> list:
        """ Returns list of node isolates. """
        return list(nx.isolates(G))

    @staticmethod
    def k_core(G: nx.Graph, k: int) -> nx.Graph:
        """ Returns k-cores after removing self-loops. """
        G.remove_edges_from(nx.selfloop_edges(G))
        return nx.k_core(G, k)

    @staticmethod
    def nodes(G: nx.Graph) -> pd.DataFrame:
        """ Returns Pandas node list from graph. """
        return pd.DataFrame(
            dict(G.nodes(data=True)).values(),
            index=G.nodes(),
        )

    @staticmethod
    def read_graph(path: str, ext: Optional[str] = None) -> nx.Graph:
        """ Returns a NetworkX graph object from file. """
        if not isinstance(path, str):
            raise TypeError(f"Expected 'str' type, got '{type(path).__name__}'.")

        if isfile(path):
            if not ext:
                ext = splitext(path)[1].lower().lstrip(".")

            if ext in READERS:
                return getattr(nx, f"read_{ext}")(path)

            if ext == "gdf":
                raise RuntimeError(
                    "Please use the `read_gdf()` method to import Geographic Data Files.")

            raise RuntimeError(
                f"Unidentified file extension (ext='{ext}'). Accepted formats: {READERS}.")

        raise FileNotFoundError(f"File '{path}' not found.")

    @staticmethod
    def remove_edges(G: nx.Graph, edges: list) -> nx.Graph:
        """ Remove node self-connections. """
        G.remove_edges_from(edges)
        return G

    @staticmethod
    def remove_nodes(G: nx.Graph, nodes: list) -> nx.Graph:
        """ Remove node self-connections. """
        G.remove_nodes_from(nodes)
        return G

    @staticmethod
    def remove_selfloops(G: nx.Graph) -> nx.Graph:
        """ Remove node self-connections. """
        G.remove_edges_from(nx.selfloop_edges(G))
        return G

    @staticmethod
    def set_node_attrs(G: nx.Graph, node_attr: pd.DataFrame) -> nx.Graph:
        """ Returns NetworkX Graph object with node attributes. """
        for attr in node_attr:
            nx.set_node_attributes(G, node_attr[attr], attr)
        return G

    @staticmethod
    def write_graph(G: nx.Graph, filepath: str, node_attr: Optional[pd.DataFrame] = None) -> None:
        """ Writes a NetworkX graph object to file, if supported. """
        ext = splitext(filepath)[1].lower().lstrip(".")

        if isinstance(node_attr, pd.DataFrame):
            for attr in node_attr.columns:
                nx.set_node_attributes(G, node_attr[attr], attr)

        if ext in WRITERS:
            return getattr(nx, f"write_{ext}")(G, filepath)

        if ext == "gdf":
            raise RuntimeError(
                "Please use the `write_gdf()` method to export Geographic Data Files.")

        raise RuntimeError(
            f"Unidentified file extension (ext='{ext}'). Accepted formats: {WRITERS}.")
