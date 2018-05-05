import os
import csv
import numpy as np
import cv2

import get_colour

# get list of emoji files, make csv that details dominant colour of each emoji

def get_list_emojis(folder_path):
    list_full = [(folder_path + x) for x in os.listdir(folder_path)]
    # print(list_full)
    return list_full

def get_emoji_colour(list_of_files, csv_path):
    emoji_colour = []
    print("Processing {} emojis...".format(len(list_of_files)))

    with open(csv_path, "w") as outfile:
        outfile.write("path|r|g|b\n")

        for emoji in list_of_files:
            img = cv2.imread(emoji)
            (r, g, b) = get_colour.get_dominant_colour(img)
            emoji_colour.append([emoji, (r,g,b)])
            outfile.write("%s|%d|%d|%d\n" % (emoji, r, g, b))
        outfile.close()
    
    print("Processed %d emojis and wrote to %s" % (len(list_of_files), csv_path))

