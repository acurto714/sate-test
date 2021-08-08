import sys
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
    - __init__: only weights verification was suppressed because that didn't
        allow floats values.
    - expand: TBD, why? research
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
            self.node_weights = {v: G.nodes[v][weight] for v in G.nodes()}

    def expand(self, C, C_weight, P):
        self.update_incumbent_if_improved(C, C_weight)
        branching_nodes = self.find_branching_nodes(P, self.incumbent_weight - C_weight)
        while branching_nodes:
            v = branching_nodes.pop()
            P.remove(v)
            new_C = C + [v]
            new_C_weight = C_weight + self.node_weights[v]
            new_P = [w for w in P if not self.G.has_edge(v, w)]
            self.expand(new_C, new_C_weight, new_P)


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
    """Generates the graph associated to the task list.

    The graph nodes are each of the listed tasks, and the associated weight
    with each one is the task "profit". The graph edges are built using tasks
    "resources", where (u, v) in E if u resources is incompatibles with v
    resources.

    Example: suppose the following tasks' list
        - tasks: [
            {"name": "t1", "resources": ["a", "b", "c"], "profit": 9.4},
            {"name": "t2", "resources": ["a", "d"], "profit": 1.4},
            {"name": "t3", "resources": ["b"], "profit": 3.2},
            {"name": "t4", "resources": ["c", "d"], "profit": 6.3},
        ]

    then, the associated graph is:
    G = (V, E) = ({t1, t2, t3, t4}, {(t1, t2), (t1, t3), (t1, t4), (t2, t4)})

    Args:
        tasks: list of tasks to be analized.

    Return:
        The graph associated to tasks' list
    """
    graph = Graph()
    while tasks:
        t1 = tasks.pop()
        try:
            graph.add_node(t1[NAME_KEY], profit=t1[PROFIT_KEY])
        except KeyError:
            logging.error("Invalid task format for task: %s", str(t1))
            sys.exit(-1)
        for t2 in tasks:
            if not are_compatibles(t1, t2):
                graph.add_edge(t1[NAME_KEY], t2[NAME_KEY])
    return graph


def get_optimal_tasks_schedule(tasks: List[dict]) -> List[str]:
    """Gets tasks' list that generates the highest profit.

    Args:
        tasks: list of tasks to be analized.

    Returns:
        List with tasks names that belong to the best schedule.
    """
    graph = from_tasks_to_graph(tasks)
    mwts = MaxWeightTasksSelector(graph, weight=PROFIT_KEY)
    mwts.find_max_weight_clique()
    logging.info(
        "The max profit is: %d and the tasks schedule is: %s",
        mwts.incumbent_weight,
        mwts.incumbent_nodes,
    )
    return mwts.incumbent_nodes


if __name__ == "__main__":
    tasks = [
        {NAME_KEY: "t1", RESOURCES_KEY: ["a", "b", "c"], PROFIT_KEY: 9.4},
        {NAME_KEY: "t2", RESOURCES_KEY: ["a"], PROFIT_KEY: 1.4},
        {NAME_KEY: "t3", RESOURCES_KEY: ["b"], PROFIT_KEY: 3.6},
        {NAME_KEY: "t4", RESOURCES_KEY: ["c"], PROFIT_KEY: 6.3},
    ]
    # import ipdb; ipdb.set_trace()
    result = get_optimal_tasks_schedule(tasks)
    print(result)
