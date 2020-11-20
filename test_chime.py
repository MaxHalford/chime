import importlib
import pathlib
import platform
import subprocess
import tempfile
import textwrap
import time
import typing

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
                         [('Linux', pathlib.Path('/', 'Users', 'chime', '.config', 'chime',
                                                 'chime.conf')),
                          ('Darwin', pathlib.Path('/', 'Users', 'chime', '.config', 'chime',
                                                  'chime.conf')),
                          ('Windows', pathlib.Path('/', 'Users', 'chime', 'AppData', 'Roaming',
                                                   'chime', 'chime.ini'))])
def test__get_config_path(system: str, expected_config_path: str,
                          monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    monkeypatch.setattr(pathlib.Path, name='home',
                        value=lambda: pathlib.Path('/', 'Users', 'chime'))
    monkeypatch.setenv('APPDATA', '/Users/chime/AppData/Roaming')
    config_path = chime._get_config_path(system)
    assert config_path == expected_config_path


def test_config_file(monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    assert chime.theme() == 'chime'
    config_text = textwrap.dedent('''\
    [chime]
    theme = zelda
    ''')
    config_file_dir = pathlib.Path('.config', 'chime')
    monkeypatch.setattr(platform, name='system', value=lambda: 'Linux')
    with tempfile.TemporaryDirectory() as home_dir:
        home_dir_path = pathlib.Path(home_dir)
        monkeypatch.setattr(pathlib.Path, name='home', value=lambda: home_dir_path)
        full_config_dir = (home_dir_path / config_file_dir)
        full_config_dir.mkdir(parents=True)
        (full_config_dir / pathlib.Path('chime.conf')).write_text(config_text)
        importlib.reload(chime)
        assert chime.theme() == 'zelda'
