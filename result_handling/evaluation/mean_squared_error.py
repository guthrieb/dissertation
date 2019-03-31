import math
import os

from PIL import Image
# from model_handling.

def get_detected_center(model, image):
    # result = detect_and_move(moadel, image, "result_handling/evaluation")

    return 744, 387


def get_actual_center(image):
    print(image)
    img = Image.open(os.path.abspath(image.rstrip("\n")))

    width, height = img.size

    pre = os.path.splitext(image)[0]

    bounding_box_file = open(pre + ".txt")
    bounding_box = bounding_box_file.readline().split()

    print(float(bounding_box[1]))
    print(float(bounding_box[2]))

    return int(float(bounding_box[1]) * width), int(float(bounding_box[2]) * height)


def calculate_mean_squared_error(model_name, data_path):

    no_of_entries = 0
    diff_sum = 0
    with open(data_path + "test.txt") as testing_files:
        for line in testing_files:
            print(line)

            detected_center = get_detected_center(line)
            actual_center = get_actual_center(line)

            print("\n" + str(actual_center))
            no_of_entries += 1

            diff_sum += math.pow(distance_between_points(detected_center, actual_center), 2)

    print("Mean Squared Error: " + str((1/no_of_entries)*diff_sum))


def distance_between_points(point1, point2):
    x_comp = math.pow(point2[0] - point1[0], 2)
    y_comp = math.pow(point2[1] - point1[1], 2)

    return math.sqrt(x_comp + y_comp)
