import csv
import cv2
import colorsys
from operator import attrgetter
from investigate_image import Image_Extract

class HSV_object:
    def __init__(self, original, h, s, v):
        self.original = original
        self.h = h
        self.s = s
        self.v = v


def parse_csv(pic_csv, emoji_csv):
    pic_list = list(csv.DictReader(pic_csv, delimiter='|'))
    emoji_list = list(csv.DictReader(emoji_csv, delimiter='|'))
    return pic_list, emoji_list
      

def rgb2hsv(r,g,b):
    return colorsys.rgb_to_hsv(r, g, b)


def convert_list_to_hsv(pic_list, emoji_list):
    pic_hsv = []
    emoji_hsv = []

    for i in pic_list:
        coordinates = {
            "start_x": i["start_x"],
            "end_x": i["end_x"],
            "start_y": i["start_y"],
            "end_y": i["end_y"]
        }
        r,g,b = int(i["r"]), int(i["g"]), int(i["b"])
        hsv = rgb2hsv(r,g,b)
        pic_hsv.append(HSV_object(coordinates, hsv[0], hsv[1], hsv[2]))

    for j in emoji_list:
        coordinates = {
            "path": j["path"]
        }
        r,g,b = int(j["r"]), int(j["g"]), int(j["b"])
        hsv = rgb2hsv(r,g,b)
        emoji_hsv.append(HSV_object(coordinates, hsv[0], hsv[1], hsv[2]))

    return pic_hsv, emoji_hsv

def match(pic_sorted, emoji_sorted):
    final = []

    # need to truncate emoji list length
    emoji_sorted = emoji_sorted[0:len(pic_sorted)]
    assert len(pic_sorted) == len(emoji_sorted), "Why are the two lists not the same length? {}, {}".format(len(pic_sorted), len(emoji_sorted))

    for i in range(0, len(pic_sorted)):
        if pic_sorted[i].h == 0:
            # if white then we somehow need to stop it replacing with emojis
            path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/white.jpg"
        else:
            path = emoji_sorted[i].original["path"]

        a = Image_Extract(path, pic_sorted[i].original["start_x"], pic_sorted[i].original["end_x"], pic_sorted[i].original["start_y"], pic_sorted[i].original["end_y"])
        final.append(a)
    
    return final

