
# what this program needs to do

# 1. get most prominent colour of an image, split into XxY blocks (width = width/X, height = height/Y)
# 2. get most prominent colour of all emoji, put into array
# 3. match (maybe exclude white?) emoji to block
# 3.1 this may not work (maybe drawn emoji is detected as most dominant white), so second method is to force the matching using opencv magic
# 4. render final image made out of emoji

# my scripts
import get_colour
import investigate_emoji
import investigate_image
import match
import render

# other imports
import cv2
import csv
import math


def get_image(path):
    img = cv2.imread(path)
    print("Image shape is ", img.shape)
    (rows, columns, channels) = img.shape
    properties = {
        "height": rows,
        "width": columns,
        "channels": channels
    }
    return img, properties

def main():
    # settings
    target_aspect_ratio = 16/9

    # picture paths
    target_pic_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/m_pic/hummingbirds+flower_final.jpg"
    target_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/pic_colour.csv"
    emoji_folder_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/emoji_128_non_transparent/"
    emoji_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/emoji_colour.csv"
    print("pic path is %s" % target_pic_path)
    print("emoji path is %s" % emoji_folder_path)

    # first select target image and get properties
    img, properties = get_image(target_pic_path)
    
    # find how many emojis there are
    list_emoji = investigate_emoji.get_list_emojis(emoji_folder_path)
    num_emoji = len(list_emoji)
    
    proposed_w_cut = int(math.floor(math.sqrt(num_emoji / (1/target_aspect_ratio))))
    proposed_h_cut = int(math.floor(math.sqrt(num_emoji / (target_aspect_ratio))))
    no_sectors = proposed_w_cut * proposed_h_cut

    print("Detected %d emojis in %s." % (num_emoji, emoji_folder_path))
    print("Propose wcut %d, hcut %d. Will use %d emojis, %d unused." % (proposed_w_cut, proposed_h_cut, no_sectors, num_emoji-no_sectors))

    # split the target image into chunks
    split_img = investigate_image.split_image(img, properties, proposed_w_cut, proposed_h_cut)
    
    if split_img is None:
        print("ERROR: no split image returned")
    else:
        # get most dominant colour for each chunk of target image
        with open(target_csv_path, 'w') as csvfile:
            csvfile.write("r|g|b|start_x|end_x|start_y|end_y\n")
            for i in range(proposed_h_cut):
                for j in range(proposed_w_cut):
                    curr = i*proposed_w_cut + j
                    print("Operating on sector {} of {} ({}%)...".format(curr, no_sectors, int(math.floor(100*curr/no_sectors))))
                    operate_on = split_img[i][j]
                    (r, g, b) = get_colour.get_dominant_colour(operate_on.image)
                    csvfile.write("%d|%d|%d|%d|%d|%d|%d\n" % (r, g, b, operate_on.start_x, operate_on.end_x, operate_on.start_y, operate_on.end_y))


    # process emojis
    investigate_emoji.get_emoji_colour(list_emoji, emoji_csv_path)

    # match

    
    # use results of match to render


main()