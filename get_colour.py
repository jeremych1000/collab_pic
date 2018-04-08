import cv2
import numpy as np
import struct
import scipy
import scipy.misc
import scipy.cluster
import binascii

path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/example_pic/3DZu1zP.jpg"
print("path is %s" % path)

def get_image(path):
    img = cv2.imread(path)
    print(img.shape)
    (rows, columns, channels) = img.shape
    properties = {
        "height": rows,
        "width": columns,
        "channels": channels
    }
    return img, properties
    
def split_image(img, properties, horizontal_cut, vertical_cut):
    # first define how big the split image should be
    target_width = properties["width"] / horizontal_cut
    target_height = properties["height"] / vertical_cut

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

                print("Picture %d coordinates are %d %d %d %d" % (y*horizontal_cut+x, start_x, start_y, end_x, end_y))

                extract = img[start_y:end_y, start_x:end_x]
                split_image_row.append(extract)
                #cv2.imshow("%d %d" % (y, x), extract)
                #cv2.waitKey(0)

            split_image.append(split_image_row)
    
    #split_image_array = np.array(split_image)
    #print(split_image_array.shape)

    return split_image
    
    
def get_dominant_colour(img):
    # https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
    NUM_CLUSTERS = 5

    ar = np.asarray(img)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # print ('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # print ('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent

    peak = codes[index_max]
    peak_int = [int(c) for c in peak]
    peak_hex = [format(c, '02x') for c in peak_int]
    
    colour = ''.join(c for c in peak_hex)
    print ('most frequent is %s (#%s)' % (peak_int, colour))

    # lets show the most frequent colour
    blank = np.zeros((100,100,3), np.uint8)
    blank[:] = (int(peak_int[0]), int(peak_int[1]), int(peak_int[2]))
    cv2.imshow("orig", img)
    cv2.imshow("colour", blank)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




def main():
    horizontal_cut = 7
    vertical_cut = 2

    img, properties = get_image(path)
    
    split_img = split_image(img, properties, horizontal_cut, vertical_cut)
    
    if split_img is None:
        print("ERROR: no split image returned")
    else:
        for i in range(vertical_cut):
            for j in range(horizontal_cut):
                get_dominant_colour(split_img[i][j])

main()