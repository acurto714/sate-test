import pytest

from tasks.scheduler import (
    NAME_KEY,
    RESOURCES_KEY,
    PROFIT_KEY,
    get_optimal_tasks_schedule,
)


@pytest.mark.parametrize(
    "tasks, expected_result"[
        ([
            {NAME_KEY: "t1", RESOURCES_KEY: ["a", "b", "c"], PROFIT_KEY: 9.4},
            {NAME_KEY: "t2", RESOURCES_KEY: ["a"], PROFIT_KEY: 1.4},
            {NAME_KEY: "t3", RESOURCES_KEY: ["b"], PROFIT_KEY: 3.2},
            {NAME_KEY: "t4", RESOURCES_KEY: ["c"], PROFIT_KEY: 6.3},
        ], ["t1, t2, t3"]),
        ([
            {NAME_KEY: "t1", RESOURCES_KEY: ["a", "b", "c"], PROFIT_KEY: 9.4},
            {NAME_KEY: "t2", RESOURCES_KEY: ["a", "d"], PROFIT_KEY: 1.4},
            {NAME_KEY: "t3", RESOURCES_KEY: ["b"], PROFIT_KEY: 3.6},
            {NAME_KEY: "t4", RESOURCES_KEY: ["c", "d"], PROFIT_KEY: 6.3},
        ], ["t3", "t4"]),
        ([], []),
        ([], []),
        ([], []),
    ]
)
def test_scheduler_selector_return_expected_tasks(tasks, expected_result):
    import ipdb

    ipdb.set_trace()
    schedule = get_optimal_tasks_schedule(tasks)
    assert schedule == expected_result
