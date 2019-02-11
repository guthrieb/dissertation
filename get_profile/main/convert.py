from os import listdir
from os.path import isfile, join, splitext
import matplotlib.pyplot as plt

from PIL import Image


def read_center_data(dataPath):
    f = open(dataPath)
    centerData = f.read()
    splitData = centerData.split(",")
    return ((int(splitData[0]), int(splitData[1])))


def getGrayScaleVal(rgbVal):
    return ((rgbVal[0] + rgbVal[1] + rgbVal[2]) / 3) / 255


def buildProfile(centerCoords, imagePath):
    im = Image.open(imagePath)
    pixels = im.load()

    minVal = 255
    maxVal = 0
    grayScaleVals = []
    for pos in range(centerCoords[0], -1, -1):
        x = pos
        y = centerCoords[1]
        rgbVal = pixels[x, y]
        grayScaleVal = getGrayScaleVal(rgbVal)

        if(grayScaleVal > maxVal):
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



def draw_lines():
    imageFiles = [f for f in listdir("../data/images") if isfile(join("../data/images", f))]
    centerData = [f for f in listdir("../data/centers") if isfile(join("../data/centers", f))]

    for imagePath in imageFiles:
        centerDataPath = splitext(imagePath)[0]
        centerDataPath = "../data/centers/" + centerDataPath + ".txt"

        centerCoords = read_center_data(centerDataPath)

        profile = buildProfile(centerCoords, "../data/images/" + imagePath)
        plotProfile(profile)



    # print(imageFiles)
    # print(centerData)


draw_lines()
