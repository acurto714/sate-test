from tasks.exceptions import InvalidTaskFormat
import pytest
import networkx as nx
from tasks.scheduler import (
    NAME_KEY,
    RESOURCES_KEY,
    PROFIT_KEY,
    are_incompatibles,
    from_tasks_to_graph,
    get_maximum_weighted_independient_set,
)


@pytest.mark.parametrize(
    "t1, t2, expected_result",
    [
        (["a"], ["b"], False),
        (["a"], ["a"], True),
        (["a", "b"], ["c"], False),
        (["a", "c"], ["c"], True),
        ([], [], False),
        (["a"], [], False),
    ],
)
def test_are_incompatibles_return_expected(t1, t2, expected_result):
    print(f"t1: {t1}, t2: {t2}, expected: {expected_result}")
    result = are_incompatibles(t1, t2)
    assert result == expected_result


@pytest.mark.parametrize(
    "tasks",
    [
        ([{"nombre": "t1", RESOURCES_KEY: ["a", "b"], PROFIT_KEY: 9.4}]),
        ([{NAME_KEY: "t1", RESOURCES_KEY: ["a", "b"], "ganancia": 9.4}]),
    ],
)
def test_from_tasks_to_graph_raises_exception_when_recieve_invalid_tasks(tasks):
    with pytest.raises(InvalidTaskFormat):
        from_tasks_to_graph(tasks)


@pytest.mark.parametrize(
    "tasks, fixture_graph",
    [
        (
            [
                {NAME_KEY: "t1", RESOURCES_KEY: ["a", "b"], PROFIT_KEY: 9.4},
                {NAME_KEY: "t2", RESOURCES_KEY: ["a"], PROFIT_KEY: 1.4},
                {NAME_KEY: "t3", RESOURCES_KEY: ["b"], PROFIT_KEY: 3.6},
            ],
            "g1",
        ),
        (
            [
                {NAME_KEY: "t1", RESOURCES_KEY: ["a", "b"], PROFIT_KEY: 9.4},
                {NAME_KEY: "t2", RESOURCES_KEY: ["c"], PROFIT_KEY: 1.4},
                {NAME_KEY: "t3", RESOURCES_KEY: ["b"], PROFIT_KEY: 3.6},
            ],
            "g2",
        ),
        (
            [
                {NAME_KEY: "t1", RESOURCES_KEY: ["a"], PROFIT_KEY: 9.4},
                {NAME_KEY: "t2", RESOURCES_KEY: ["b"], PROFIT_KEY: 1.4},
                {NAME_KEY: "t3", RESOURCES_KEY: ["c"], PROFIT_KEY: 3.6},
            ],
            "g3",
        ),
        ([], "g4"),
        (
            [
                {NAME_KEY: "t1", RESOURCES_KEY: ["a", "b", "c"], PROFIT_KEY: 9.4},
                {NAME_KEY: "t2", RESOURCES_KEY: ["a", "d", "e"], PROFIT_KEY: 1.4},
                {NAME_KEY: "t3", RESOURCES_KEY: ["b", "e", "d"], PROFIT_KEY: 3.6},
                {NAME_KEY: "t4", RESOURCES_KEY: ["c", "d"], PROFIT_KEY: 3.1},
            ],
            "g5",
        ),
        (
            [
                {NAME_KEY: "t1", RESOURCES_KEY: ["a"], PROFIT_KEY: 9.4},
                {NAME_KEY: "t2", RESOURCES_KEY: ["a"], PROFIT_KEY: 1.4},
            ],
            "g6",
        ),
    ],
)
def test_from_tasks_to_graph_return_expected_graph(tasks, fixture_graph, request):
    expected_graph = request.getfixturevalue(
        fixture_graph
    )  # to get fixture named fixture_graph
    graph = from_tasks_to_graph(tasks)
    assert nx.is_isomorphic(
        graph,
        expected_graph,
        node_match=lambda n1, n2: n1[PROFIT_KEY] == n2[PROFIT_KEY],
    )


@pytest.mark.parametrize(
    "fixture_graph, expected_schedule",
    [
        ("g1", ["t1"]),
        ("g2", ["t1", "t2"]),
        ("g3", ["t1", "t2", "t3"]),
        ("g4", []),
        ("g5", ["t1"]),
        ("g6", ["t1"]),
    ],
)
def test_get_maximum_weighted_independient_set_return_expected(
    fixture_graph, expected_schedule, request
):
    graph = request.getfixturevalue(fixture_graph)
    schedule = get_maximum_weighted_independient_set(graph)
    assert set(schedule) == set(expected_schedule)  # because orer doesn`t care
