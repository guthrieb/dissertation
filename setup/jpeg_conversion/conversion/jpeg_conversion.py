from os import listdir
from os.path import isfile, join

import os
from PIL import Image

def convertTif(image_out_path):
    yourpath = os.getcwd() +"/" + image_out_path
    print(yourpath)
    print(yourpath)
    for root, dirs, files in os.walk(yourpath, topdown=False):
        for name in files:
            print(os.path.splitext(os.path.join(root, name))[1].lower())
            if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
                if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                    print("A jpeg file already exists for %s" % name)
                # If a jpeg is *NOT* present, create one from the tiff.
                else:
                    outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                    try:
                        im = Image.open(os.path.join(root, name))
                        print("Generating jpeg for %s" % name)
                        im.thumbnail(im.size)
                        im.save(outfile, "JPEG", quality=100)
                    except Exception as e:
                        print(e)

                os.remove(root + name)
