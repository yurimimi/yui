Yum ( Yu's utility manager/menu )

It frees your from memorizing script file names so that you only has to call for one script
which shows every script in the specified folder and you can choose and run one or more
than one.

This menu tool uses [survey](https://github.com/Exahilosys/survey) for the interactive
menu.

I had been interested in automating stuff like file rename, normalization and other
management stuff so I decided to learn Python for that. In a couple of days I got some
set of scripts to rename things, edit images, and generate files. It's a lot for me so
why not to build a tool that manages it for me? For UI I had chosen a CLI lib of course
because it's something new for me and I want to learn it and also because we don't have
to switch from one context (terminal) to another (GUI) while working from command line.

At the beginning I just imported every single script and module into a main file which
managed that stuff for me with a simple CLI menu. After that, consulting with ChatGPT,
I figured that dynamically import stuff will be more... Idk it's just better.

Also, while working on the normalization and renaming many files at once in general I've
abstracted some of the file operations like getting parts of the filename, renaming one,
also added an ImageFile class with crop function from the image editing scripts so in the
future I could crop (and do other image manipulations) on many images at once. I believe
it'll work out.

Now I'm not sure how do I manage all of these as package. The packaging thing! I never ded
it before. I have problems with importing modules though it's pretty simple but I would
like to focus on other things than mapping all the files in my mind.

- [ ] managing a Python project. Packagin and import.

After that I have to design a convenient enough menu logic, simply name it front-end.
There are many ideas from simply reinvent something or to use some existing patterns like
MVC for this project.

Now I'm thinking of transforming the scripts into a business logic component as in a normal
application, that is that not juts importing some scripts but using predefined (business)
logic of a self-contained software.
