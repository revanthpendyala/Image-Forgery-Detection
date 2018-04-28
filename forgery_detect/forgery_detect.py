import os
import time
import image_object

def detect(sourceDirectory, fileName, outputDirectory, blockSize=32):
    """
    Detects an image under a specific directory
    :return: None
    """

    if not os.path.exists(sourceDirectory):
        print "Error: Source Directory did not exist."
        return
    elif not os.path.exists(sourceDirectory + fileName):
        print "Error: Image file did not exist."
        return
    elif not os.path.exists(outputDirectory):
        print "Error: Output Directory did not exist."
        return

    singleImage = image_object.image_object(sourceDirectory, fileName, blockSize, outputDirectory)
    imageResultPath = singleImage.run()

    print "Done."
    return imageResultPath
