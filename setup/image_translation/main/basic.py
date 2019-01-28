import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import csv

BOUNDING_BOX_SIZE = 40

# img_hsv=cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
#
# # lower mask (0-10)
# lower_red = np.array([0,50,50])
# upper_red = np.array([10,255,255])
# mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
#
# # upper mask (170-180)
# lower_red = np.array([170,50,50])
# upper_red = np.array([180,255,255])
# mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
#
# # join my masks
# mask = mask0+mask1
#
# # set my output img to zero everywhere except my mask
# output_img = im.copy()
# # output_img[np.where(mask!=0)] = 0
#
# 
# cv2.imwrite(os.path.join(os.getcwd(),'../out','tropical_image_sig5.bmp'), output_img)
#
#
# # or your HSV image, which I *believe* is what you want
# output_hsv = img_hsv.copy()
# output_hsv[np.where(mask==0)] = 0

onlyfiles = [f for f in listdir("../data") if isfile(join("../data", f))]



def getSurroundingColours(y, x, image):
    surrounding = []

    if y - 1 > 0:
        above = image[y - 1, x]
        surrounding.append(above)

    # 
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
    img_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0 + mask1

    # return np.where(mask!=0)
    return mask

def getBoundingBoxDimensions(center_point, image_x, image_y):
    
    

    center_x = center_point[1]
    center_y = center_point[0]
    

    right_boundary = image_x
    left_boundary = 0

    lower_boundary = image_y
    upper_boundary = 0

    if((center_x + BOUNDING_BOX_SIZE/2) < image_x):
        right_boundary = center_x + BOUNDING_BOX_SIZE/2

    if((center_x - BOUNDING_BOX_SIZE/2) > 0):
        left_boundary = center_x - BOUNDING_BOX_SIZE/2

    if((center_y + BOUNDING_BOX_SIZE/2) < image_y):
        lower_boundary = center_y + BOUNDING_BOX_SIZE/2

    if((center_y - BOUNDING_BOX_SIZE/2) > 0):
        upper_boundary = center_y - BOUNDING_BOX_SIZE/2

    
    

    ydim = (lower_boundary - upper_boundary)
    y_center_point= upper_boundary + (ydim / 2)
    xdim = (right_boundary - left_boundary)
    x_center_point = left_boundary + (xdim / 2)

    
    

    return (x_center_point, y_center_point, xdim, ydim)


def getCenterPoints(red_pixels):
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
    if(len(center_points) > 1):
        if center_points[0][1] > center_points[1][1]:
            center_point = center_points[1]
        else:
            center_point = center_points[0]

    else:
        center_point = -1


    return center_point


# csv_writer = csv.writer(csv_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

i = 0
for file in onlyfiles:

    #Open bounding box folder
    translation_file_path = "../out/bounding_box_information/" + "clean_" + ('.').join(file.split('.')[:-1]) + ".txt"

    translation_file = open(translation_file_path, "wb")

    #Find red pixels in image
    red = [0, 0, 255]
    im = cv2.imread('../data/' + file, 1)
    mask = getMask(im)
    output_img = im.copy()

    im_y,im_x = im.shape[:2]

    left = (np.where(mask != 0)[0])
    right =(np.where(mask != 0)[1])

    redPoints = zip(np.where(mask != 0)[0], np.where(mask != 0)[1])

    center_point = getCenterPoints(redPoints)
    if(center_point != -1):
        for posX, posY in redPoints:
            output_img[posX][posY] = getSurroundingColours(posX, posY, im)

        center_data = getBoundingBoxDimensions(center_point, im_x, im_y)

        center_x = center_data[0]
        center_y = center_data[1]
        xdim = center_data[2]
        ydim = center_data[3]

        print file
        cv2.imwrite("../out/clean/" + "clean_" + file, output_img)


        # Write out
        translation_file.write("0 " + str(center_x) + " " + str(center_y) + " " + str(xdim) + " " + str(ydim))

