import cv2
import random
import numpy as np

import investigate_emoji
from investigate_image import get_image

def greyscale_to_bw():
    img = cv2.imread("C:/Users/Jeremy/Documents/GitHub/collab_pic/example_pic/dxV2T1v_g.jpg", cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    (thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    (thresh, im_bw_blur) = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow("bnw", im_bw)
    cv2.imwrite("bw.jpg", im_bw)

    cv2.imshow("bw_blur", im_bw_blur)
    cv2.imwrite("bw_blur.jpg", im_bw_blur)


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def generate_final_image(final, properties, target=None):
    new = np.zeros((properties["height"], properties["width"] ,3), np.uint8)
    
    for i in range(0, len(final)):
        curr_emoji, curr_properties = get_image(final[i].image)
        #print(curr_emoji_path)
        #curr_emoji = cv2.imread(curr_emoji_path)

        if target is not None and target != curr_properties:
            curr_emoji = image_resize(curr_emoji, width=target, height=target)

        # start replace
        new[final[i].start_y:final[i].end_y, final[i].start_x:final[i].end_x] = curr_emoji

    return new
