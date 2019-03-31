import glob
import math
import os
import random

PERCENTAGE_TEST = 10


def perform_separation(training_data_path, image_out_path, write_out_path):
    files = glob.glob(training_data_path + "/*.jpg")
    # Randomise splitting of data
    random.shuffle(files)

    fraction_of_files = PERCENTAGE_TEST * 0.01 * len(files)
    split = round(fraction_of_files)

    training_splits_dir = write_out_path + "/training_splits"
    os.mkdir(training_splits_dir)

    print(split)
    for split_instance in range(0, PERCENTAGE_TEST):
        count = 0
        current_split = training_splits_dir + "/split_" + str(split_instance)
        os.mkdir(current_split)

        file_train = open(current_split + '/train.txt', 'w')
        file_test = open(current_split + '/test.txt', 'w')

        for index, pathAndFilename in enumerate(files):
            resulting_name = image_out_path + os.path.basename(pathAndFilename) + "\n"

            if math.floor(index / split) != split_instance:
                file_train.write(resulting_name)
            else:
                file_test.write(resulting_name)

        count += 1


perform_separation("../../training/darknet/data/images/", "../../training/darknet/data/images/",
                   "../../training/darknet/data")
