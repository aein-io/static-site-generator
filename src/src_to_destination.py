import os
import shutil


def src_to_destination(source, destination):
    # check if directory exista, if not create a new public directory
    isExist = os.path.exists(destination)

    if not isExist:
        os.mkdir("static-site-generator/public")
    else:
        # delete all files in public
        # shutil.rmtree
        shutil.rmtree("static-site-generator/public")
        os.mkdir("static-site-generator/public")

        # copy all files from static and put it in the public directory
        # os.listdir
        # os.path.join
        # os.path.isfile
        # shutil.copy
        # log each file and subdirectory for easier debugging
