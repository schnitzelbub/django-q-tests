#!/usr/bin/env python3

import logging
import sys
import time

logger = logging.getLogger(__name__)

WAIT = 1

if len(sys.argv) > 1:
    WAIT = float(sys.argv[1])

if __name__ == "__main__":
    logger.warning("External worker started -> waiting for {} seconds".format(WAIT))
    time.sleep(WAIT)
    logger.warning("External worker finished.")
