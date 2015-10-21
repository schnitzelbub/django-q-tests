import os
import subprocess
import logging
import time

logger = logging.getLogger(__name__)
CWD = os.path.dirname(__file__)


def do_work(st: int, external: bool = True) -> str:
    logger.warning("do_work called!")

    if external:
        logging.warning("running external process via subprocess ...")
        subprocess.call(['python3', 'worker.py', '{}'.format(st)], cwd=CWD)
    else:
        logging.warning("running in process ...")
        time.sleep(st)

    logger.warning("do_work done!")
    return "OK"
