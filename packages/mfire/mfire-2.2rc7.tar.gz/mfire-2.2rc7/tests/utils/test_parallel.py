import time

from mfire.utils.parallel import Parallel, TaskStatus


def func(n: int) -> int:
    if n == 2:
        raise ValueError(n)
    if n > 3:
        time.sleep(30)
    return n * n


def test_parallel() -> None:
    p = Parallel(3)
    res = []
    _ = [p.apply(func, args=(i,), callback=res.append) for i in range(8)]
    p.run(timeout=15)
    assert sorted(res) == [0, 1, 9]

    expected_statuses = [
        TaskStatus.DONE,
        TaskStatus.DONE,
        TaskStatus.FAILED,
        TaskStatus.DONE,
        TaskStatus.TIMEOUT,
        TaskStatus.TIMEOUT,
        TaskStatus.TIMEOUT,
        TaskStatus.TIMEOUT,
    ]
    for task, exp_status in zip(p, expected_statuses):
        assert task.status == exp_status
