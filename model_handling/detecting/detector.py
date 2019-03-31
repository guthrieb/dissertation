import os
import subprocess
import sys
from pathlib import Path

from PIL import Image


def convertModelAndImage(model, image_name):
    model = "../../../" + model
    image_name = "../../../" + image_name

    return model, image_name


def get_detected_center(image, bounding_box_file):

    img = Image.open(image.rstrip("\n"))

    width, height = img.size

    bounding_box_file = open(bounding_box_file)
    bounding_box = bounding_box_file.readline().split()

    print(float(bounding_box[0]))
    print(float(bounding_box[1]))

    print(height)
    print(width)
    return int(float(bounding_box[0]) * width), int(float(bounding_box[1]) * height)


def detect(model, image_name):
    """

    :param model: path relative to the main
    :param image_name_reformatted: path relative to the main
    """

    print("DETECTING")
    model, image_name_reformatted = convertModelAndImage(model, image_name)
    print(model)
    print(image_name_reformatted)
    #
    #
    command = "cd ../model_handling/training/darknet; ./darknet detector test cfg/obj.data cfg/yolo-obj.cfg " \
              + model + " " + image_name_reformatted
    print(command)
    #
    # # print(model_filename)
    #
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    # output, error = process.communicate()

    while True:
        out = p.stdout.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

    file = Path("../model_handling/training/darknet/tmp_result.txt")

    if file.is_file():
        detected_center = get_detected_center("../" + image_name, "../model_handling/training/darknet/tmp_result.txt")
        os.remove(file)

    # Print result to image_path + <image_name>_center.txt
