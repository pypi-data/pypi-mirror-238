from abc import abstractmethod
from typing import Optional, Union

import networkx as nx
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

from .layout import Layout

pio.templates.default = "none"

DEFAULT_NODE_COLOR = "#ccc"
DEFAULT_NODE_SIZE = 7

DEFAULT_GROUP_COLORS = [
    "#006cb7",
    "#ff7700",
    "#00b035",
    "#ed0000",
    "#a643bd",
    "#965146",
    "#fb4cbe",
    "#7f7f7f",
    "#b2cb10",
    "#00c2d3",
]

DEFAULT_COLORSCALE = [
    "#4e9cd5",
    "#ffffff",
    "#f6e16d",
    "#f76717",
    "#d11e26",
]


class Plot():

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    @staticmethod
    def plot(
        G: nx.Graph,
        pos: Optional[Union[str, dict, pd.DataFrame]] = None,
        colorbar_title: str = "",
        colorbar_thickness: int = 10,
        colorscale: Union[list, bool] = None,
        edge_color: str = "#bbb",
        edge_width: float = 1.0,
        font_color: str = "grey",
        font_family: str = "sans-serif",
        font_size: int = 16,
        groups: dict = None,
        group_colors: list = DEFAULT_GROUP_COLORS,
        height: int = 1000,
        labels: dict = None,
        node_color: Union[str, dict] = None,
        node_line_color: str = "#000",
        node_line_width: float = 1.0,
        node_opacity: float = 1.0,
        node_size: Union[int, dict] = None,
        reversescale: bool = False,
        showarrow: bool = False,
        showbackground: bool = False,
        showgrid: bool = None,
        showlabels: bool = False,
        showlegend: bool = None,
        showline: bool = False,
        showscale: bool = False,
        showspikes: bool = False,
        showticklabels: bool = False,
        title: str = None,
        titlefont_size: int = 16,
        unlabeled: str = "Nodes",
        width: int = 1000,
        zeroline: bool = False,
    ) -> go.Figure:
        """
        Returns graph rendered as a Plotly figure.

        References for built-in color sequences:
        * [Built-in Colorscales](https://plotly.com/python/builtin-colorscales/)
        * [Colorscales](https://plotly.com/python/colorscales/)
        * [Templates](https://plotly.com/python/templates/)
        """
        # Node positions in graph
        if type(pos) in (str, type(None)):
            pos = Layout.layout(G, pos)

        if type(pos) == dict:
            pos = pd.DataFrame.from_dict(
                pos,
                orient="index",
            ).rename(
                columns={
                    0: "x",
                    1: "y",
                    2: "z"
                }
            )

        pos = pos.loc[list(G.nodes())]

        # Set default options if unset
        if showlabels and pos.shape[1] != 2:
            raise NotImplementedError("Showing labels only implemented for 2-dimensional plots.")

        if showgrid is None:
            showgrid = (showgrid is None and pos.shape[1] == 3)

        colorscale = colorscale if type(colorscale) == list else DEFAULT_COLORSCALE\
                                if (colorscale in (True, None) and not groups) else None

        # Dictionary of node groups
        node_groups = {
            **{group: [] for group in (groups or {})},
            **({unlabeled: []} if sum([len(nodes) for nodes in (groups or {}).values()]) != G.order() else {})
        }
        list(node_groups[(groups or {}).get(node, unlabeled)].append(node) for node in G.nodes())

        # Size of nodes by degree
        min_node_size = 0

        if node_size is None:
            min_node_size = DEFAULT_NODE_SIZE
            node_size = (
                pd
                .Series(dict(G.degree()))
                .dropna()
                .apply(lambda x: x + min_node_size)
                .to_dict()
            )

        # Trace nodes per group
        node_traces = []

        for i, group, nodes in zip(range(len(node_groups)), node_groups.keys(), node_groups.values()):
            group_color = node_color if group == unlabeled else group_colors[::-1][-i-1]

            size = [
                node_size.get(node) if type(node_size) == dict else node_size
                for node in nodes
            ]

            color = [
                node_color.get(node) if type(node_color) == dict else (group_color or DEFAULT_NODE_COLOR)
                for node in nodes
            ]

            node_traces.append(
                (go.Scatter3d if pos.shape[1] == 3 else go.Scatter)(
                    x=pos["x"].values.tolist(),
                    y=pos["y"].values.tolist(),
                    mode="markers",
                    hoverinfo="text",
                    name=str(group).format(len(nodes)),
                    text=[labels.get(node, node) for node in nodes] if labels else nodes,
                    marker=dict(
                        color=[x - min_node_size for x in size] if colorscale else color,
                        colorscale=colorscale,
                        opacity=node_opacity,
                        reversescale=reversescale,
                        showscale=showscale,
                        size=size,
                        colorbar=dict(
                            title=colorbar_title,
                            thickness=colorbar_thickness,
                            titleside="bottom",
                            xanchor="left",
                        ),
                        line=dict(
                            color=node_line_color,
                            width=node_line_width,
                        )
                    ),
                    **(dict(z=pos["z"].values.tolist()) if pos.shape[1] == 3 else {})
                )
            )

        # Trace edges
        edge_trace = (go.Scatter3d if pos.shape[1] == 3 else go.Scatter)(
            x=[x for x in [(pos["x"][u], pos["x"][v]) for u, v in list(G.edges())] for x in x],
            y=[x for x in [(pos["y"][u], pos["y"][v]) for u, v in list(G.edges())] for x in x],
            mode="lines",
            hoverinfo="none",
            line=dict(
                color=edge_color,
                width=edge_width,
            ),
            name="Edges",
            **(dict(z=[x for x in [(pos["z"][u], pos["z"][v]) for u, v in list(G.edges())] for x in x]) if pos.shape[1] == 3 else {})
        )

        axis = dict(
            showgrid=showgrid,
            showticklabels=showticklabels,
            zeroline=zeroline,
            showspikes=showspikes,
            title="",
        )

        fig = go.Figure(
            data=[edge_trace, *node_traces],
            layout=go.Layout(
                height=height,
                legend=dict(
                    y=0.5,
                    font=dict(
                        family=font_family,
                        size=font_size,
                        color=font_color,
                        ),
                    ),
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=showlegend if showlegend is not None else (True if len(node_traces) > 1 else False),
                title=title,
                titlefont=dict(
                    size=titlefont_size,
                ),
                width=width,
                xaxis=axis,
                yaxis=axis,
                scene=dict(
                    xaxis=axis,
                    yaxis=axis,
                    zaxis=axis,
                )
            ),
        )

        if showlabels:
            fig.update_layout(
                annotations=Plot._make_annotations(
                    labels=labels,
                    nodes=list(G.nodes()),
                    pos=pos,
                    showarrow=showarrow,
                ),
            )

        return fig

    @staticmethod
    def _make_annotations(
        pos: pd.DataFrame,
        color: str = "#555",
        labels: dict = None,
        nodes: list = None,
        offset: Union[int, dict] = 0,
        showarrow: bool = False,
        size: int = 12,
    ) -> list:
        """
        Adds node labels as text to Plotly 2-d figure.
        * [Example](https://plot.ly/~empet/14683/networks-with-plotly/)
        """
        return [
            dict(
                font=dict(
                    color=color,
                    size=size,
                ),
                showarrow=showarrow,
                text=labels.get(node) if labels else node,
                x=pos.loc[node][0],
                y=pos.loc[node][1] + (offset.get(node, 0) if type(offset) == dict else (offset or 0)),
                xref="x1", # "paper",
                yref="y1", # "paper",
                # xanchor="left",
                # yanchor="bottom",
            )
            for node in (nodes or pos.index)
        ]
