from argparse import ArgumentParser
from inspect import signature
from os.path import isfile, splitext
from sys import argv

import networkx as nx
import pandas as pd

from ..graph_express import (
    GraphExpress,
    AVAILABLE_ATTRS,
    AVAILABLE_LAYOUTS,
    DEFAULT_ATTRS,
    DEFAULT_LAYOUT,
)

gx = GraphExpress()


def main():
    args = argparser()
    args["attrs"] = DEFAULT_ATTRS + [_ for _ in (args["attrs"] or []) if _ not in DEFAULT_ATTRS]

    def build(G, output, ext):
        gx.write_graph(G, f"{output}{f'_k={k}' if k else ''}{ext or '.graphml'}")

    def compute(G, output, ext):
        compute = gx.compute(G, **{arg: args[arg] for arg in signature(gx.compute).parameters if arg in args})
        getattr(compute, f"to_{ext.lstrip('.') or 'excel'}")(f"{output}{ext or '.xlsx'}")
        print(compute.select_dtypes(float).describe().drop("count").T.applymap(lambda x: f"{x:.2f}"))
        # var = {c: compute[c].var() for c in compute.columns}
        # var/mean = {c: compute[c].var()/compute[c].mean() for c in compute.columns}

    def plot(G, output, ext):
        plot = gx.plot(G, **{arg: args[arg] for arg in signature(gx.compute).parameters if arg in args})
        getattr(plot, f"write_{ext.lstrip('.') or 'image'}")(f"{output}{ext or '.png'}")

    G = gx.compose([
        read_graph(f, **{arg: args[arg] for arg in signature(read_graph).parameters if arg in args})
        for f in args["input"]])

    k = args.pop("k_core")
    order, size = G.order(), G.size()
    gx.describe(G)

    if k:
        G = gx.k_core(G, k)

        print(f"k={k}: {G.order()} nodes ({100*G.order()/order:.2f}%) "
              f"and {G.size()} ({100*G.size()/size:.2f}%) edges.")

    locals()[args["main"]](G, *splitext(args["output"]))


def argparser(args=argv[1:]):
    parser = ArgumentParser(description=str("graph-express"))

    parser.add_argument("main",
                        action="store",
                        choices=["build", "compute", "plot"],
                        help="Action to execute.")

    parser.add_argument("input",
                        action="store",
                        help="Path to input graphs or data set files.",
                        nargs="+")

    parser.add_argument("-o", "--output",
                        default="output",
                        help=f"Output path to write returned data.")

    parser.add_argument("-a", "--attrs",
                        help=f"Available attributes: {list(AVAILABLE_ATTRS)}.",
                        nargs="+",
                        type=lambda x: x.replace("-", "_"))

    parser.add_argument("-c", "--color",
                        action="store",
                        dest="node_color",
                        help="Set node color (example: '#ccc').",
                        type=read_file)

    parser.add_argument("-e", "--edge-attrs",
                        action="store",
                        dest="edge_attr",
                        help="Set edge attributes to consider when building graphs.",
                        nargs="+")

    parser.add_argument("-g", "--groups",
                        action="store",
                        help="Get node groups from file (containing two columns, indexed by 'id').",
                        type=read_file)

    parser.add_argument("-k", "--k-core",
                        action="store",
                        help="Apply k-core to graph.",
                        type=int)

    parser.add_argument("-l", "--layout",
                        action="store",
                        default=DEFAULT_LAYOUT,
                        help=f"Available layouts: {list(AVAILABLE_LAYOUTS)} (default: '{DEFAULT_LAYOUT}').",
                        type=lambda x: "%s_layout" % x.replace("-", "_"))

    parser.add_argument("-n", "--node-attrs",
                        action="store",
                        dest="node_attr",
                        help="Set node attributes to consider when building graphs.",
                        nargs="+")

    parser.add_argument("-p", "--positions",
                        action="store",
                        dest="pos",
                        help="Get node 2 or 3-dimensional positions from file.",
                        type=read_file)

    parser.add_argument("-r", "--random-seed",
                        action="store",
                        dest="seed",
                        help="Specify random seed for predictable randomness.",
                        type=int)

    parser.add_argument("-s", "--source",
                        action="store",
                        help="Field name to consider as source.")

    parser.add_argument("-t", "--target",
                        action="store",
                        help="Field name to consider as target.")

    parser.add_argument("--directed",
                        action="store_true",
                        help="Set as directed graph.")

    parser.add_argument("--multigraph",
                        action="store_true",
                        help="Set as multigraph (allow multiple edges connecting a same pair of nodes).")

    parser.add_argument("--no-edges-attrs",
                        action="store_const",
                        const=False,
                        dest="node_attr",
                        help="Ignore edge attributes when building graphs.")

    parser.add_argument("--no-node-attrs",
                        action="store_const",
                        const=False,
                        dest="node_attr",
                        help="Ignore node attributes when building graphs.")

    parser.add_argument("--normalized",
                        action="store_true",
                        help="Returns normalized centrality values (from 0 to 1.0).")

    parser.add_argument("--selfloops",
                        action="store_false",
                        dest="no_selfloops",
                        help="Allow edges connecting a node to itself.")

    return vars(parser.parse_args(args))


def read_file(path,
              engine: str = None,
              index_col: str = None,
              low_memory: bool = False,
              sep: str = None) -> pd.DataFrame:

    def get_sep(path):
        delimiters = ["|", "\t", ";", ","]

        with open(path, "rt") as f:
            header = f.readline()

        for char in delimiters:
            if char in header:
                return char

        return "\n"

    if isfile(path):
        return (
            pd.read_json(path)
            if
                path.endswith(".json")
            else
                pd.read_excel(path, index_col=index_col)
            if
                any(path.endswith(_) for _ in (".xls", ".xlsx"))
            else
                pd.read_table(
                    path,
                    engine=engine,
                    index_col=index_col,
                    low_memory=low_memory,
                    sep=sep or get_sep(path),
                )
        )\
        .squeeze("columns")

    raise FileNotFoundError(f"File not found: '{path}'.")


def read_graph(path: str,
               source: str = None,
               target: str = None,
               directed: bool = True,
               edge_attr : list = None,
               node_attr : list = None,
               multigraph: bool = True) -> nx.Graph:

    if not isinstance(path, str):
        raise TypeError(f"Expected 'str' type, got '{type(path).__name__}'.")

    if isfile(path):
        if path.endswith(".gdf"):
            return gx.read_gdf(path,
                               directed=directed,
                               edge_attr=edge_attr,
                               node_attr=node_attr)

        if gx.is_graph_supported(path):
            return gx.read_graph(path)

        return gx.pd2nx(read_file(path),
                        source=source,
                        target=target,
                        directed=directed,
                        edge_attr=edge_attr,
                        multigraph=multigraph)

    raise FileNotFoundError(f"File not found: '{path}'.")
