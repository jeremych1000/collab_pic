
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
from operator import attrgetter # used for sorting


def main():
    # settings
    overwrite_pic = True # change to True every time after you change the image
    overwrite_emoji = True # change to True every time after you modify subsample, or emojis
    subsample = 2 # default 1, if subsample = 2, then the no. of emojis that will be used is 2**2, as it divides both width and height by subsample ratio

    # picture paths
    print("### SETTING PATHS...")

    target_pic_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/m_pic/acc.png" # target pic to replace with emojis
    emoji_folder_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/emoji_128_non_transparent/" # where the emojis are located

    # temp files to be created
    target_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/pic_colour.csv"
    emoji_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/emoji_colour.csv"
    
    render_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/render.png" # final image path
    print("pic path is %s" % target_pic_path)
    print("emoji path is %s" % emoji_folder_path)
    print("########################")

    # first select target image and get properties
    try:
        img, properties = investigate_image.get_image(target_pic_path)
    except Exception as e:
        print(str(e))
        assert False, "No image loaded."

    aspect_ratio = properties["width"] / properties["height"]

    # find how many emojis there are
    print("### GETTING LIST OF EMOJIS...")
    list_emoji = investigate_emoji.get_list_emojis(emoji_folder_path, subsample=subsample)
    num_emoji = len(list_emoji)
    print("Detected %d emojis in %s." % (num_emoji, emoji_folder_path))

    print("### DETERMINING OPTIMAL SECTOR SIZES...")
    proposed_w_cut = int(math.floor(subsample * math.sqrt((num_emoji/subsample**2) / (1/aspect_ratio))))
    proposed_h_cut = int(math.floor(subsample * math.sqrt((num_emoji/subsample**2) / (aspect_ratio))))
    no_sectors = proposed_w_cut * proposed_h_cut

    print("Propose wcut %d, hcut %d. Will use %d emojis, %d unused of %d." % (proposed_w_cut, proposed_h_cut, no_sectors, num_emoji-no_sectors, num_emoji))

    # split the target image into chunks
    print("### STARTING SPLIT IMAGE...")
    split_img, final_cut_size = investigate_image.split_image(img, properties, proposed_w_cut, proposed_h_cut)
    
    if split_img is None:
        print("ERROR: no split image returned")
    else:
        # get most dominant colour for each chunk of target image
        if overwrite_pic:
            print("### STARTING ANALYSIS OF ORIGINAL IMAGE...")
            with open(target_csv_path, 'w') as csvfile:
                csvfile.write("r|g|b|start_x|end_x|start_y|end_y\n")
                for i in range(proposed_h_cut):
                    for j in range(proposed_w_cut):
                        curr = i*proposed_w_cut + j + 1
                        print("\rProcessing sector {} of {} ({}%)...".format(curr, no_sectors, int(100*curr/no_sectors)), end="")
                        operate_on = split_img[i][j]
                        (r, g, b) = get_colour.get_dominant_colour(operate_on.image)
                        csvfile.write("%d|%d|%d|%d|%d|%d|%d\n" % (r, g, b, operate_on.start_x, operate_on.end_x, operate_on.start_y, operate_on.end_y))
                print("\n")
                csvfile.close()


    # process emojis
    if overwrite_emoji:
        print("### STARTING PROCESS EMOJI...")
        investigate_emoji.get_emoji_colour(list_emoji, emoji_csv_path)

    # match
    print("### STARTING MATCH...")
    with open(target_csv_path) as pic_csv, open(emoji_csv_path) as emoji_csv:
        pic_list, emoji_list = match.parse_csv(pic_csv, emoji_csv)
        pic_csv.close()
        emoji_csv.close()

    pic_hsv, emoji_hsv = match.convert_list_to_hsv(pic_list, emoji_list)

    # sort the picture csv and the emoji csv by their colour, represented by the hue
    pic_sorted = sorted(pic_hsv, key=attrgetter('h'), reverse=False)
    emoji_sorted = sorted(emoji_hsv, key=attrgetter('h'), reverse=False)

    final = match.match(pic_sorted, emoji_sorted, randomize=False)
    final = sorted(final, key=attrgetter('start_y', 'start_x'))

    # use results of match to render
    print("### STARTING FINAL RENDER...")
    rendered = render.generate_final_image(final, properties, target=final_cut_size)
    #cv2.imshow('final', rendered)
    #cv2.waitKey(0)

    print("### SAVING FINAL RENDER...")
    cv2.imwrite(render_path, rendered)
    print("Image saved to {}".format(render_path))

    print("### COMPLETE")

main()