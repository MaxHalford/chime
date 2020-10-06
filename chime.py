import pathlib
import platform
import random
import subprocess
import sys
import typing
import warnings

if platform.system() == 'Windows':
    import winsound

try:
    from IPython.core import magic
    IPYTHON_INSTALLED = True
except ImportError:
    IPYTHON_INSTALLED = False


THEME = 'chime'  # default theme


__all__ = [
    'error',
    'info',
    'notify_exceptions',
    'success'
    'theme',
    'themes',
    'warning'
]


def run(command: str, sync: bool):
    if sync:

        try:
            pipe = subprocess.PIPE
            subprocess.run(command, shell=True, check=True, stdout=pipe, stderr=pipe)
        except subprocess.CalledProcessError as e:
            warnings.warn(f'{e} stderr: {e.stderr.decode().strip()}')
    else:
        subprocess.Popen(command, shell=True, stderr=subprocess.DEVNULL)


def play_wav(path: pathlib.Path, sync=True):
    """Play a .wav file.

    This function is platform agnostic, meaning that it will determine what to do based on
    the `sys.platform` variable.

    Parameters:
        path: Path to a .wav file.
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played asynchronously in a separate process. In such a case, the process will
            fail silently if an error occurs.

    Raises:
        RuntimeError: If the platform is not supported.

    """

    system = platform.system()

    if system == 'Darwin':
        run(f'afplay {path}', sync)
    elif system == 'Linux':
        run(f'aplay {path}', sync)
    elif system == 'Windows':
        winsound.PlaySound(str(path), winsound.SND_ASYNC | winsound.SND_FILENAME)
    else:
        raise RuntimeError(f'Unsupported platform ({sys.platform})')


def themes_dir() -> pathlib.Path:
    """Return the directory where the themes are located."""
    here = pathlib.Path(__file__).parent
    return here.joinpath('themes')


def current_theme_dir() -> pathlib.Path:
    """Return the current theme's sound directory."""
    if THEME == 'random':
        return themes_dir().joinpath(random.choice(themes()))
    return themes_dir().joinpath(THEME)


def themes() -> typing.List[str]:
    """Return the available themes to choose from."""
    return sorted(
        theme.name
        for theme in themes_dir().iterdir()
        if not theme.name.startswith('.')  # ignores .DS_Store on MacOS
    )


def theme(name: str = None):
    """Set the current theme.

    Parameters:
        name: The change will be switched if a valid name is provided. The current theme is
            returned if `None`.

    Raises:
        ValueError: If the theme is unknown.

    """

    global THEME

    if name is None:
        return THEME

    if name != 'random' and name not in themes():
        raise ValueError(f'Unknown theme ({name})')

    THEME = name


def notify(event: str, sync: bool):
    wav_path = current_theme_dir().joinpath(f'{event}.wav')
    if not wav_path.exists():
        raise ValueError(f"{wav_path} is doesn't exist")
    play_wav(wav_path, sync)


def success(sync=False):
    """Make a success sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.

    """
    return notify('success', sync)


def warning(sync=False):
    """Make a warning sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.

    """
    return notify('warning', sync)


def error(sync=False):
    """Make an error sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.

    """
    return notify('error', sync)


def info(sync=False):
    """Make a generic information sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.

    """
    return notify('info', sync)


def notify_exceptions():
    """Will call error() whenever an exception occurs."""

    def except_hook(exctype, value, traceback):
        error(sync=False)
        sys.__excepthook__(exctype, value, traceback)
    sys.excepthook = except_hook

    if IPYTHON_INSTALLED:

        class Watcher:

            def __init__(self, ipython):
                self.shell = ipython

            def post_run_cell(self, result):
                if result.error_in_exec:
                    error(sync=False)

        try:
            ipython = get_ipython()
        except NameError:
            return

        watcher = Watcher(ipython)
        ipython.events.register('post_run_cell', watcher.post_run_cell)


if IPYTHON_INSTALLED:

    @magic.magics_class
    class ChimeMagics(magic.Magics):

        @magic.line_cell_magic
        def chime(self, line, cell=None):

            def run(code):
                try:
                    exec(line)
                    success()
                except Exception as e:
                    error()

            if cell is None:
                run(line)
            else:
                run(cell)

    def load_ipython_extension(ipython):
        ipython.register_magics(ChimeMagics)
