import argparse
import base64
import configparser
import os
import pathlib
import platform
import random
import shlex
import subprocess as sp
import sys
import typing
import warnings

if platform.system() == "Windows":
    import winsound


def _is_wsl() -> bool:
    """Return whether we're running inside the Windows Subsystem for Linux."""
    if platform.system() != "Linux":
        return False
    return "microsoft" in platform.uname().release.lower()

try:
    from IPython.core import magic

    IPYTHON_INSTALLED = True
except ImportError:
    IPYTHON_INSTALLED = False


def _get_config_path(system: str) -> pathlib.Path:
    """Return the path of the config file.

    Parameters:
        system: The OS being used.
    """
    home_dir = pathlib.Path.home()
    if system == "Windows":
        config_path = pathlib.Path(
            os.getenv("APPDATA", home_dir / pathlib.Path("AppData", "Roaming"))
        ) / pathlib.Path("chime", "chime.ini")
    else:
        config_path = home_dir / pathlib.Path(".config", "chime", "chime.conf")
    return config_path.resolve().absolute()


def _get_default_theme(path: pathlib.Path, fallback_theme: str) -> str:
    """Check for the existence of a theme in a config file.

    Parameters:
        path: Path of the config file.
        fallback_theme: The theme to fallback to if a config file is not found or contains no
            theme.

    """
    if path.exists():
        config = configparser.ConfigParser()
        config.read(path)
        if "chime" in config:
            default_theme = config["chime"].get("theme", fallback_theme)
        else:
            default_theme = fallback_theme
    else:
        default_theme = fallback_theme
    return default_theme


def _get_default_run_args(path: pathlib.Path) -> str:
    """Check for the existence of default run arguments in a config file.

    Parameters:
        path: Path of the config file.

    """
    if path.exists():
        config = configparser.ConfigParser()
        config.read(path)
        if "chime" in config:
            default_args = config["chime"].get("cli_args", "")
        else:
            default_args = ""
    else:
        default_args = ""
    return default_args


config_path = _get_config_path(platform.system())
THEME = _get_default_theme(config_path, fallback_theme="chime")
RUN_ARGS = _get_default_run_args(config_path)


__all__ = ["error", "info", "notify_exceptions", "success", "theme", "themes", "warning"]


def run(command, sync: bool, raise_error: bool, shell: bool = True):
    if sync:

        try:
            sp.run(command, shell=shell, check=True, stdout=sp.PIPE, stderr=sp.PIPE)
        except sp.CalledProcessError as e:
            stderr = e.stderr.decode().strip() if e.stderr else ""
            msg = f"{e} stderr: {stderr}"
            if raise_error:
                raise RuntimeError(msg)
            else:
                warnings.warn(msg)
    else:
        sp.Popen(command, shell=shell, stderr=sp.DEVNULL)


def play_wav(path: pathlib.Path, sync=True, raise_error=True):
    """Play a .wav file.

    This function is platform agnostic, meaning that it will determine what to do based on
    the `sys.platform` variable.

    Parameters:
        path: Path to a .wav file.
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played asynchronously in a separate process. In such a case, the process will
            fail silently if an error occurs.
        raise_error: Whether to raise an exception when an occurs, or instead to just send a
            warning.

    Raises:
        RuntimeError: If the platform is not supported.

    """

    # When running in the browser (Pyodide/Emscripten) there is no shell to play
    # sound with, so we hand the audio off to the Web Audio API via the bundled bytes.
    if sys.platform == "emscripten":
        play_wav_in_browser(path, raise_error)
        return

    system = platform.system()
    quoted = shlex.quote(str(path))

    if _is_wsl():
        # WSL has no audio device of its own, so we play the file through the
        # Windows host using PowerShell's SoundPlayer.
        win_path = sp.run(
            ["wslpath", "-w", str(path)], stdout=sp.PIPE, text=True
        ).stdout.strip()
        ps = f"(New-Object Media.SoundPlayer '{win_path}').PlaySync()"
        run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps],
            sync,
            raise_error,
            shell=False,
        )

    elif system == "Darwin":
        run(f"afplay {RUN_ARGS} {quoted}", sync, raise_error)

    elif system == "Linux":
        run(f"aplay {RUN_ARGS} {quoted}", sync, raise_error)

    elif system == "OpenBSD":
        run(f"aucat {RUN_ARGS} -i {quoted}", sync, raise_error)

    elif system == "Windows":
        flags = winsound.SND_FILENAME
        if not sync:
            flags |= winsound.SND_ASYNC
        try:
            winsound.PlaySound(str(path), flags)
        except RuntimeError as e:
            if raise_error:
                raise e
            else:
                warnings.warn(str(e))

    else:
        raise RuntimeError(f"Unsupported platform ({sys.platform})")


def play_wav_in_browser(path: pathlib.Path, raise_error: bool):
    """Play a .wav file in the browser via the Web Audio API.

    This is used when chime runs under Pyodide/Emscripten, where there is no shell to
    spawn an audio player. The .wav bytes are embedded in a data URL and handed to a
    JavaScript ``Audio`` element. Playback is always asynchronous in this context.
    """
    try:
        from js import Audio  # type: ignore

        data = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
        Audio.new(f"data:audio/wav;base64,{data}").play()
    except Exception as e:  # pragma: no cover - only reachable in a browser
        if raise_error:
            raise
        else:
            warnings.warn(str(e))


def themes_dir() -> pathlib.Path:
    """Return the directory where the themes are located."""
    here = pathlib.Path(__file__).parent
    return here.joinpath("themes")


def current_theme_dir() -> pathlib.Path:
    """Return the current theme's sound directory."""
    if THEME == "random":
        return themes_dir().joinpath(random.choice(themes()))
    return themes_dir().joinpath(THEME)


def themes() -> typing.List[str]:
    """Return the available themes to choose from."""
    return sorted(
        theme.name
        for theme in themes_dir().iterdir()
        if not theme.name.startswith(".")  # ignores .DS_Store on MacOS
    )


def theme(name: typing.Optional[str] = None):
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

    if name != "random" and name not in themes():
        raise ValueError(f"Unknown theme ({name})")

    THEME = name


def notify(event: str, sync: bool, raise_error: bool):
    wav_path = current_theme_dir().joinpath(f"{event}.wav")
    if not wav_path.exists():
        raise ValueError(f"{wav_path} doesn't exist")
    play_wav(wav_path, sync, raise_error)


def success(sync=False, raise_error=False):
    """Make a success sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.
        raise_error: Whether to raise an exception when an occurs, or instead to just send a
            warning.

    """
    return notify("success", sync, raise_error)


def warning(sync=False, raise_error=False):
    """Make a warning sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.
        raise_error: Whether to raise an exception when an occurs, or instead to just send a
            warning.

    """
    return notify("warning", sync, raise_error)


def error(sync=False, raise_error=False):
    """Make an error sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.
        raise_error: Whether to raise an exception when an occurs, or instead to just send a
            warning.

    """
    return notify("error", sync, raise_error)


def info(sync=False, raise_error=False):
    """Make a generic information sound.

    Parameters:
        sync: The sound file will be played synchronously if this is `True`. If not, then the sound
            will be played in a separate process. In such a case, the process will fail silently if
            an error occurs.
        raise_error: Whether to raise an exception when an occurs, or instead to just send a
            warning.

    """
    return notify("info", sync, raise_error)


def notify_exceptions():
    """Will call error() whenever an exception occurs."""

    def except_hook(exctype, value, traceback):
        error()
        sys.__excepthook__(exctype, value, traceback)

    sys.excepthook = except_hook

    if IPYTHON_INSTALLED:

        class Watcher:
            def __init__(self, ipython):
                self.shell = ipython

            def post_run_cell(self, result):
                if result.error_in_exec:
                    error()

        try:
            ipython = get_ipython()
        except NameError:
            return

        watcher = Watcher(ipython)
        ipython.events.register("post_run_cell", watcher.post_run_cell)


if IPYTHON_INSTALLED:

    @magic.magics_class
    class ChimeMagics(magic.Magics):
        @magic.needs_local_scope
        @magic.line_cell_magic
        def chime(self, line, cell=None, local_ns=None):
            def run(code):
                try:
                    exec(code, local_ns)
                    success()
                except Exception as e:
                    error()
                    raise e

            if cell is None:
                run(line)
            else:
                run(cell)

    def load_ipython_extension(ipython):
        ipython.register_magics(ChimeMagics)


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "event",
        nargs="?",
        default="success",
        help="either one of {success, warning, error, info}",
    )
    parser.add_argument("--theme", help=f'either one of {{{", ".join(themes())}}}')
    args = parser.parse_args()
    if args.theme:
        theme(args.theme)
    notify(args.event, sync=False, raise_error=False)


if __name__ == "__main__":
    main()
