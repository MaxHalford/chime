import importlib
import pathlib
import tempfile

import _pytest.monkeypatch
import pytest

import chime


@pytest.fixture(scope='function', autouse=True)
def reload_chime():
    importlib.reload(chime)


@pytest.fixture(scope='function', autouse=True)
def mock_pathlib_home(monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    with tempfile.TemporaryDirectory() as home_dir:
        home_dir_path = pathlib.Path(home_dir)
        monkeypatch.setattr(pathlib.Path, name='home', value=lambda: home_dir_path)
        monkeypatch.setenv('APPDATA', value=str(pathlib.Path(home_dir)))
