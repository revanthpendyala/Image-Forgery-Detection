from PIL import Image
import scipy.misc
from math import pow
import numpy as np
import __builtin__
from tqdm import tqdm, trange
import time

import Container
import Blocks


class ImageObject(object):
    """
    Object to contains a single image, then detects a fraud in it
    """

    def __init__(self, imageDirectory, imageName, blockDimension, outputDirectory):
        """
        Constructor to initialize the algorithm's parameters
        """

        print imageName
        print "Step 1 of 4: Object and variable initialization",

        # image parameter
        self.imageOutputDirectory = outputDirectory
        self.imagePath = imageName
        self.imageData = Image.open(imageDirectory + imageName)
        self.imageWidth, self.imageHeight = self.imageData.size  # height = vertikal, width = horizontal

        if self.imageData.mode != 'L':  # L means grayscale
            self.isThisRGBImage = True
            self.imageData = self.imageData.convert('RGB')
            RGBImagePixels = self.imageData.load()
            self.imageGrayscale = self.imageData.convert(
                'L')  # creates a grayscale version of current image to be used later
            GrayscaleImagePixels = self.imageGrayscale.load()

            for yCoordinate in range(0, self.imageHeight):
                for xCoordinate in range(0, self.imageWidth):
                    redPixelValue, greenPixelValue, bluePixelValue = RGBImagePixels[xCoordinate, yCoordinate]
                    GrayscaleImagePixels[xCoordinate, yCoordinate] = int(0.299 * redPixelValue) + int(
                        0.587 * greenPixelValue) + int(0.114 * bluePixelValue)
        else:
            self.isThisRGBImage = False
            self.imageData = self.imageData.convert('L')

        # algorithm's parameters from the first paper
        self.N = self.imageWidth * self.imageHeight
        self.blockDimension = blockDimension
        self.b = self.blockDimension * self.blockDimension
        self.Nb = (self.imageWidth - self.blockDimension + 1) * (self.imageHeight - self.blockDimension + 1)
        self.Nn = 2  # amount of neighboring block to be evaluated
        self.Nf = 188  # minimum treshold of the offset's frequency
        self.Nd = 50  # minimum treshold of the offset's magnitude

        # algorithm's parameters from the second paper
        self.P = (1.80, 1.80, 1.80, 0.0125, 0.0125, 0.0125, 0.0125)
        self.t1 = 2.80
        self.t2 = 0.02

        print self.Nb, self.isThisRGBImage

        # container initialization to later contains several data
        self.featuresContainer = Container.Container()
        self.blockPairContainer = Container.Container()
        self.offsetDictionary = {}

    def run(self):
        """
        Run the created algorithm
        :return: None
        """

        # time logging (optional, for evaluation purpose)
        startTimestamp = time.time()
        self.compute()
        timestampAfterComputing = time.time()
        self.sort()
        timestampAfterSorting = time.time()
        self.analyze()
        timestampAfterAnalyze = time.time()
        imageResultPath = self.reconstruct()
        timestampAfterImageCreation = time.time()

        print "Computing time :", timestampAfterComputing - startTimestamp, "second"
        print "Sorting time   :", timestampAfterSorting - timestampAfterComputing, "second"
        print "Analyzing time :", timestampAfterAnalyze - timestampAfterSorting, "secon"
        print "Image creation :", timestampAfterImageCreation - timestampAfterAnalyze, "second"

        totalRunningTimeInSecond = timestampAfterImageCreation - startTimestamp
        totalMinute, totalSecond = divmod(totalRunningTimeInSecond, 60)
        totalHour, totalMinute = divmod(totalMinute, 60)
        print "Total time    : %d:%02d:%02d second" % (totalHour, totalMinute, totalSecond), '\n'
        return imageResultPath

    def compute(self):
        """
        To compute the characteristic features of image block
        :return: None
        """
        print "Step 2 of 4: Computing characteristic features"

        imageWidthOverlap = self.imageWidth - self.blockDimension
        imageHeightOverlap = self.imageHeight - self.blockDimension

        if self.isThisRGBImage:
            for i in tqdm(range(0, imageWidthOverlap + 1, 1)):
                for j in range(0, imageHeightOverlap + 1, 1):
                    imageBlockRGB = self.imageData.crop((i, j, i + self.blockDimension, j + self.blockDimension))
                    imageBlockGrayscale = self.imageGrayscale.crop(
                        (i, j, i + self.blockDimension, j + self.blockDimension))
                    imageBlock = Blocks.Blocks(imageBlockGrayscale, imageBlockRGB, i, j, self.blockDimension)
                    self.featuresContainer.addBlock(imageBlock.computeBlock())
        else:
            for i in range(imageWidthOverlap + 1):
                for j in range(imageHeightOverlap + 1):
                    imageBlockGrayscale = self.imageData.crop((i, j, i + self.blockDimension, j + self.blockDimension))
                    imageBlock = Blocks.Blocks(imageBlockGrayscale, None, i, j, self.blockDimension)
                    self.featuresContainer.addBlock(imageBlock.computeBlock())

    def sort(self):
        """
        To sort the container's elements
        :return: None
        """
        self.featuresContainer.sortFeatures()

    def analyze(self):
        """
        To analyze pairs of image blocks
        :return: None
        """
        print "Step 3 of 4:Pairing image blocks"
        z = 0
        time.sleep(0.1)
        featureContainerLength = self.featuresContainer.getLength()
        for i in tqdm(range(featureContainerLength)):
            for j in range(i + 1, featureContainerLength):
                result = self.isValid(i, j)
                if result[0]:
                    self.addDict(self.featuresContainer.container[i][0], self.featuresContainer.container[j][0],
                                 result[1])
                    z += 1
                else:
                    break

        return 0,

    def addDict(self, firstCoordinate, secondCoordinate, pairOffset):
        """
        Add a pair of coordinate and its offset to the dictionary
        """
        if self.offsetDictionary.has_key(pairOffset):
            self.offsetDictionary[pairOffset].append(firstCoordinate)
            self.offsetDictionary[pairOffset].append(secondCoordinate)
        else:
            self.offsetDictionary[pairOffset] = [firstCoordinate, secondCoordinate]

    def reconstruct(self):
        """
        Reconstruct the image according to the fraud detection result
        """
        print "Step 4 of 4: Image reconstruction"

        # create an array as the canvas of the final image
        groundtruthImage = np.zeros((self.imageHeight, self.imageWidth))
        linedImage = np.array(self.imageData.convert('RGB'))

        for key in sorted(self.offsetDictionary, key=lambda key: __builtin__.len(self.offsetDictionary[key]),
                          reverse=True):
            if self.offsetDictionary[key].__len__() < self.Nf * 2:
                break
            print key, self.offsetDictionary[key].__len__()
            for i in range(self.offsetDictionary[key].__len__()):
                # The original image (grayscale)
                for j in range(self.offsetDictionary[key][i][1],
                               self.offsetDictionary[key][i][1] + self.blockDimension):
                    for k in range(self.offsetDictionary[key][i][0],
                                   self.offsetDictionary[key][i][0] + self.blockDimension):
                        groundtruthImage[j][k] = 255

        timeStamp = time.strftime("%Y%m%d_%H%M%S")
        scipy.misc.imsave(self.imageOutputDirectory + timeStamp + "_" + self.imagePath, groundtruthImage)
        scipy.misc.imsave(self.imageOutputDirectory + timeStamp + "_lined_" + self.imagePath, linedImage)

        return self.imageOutputDirectory + timeStamp + "_lined_" + self.imagePath
