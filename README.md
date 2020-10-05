<div align='center'>
    <h1>horn</h1>
    <q>Python sound notifications made easy.</q>
    <br>
</div>

I made this because I wanted something simple to monitor long-running number crunching scripts.

## Installation

```sh
pip install horn
```

This library has no dependencies. The IPython/Jupyter functionality is only imported if you've installed the `ipython` library. It should work for any Python version above or equal to 3.4.

## Basic usage

`horn` puts four functions at your disposal:

```py
>>> import horn

>>> horn.success()
>>> horn.warning()
>>> horn.error()
>>> horn.info()

```

Calling any of the above functions will play a sound. Note that the sounds are played in separate processes, and are thus non-blocking. Each function should take around 2ms to execute. You're free to use each sound notification in any way you see fit. I'm not your mama.

## Theming

The sounds that are played depend on which theme is being used.

```py
>>> horn.theme()  # return the current theme
'chime'

```

Several themes are available:

```py
>>> horn.themes()
['chime', 'mario', 'zelda']

```

The theme can be changed by passing a theme name to the `theme` function:

```py
>>> horn.theme('zelda')

```

Note that if you set the theme to `'random'`, a random theme will be picked each time you play a sound.

## IPython/Jupyter magic

Load the extension as so:

```py
%load_ext horn
```

You can wrap a line:

```py
%horn print("I'm a line")
```

You can also wrap an entire cell:

```py
%%horn

print("I'm a cell")
```

The magic command will call `horn.success()` when the line/cell finishes successfully. Otherwise, `horn.error()` is called whenever an exception is raised.

## Exception notifications

If you run `horn.notify_exceptions()`, then `horn.error()` will be called whenever an exception is raised.

```py
horn.notify_exceptions()

raise ValueError("I'm going to make some noise")
```

## Platform support

Under the hood, `horn` runs a command in the shell to play a `.wav` file. The program that is used depends on the [platform](https://www.wikiwand.com/en/Computing_platform). Platform information is available in `sys.platform` as well as the `platform` module from the standard library. Currently, the supported platforms are:

- `darwin` (which is technically an OS, but whatever)
- `linux`
- `windows`

A `UserWarning` is raised if you run this on an unsupported platform. Feel free to get in touch or issue a pull request if you want to add support for a specific platform. Likewise if you're having trouble with one of the above platforms. I won't bite.

## Things to do

- Some mechanism to automatically call `horn.warning()` when a warning occurs.
- More themes!

## Adding a new theme

I have toyed with the idea of allowing users to add their own theme(s), but at the moment I rather keep things minimal. However, I'm happy to integrate new themes into the library. You can propose a new theme by [opening a pull request](https://github.com/creme-ml/creme/issues/new) that adds the necessary .wav files to the [`themes` directory](https://github.com/MaxHalford/horn/tree/main/themes). Be creative 👩‍🎨!

## What about unit tests?

God no. I wouldn't even know where to begin.

## License

As you would probably except, this is MIT licensed.
