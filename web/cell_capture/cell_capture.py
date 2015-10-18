##############################################################################
# Copyright (c) 2015 Thomas Durant
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##########################################################################

##############################################################################
# Purpose
# Create Mask and Coordinate array of rbcs
# Input: image
# Output: Mask.png and pandas array of corresponding coordinates
##########################################################################


###############################################################################
# Import
###############################################################################

import numpy as np
import cv2

__author__ = 'Thomas Durant'
__date__ = '10/14/2015'
__pyver__ = '2.7'

###############################################################################
# Classes/Functions
###############################################################################


def rbc_capture(path):
    print(path)
    im = cv2.imread(path)

    # color to gray
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # blur
    imgray = cv2.medianBlur(imgray, 5)

    # thresh image
    ret, thresh = cv2.threshold(imgray, 205, 255, 0)

    # find all contours
    image, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # create mask image where all elements are zero (black image) with same
    # size as source (1st param)
    mask = np.zeros(imgray.shape, np.uint8)

    coordinates = []

    # filter contours based on area
    for h, cnt in enumerate(contours):

        area = cv2.contourArea(cnt)
        if area < 300:
            continue
        if area > 2000:
            continue
        if len(cnt) < 5:
            continue

        # find coordinates for contour objects
        x, y, w, h = cv2.boundingRect(cnt)
        xywh = (x, y, w, h)
        # append coordinates to list
        coordinates.append(xywh)

        # draw contours to mask image
        cv2.drawContours(mask, [cnt], 0, 255, -1)

    # write mask image to file
    cv2.imwrite('mask.png', mask)

    # pass list and index to pandas
    coordinate_array = np.array(coordinates)
    return coordinate_array
