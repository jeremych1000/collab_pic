import datetime
import cv2

# what this program needs to do

# 1. get most prominent colour of an image, split into XxY blocks (width = width/X, height = height/Y)
# 2. get most prominent colour of all emoji, put into array
# 3. match (maybe exclude white?) emoji to block
# 4. render final image made out of emoji

import get_colour
import investigate_emoji
import investigate_image
import match
import render