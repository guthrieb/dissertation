from shutil import copyfile

from model_handling.detecting import detector


def detect_and_move(path_of_image, path_of_package):
    detector.detect("PLACEHOLDER_FOR_MODEL", path_of_image)

    copyfile(path_of_image, path_of_package + "/data/images/")

    copyfile(path_of_image + "_result.txt", path_of_package + "/data/centers")
