# graph-express

A Python package for the analysis and visualization of network graphs which uses familiar libraries such as
[NetworkX](https://networkx.org/), [NetworKit](https://networkit.github.io/), [igraph](https://igraph.org/), and [plotly](https://plotly.com/).

> Current version: **0.1.0-alpha1-dev1** (WIP).

### Requirements

* **Python 3.6.8+**
* datashader>=0.10.0
* kaleido>=0.2.1
* leidenalg>=0.8.3
* networkit>=7.0
* networkx>=2.3
* openpyxl>=3.1.2
* pandas>=0.25.3
* plotly>=3.10.0
* python-igraph>=0.8.3
* python-louvain>=0.14

### Usage

```
import graph_express.graph_express as gx

# Build graph from file
G = gx.graph("/path/to/file", ...)

# Compute centrality and partitions (communities)
df = gx.compute(G, ...)

# Plot network graph
fig = gx.plot(G, ...)
```

### Command line interface

A CLI is **partially** implemented and may be executed with:

```
graph-express {build,compute,plot} input [...]
```

### References

* [Datashader](http://datashader.org)
* [igraph](https://igraph.org)
* [Leiden](https://leidenalg.readthedocs.io)
* [NetworkX](https://networkx.github.io)
* [Networkit](https://github.com/networkit/networkit)
* [Plotly](https://plot.ly)
