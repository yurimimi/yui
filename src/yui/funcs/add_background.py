#!/usr/bin/python3
"""Add color background to image

Adds background layer of specified color to image 
"""
import logging
import argparse
from filemanagement.core import ImageFile


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def main(args=None):
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
	# @todo add background image
	# @todo add web safe colors by color name
    parser.add_argument("-bg", "--bg-color",
                        help="""background image path or color specified
                        by hex code or web safe color name""",
                        required=True)
	# Get all specified arguments

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args.split())

	# Get input file filename and extension
	# Get current working directory
    image_file = ImageFile(args.input)

    logger.debug("Input image shape %s", image_file.image.shape)
    logger.debug("Does image have alpha?: %s", image_file.image.shape[2]==4)
    logger.debug("Input image shape: %s", image_file.image.shape)

    # Crop image
    image_file.crop(args.crop)

    logger.debug("Output image shape %s", image_file.image.shape)

	# Save image file
    image_file.save(args.output)

	#background_mat = np.array(bg_w, bg_h)
	#logger.debug("Bg image shape: %s", background_mat)


if __name__ == "__main__":
    main()
