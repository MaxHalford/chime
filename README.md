<div align='center'>
    <h1>chime</h1>
    <q><i>Python sound notifications made easy.</i></q>
</div>
<br>

I made this because I wanted something simple to monitor long-running number crunching scripts.

Special thanks to [Michael Vlah](https://github.com/vlahm) for giving up the "chime" name on PyPI.

## Installation

```sh
pip install chime
```

This library has **no dependencies**. The IPython/Jupyter functionality is only imported if you've installed the `ipython` library. It should work for any Python version above or equal to 3.4.

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

Under the hood, `chime` runs a command in the shell to play a `.wav` file. The command-line program that is used depends on the [platform](https://www.wikiwand.com/en/Computing_platform). Platform information is available in the [`sys.platform` variable](https://docs.python.org/3/library/sys.html#sys.platform) as well as the [`platform` module](https://docs.python.org/3/library/platform.html) from the standard library. Currently, the supported platforms are:

- `darwin` (which is technically an OS, but whatever)
- `linux`
- `windows`

A `UserWarning` is raised if you run a `chime` sound on an unsupported platform. Feel free to get in touch or issue a pull request if you want to add support for a specific platform. Likewise, don't hesitate if you're encountering trouble with one of the above platforms. I won't bite.

## Adchime a new theme

I have toyed with the idea of allowing users to add their own theme(s), but at the moment I rather keep things minimal. However, I'm happy to integrate new themes into the library. You can propose a new theme by [opening a pull request](https://github.com/creme-ml/creme/issues/new) that adds the necessary .wav files to the [`themes` directory](https://github.com/MaxHalford/chime/tree/main/themes). Be creative 👩‍🎨!

## Things to do

- Some mechanism to automatically call `chime.warning` when a warning occurs.
- Command-line support, maybe.
- More themes!

## What about unit tests?

God no. I wouldn't even know where to begin.

## License

As you would probably expect, this is MIT licensed.
