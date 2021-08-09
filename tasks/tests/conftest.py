import pytest
from networkx import Graph


@pytest.fixture
def g1():
    g1 = Graph()
    g1.add_node("t1", profit=9.4)
    g1.add_node("t2", profit=1.4)
    g1.add_node("t3", profit=3.6)
    g1.add_edge("t1", "t2")
    g1.add_edge("t1", "t3")
    return g1


@pytest.fixture
def g2():
    # graph with just one edge
    g2 = Graph()
    g2.add_node("t1", profit=9.4)
    g2.add_node("t2", profit=1.4)
    g2.add_node("t3", profit=3.6)
    g2.add_edge("t1", "t3")
    return g2


@pytest.fixture
def g3():
    # graph without edges
    g3 = Graph()
    g3.add_node("t1", profit=9.4)
    g3.add_node("t2", profit=1.4)
    g3.add_node("t3", profit=3.6)
    return g3


@pytest.fixture
def g4():
    # empty graph
    return Graph()


@pytest.fixture
def g5():
    # complete graph
    g5 = Graph()
    g5.add_node("t1", profit=9.4)
    g5.add_node("t2", profit=1.4)
    g5.add_node("t3", profit=3.6)
    g5.add_node("t4", profit=3.1)
    g5.add_edge("t1", "t2")
    g5.add_edge("t1", "t3")
    g5.add_edge("t1", "t4")
    g5.add_edge("t2", "t3")
    g5.add_edge("t2", "t4")
    g5.add_edge("t3", "t4")
    return g5


@pytest.fixture
def g6():
    # complete graph
    g6 = Graph()
    g6.add_node("t1", profit=9.4)
    g6.add_node("t2", profit=1.4)
    g6.add_edge("t1", "t2")
    return g6
