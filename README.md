<div align='center'>
    <h1>horn</h1>
    <q>Python sound notifications made easy.</q>
</div>

I made this because I wanted something simple to monitor number crunching scripts that take some time to run.

## Installation

```sh
pip install horn
```

This library has no dependencies.

## Basic usage

`horn` puts four functions at your disposal:

```py
>>> import horn

>>> horn.success()
>>> horn.warning()
>>> horn.error()
>>> horn.info()
```

Calling each function will play a sound. You're free to use each sound notification in any way you see fit. I'm not your mama.

## Theming

The sounds that are played depend on what theme is being used.

```py
>>> horn.theme()  # return the current theme

```

Several themes are available:

```py
>>> horn.themes()

```

The theme can be changed by passing a theme name to the `theme` function:

```py
>>> horn.theme('wind_waker')
```

## Jupyter/IPython support

Load the extension as so:

```py
%load_ext horn
```

You can wrap a line:

```py
%horn print("I'm a line of code")
```

You can also wrap an entire cell:

```py
%%horn

print("I'm a cell of code")
```

The magic command will call `horn.success()` when the line/cell finishes successfully. Otherwise, `horn.error()` is called if an exception is raised.

## Does this work on X?

Under the hood, `horn` runs a command in the shell to play a `.wav` file. The program that is used depends on the [platform](https://www.wikiwand.com/en/Computing_platform). Platform information is available in `sys.platform` as well as the `platform` module from the standard library. A `UserWarning` is raised if you run this on an unsupported platform. Feel free to get in touch or issue a pull request if you want to add support for a specific platform. I won't bite.

## Things to do

- Some mechanism to automatically call `warning()` when a warning occurs.
- More themes!

## License

As you would except, this is MIT licensed.
