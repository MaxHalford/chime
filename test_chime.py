import subprocess
import time

import pytest

import chime


def test_speed():
    tic = time.time()
    chime.success()
    toc = time.time()
    assert toc - tic < .1


def test_no_warning():
    with pytest.warns(None) as record:
        chime.success(sync=True)
    assert len(record) == 0


def test_no_exception():
    chime.success(sync=True, raise_error=True)


def test_script():
    subprocess.run(["chime"], check=True)
