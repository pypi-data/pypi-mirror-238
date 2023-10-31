#!/usr/bin/env python
# -*- coding: utf-8 -*-

import colorsys
import colorir as cir
from colour import Color
import ArtSciColor.constants as cst

def sortSwatchByFrequency(freqSwatch):
    freqSwatch.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb[0].get_rgb()))
    swatchHex = [s[0] for s in freqSwatch]
    return swatchHex


def sortSwatchHSV(
        freqSwatch,
        hue_classes=None, gray_thresh=255, 
        gray_start=True, alt_lum=True, invert_lum=False
    ):
    swatchHex = [s[0].hex for s in freqSwatch]
    swatchHex.sort(
        key=cir.hue_sort_key(
            hue_classes=hue_classes, gray_thresh=gray_thresh,
            gray_start=gray_start, alt_lum=alt_lum, invert_lum=invert_lum
        )
    )
    swatchHex = [Color(c) for c in swatchHex]
    return swatchHex


def getTextColor(hexBackground, threshold=0.55):
    # https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
    (r, g, b) = hexBackground.rgb
    tcol = (0, 0, 0) if (r*0.299+g*0.587+b*0.114)>threshold else (1, 1, 1)
    return Color(rgb=tcol)


def getSwatch(swatchID):
    return cst.SWATCHES[swatchID]