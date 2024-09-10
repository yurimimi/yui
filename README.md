Yui is a utility manager that provides the user with a CLI menu with various functions,
from image edit to file management. You are very welcome to fork it and modify so that it
becomes your utility manager!

I use [this awesome survey lib](https://github.com/Exahilosys/survey) for this app.

# Installation and use

To install, run this

```bash
python -m pip install git+https://github.com/yurimimi/yui.git@master
```

To make it show up in your command line, just call

```bash
yui
```

or

```bash
python -m yui
```

You can also call a function by it's name as an argument

```bash
yui <function>
```

# Utils

- File management

  - Normalize filenames in a directory

  `normalize_filenames` removes 'bad' symbols and trailing whitespaces. Got it [here](https://github.com/django/django/blob/ca5cd3e3e8e53f15e68ccd727ec8fe719cc48099/django/utils/text.py#L269).

  - Generate `.gitignore` for a specific project (WIP)

  Does not work yet.

- Image operations

  - Crop image

  `crop_image` crops the image from its edges based on the specified range of pixels.
  The parameters order is like CSS's padding and margin.

  - Expand image

  `expand_image` works like `crop_image` but inversely: it expands the image at the edges
  filling the area with transparency.

  - Add background (WIP)

  Does not work yet.

- System related

  - Check battery(-ies)

  `battery_check` shows the percentage of the current battery charge. It takes either one
  arg - the battery number, or shows the summary charge if no argument was provided.

  - Set brightness

  `set_brightness` calls `xrandr` to set the brightness with a value specified as an argument
  here. The argument can be an absolute value, e.g., 100 or 75, or a relative one like -15
  or +5.

# Contrib

Please don't hesitate to add stuff and fix grammatical and other mistakes in the text
(comments, docs, etc.) because I'm just learning English. It'll help me a lot. :)

# Todo

## general

- categorise utils
- select multiple utils to run
  - specify order of exectution
- better navigation

## git related stuff

- add git config file generator with presets and/or custom configuration
  - custom config managed by yui, somewhat `git config` does
  - but yui can keep a number of configs at the time, so you can ask it to generate the file for a particular repo (directory)
  - it has a nice CLI
  - it keeps all the presets in a config file that the user could upload somewhere like GitHub to share (locally kept at .config)
- could I finally implement the .gitignore file generator..?
