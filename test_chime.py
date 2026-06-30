import importlib
import pathlib
import platform
import shlex
import subprocess
import tempfile
import textwrap
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


def test_no_warning(recwarn):
    chime.success(sync=True)
    assert len(recwarn) == 0


def test_no_exception():
    chime.success(sync=True, raise_error=True)


def test_script():
    subprocess.run(['chime'], check=True)


@pytest.mark.skipif(platform.system() == 'Windows',
                    reason='Windows plays via winsound, which takes the path directly')
def test_play_wav_with_spaces_in_path(tmp_path: pathlib.Path,
                                      monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    """Paths containing spaces must be passed as a single argument (regression for #28)."""
    commands = []
    monkeypatch.setattr(chime, 'run',
                        lambda command, *args, **kwargs: commands.append(command))
    spaced_dir = tmp_path / 'a directory with spaces'
    spaced_dir.mkdir()
    dst = spaced_dir / 'success.wav'
    dst.write_bytes(b'')
    chime.play_wav(dst, sync=True, raise_error=True)
    # Were the path not quoted, the shell would split it into several arguments.
    assert str(dst) in shlex.split(commands[0])


@pytest.mark.parametrize('theme', [theme for theme in chime.themes()])
@pytest.mark.parametrize('event',
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
def test__get_config_path(system: str, expected_config_path: pathlib.Path,
                          monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    monkeypatch.setattr(pathlib.Path, name='home',
                        value=lambda: pathlib.Path('/', 'Users', 'chime'))
    monkeypatch.setenv('APPDATA', '/Users/chime/AppData/Roaming')
    config_path = chime._get_config_path(system)
    # _get_config_path calls .resolve().absolute(); apply the same normalisation to the
    # expected path so the comparison holds on every OS (e.g. Windows prepends a drive).
    assert config_path == expected_config_path.resolve().absolute()


def test_config_file(monkeypatch: _pytest.monkeypatch.MonkeyPatch):
    assert chime.theme() == 'chime'
    config_text = textwrap.dedent("""\
    [chime]
    theme = zelda
    """)
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
