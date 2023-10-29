# NetworkZ

NetworkZ is a library of graph algorithms in Python. It is an extension of the [NetworkX](https://github.com/networkx/networkx). It contains (by import) everything that is in NetworkX, plus some additional algorithms that were submitted into NetworkX but not merged yet. Currently, NetworkZ contains the following additional algorithms:

* [Rank-maximal matching](networkz/algorithms/bipartite/rank_maximal_matching.py): by Oriya Alperin, Liel Vaknin and Amiel Lejzor.
* [Social-aware coalition formation](networkz/algorithms/approximation/coalition_formation.py) - by Victor Kushnir.

## Installation

```
pip install networkz
```

This installs the latest version of networkx, and the new algorithms added in networkz.


## Usage

### Rank Maximal Matching Algorithm
A rank-maximal matching is a matching that maximizes the number of agents who are matched to their 1st priority; subject to that, it maximizes the number of agents matched to their 2nd priority; and so on.

```
import networkz as nx
G = nx.Graph()
G.add_nodes_from(["agent1", "agent2"], bipartite=0)
G.add_nodes_from(["product1", "product2"], bipartite=1)
G.add_weighted_edges_from([("agent1", "product1", 1), ("agent1", "product2", 1), ("agent2", "product2", 2)])
matching = nx.rank_maximal_matching(G, rank="weight")
print(matching)
```

See [demo website](https://rmm.csariel.xyz/) for more information.

### Social-aware coalition formation

(TODO)


## Contribution

Any additions or bug-fixes to `networkx` should first be submitted there, according to the [NetworkX Contributor Guide](https://github.com/networkx/networkx/blob/main/CONTRIBUTING.rst).

If the pull-request is not handled, you are welcome to submit it here too.





