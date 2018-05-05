
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
from operator import attrgetter


def main():
    # settings
    target_aspect_ratio = 16/9
    overwrite_csv = True
    overwrite_emoji = True
    subsample = 2 # default None

    # picture paths
    print("### SETTING PATHS...")
    target_pic_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/example_pic/3DZu1zP.jpg"
    target_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/pic_colour.csv"
    emoji_folder_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/emoji_128_non_transparent/"
    emoji_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/emoji_colour.csv"
    render_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/render.png"
    print("pic path is %s" % target_pic_path)
    print("emoji path is %s" % emoji_folder_path)
    print("########################")

    # first select target image and get properties
    try:
        img, properties = investigate_image.get_image(target_pic_path)
    except Exception as e:
        print(str(e))

    # find how many emojis there are
    list_emoji = investigate_emoji.get_list_emojis(emoji_folder_path, subsample=subsample)
    num_emoji = len(list_emoji)
    
    proposed_w_cut = int(math.floor(subsample * math.sqrt((num_emoji/subsample**2) / (1/target_aspect_ratio))))
    proposed_h_cut = int(math.floor(subsample * math.sqrt((num_emoji/subsample**2) / (target_aspect_ratio))))
    no_sectors = proposed_w_cut * proposed_h_cut

    print("Detected %d emojis in %s." % (num_emoji, emoji_folder_path))
    print("Propose wcut %d, hcut %d. Will use %d emojis, %d unused of %d." % (proposed_w_cut, proposed_h_cut, no_sectors, num_emoji-no_sectors, num_emoji))

    # split the target image into chunks
    print("### STARTING SPLIT IMAGE...")
    split_img, final_cut_size = investigate_image.split_image(img, properties, proposed_w_cut, proposed_h_cut)
    
    if split_img is None:
        print("ERROR: no split image returned")
    else:
        # get most dominant colour for each chunk of target image
        if overwrite_csv:
            print("### STARTING GET DOMINANT COLOUR FOR ORIGINAL IMAGE...")
            with open(target_csv_path, 'w') as csvfile:
                csvfile.write("r|g|b|start_x|end_x|start_y|end_y\n")
                for i in range(proposed_h_cut):
                    for j in range(proposed_w_cut):
                        curr = i*proposed_w_cut + j
                        print("\rOperating on sector {} of {} ({}%)...".format(curr, no_sectors, int(math.floor(100*curr/no_sectors))), end="")
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

    pic_sorted = sorted(pic_hsv, key=attrgetter('h'))
    emoji_sorted = sorted(emoji_hsv, key=attrgetter('h'))

    final = match.match(pic_sorted, emoji_sorted)

    # use results of match to render
    print("### STARTING RENDER...")
    rendered = render.generate_final_image(final, properties, target=final_cut_size)
    #cv2.imshow('final', rendered)
    #cv2.waitKey(0)

    print("### SAVING...")
    cv2.imwrite(render_path, rendered)
    print("Image saved to {}".format(render_path))

    print("### COMPLETE")

main()