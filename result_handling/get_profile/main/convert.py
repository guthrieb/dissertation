import math
from os import listdir
from os.path import isfile, join, splitext

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from PIL import Image


def read_center_data(dataPath):
    f = open(dataPath)
    centerData = f.read()
    splitData = centerData.split(",")
    return ((int(splitData[0]), int(splitData[1])))


def getGrayScaleVal(rgbVal):
    return ((rgbVal[0] + rgbVal[1] + rgbVal[2]) / 3) / 255


def linear_interpolate(pixels, x, y):
    y_floored = int(y)
    y_floored_rem = y - y_floored

    y_ceil = math.ceil(y)
    y_ceil_rem = 1 - y_floored_rem

    r = interpolate_val(pixels, x, y_floored, y_ceil_rem, y_ceil, y_floored_rem, 0)
    g = interpolate_val(pixels, x, y_floored, y_ceil_rem, y_ceil, y_floored_rem, 1)
    b = interpolate_val(pixels, x, y_floored, y_ceil_rem, y_ceil, y_floored_rem, 2)

    return [r, g, b]


def interpolate_val(pixels, x, y_floored, y_ceil_rem, y_ceil, y_floored_rem, ind):
    #TODO Test this
    new_pix_val1 = pixels[x, y_floored][ind] * y_ceil_rem
    new_pix_val2 = pixels[x, y_ceil][ind] * y_floored_rem

    return (new_pix_val1 + new_pix_val2) / 2


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

        rgbVal = linear_interpolate(pixels, x, y)
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


def plot_minima_profile(t, x, y, profile, ax1):
    ax2 = plt.subplot(t, x, y, sharex=ax1)
    plt.eventplot(profile, lineoffsets=0.5, colors=[0, 0, 0])
    plt.yticks([], [])

def plot_width_profile(profile, ax1):
    plt.subplot(4, 1, 4, sharex=ax1)
    plt.stem(profile[0], profile[1])


def filter(data):
    N = 2
    Wn = 0.8
    B, A = signal.butter(N, [0.05, 0.2], output='ba', btype='band')

    tempf = signal.filtfilt(B, A, data)

    return tempf


def local_minima(data):
    minima = []
    for index, value in enumerate(data, 1):
        if index < len(data) - 1 and value < data[index - 2] and value < data[index]:
            minima.append(1)
        else:
            minima.append(0)

    return minima


def get_minima_graphable(minima_profile):
    graphable_minima = []
    for index, value in enumerate(minima_profile):
        if value == 1:
            graphable_minima.append(index)

    return graphable_minima


def build_widths(minima_profile):
    widths = []

    for index, minima in enumerate(minima_profile):
        if index > 0:
            widths.append(float(minima - minima_profile[index-1]))
        else:
            widths.append(float(minima))

    return minima_profile, widths


def perform_stft(profile):
    return signal.stft(profile, 1, nperseg=20)


def plot_frequency_heatmap(param, param1, param2, frequency_profile, ax1):
    plt.subplot(param, param1, param2, sharex=ax1)

    plt.pcolormesh(frequency_profile[0], frequency_profile[1], np.abs(frequency_profile[2]))


def draw_lines(filename):
    image_files = [f for f in listdir("../data/images") if isfile(join("../data/images", f))]

    for image_path in image_files:

        center_data_path = splitext(filename)[0]
        center_data_path = "../data/centers/" + center_data_path + ".txt"

        center_coords = read_center_data(center_data_path)

        profile_1 = buildProfile(center_coords, "../data/images/" + image_path, 0)
        profile_2 = buildProfile(center_coords, "../data/images/" + image_path, 1)
        profile_3 = buildProfile(center_coords, "../data/images/" + image_path, -1)

        line_profile = []
        for x in range(len(profile_1)):
            line_profile.append((profile_1[x] + profile_2[x] + profile_3[x]) / 3)

        line_profile = filter(line_profile)
        minima_profile = local_minima(line_profile)
        minima_profile_indexes = get_minima_graphable(minima_profile)
        frequency_profile = perform_stft(minima_profile)
        width_profile = build_widths(minima_profile_indexes)
        times = range(len(frequency_profile))

        ax1 = plt.subplot(4, 1, 1)
        plt.plot(line_profile)

        plot_minima_profile(4, 1, 2, minima_profile_indexes, ax1)
        # plot_frequency_heatmap(4, 1, 3, frequency_profile, ax1)

        plt.show()

    # print(image_files)
    # print(centerData)




# draw_lines("clean_93_0261.jpg")
