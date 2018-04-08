
# what this program needs to do

# 1. get most prominent colour of an image, split into XxY blocks (width = width/X, height = height/Y)
# 2. get most prominent colour of all emoji, put into array
# 3. match (maybe exclude white?) emoji to block
# 4. render final image made out of emoji

# my scripts
import get_colour
import investigate_emoji
import investigate_image
import match
import render

# other imports
import cv2


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

def main():
    # settings
    horizontal_cut = 2
    vertical_cut = 4

    # picture paths
    target_pic_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/example_pic/3DZu1zP.jpg"
    emoji_folder_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/emoji_128/"
    print("pic path is %s" % target_pic_path)
    print("emoji path is %s" % emoji_folder_path)

    # first select target image and get properties
    img, properties = get_image(target_pic_path)
    
    # split the target image into chunks
    split_img = investigate_image.split_image(img, properties, horizontal_cut, vertical_cut)
    
    if split_img is None:
        print("ERROR: no split image returned")
    else:
        # get most dominant colour for each chunk of target image
        for i in range(vertical_cut):
            for j in range(horizontal_cut):
                get_colour.get_dominant_colour(split_img[i][j])

main()