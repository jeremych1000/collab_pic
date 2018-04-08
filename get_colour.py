import cv2
import numpy as np
import struct
import scipy
import scipy.misc
import scipy.cluster
import binascii


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
    # blank = np.zeros((100,100,3), np.uint8)
    # blank[:] = (int(peak_int[0]), int(peak_int[1]), int(peak_int[2]))
    
    # cv2.imshow("orig", img)
    # cv2.imshow("colour", blank)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return peak_int

