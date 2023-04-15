import numpy as np
from src.EldenRing.player_damaged.config import threshold_red, threshold_green, threshold_blue


def set_threshold(img, red_thresh=threshold_red, green_thresh=threshold_green, blue_thresh=threshold_blue):
    # sets minimum threshold of each color channel
    minimum_rgb = (red_thresh[0], green_thresh[0], blue_thresh[0])
    maximum_rgb = (red_thresh[1], green_thresh[1], blue_thresh[1])
    img_where = None  # instantiates image object holding the pixel coordinates
    for i in range(len(minimum_rgb)):
        mask1 = minimum_rgb[i] < img[:, :, i]  # sets mask for pixel which is greater than minimum threshold
        mask2 = img[:, :, i] < maximum_rgb[i]  # sets mask for pixel which is less than maximum threshold
        coords = (np.argwhere(np.logical_and(mask1, mask2)))
        if img_where is None:
            img_where = coords  # sets initial pixels which meet set criteria
        else:
            # keep all pixel coordinates which meet all criteria in checked color channels
            img_where = np.array([x for x in set(tuple(x) for x in img_where) & set(tuple(x) for x in coords)])
    return img_where


def region_extraction(img, crop, red_thresh=threshold_red, green_thresh=threshold_green, blue_thresh=threshold_blue):
    # crop image and transform into numpy array
    cropped_image = img.crop(crop)
    na = np.array(cropped_image)
    # Find all pixels in cropped portion that are within set color threshold
    coords = set_threshold(na, red_thresh, green_thresh, blue_thresh)
    Y = [int(item[0]) for item in coords]
    Y.sort()
    X = [int(item[1]) for item in coords]
    X.sort()
    # Find first and last row/column containing red pixels
    top, bottom = Y[0], Y[-1]
    left, right = X[0], X[-1]
    # Extract Region of Interest
    ROI = na[top:bottom, left:right]
    return left, top, right, bottom, ROI
