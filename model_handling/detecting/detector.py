import subprocess
import sys


def convertModelAndImage(model, image_name):
    model = "../../../" + model
    image_name = "../../../" + image_name

    return model, image_name


def detect(model, image_name):
    """

    :param model: path relative to the main
    :param image_name: path relative to the main
    """

    model, image_name = convertModelAndImage(model, image_name)
    print(model)
    print(image_name)
    #
    #
    command = "cd ../model_handling/training/darknet; ./darknet detector test cfg/obj.data cfg/yolo-obj.cfg " \
              + model + " " + image_name
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

    # Print result to image_path + <image_name>_center.txt
