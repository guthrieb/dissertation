import glob
import os

PERCENTAGE_TEST = 10


def build_train_test_files(training_data_path, image_out_path):
    # Build out path
    path_data = image_out_path

    # Open data files
    file_train = open(training_data_path + 'train.txt', 'w')
    file_test = open(training_data_path + 'test.txt', 'w')

    print(image_out_path)

    counter = 1
    # Generate index for which the next image will be designated a testing file
    index_for_testing_file = round(100 / PERCENTAGE_TEST)

    for pathAndFilename in glob.iglob(os.path.join(path_data, "*.jpg")):

        title = os.path.splitext(os.path.basename(pathAndFilename))[0]

        # If index matches testing index add to test file, otherwise training file
        if counter == index_for_testing_file:
            counter = 1
            print(path_data + title + ".jpg")
            file_test.write(path_data + title + '.jpg' + "\n")
        else:
            print(path_data + title + ".jpg")
            file_train.write(path_data + title + '.jpg' + "\n")
            counter = counter + 1
