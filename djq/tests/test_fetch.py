import unittest
import logging
import django_q
from nose_parameterized import parameterized, param
from djq.tests.nose_parameterized_helper import custom_name_func, custom_name_func_param_num

logger = logging.getLogger(__name__)

WAIT_TIME = 10 * 1000

q_opts = {
    'hook': 'print',
    "cached": 60 * 10,  # 10 minutes cache timeout
    "timeout": 60,  # default timeout for worker processes
}


def offload_task(sleep_time: int = 10, ext_process: bool = True, cached: bool = True) -> str:
    q_opts = {
        'hook': 'print',
        "cached": 60 * 10,  # 10 minutes cache timeout
        "timeout": 60,  # default timeout for worker processes
    }

    if not cached:
        q_opts["cached"] = False

    tid = django_q.async(
        "djq.work.do_work",
        st=sleep_time,
        external=ext_process,
        q_options=q_opts.copy())  # the q_opts dictionary is manipulated by async(), thus we need a copy here

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

    @parameterized.expand([param(external=True, cached=True),
                           param(external=False, cached=True),
                           param(external=False, cached=False),
                           param(external=True, cached=False)],
                          testcase_func_name=custom_name_func)
    def test_fetch_many(self, external, cached):
        self.fetch_and_assert(external=external, cached=cached)
        return

    @parameterized.expand([param(cached=True),
                           param(cached=False),
                           param(cached=True),
                           param(cached=False),
                           param(cached=True)],
                          testcase_func_name=custom_name_func_param_num)
    def test_fetch_one(self, cached):
        """
        This test offloads and fetches only one task per test run.
        :param cached: defines whether the cache should be used.
        :return: None
        """
        tid = offload_task(sleep_time=3, ext_process=False, cached=cached)
        task = django_q.fetch(tid, wait=WAIT_TIME, cached=cached)
        assert task is not None
