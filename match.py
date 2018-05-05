import csv
import cv2
import colorsys
from operator import attrgetter


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


target_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/pic_colour.csv"
emoji_csv_path = "C:/Users/Jeremy/Documents/GitHub/collab_pic/tmp/emoji_colour.csv"
with open(target_csv_path) as pic_csv, open(emoji_csv_path) as emoji_csv:
    pic_list, emoji_list = parse_csv(pic_csv, emoji_csv)
    pic_csv.close()
    emoji_csv.close()

pic_hsv, emoji_hsv = convert_list_to_hsv(pic_list, emoji_list)
print(pic_hsv[0].original)
print(emoji_hsv[0].original)

pic_sorted = sorted(pic_hsv, key=attrgetter('h'))
emoji_sorted = sorted(emoji_hsv, key=attrgetter('h'))

for i in range(0, 10):
    print(pic_hsv[i].h)
    print(emoji_hsv[i].h)
    print('\n')