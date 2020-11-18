import subprocess
import time
import typing

import _pytest.monkeypatch
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


@pytest.mark.parametrize("theme", [theme for theme in chime.themes()])
@pytest.mark.parametrize("event",
                         [lambda x: x.error(), lambda x: x.info(), lambda x: x.success(),
                          lambda x: x.warning()])
def test_theme_events(theme: str, event: typing.Callable):
    chime.theme(theme)
    assert event(chime) is None


@pytest.mark.parametrize('system, expected_config_path',
                         [('Linux', '/Users/chime/.config/chime/chime.conf'),
                          ('Darwin', '/Users/chime/.config/chime/chime.conf'),
                          ('Windows', '/Users/chime/AppData/Roaming/chime/chime.ini')])
def test__get_config_path(system: str, expected_config_path: str,
                          monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    monkeypatch.setenv('HOME', '/Users/chime')
    monkeypatch.setenv('APPDATA', '/Users/chime/AppData/Roaming')
    config_path = chime._get_config_path(system)
    assert config_path.as_posix() == expected_config_path
