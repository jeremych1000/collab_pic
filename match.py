import csv
import cv2
import colorsys
import random
from operator import attrgetter
from investigate_image import Image_Extract

class HSV_object:
    def __init__(self, original, h, s, v):
        self.original = original
        self.h = int(360*h)
        self.s = int(100*s)
        self.v = int(100*v)


def parse_csv(pic_csv, emoji_csv):
    pic_list = list(csv.DictReader(pic_csv, delimiter='|'))
    emoji_list = list(csv.DictReader(emoji_csv, delimiter='|'))
    return pic_list, emoji_list
      

def rgb2hsv(r,g,b):
    h,s,v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return h, s,v


def shuffle_list(input):
    a = input
    random.shuffle(a)
    return a


def convert_list_to_hsv(pic_list, emoji_list):
    pic_hsv = []
    emoji_hsv = []

    for i in pic_list:
        metadata = {
            "start_x": i["start_x"],
            "end_x": i["end_x"],
            "start_y": i["start_y"],
            "end_y": i["end_y"]
        }
        r,g,b = int(i["r"]), int(i["g"]), int(i["b"])
        h, s, v = rgb2hsv(r,g,b)
        pic_hsv.append(HSV_object(metadata, h, s, v))

    for j in emoji_list:
        metadata = {
            "path": j["path"]
        }
        r,g,b = int(j["r"]), int(j["g"]), int(j["b"])
        h, s, v = rgb2hsv(r,g,b)
        emoji_hsv.append(HSV_object(metadata, h, s, v))

    return pic_hsv, emoji_hsv

def match(pic_sorted, emoji_sorted, base_repo_path, randomize=False):
    final = []
    len_pic = len(pic_sorted)
    len_emoji = len(emoji_sorted)
    if len_pic != len_emoji:
        # need to truncate emoji list length
        print("Truncating emoji list by {} to match length of picture list ({}).".format(len_emoji-len_pic, len_pic))
        emoji_sorted = emoji_sorted[0:len(pic_sorted)]

    if randomize:
        print("Randomising emoji list...")
        emoji_sorted = shuffle_list(emoji_sorted)

    count_not_white = 0
    for i in range(0, len(pic_sorted)):
        # play with these to filter out white, sometimes it's not exactly 255,255,255
        # maybe consider HSL? https://stackoverflow.com/questions/22588146/tracking-white-color-using-python-opencv
        if pic_sorted[i].s <= 1 and pic_sorted[i].v >= 99: 
            # if white then we somehow need to stop it replacing with emojis
            path = base_repo_path + "/white.jpg"
        else:
            count_not_white += 1
            path = emoji_sorted[i].original["path"]

        a = Image_Extract(path, pic_sorted[i].original["start_x"], pic_sorted[i].original["end_x"], pic_sorted[i].original["start_y"], pic_sorted[i].original["end_y"])
        final.append(a)
    
    print("Skipped matching of {} white sectors ({}%)".format(count_not_white, int(100*count_not_white/len_pic)))
    return final

