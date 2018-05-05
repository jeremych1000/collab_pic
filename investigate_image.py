import numpy as np
import math
import cv2

class Image_Extract:
    def __init__(self, image, start_x, end_x, start_y, end_y):
        self.image = image
        self.start_x = int(start_x)
        self.end_x = int(end_x)
        self.start_y = int(start_y)
        self.end_y = int(end_y)

def get_image(path):
    try:
        img = cv2.imread(path)
    except Exception as e:
        print(str(e))
    #print("Image shape is ", img.shape)
    (rows, columns, channels) = img.shape
    properties = {
        "height": rows,
        "width": columns,
        "channels": channels
    }
    return img, properties


def split_image(img, properties, horizontal_cut, vertical_cut):
    # first define how big the split image should be
    target_width = int(math.floor(properties["width"] / horizontal_cut))
    target_height = target_width #initially int(math.floor(properties["height"] / vertical_cut)), but emojis are square, so let's use the same!

    print("Original W {} H {}, target W {} H {}".format(properties["width"], properties["height"], target_width, target_height))
    if target_width % 1 != 0:
        print("Target width %f is not integer." % target_width)
        return None
    elif target_height % 1 != 0:
        print("Target height %f is not integer." % target_height)
        return None
    else:
        # both width and height are integers, continue
        split_image = []
    
        for y in range(vertical_cut):
            split_image_row = []
            for x in range(horizontal_cut):
                # first slice is x: 0 --> 0+target_width; y: 0 --> 0+target_height
                # second slice is x: target_width --> 2*target_width, y: 0 --> target_height
                # therefore first top left is 0,0; bottom right is target_width, target_height
                # second top left is target_width, 0; bottom right is 2*target_width, target_height
                # third top left is 2*target_width, 0; bottmo right is 3*target_width, target_height
                # therefore x1,y1; x2,y2 is x*target_width, y*target_height; (x+1)*target_width, (y+1)*target_height

                # syntax is we first supply the startY and endY coordinates, followed by the startX and endX coordinates to the slice
                start_x, start_y = int(x*target_width), int(y*target_height)
                end_x, end_y = int((x+1)*target_width), int((y+1)*target_height)

                #print("Picture %d coordinates are %d %d %d %d" % (y*horizontal_cut+x, start_x, start_y, end_x, end_y))

                extract = img[start_y:end_y, start_x:end_x]
                extract_image = Image_Extract(extract, start_x, end_x, start_y, end_y)
                split_image_row.append(extract_image)
                #cv2.imshow("%d %d" % (y, x), extract)
                #cv2.waitKey(0)

            split_image.append(split_image_row)
    
    #split_image_array = np.array(split_image)
    #print(split_image_array.shape)

    return split_image, target_width #return final cut size