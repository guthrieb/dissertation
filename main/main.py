import sys

import model_handling.builder.build_model
import model_handling.detecting.detector
import result_handling.evaluation.mean_squared_error
import result_handling.get_profile.main.convert


def main():
    clean_images_build_model = False

    detecting = False

    # File finding
    image_filename = None
    to_detect_image = False

    mean_squared_error = False
    build_profile = False

    for arg in sys.argv[1:]:
        if to_detect_image:
            # Utility to find next argument filename
            image_filename = arg
            to_detect_image = False
        elif arg == "-b":
            # Rebuild the model
            clean_images_build_model = True
        elif arg == "-d":
            # Detect the center of a specific image
            detecting = True
            to_detect_image = True
            continue
        elif arg == "-mse":
            # Calculate the MSE across the model
            mean_squared_error = True
        elif arg == "-bp":
            # Build 2D profile of specific image
            build_profile = True
            to_detect_image = True
            continue

    if clean_images_build_model:
        model_handling.builder.build_model.build_model()
    elif detecting:
        model_handling.detecting.detector.detect("PLACEHOLDER_FOR_MODEL", image_filename)
    elif build_profile:
        model_handling.detecting.detector.detect("PLACEHOLDER_FOR_MODEL", image_filename,
                                                 out_path="./result_handling/get_profile/data/centers")
        result_handling.get_profile.main.convert.draw_lines(image_filename)
    elif mean_squared_error:
        result_handling.evaluation.mean_squared_error.calculate_mean_squared_error(
            "../model_handling/training/darknet/data/")
    elif build_profile:
        result_handling.get_profile.main.convert.draw_lines(image_filename)

if __name__ == "__main__":
    main()
