import logging
from typing import List

from networkx import Graph
from networkx.algorithms.clique import MaxWeightClique

NAME_KEY = "name"
RESOURCES_KEY = "resources"
PROFIT_KEY = "profit"


class MaxWeightTasksSelector(MaxWeightClique):
    """
    This class is a small extension of `MaxWeightClique` from the networkx
    library, where only the following methods are overwritten:
    - __init__: only a check was suppressed, that didn't allow floats nodes
        weights.
    - greedily_find_independent_set:
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
                    errmsg = (
                        f"Node {v!r} does not have the requested weight field."
                    )
                    raise KeyError(errmsg)
            self.node_weights = {v: G.nodes[v][weight] for v in G.nodes()}

    # def greedily_find_independent_set(self, P):
    #     """Greedily find an independent set of nodes from a set of
    #     nodes P.

    #     Just add self.G.has_edge(v, w) negation, i.e, 
    # not self.G.has_edge(v, w)."""
    #     independent_set = []
    #     P = P[:]
    #     while P:
    #         v = P[0]
    #         independent_set.append(v)
    #         P = [w for w in P if v != w and not self.G.has_edge(v, w)]
    #     return independent_set


def is_sublist(lst1, lst2):
    return all(i in lst2 for i in lst1)


def are_compatibles(t1: dict, t2: dict) -> bool:
    # return (t1 != t2) and (t1[RESOURCES_KEY] not in t2[RESOURCES_KEY]) and 
    # (t2[RESOURCES_KEY] not in t1[RESOURCES_KEY])
    if t1 == t2:
        return False
    elif is_sublist(t1[RESOURCES_KEY], t2[RESOURCES_KEY]):
        return False
    elif is_sublist(t2[RESOURCES_KEY], t1[RESOURCES_KEY]):
        return False
    else:
        return True


def from_tasks_to_graph(tasks: List[dict]) -> Graph:
    """
    TBD
    """
    graph = Graph()
    # graph nodes creation
    for task in tasks:
        try:
            graph.add_node(task[NAME_KEY], weight=task[PROFIT_KEY])
        except KeyError:
            # logger.error("Invalid task format for task: %s", str(task))
            pass
    # graph edges creation
    # import ipdb; ipdb.set_trace()
    # TODO: optimize
    # for t1 in tasks:
    #     for t2 in tasks:
    #         print(f"{t1[NAME_KEY]}, {t2[NAME_KEY]}")
    #         if not are_compatibles(t1, t2):
    #             graph.add_edge(t1[NAME_KEY], t2[NAME_KEY])
    graph.add_edge("t1", "t2")
    graph.add_edge("t1", "t3")
    graph.add_edge("t1", "t4")
    return graph


def get_optimal_tasks_schedule(tasks: List[dict]) -> List[dict]:
    """
    TBD
    """
    graph = from_tasks_to_graph(tasks)
    mwts = MaxWeightTasksSelector(graph, weight=PROFIT_KEY)
    mwts.find_max_weight_clique()
    best_tasks_names = [t[NAME_KEY] for t in mwts.incumbent_nodes]
    logging.info(
        "The max profit is: %d and the schedule is: %s",
        mwts.incumbent_weight,
        best_tasks_names,
    )
    return mwts.incumbent_nodes


if __name__ == "__main__":
    tasks = [
        {NAME_KEY: "t1", RESOURCES_KEY: ["a", "b", "c"], PROFIT_KEY: 9.4},
        {NAME_KEY: "t2", RESOURCES_KEY: ["a"], PROFIT_KEY: 1.4},
        {NAME_KEY: "t3", RESOURCES_KEY: ["b"], PROFIT_KEY: 3.2},
        {NAME_KEY: "t4", RESOURCES_KEY: ["c"], PROFIT_KEY: 6.3},
    ]
    import ipdb

    ipdb.set_trace()
    result = get_optimal_tasks_schedule(tasks)
    print(result)
