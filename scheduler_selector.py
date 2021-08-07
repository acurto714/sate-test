import networkx as nx


class MaxWeightClique(object):
    """A class for the maximum weight clique algorithm.

    This class is a helper for the `max_weight_clique` function.  The class
    should not normally be used directly.

    Parameters
    ----------
    G : NetworkX graph
        The undirected graph for which a maximum weight clique is sought
    weight : string or None, optional (default='weight')
        The node attribute that holds the integer value used as a weight.
        If None, then each node has weight 1.

    Attributes
    ----------
    G : NetworkX graph
        The undirected graph for which a maximum weight clique is sought
    node_weights: dict
        The weight of each node
    incumbent_nodes : list
        The nodes of the incumbent clique (the best clique found so far)
    incumbent_weight: int
        The weight of the incumbent clique
    """

    def __init__(self, G, weight):
        self.G = G
        self.incumbent_nodes = []
        self.incumbent_weight = 0

        if weight is None:
            self.node_weights = {v: 1 for v in G.nodes()}
        else:
            for v in G.nodes():
                if weight not in G.nodes[v]:
                    errmsg = f"Node {v!r} does not have the requested weight field."
                    raise KeyError(errmsg)
                # # TODO: remove this if to accept float
                # if not isinstance(G.nodes[v][weight], int):
                #     errmsg = f"The {weight!r} field of node {v!r} is not an integer."
                #     raise ValueError(errmsg)
            self.node_weights = {v: G.nodes[v][weight] for v in G.nodes()}

    def update_incumbent_if_improved(self, C, C_weight):
        """Update the incumbent if the node set C has greater weight.

        C is assumed to be a clique.
        """
        if C_weight > self.incumbent_weight:
            self.incumbent_nodes = C[:]
            self.incumbent_weight = C_weight

    def greedily_find_independent_set(self, P):
        """Greedily find an independent set of nodes from a set of
        nodes P."""
        independent_set = []
        P = P[:]
        while P:
            v = P[0]
            independent_set.append(v)
            P = [w for w in P if v != w and not self.G.has_edge(v, w)]
        return independent_set

    def find_branching_nodes(self, P, target):
        """Find a set of nodes to branch on."""
        residual_wt = {v: self.node_weights[v] for v in P}
        total_wt = 0
        P = P[:]
        while P:
            independent_set = self.greedily_find_independent_set(P)
            # TODO: maybe this could be max
            min_wt_in_class = min(residual_wt[v] for v in independent_set)
            # min_wt_in_class = max(residual_wt[v] for v in independent_set)
            total_wt += min_wt_in_class
            if total_wt > target:
                break
            for v in independent_set:
                residual_wt[v] -= min_wt_in_class
            P = [v for v in P if residual_wt[v] != 0]
        return P

    def expand(self, C, C_weight, P):
        """Look for the best clique that contains all the nodes in C and zero or
        more of the nodes in P, backtracking if it can be shown that no such
        clique has greater weight than the incumbent.
        """
        self.update_incumbent_if_improved(C, C_weight)
        branching_nodes = self.find_branching_nodes(P, self.incumbent_weight - C_weight)
        while branching_nodes:
            v = branching_nodes.pop()
            P.remove(v)
            new_C = C + [v]
            new_C_weight = C_weight + self.node_weights[v]
            new_P = [w for w in P if not self.G.has_edge(v, w)]
            self.expand(new_C, new_C_weight, new_P)

    def find_max_weight_clique(self):
        """Find a maximum weight clique."""
        # Sort nodes in reverse order of degree for speed
        nodes = sorted(self.G.nodes(), key=lambda v: self.G.degree(v), reverse=True)
        nodes = [v for v in nodes if self.node_weights[v] > 0]
        self.expand([], 0, nodes)


# [docs]@not_implemented_for("directed")
def max_weight_clique(G, weight="weight"):
    """Find a maximum weight clique in G.

    A *clique* in a graph is a set of nodes such that every two distinct nodes
    are adjacent.  The *weight* of a clique is the sum of the weights of its
    nodes.  A *maximum weight clique* of graph G is a clique C in G such that
    no clique in G has weight greater than the weight of C.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph
    weight : string or None, optional (default='weight')
        The node attribute that holds the integer value used as a weight.
        If None, then each node has weight 1.

    Returns
    -------
    clique : list
        the nodes of a maximum weight clique
    weight : int
        the weight of a maximum weight clique

    Notes
    -----
    The implementation is recursive, and therefore it may run into recursion
    depth issues if G contains a clique whose number of nodes is close to the
    recursion depth limit.

    At each search node, the algorithm greedily constructs a weighted
    independent set cover of part of the graph in order to find a small set of
    nodes on which to branch.  The algorithm is very similar to the algorithm
    of Tavares et al. [1]_, other than the fact that the NetworkX version does
    not use bitsets.  This style of algorithm for maximum weight clique (and
    maximum weight independent set, which is the same problem but on the
    complement graph) has a decades-long history.  See Algorithm B of Warren
    and Hicks [2]_ and the references in that paper.

    References
    ----------
    .. [1] Tavares, W.A., Neto, M.B.C., Rodrigues, C.D., Michelon, P.: Um
           algoritmo de branch and bound para o problema da clique máxima
           ponderada.  Proceedings of XLVII SBPO 1 (2015).

    .. [2] Warrent, Jeffrey S, Hicks, Illya V.: Combinatorial Branch-and-Bound
           for the Maximum Weight Independent Set Problem.  Technical Report,
           Texas A&M University (2016).
    """

    mwc = MaxWeightClique(G, weight)
    mwc.find_max_weight_clique()
    return mwc.incumbent_nodes, mwc.incumbent_weight

# CASO: mismo peso para un solo vertice que para muchos
g1 = nx.Graph()
g1.add_node("t1", weight=9.4)
g1.add_node("t2", weight=3.1)
g1.add_node("t3", weight=2.1)
g1.add_node("t4", weight=4.2)
g1.add_edge("t1", "t2")
g1.add_edge("t1", "t3")
g1.add_edge("t1", "t4")

# CASO: tipico, muchas tareas suman mas
g2 = nx.Graph()
g2.add_node("t1", weight=9)
g2.add_node("t2", weight=5)
g2.add_node("t3", weight=2)
g2.add_node("t4", weight=4)
g2.add_edge("t1", "t2")
g2.add_edge("t1", "t3")
g2.add_edge("t1", "t4")

# g3 = nx.Graph()
# g4 = nx.Graph()


if __name__ == "__main__":
    import ipdb; ipdb.set_trace()
    result = max_weight_clique(g1)
    print(result)