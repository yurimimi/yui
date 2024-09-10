"""Expand image with transparent background (for now only transparent)."""
import logging
import argparse
from filemanagement.core import ImageFile

from ..ui import notify


logger = logging.getLogger(__name__)


YUI_HELP = """Expand an image

Image will be expanded at the edges with transparent background.

Paremeters
----------
path : str
    With -i flag
    Absolute or relative path to the image.
expand_args : str
    With -e flag
    Format is either X,X,X,X or X,X,X or X,X or X where X is count of
    pixels to expand the image at its edges, clockwise. For example,
    if you want to make it wider use something like 0,50,0,50 or just
    0,50,0.
    With -o flag
output_path : str, optional
    Absolute or relative path where to save expanded image."""


def _parse_args(args):
    """Parse command line arguments and return"""

    # Set up args parser
    parser = argparse.ArgumentParser(prog="Expand image",)
    parser.add_argument("-i", "--input",
                        help="""input image to edit""",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="""output image location (optional)""",
                        required=False)
    # Make it like css think where 0,1 is actually 0,1,0,1
    # 0,1,2 is actually 0,1,2,1
    # 2 is actually 2,2,2,2
    # etc.
    parser.add_argument("-e", "--expand",
                        help="""expand parameters""",
                        required=True)
    # Get all specified arguments
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args.split())

    return args


def main(args=None) -> None:

    # Parse args
    args = _parse_args(args)
	# Read image
    image_file = ImageFile(args.input)
    logger.debug("Input image shape %s", image_file.image.shape)
    # Expand image
    image_file.expand(args.expand)
    logger.debug("Output image shape %s", image_file.image.shape)
	# Save image file
    result = image_file.save(args.output)
    if isinstance(result, Exception):
        notify(f"{result}", "err")
    else:
        notify(f"Saved as {image_file.get_name()}", "ok")


if __name__ == "__main__":
    main()
