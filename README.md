<div align="center">
  <h1>chime</h1>
  <q><i>Python sound notifications made easy.</i></q>
</div>
<br>

<div align="center">
  <!-- Tests -->
  <a href="https://github.com/MaxHalford/chime/actions?query=workflow%3Atests">
    <img src="https://github.com/MaxHalford/chime/workflows/tests/badge.svg?style=flat-square" alt="tests">
  </a>
  <!-- Soundboard -->
  <a href="https://chime-soundboard.herokuapp.com/">
    <img src="https://github.com/MaxHalford/chime/workflows/soundboard/badge.svg?style=flat-square" alt="soundboard">
  </a>
  <!-- PyPI -->
  <a href="https://pypi.org/project/chime">
    <img src="https://img.shields.io/pypi/v/chime.svg?label=release&color=blue&style=flat-square" alt="pypi">
  </a>
  <!-- PePy -->
  <a href="https://pepy.tech/project/chime">
    <img src="https://img.shields.io/badge/dynamic/json?style=flat-square&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fchime" alt="pepy">
  </a>
  <!-- License -->
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="license">
  </a>
</div>
<br>

## Table of contents

- [Table of contents](#table-of-contents)
- [Motivation](#motivation)
- [Installation](#installation)
- [Basic usage](#basic-usage)
- [Theming](#theming)
- [IPython/Jupyter magic](#ipythonjupyter-magic)
- [Exception notifications](#exception-notifications)
- [Command-line usage](#command-line-usage)
- [Platform support](#platform-support)
- [I can't hear anything 🙉](#i-cant-hear-anything-)
- [Adding a new theme](#adding-a-new-theme)
- [Things to do](#things-to-do)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Motivation

I made this because I wanted a simple auditory cue system to tell me when a long-running number crunching script had finished. I didn't want to have to fiddle with the command-line, and also wanted a cross-platform solution. Thus was born `chime`!

## Installation

```sh
pip install chime
```

This library has **no dependencies**. The IPython/Jupyter functionality is only imported if you've installed the `ipython` library. It should work for any Python version above or equal to 3.6.

## Basic usage

`chime` puts four functions at your disposal:

```py
>>> import chime

>>> chime.success()
>>> chime.warning()
>>> chime.error()
>>> chime.info()

```

Calling any of the above functions will play a sound. Note that the sounds are played in asynchronous processes, and are thus non-blocking. Each function should take around 2ms to execute, regardless of the sound length. You're free to use each sound notification in any way you see fit. I'm not your mama.

## Theming

The sounds that are played depend on which theme is being used.

```py
>>> chime.theme()  # return the current theme
'chime'

```

Several themes are available:

```py
>>> chime.themes()
['big-sur', 'chime', 'mario', 'material', 'zelda']

```

The theme can be changed by passing a theme name to the `theme` function:

```py
>>> chime.theme('zelda')

```

A couple of things to note:

- You can listen to the sounds interactively via [this soundboard](https://chime-soundboard.herokuapp.com/), which is made with [Streamlit](https://www.streamlit.io/).
- A random theme will be picked each time you play a sound if you set the theme to `'random'`.

## IPython/Jupyter magic

Load the extension as so:

```py
%load_ext chime
```

You can wrap a line:

```py
%chime print("I'm a line")
```

You can also wrap an entire cell:

```py
%%chime

print("I'm a cell")
```

The magic command will call `chime.success` when the line/cell finishes successfully. Otherwise, `chime.error` is called whenever an exception is raised.

## Exception notifications

If you run `chime.notify_exceptions`, then `chime.error` will be called whenever an exception is raised.

```py
chime.notify_exceptions()

raise ValueError("I'm going to make some noise")
```

## Command-line usage

You can run `chime` from the command-line:

```sh
$ chime
```

By default, this will play the success sound. You can also choose which sound to play, like so:

```sh
$ chime info
```

You can also choose which theme to use:

```sh
$ chime info --theme zelda
```

If you're using bash, then you can use `chime` to notify you when a program finishes:

```sh
$ echo "Hello world!"; chime
```

This will play the sound regardless of the fact that the first command succeeded or not. If you're running on Windows, then you can run the following equivalent:

```sh
> echo "Hello world!" & chime
```

## Platform support

Under the hood, `chime` runs a command in the shell to play a `.wav` file. The command-line program that is used depends on the [platform](https://www.wikiwand.com/en/Computing_platform) that you're using. Platform information is available in the [`sys.platform` variable](https://docs.python.org/3/library/sys.html#sys.platform) as well as the [`platform` module](https://docs.python.org/3/library/platform.html) from the standard library. Currently, the supported platforms are:

- Darwin
- Linux
- Windows

A `UserWarning` is raised if you run a `chime` sound on an unsupported platform. Feel free to get in touch or issue a pull request if you want to add support for a specific platform. Likewise, don't hesitate if you're encountering trouble with one of the above platforms. I won't bite.

## I can't hear anything 🙉

Did you check if you turned your sound on? Just kidding. 😜

This library is designed to be non-invasive. By default, sounds are played asynchronously in unchecked processes. Therefore, if something goes wrong, the process dies silently. If you can't hear anything and you think that the issue is coming from `chime`, then set the `sync` parameter when you play a sound:

```py
>>> chime.info(sync=True)

```

This will play the sound synchronously and issue a warning if something goes wrong, which should allow you to debug the issue. You can also raise an exception instead of sending a warning by setting the `raise_error` parameter:

```py
>>> chime.info(sync=True, raise_error=True)

```

Note that setting `raise_error` won't do anything if `sync` is set to `False`.

## Adding a new theme

I have toyed with the idea of allowing users to add their own theme(s), but at the moment I rather keep things minimal. However, I'm happy to integrate new themes into the library. You can propose a new theme by [opening a pull request](https://github.com/creme-ml/creme/issues/new) that adds the necessary .wav files to the [`themes` directory](https://github.com/MaxHalford/chime/tree/main/themes). A theme is made up of four files: `success.wav`, `warning.wav`, `error.wav`, and `info.wav`. Be creative! 👩‍🎨

## Things to do

- Some mechanism to automatically call `chime.warning` when a warning occurs.
- More themes!

## Acknowledgements

- Special thanks to [Michael Vlah](https://github.com/vlahm) for being a gentleman by giving up the "chime" name on PyPI.
- Thanks to u/Pajke on reddit for helping me debug Windows support.
- Thanks to [David Chen](https://github.com/dchen327) for adding Linux support by suggesting the use of [aplay](https://linux.die.net/man/1/aplay).
- Thanks to [Vincent Warmerdam](https://twitter.com/fishnets88) for suggesting a command-line interface.
- Calmcode made a [video introduction to chime](https://calmcode.io/chime/introduction.html) ❤️
- Thanks to [Paulo S. Costa](https://github.com/paw-lu) for improving the command-line interface.

## License

As you would probably expect, this is [MIT licensed](LICENSE).
