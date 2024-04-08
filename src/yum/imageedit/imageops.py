"""Image operations & a lil of processing maybe
"""
import logging
import numpy as np
from skimage.util import crop


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _parse_crop_args(crop_args_str):
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


def crop_image(image_file, crop_args):

	# Crop image
    crop_args = _parse_crop_args(crop_args)
	# @todo Check if crop isn't egative
    # y axis top, down
    # then x axis left, right
    cropped_image = crop(image_file.image,
                        ((crop_args[0], crop_args[2]),
                         (crop_args[3], crop_args[1]),
                         (0,0)),
                        copy=False)

    return cropped_image

def add_background(input_image) -> np.ndarray:
# Create a matrix and fill it with specified color
# or read specified background image file

# Get image size
    bg_h = input_image.shape[0]
    bg_w = input_image.shape[1]
    im_depth = input_image.shape[2]
# Hardcoded white color for background
    white = [255,255,255,255]
# Create a matrix for bg image filled with white [255,255,255,255]
    white_mat = np.full((bg_h, bg_w, 4), white)
    logger.debug("Bg matrix shape %s", white_mat.shape)

    template = np.zeros((bg_h, bg_w, im_depth), dtype=np.uint8)
    template[:bg_h, :bg_w, :] = input_image 

    mask = np.stack([template[:,:,3] for _ in range(4)], axis=2)

    inv_mask = 255 - mask.astype(np.uint8)
    print(mask)

    result = white_mat * inv_mask + template * mask

    return result

