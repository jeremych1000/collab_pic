import os
from PIL import Image

def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im

dir  = "C:\\Users\\Jeremy\\Documents\\GitHub\\collab_pic\\emoji_128_non_transparent"
for root, subfolders, files in os.walk(dir):
    for file in files:
        try:
            image = Image.open(os.path.join(dir, root, file))
            ret = remove_transparency(image)
            try:
                ret.save(os.path.join(dir, root, file), "PNG")
            except Exception as e:
                print(str(e))
            

        except:
            pass

