import time

import chime


def test_speed():
    tic = time.time()
    chime.success()
    toc = time.time()
    assert toc - tic < .1
