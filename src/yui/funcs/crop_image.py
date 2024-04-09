"""Crop an image."""
import logging
import argparse

from ..filemanagement import ImageFile


logger = logging.getLogger(__name__)


YUI_HELP = """Crop an image.

Image will be cropped from the edges. 

Parameters
----------
path : str
    Absolute or relative path to the image.
crop_args : str
    Format is either X,X,X,X or X,X,X or X,X or X where X is count of
    pixels to crop from the edges, clockwise. For example, if you want
    to make it narrower use something like 0,50,0,50 or just 0,50,0.
output_path : str, optional
    Absolute or relative path where to save cropped image."""


def _parse_args(args):
    """Parse command line arguments and return"""

    # Set up args parser
    parser = argparse.ArgumentParser(
                        prog="Crop image",
                        description="""This script crops image
                        how??
                        output file is output.<ext> if output arg is not
                        specified.""",)
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
    parser.add_argument("-c", "--crop",
                        help="""crop parameters [description here]""",
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
    # Crop image
    image_file.crop(args.crop)
    logger.debug("Output image shape %s", image_file.image.shape)
	# Save image file
    image_file.save(args.output)


if __name__ == "__main__":
    main()
