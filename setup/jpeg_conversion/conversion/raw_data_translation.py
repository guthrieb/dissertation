import cv2
import numpy as np
from os import listdir
import os

from os.path import isfile, join
import test_train_files_build
import jpeg_conversion
import csv

CLEAN_PREFIX = "clean_"

RAW_DATA_PATH = '../raw_data/'

IMAGE_OUT_PATH = "../../training/darknet/data/images/"
TRAINING_DATA_PATH = "../../training/darknet/data/"

BOUNDING_BOX_SIZE = 40


def getSurroundingColours(y, x, image):
    red = [0, 0, 255]
    surrounding = []

    if y - 1 > 0:
        above = image[y - 1, x]
        surrounding.append(above)

    if y + 1 < image.shape[0]:
        below = image[y + 1, x]
        surrounding.append(below)

    if x + 1 < image.shape[1]:
        right = image[y, x + 1]
        surrounding.append(right)

    if x - 1 > 0:
        left = image[y, x - 1]
        surrounding.append(left)

    surrounding = [s for s in surrounding if set(s) != set(red)]
    return np.mean(surrounding, 0)


def getMask(image):
    #Find all points where image is red
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)


    mask = mask0 + mask1

    return mask


def getBoundingBoxDimensions(center_point, image_x, image_y):
    center_x = center_point[1]
    center_y = center_point[0]

    right_boundary = image_x
    left_boundary = 0

    lower_boundary = image_y
    upper_boundary = 0

    if ((center_x + BOUNDING_BOX_SIZE / 2) < image_x):
        right_boundary = center_x + BOUNDING_BOX_SIZE / 2

    if ((center_x - BOUNDING_BOX_SIZE / 2) > 0):
        left_boundary = center_x - BOUNDING_BOX_SIZE / 2

    if ((center_y + BOUNDING_BOX_SIZE / 2) < image_y):
        lower_boundary = center_y + BOUNDING_BOX_SIZE / 2

    if ((center_y - BOUNDING_BOX_SIZE / 2) > 0):
        upper_boundary = center_y - BOUNDING_BOX_SIZE / 2

    ydim = (lower_boundary - upper_boundary)
    y_center_point = upper_boundary + (ydim / 2)
    xdim = (right_boundary - left_boundary)
    x_center_point = left_boundary + (xdim / 2)

    return (x_center_point, y_center_point, xdim, ydim)


def getCenterPoints(red_pixels):
    print(red_pixels)
    center_points = []

    for pos in red_pixels:
        pos_right = (pos[0], pos[1] + 1)
        pos_below = (pos[0] + 1, pos[1])
        pos_left = (pos[0] - 1, pos[1])
        pos_above = (pos[0], pos[1] - 1)

        below_red = pos_below in red_pixels
        left_red = pos_left in red_pixels
        right_not_red = pos_right not in red_pixels
        above_red = pos_above in red_pixels

        if right_not_red & left_red & below_red & above_red:
            center_points.append(pos)

    # center_point = 0
    if (len(center_points) > 1):
        if center_points[0][1] > center_points[1][1]:
            center_point = center_points[1]
        else:
            center_point = center_points[0]

    else:
        center_point = -1

    return center_point


# csv_writer = csv.writer(csv_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

def removeRed(files):
    print(files)
    i = 0
    for file in files:
        # Open bounding box folder
        translation_file_path = IMAGE_OUT_PATH + CLEAN_PREFIX + ('.').join(file.split('.')[:-1]) + ".txt"

        translation_file = open(translation_file_path, "wb+")

        # Find red pixels in image

        im = cv2.imread(RAW_DATA_PATH + file, 1)
        mask = getMask(im)
        output_img = im.copy()

        im_y, im_x = im.shape[:2]

        redPoints = list(zip(np.where(mask != 0)[0], np.where(mask != 0)[1]))

        center_point = getCenterPoints(redPoints)

        if (center_point != -1):
            for posX, posY in redPoints:
                output_img[posX][posY] = getSurroundingColours(posX, posY, im)

            center_data = getBoundingBoxDimensions(center_point, im_x, im_y)

            center_x = center_data[0]
            center_y = center_data[1]
            xdim = center_data[2]
            ydim = center_data[3]

            cv2.imwrite(IMAGE_OUT_PATH + CLEAN_PREFIX + file, output_img)

            # Write out in correct format
            translation_file.write(bytes("0 " + str(center_x / float(im_x)) + " " + str(center_y / float(im_y)) + " "
                                   + str(xdim / float(im_x)) + " " + str(ydim / float(im_y)),'UTF-8'))


def main():
    print("Running main")
    onlyfiles = [f for f in listdir("../raw_data") if isfile(join("../raw_data", f))]
    removeRed(onlyfiles)

    jpeg_conversion.convertTif(IMAGE_OUT_PATH)
    test_train_files_build.buildTrainTestFiles(TRAINING_DATA_PATH, IMAGE_OUT_PATH)


main()