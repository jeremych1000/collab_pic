import os
import csv
import numpy as np
import cv2
import math

import get_colour

# get list of emoji files, make csv that details dominant colour of each emoji

def get_list_emojis(folder_path, subsample=None):
    list_full = [(folder_path + x) for x in os.listdir(folder_path)]

    if subsample != 1:
        long_list = []
        num_times_to_copy_list = subsample ** 2
        for i in range(0, num_times_to_copy_list):
            for j in list_full:
                long_list.append(j)
    else:
        long_list = list_full
    # print(list_full)
    return long_list

def get_emoji_colour(list_of_files, csv_path):
    emoji_colour = []
    print("Processing {} emojis...".format(len(list_of_files)))

    with open(csv_path, "w") as outfile:
        outfile.write("path|r|g|b\n")

        for i in range(0, len(list_of_files)):
            print("\rProcessing emoji {} out of {} ({}%)...".format(i+1, len(list_of_files), int(100*i/len(list_of_files))), end="")
            img = cv2.imread(list_of_files[i])
            (r, g, b) = get_colour.get_dominant_colour(img)
            emoji_colour.append([list_of_files[i], (r,g,b)])
            outfile.write("%s|%d|%d|%d\n" % (list_of_files[i], r, g, b))
        print("\n")
        outfile.close()
    
    print("Processed %d emojis and wrote to %s" % (len(list_of_files), csv_path))

