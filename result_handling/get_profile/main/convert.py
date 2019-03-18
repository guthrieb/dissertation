import math
from os import listdir
from os.path import isfile, join, splitext

import matplotlib.pyplot as plt
from PIL import Image
import result_handling.get_profile.main.lowpass_filter as lowpass

def read_center_data(dataPath):
    f = open(dataPath)
    centerData = f.read()
    splitData = centerData.split(",")
    return ((int(splitData[0]), int(splitData[1])))


def getGrayScaleVal(rgbVal):
    return ((rgbVal[0] + rgbVal[1] + rgbVal[2]) / 3) / 255


def buildProfile(centerCoords, imagePath, angle_offset):
    im = Image.open(imagePath)
    pixels = im.load()

    minVal = 255
    maxVal = 0
    grayScaleVals = []
    for pos in range(centerCoords[0], -1, -1):
        x = pos
        # y = centerCoords[1]

        y = centerCoords[1] - (centerCoords[0] - x) * math.tan(angle_offset * math.pi / 180)


        # print(x)
        # print(y)
        rgbVal = pixels[x, y]
        grayScaleVal = getGrayScaleVal(rgbVal)

        if (grayScaleVal > maxVal):
            maxVal = grayScaleVal

        if (grayScaleVal < minVal):
            minVal = grayScaleVal

        grayScaleVals.append(grayScaleVal)

    grayScaleVals = normalise(grayScaleVals, maxVal, minVal)

    return grayScaleVals


def normalise(grayScaleVals, maxVal, minVal):
    for index, value in enumerate(grayScaleVals):
        normalisedVal = (value - minVal) / (maxVal - minVal)
        grayScaleVals[index] = normalisedVal
    return grayScaleVals


def plotProfile(profile):
    # for val in profile:
    plt.plot(profile)
    plt.show()


def draw_lines(filename):
    image_files = [f for f in listdir("../data/images") if isfile(join("../data/images", f))]

    for image_path in image_files:

        center_data_path = splitext(image_path)[0]
        center_data_path = "../data/centers/" + center_data_path + ".txt"

        center_coords = read_center_data(center_data_path)

        profile_1 = buildProfile(center_coords, "../data/images/" + image_path, 0)
        profile_2 = buildProfile(center_coords, "../data/images/" + image_path, 1)
        profile_3 = buildProfile(center_coords, "../data/images/" + image_path, -1)

        final_profile = []
        for x in range(len(profile_1)):
            print("\n")
            print(profile_1[x])
            print(profile_2[x])
            print(profile_3[x])
            final_profile.append((profile_1[x] + profile_2[x] + profile_3[x])/3)

        final_profile = lowpass.filter(final_profile)
        plotProfile(final_profile)

    # print(image_files)
    # print(centerData)


draw_lines("clean_93_0261.jpg")
