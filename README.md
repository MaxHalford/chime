<div align='center'>
  <h1>chime</h1>
  <q><i>Python sound notifications made easy.</i></q>
</div>
<br>

<div align='center'>
  <!-- CI -->
  <a href="https://github.com/MaxHalford/chime/actions">
    <img src="https://github.com/MaxHalford/chime/workflows/chime/badge.svg?style=flat-square" alt="ci">
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

I made this because I wanted something simple to monitor long-running number crunching scripts.

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
['chime', 'mario', 'zelda']

```

The theme can be changed by passing a theme name to the `theme` function:

```py
>>> chime.theme('zelda')

```

Note that if you set the theme to `'random'`, a random theme will be picked each time you play a sound.

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

## Platform support

Under the hood, `chime` runs a command in the shell to play a `.wav` file. The command-line program that is used depends on the [platform](https://www.wikiwand.com/en/Computing_platform). Platform information is available in the [`sys.platform` variable](https://docs.python.org/3/library/sys.html#sys.platform) as well as the [`platform` module](https://docs.python.org/3/library/platform.html) from the standard library. Currently, the supported systems are:

- Darwin
- Linux
- Windows

A `UserWarning` is raised if you run a `chime` sound on an unsupported platform. Feel free to get in touch or issue a pull request if you want to add support for a specific platform. Likewise, don't hesitate if you're encountering trouble with one of the above platforms. I won't bite.

## It's not working

Did you check if you turned your sound on? Just kidding. 😜

This library is designed to be non-invasive by default. Therefore, if something goes wrong, it fails silently. If you can't hear any sound and you think that the issue is coming from `chime`, then set the `silent` parameter to `False` when you make a sound:

```py
>>> chime.info(silent=False)

```

This will play the sound synchronously and print an error if something goes wrong.

## Adding a new theme

I have toyed with the idea of allowing users to add their own theme(s), but at the moment I rather keep things minimal. However, I'm happy to integrate new themes into the library. You can propose a new theme by [opening a pull request](https://github.com/creme-ml/creme/issues/new) that adds the necessary .wav files to the [`themes` directory](https://github.com/MaxHalford/chime/tree/main/themes). Be creative! 👩‍🎨

## Things to do

- Some mechanism to automatically call `chime.warning` when a warning occurs.
- Command-line support, maybe.
- More themes!

## Acknowledgements

- Special thanks to @vlahm for giving up the "chime" name on PyPI.
- Thanks to @dchen327 for adding Linux support by suggesting the use of [aplay](https://linux.die.net/man/1/aplay).

## License

As you would probably expect, this is MIT licensed.
