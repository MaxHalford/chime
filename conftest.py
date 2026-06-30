import importlib
import pathlib
import platform
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
        monkeypatch.setenv('APPDATA', value=str(home_dir_path))


@pytest.fixture(scope='function', autouse=True)
def silence_audio(reload_chime, monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    """Stub out the OS-level sound player.

    CI runners have no audio device, so actually playing a sound fails (winsound
    raises, aplay exits non-zero). We're testing chime's logic, not the host's audio
    stack, so we replace the player with a no-op that simulates a successful playback.
    Individual tests may re-patch ``chime.run`` to inspect the command that gets built.
    """
    monkeypatch.setattr(chime, 'run', lambda *args, **kwargs: None)
    if platform.system() == 'Windows':
        monkeypatch.setattr(chime.winsound, 'PlaySound', lambda *args, **kwargs: None)
