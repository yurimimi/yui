Yui is a utility manager that provides the user with a CLI menu with a variety 
of functions, from image editing to file management. You are very welcome to 
fork and modify it into your utility manager!

I use [this awesome survey lib](https://github.com/Exahilosys/survey) for this app.

# Installation and use

To install, run this

```bash
python -m pip install git+https://github.com/yurimimi/yui.git@master
```

To make it show up in your command line, just call

```bash
yui # or python -m yui
```

You can also call a function immediately by typing its name as argument.

```bash
yui <function>
```

## Development

To use this package in editable mode, which means that it will be called from 
the project directory each time Yui is executed, taking into account the 
changes you made there, clone this repository first, and then install it using 
pip with the -e option:

```bash
git clone https://github.com/yurimimi/yui.git ~/src/yui
pip install -e ~/src/yui
```

# Functions

**File management**

- Normalize filenames in a directory

`normalize_filenames` removes 'bad' symbols and trailing whitespaces. Got it [here](https://github.com/django/django/blob/ca5cd3e3e8e53f15e68ccd727ec8fe719cc48099/django/utils/text.py#L269).

- Generate `.gitignore` for a specific project (WIP)

Does not work yet.

**Image operations**

This functions catalog is an attempt to adapt the [skimage](https://github.com/scikit-image/scikit-image/tree/main/skimage) 
library as a lightweight set of image processing utilities for use from the 
command line.

- Crop image

`crop_image` crops the image from its edges based on the specified range of 
pixels. The parameters order is like CSS's padding and margin.

- Expand image

`expand_image` works like `crop_image` but inversely: it expands the image at 
the edges, filling the area with transparency.

- Add background (WIP)

Does not work yet.

**System-related**

- Check battery(-ies)

`battery_check` shows the percentage of the current battery charge. It takes either one
arg—the battery number—or shows the summary charge if no argument was provided.

- Set brightness

`set_brightness` calls `xrandr` to set the brightness with a value specified as an argument
here. The argument can be an absolute value, e.g., 100 or 75, or a relative one like -15
or +5.

**Misc**

- Set wallpaper

`set_wallpaper` replaces the feh --bg (background) command in .xinitrc with a new one with 
a set wallpaper image.

# Todo

For to do list see ./todo.md file.
