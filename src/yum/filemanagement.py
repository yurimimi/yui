"""Utilities suite for file management"""
import os
import re
import logging
from typing import TypeAlias
from pathlib import Path
import numpy as np
from skimage.io import imread, imsave

from .imageedit.imageops import crop_image


logger = logging.getLogger(__name__)


RenameResult: TypeAlias = dict[str, str | tuple]


def has_file(directory, checking_filename):
    """Returns True if directory has a filename otherwise returns False."""

    return checking_filename in os.listdir(directory)


class File():
    """Virtual file, file representation

    - [ ] add lazy fields eval, maybe by using a decorator
    """

    abspath: str

    def __init__(self, filename: str):
        # Raise on empty string
        if not filename:
            raise ValueError()

        # Evaluate file's absolute path
        self.abspath = os.path.abspath(os.path.join(os.getcwd(), filename))

        # Raise on invalid name or missing file
        if not os.path.exists(self.abspath):
            raise OSError()

    def get_abspath(self) -> str:
        """Get absolute path of this file"""

        return self.abspath

    def get_base_name(self) -> str:
        """Get base name of this file

        path/to/file.ext -> file
        """

        return Path(self.abspath).stem

    def get_root(self) -> str:
        """Get name of this file

        path/to/file.ext -> path/to/file
        """

        file_name, _ = os.path.splitext(self.abspath)
        return file_name

    def get_name(self) -> str:
        """Get name of this file

        path/to/file.ext -> file.ext
        """
        if self.get_extension() is not None:
            return self.get_base_name() + self.get_extension()

        return self.get_base_name()

    def get_extension(self) -> str | None:
        """Get extension of this file if any. If no ext returns None

        path/to/file.ext -> .ext
        """

        _, file_extension = os.path.splitext(self.abspath)

        if not file_extension:
            return None

        return file_extension

    def rename(self, new_name: str, force_rewrite: bool=False) -> RenameResult:
        """Rename file"""

        file_name = self.get_name()

        # Eval directory path where the file to be renamed located
        procing_dir = self.abspath[:-len(file_name)]

        # Eval new abs path with new file name
        new_abspath = procing_dir + new_name

        result: RenameResult

        # If specified `new_filename` is the same as the current file name do nothing
        if file_name == new_name:
            logger.info("%s unchanged", file_name)

            result = {"status": "unchanged",
                      "names": (file_name, file_name)}
        # If file with `new_filename` already exists do nothing except the case force set to True
        elif has_file(procing_dir, new_name) and not force_rewrite:
            logger.warning("File with name %s already exists! No changes were made.", new_name)

            result = {"status": "collision",
                      "names": (file_name, new_name)}
        # In any other case rename it
        else:
            os.rename(self.abspath, new_abspath)

            logger.info("%s -> %s", file_name, new_name)

            result = {"status": "changed",
                      "names": (file_name, new_name)}

        # Update absolute path
        self.abspath = new_abspath

        return result

    def normalize_filename(self, force_rewrite=False) -> RenameResult:
        """Remove bad symbols in the name of the file"""

        name = self.get_name()

        new_filename = name.strip().replace(" ", "_")
        new_filename = re.sub(r"(?u)[^-\w.]", "", new_filename)

        return self.rename(new_filename, force_rewrite)

    @staticmethod
    def __update_filename_with_version_num(filename, num=0):
        """Updates the filename with a version number if necessary,
        without adding anything if no versioning is needed

        - [ ] It doesn't work. Fix this, please 
        """

        if os.path.isfile(filename):
            name, extension = os.path.splitext(filename)

            num += 1
            name += "_v" + str(num)
            logger.debug(name+extension)
            return File.__update_filename_with_version_num(name+extension, num)

        return filename

    def __repr__(self) -> str:
        return f"Filename {self.abspath}"


class ImageFile(File):
    """Image file manager"""
    image: np.ndarray

    def __init__(self, filename: str):
        File.__init__(self, filename)
        self.image = imread(self.get_abspath())

    def crop(self, args) -> None:
        """Crop image"""

        self.image = crop_image(self.image, args)

    def save(self, output_image, output_filename=None) -> None:
        """Saves file with filename specified"""

        # Set filename
        if output_filename is not None:
            output_filename = output_filename + self.get_extension()
        else:
            output_filename = self.get_name() + "_cropped" + self.get_extension()

        # If file already exists update filename
        output_filename = File.__update_filename_with_version_num(output_filename)
        logger.debug(output_filename)

        imsave(output_filename, output_image)
        print("[v] Saved as", output_filename)


class Directory(File):
    """Virtual directory class

    An object of this class is a virtual file itself. It extends file class with
    some utilities like normalize filenames in this dir, etc.
    The object of this class contains a flat (w/o dir objects) list of its children
    files [!] just a list of abs paths as strings for now.

    I'm not sure about if it does worth it cuz having all the files in the dir as 
    objects, and even before this -- instantiate every single of -- could be quite
    expensive.
    """

    def __init__(self, filename: str):
        File.__init__(self, filename)

        if not os.path.isdir(self.get_abspath()):
            logger.warning("%s is not a directory.", self.get_abspath())
            raise OSError(f"{self.get_abspath()} is not a directory.")

        self.file_list = os.listdir(self.get_abspath())

    def normalize_filenames(self, force_rewrite: bool | None = None) -> list[RenameResult]:
        """Normalize filenames in directory

        This script removes some 'bad'
        symbols from files' names in specified or
        current directory (just spaces for now -3-)
        """

        # v1
        #FileManager.normalize_filenames(self.abspath, force_rewrite)

        # v2
        # For each file in dir rename if file's name contains bad symbols
        change_log: list[RenameResult] = []

        for filename in self.file_list:
            file = File(filename)

            result = file.normalize_filename(force_rewrite=force_rewrite)

            change_log.append(result)

        return change_log

    def add_background(self, filt: str | None=None) -> None:
        """Adds background to images in directory

        Image files to which background to be added can be filtered by regex with
        `filt` argument
        """
        raise NotImplementedError()
