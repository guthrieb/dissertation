import glob
import os

def buildTrainTestFiles(training_data_path, image_out_path):
    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    path_data = current_dir + "/" + image_out_path



    percentage_test = 10

    file_train = open(training_data_path + 'train.txt', 'w')
    file_test = open(training_data_path + 'test.txt', 'w')

    print(path_data)
    counter = 1
    index_test = round(100 / percentage_test)
    for pathAndFilename in glob.iglob(os.path.join(path_data, "*.jpg")):


        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        if counter == index_test:
            counter = 1
            file_test.write(path_data + title + '.jpg' + "\n")
        else:
            file_train.write(path_data + title + '.jpg' + "\n")
            counter = counter + 1

