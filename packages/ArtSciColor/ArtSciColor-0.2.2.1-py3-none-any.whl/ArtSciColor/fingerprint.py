#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import cv2
import numpy as np
from PIL import Image
from colour import Color
from collections import Counter
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw, ImageFont
import ArtSciColor.swatches as sws
import ArtSciColor.auxiliary as aux


def rgbToHex(rgb):
    '''
    Converts an RGB triplet to its hex equivalent.
    * I: RGB 8-bit list
    * O: Hex color string
    '''
    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hexToRgb(chex, eightBit=False):
    if eightBit:
        return tuple([int(i*255) for i in chex.rgb])
    else:
        return chex.rgb

def calcDominantColors(
        img, 
        cFun=KMeans, cArgs={'n_clusters': 10, 'max_iter': 1000}
    ):
    '''
    Returns a tuple with the dominant colors arrays and their
        clustering labels (sklearn).
    * I: 
        -img: Image imported with cv2.imread
        -clstNumb: Number of desired clusters
        -maxIter: Maximum iterations number for detection
    * O: Dominant colors arrays and clusters labels (sklearn)
    '''
    frame = img.reshape((img.shape[0]*img.shape[1], 3))
    # Cluster the colors for dominance detection
    kmeans = cFun(**cArgs).fit(frame)
    labels = kmeans.labels_
    return (frame, labels)


def colorClusterCentroid(cluster, cFun=np.median, round=True):
    cntr = [cFun(cel) for cel in cluster.T]
    if round:
        return [int(c) for c in cntr]
    else:
        return cntr


def getDominantSwatch(
        pixels, labels, 
        grpFun=np.median, round=True
    ):
    cntLbls = [i[0] for i in Counter(labels).most_common()]
    clusters = [pixels[labels==i] for i in cntLbls]
    swatch = [
        (
            Color(rgbToHex(colorClusterCentroid(c, cFun=grpFun, round=round))), 
            c.shape[0]
        ) 
        for c in clusters
    ]
    return swatch


def reshapeColor(colorEightBit):
    '''
    Returns a color triplet in the range of 0 to 1 from 0 to 255.
    * I: List of 8-bit RGB components
    * O: Normalized RBG components
    '''
    return [i / 255 for i in colorEightBit]


def upscaleColor(colorNormalized):
    '''
    Returns a color triplet of 0 to 255 from 0 to 1.
    * I: Normalized list of RGB components
    * O: List of 8-bit RGB components
    '''
    return [int(round(i * 255)) for i in colorNormalized]



def calcHexAndRGBFromPalette(palette):
    '''
    Returns the hex and RGB codes for the colors in a palette.
    * I: Color palette
    * O: Dictionary with hex and rgb colors
    '''
    sortedPalette = [upscaleColor(i) for i in palette]
    (hexColors, rgbColors) = (
            [rgbToHex(i) for i in sortedPalette],
            sortedPalette
        )
    return {'hex': hexColors, 'rgb': rgbColors}


def genColorSwatch(img, barsHeight, swatch, proportionalHeight=True):
    '''
    Creates a color swatch that is proportional in height to the original
       image (whilst being the same width).
    * I:
        -img: Image imported with cv2.imread
        -heightProp: Desired height of the swatch in proportion to original img
        -palette: Calculated palette through dominance detection
    * O:
    '''
    palette = [hexToRgb(c) for c in swatch]
    clstNumber = len(palette)
    (height, width, depth) = img.shape
    if proportionalHeight:
        pltAppend = np.zeros((round(height*barsHeight), width, depth))
        (wBlk, hBlk) = (round(width/clstNumber), round(height*barsHeight))
    else:
        pltAppend = np.zeros((barsHeight, width, depth))
        (wBlk, hBlk) = (round(width/clstNumber), barsHeight)
    for row in range(hBlk):
        colorIter = -1
        for col in range(width):
            if (col%wBlk==0) and (colorIter<clstNumber-1):
                colorIter=colorIter+1
            pltAppend[row][col] = palette[colorIter]
    return pltAppend*255


def writeColorPalette(filepath, palette):
    '''
    Exports the HEX and RGB values of the palette to a tsv file.
    * I:
        -filepath: Path on disk to write the file to
        -palette: Palette output of the getDominancePalette
    * O:
        -True
    '''
    with open(filepath, 'w') as csvfile:
        wtr = csv.writer(csvfile, delimiter='\t')
        for i in range(len(palette['hex'])):
            wtr.writerow([
                    palette['hex'][i],
                    palette['rgb'][i]
                ])
    return True


def genColorBar(width, height, color=[0, 0, 0], depth=3):
    '''
    Creates a solid color bar to act as visual buffer between frames rows.
    * I:
        -width: Desired width of the bar
        -height: Desired height of the bar
        -color: Desired color of the bar
        -depth: Number of color components (3 for RGB)
    * O:
        -colorBar: Image with a solid color bar
    '''
    colorBar = np.full((height, width, depth), color)
    return colorBar


def getDominancePalette(
            imgPath,
            clstNum=6,
            maxIters=1000,
            colorBarHeight=.03,
            bufferHeight=.005,
            colorBuffer=[0, 0, 0]
        ):
    '''
    Wrapper function that puts together all the elements to create the frame
        with its swatch, and buffer bars.
    * I:
        -imgPath: Image location
        -clstNum: Number of desired clusters
        -maxIters: Maximum number of iterations for convergence
        -colorBarHeight: Height of the color swatch (as proportion to img)
        -bufferHeight: Height of the color buffer (as proportion to img)
        -colorBuffer: Color of the buffer
    * O:
        -imgOut: Compiled image with swatch and buffers
        -swatch: Color swatch
        -palette: Hex and RGB color values
    '''
    # Load image --------------------------------------------------------------
    bgr = cv2.imread(imgPath)
    img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    (height, width, depth) = img.shape
    # Cluster for dominance ---------------------------------------------------
    (colors, labels) = calcDominantColors(
            img, cltsNumb=clstNum, maxIter=maxIters
        )
    (hexColors, rgbColors) = calcHexAndRGBFromPalette(colors)
    # Create color swatch -----------------------------------------------------
    colorsBars = genColorSwatch(img, colorBarHeight, colors)
    # Put the image back together ---------------------------------------------
    whiteBar = genColorBar(
            width, round(height * bufferHeight), color=colorBuffer
        )
    newImg = np.row_stack((
            whiteBar, colorsBars,
            img,
            colorsBars, whiteBar
        ))
    palette = calcHexAndRGBFromPalette(colors)
    swatch = Image.fromarray(colorsBars.astype('uint8'), 'RGB')
    imgOut = Image.fromarray(newImg.astype('uint8'), 'RGB')
    return (imgOut, swatch, palette)



def addHexColorText(
        barsImg, swatchHex, 
        font='Avenir', fontSize=75, hexLabel=True
    ):
    font = ImageFont.truetype(aux.getFontFile(family=font), fontSize)
    draw = ImageDraw.Draw(barsImg)
    (W, H) = (barsImg.width/len(swatchHex), barsImg.height/2)
    for (ix, hex) in enumerate(swatchHex):
        (colorHex, colorRGB) = (hex.hex.upper(), hex.rgb)
        tcol = sws.getTextColor(hex)
        label = (
            colorHex 
            if hexLabel else 
            str(tuple([int(255*i) for i in colorRGB]))
        )
        # Generate bbox and draw centered -------------------------------------
        bbox = draw.textbbox(xy=(0, 0), text=label, font=font, align='center')
        (w, h) = (bbox[2]-bbox[0], bbox[3]-bbox[1])
        xy = (((2*ix+1)*W-w)/2, H-h/2)
        draw.text(
            xy, label, 
            tuple([int(255*i) for i in tcol.rgb]), 
            font=font, align='center'
        )
    return barsImg