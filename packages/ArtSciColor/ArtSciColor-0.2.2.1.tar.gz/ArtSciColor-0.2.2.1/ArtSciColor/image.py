#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

def readCV2Image(
        imgPath, scaleFactor=1, interpolation=cv2.INTER_AREA
    ):
    bgr = cv2.imread(imgPath)
    img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return img

def resizeCV2Image(
        img, resizeToFraction, 
        interpolation=cv2.INTER_AREA
    ):
    # Rescale image -----------------------------------------------------------
    (width, height) = (
        int(img.shape[1]*resizeToFraction), 
        int(img.shape[0]*resizeToFraction)
    )
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=interpolation)
    return resized

def resizeCV2ImageAspect(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def resizeCV2BySide(img, maxSize):
    if img.shape[0] > img.shape[1]:
        resized = resizeCV2ImageAspect(img, width=maxSize)
    else:
        resized = resizeCV2ImageAspect(img, height=maxSize)
    return resized
