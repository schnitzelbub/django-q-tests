import unittest
import logging
import django_q

logger = logging.getLogger(__name__)

WAIT_TIME = 10 * 1000

q_opts = {
    'hook': 'print',
    "cached": 60 * 10,  # 10 minutes cache timeout
    "timeout": 60,  # default timeout for worker processes
}


def offload_task(sleep_time: int = 10, ext_process: bool = True, cached: bool = True) -> str:
    if not cached:
        q_opts["cached"] = False

    tid = django_q.async(
        "djq.work.do_work",
        st=sleep_time,
        external=ext_process,
        q_options=q_opts)

    return tid


class TestFetch(unittest.TestCase):
    """
    This test case examines the django_q.fetch function.
    """

    def fetch_and_assert(self, external: bool, cached: bool) -> None:
        """
        This test offloads multiple tasks and asserts that fetch returns the according task
        :param external: selects whether the worker should be run in an external process or not.
        :param cached: selects whether the task should only reside in cache or not
        :return: None
        """
        tid1 = offload_task(sleep_time=6, ext_process=external, cached=cached)
        tid2 = offload_task(sleep_time=4, ext_process=external, cached=cached)
        tid3 = offload_task(sleep_time=2, ext_process=external, cached=cached)

        t1 = django_q.fetch(tid1, wait=WAIT_TIME, cached=cached)
        assert t1 is not None
        assert t1.success is True
        assert t1.id == tid1

        t2 = django_q.fetch(tid2, wait=WAIT_TIME, cached=cached)
        assert t2 is not None
        assert t2.success is True
        assert t2.id == tid2

        t3 = django_q.fetch(tid3, wait=WAIT_TIME, cached=cached)
        assert t3 is not None
        assert t3.success is True
        assert t3.id == tid3

    def test_fetch_1(self):
        self.fetch_and_assert(external=True, cached=True)
        return

    def test_fetch_2(self):
        self.fetch_and_assert(external=False, cached=True)
        return

    def test_fetch_3(self):
        self.fetch_and_assert(external=False, cached=False)
        return

    def test_fetch_4(self):
        self.fetch_and_assert(external=True, cached=False)
        return
