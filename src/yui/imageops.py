"""Image operations & a lil of processing maybe
"""
import logging
import numpy as np
from skimage.util import crop


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _parse_crop_args(crop_args_str: str) -> list[int]:
    """Parse argument string of crop arguments into a list of args
    """

	# Possibly make different ways: aspect ratio, crop from edges, by
	# percentage, from center, etc.
	# For now it's 'cropping edges'. The edges order is like in CSS --
	# clockwise
    crop_args_list = crop_args_str.split(",")
    # @todo Add crop by percent
    crop_args = [int(num) for num in crop_args_list]
    # @todo I see here a pattern. Can I do this with a single recursive function?
    if len(crop_args) == 4:
        pass
    elif len(crop_args) == 3:
        crop_args.append(crop_args[1])
    elif len(crop_args) == 2:
        crop_args.append(crop_args[0])
        crop_args.append(crop_args[1])
    elif len(crop_args) == 1:
        crop_args.append(crop_args[0])
        crop_args.append(crop_args[0])
        crop_args.append(crop_args[0])
    else:
        # @todo make error message more clear. Like that the user has to provide
        # from 1 to 4 arguments and it works like in CSS.
        raise ValueError("Too few or too many params in --crop.")

    return crop_args


def crop_image(image, crop_args) -> np.ndarray:

	# Get crop args
    crop_args = _parse_crop_args(crop_args)
    top, right, bottom, left = _parse_crop_args(crop_args)
	# @todo Check if crop isn't egative
    # y axis top, down
    # then x axis left, right
    cropped_image = crop(image,
                         ((top, bottom),
                          (left, right),
                          (0, 0)),
                         copy=False)

    return cropped_image


def expand_image(image: np.ndarray, expand_args: str) -> np.ndarray:
    """Expand image at the edges by specified range filling with transparent pixels"""

	# Get expand args
    top, right, bottom, left = _parse_crop_args(expand_args)

    # Get height and width of the processing image
    h, w, p = image.shape

    # Sum the sizes with the args: width + left_exp + right_exp, and same for h

    eh = h + top + bottom
    ew = w + left + right

    # Create a matrix `tm` filled with 0 alpha pixels (transparent pixels)
    expanded_image = np.zeros((eh, ew, p), dtype=np.uint8)
    logger.debug("Bg matrix shape %s", expanded_image.shape)

    # Add the original image to `mt` with offset of `art.left` and `arg.top`
    expanded_image[top : top + h, left : left + w, :] = image
    logger.debug(expanded_image.shape)

    # Return expanded image
    return expanded_image


def add_background(image: np.ndarray, color: list[int] | None = None) -> np.ndarray:
    """Create a matrix and fill it with specified color or read specified background image file"""

    if color is None:
        color = [255, 255, 255, 255]
    if len(color) < 4:
        raise ValueError("Color must be a list of 4 int values from 0 to 255")

    # Get image size
    bg_h, bg_w, bg_p = image.shape

    # Create a matrix for bg image filled specified color
    white_mat = np.full((bg_h, bg_w, 4), color, dtype=np.uint8)
    logger.debug("Bg matrix shape %s", white_mat.shape)

    template = np.zeros((bg_h, bg_w, bg_p))
    template[:bg_h, :bg_w, :] = image

    # Here's a problem I don't understand. I'll do it later
    mask = np.stack([template[:,:,3] for _ in range(4)], axis=2)

    inv_mask = 255 - mask.astype(np.uint8)
    print(mask)

    result = white_mat * inv_mask + template * mask

    return result
