#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.ListedColormap.html
# 

from matplotlib.colors import ColorConverter, LinearSegmentedColormap

def addHexOpacity(colors, alpha='1A'):
    return [c+alpha for c in colors]


def replaceHexOpacity(colors, alpha='FF'):
    return [i[:-2]+alpha for i in colors]


def generateAlphaColorMapFromColor(color, minAlpha=0, maxAlpha=1):
    """Creates a linear cmap that runs from transparent to full opacity of the provided color.

    Args:
        color (_type_): _description_
        minAlpha (float):
        maxAlpha (float):

    Returns:
        _type_: _description_
    """    
    alphaMap = LinearSegmentedColormap.from_list(
        'alphaMap', 
        [(0.0, 0.0, 0.0, 0.0), color], 
        gamma=0
    )
    return alphaMap

def colorPaletteFromHexList(clist):
    """Takes a list of colors in hex-form and generates a matplotlib-compatible
    cmap function.

    Args:
        clist (list of hex colors): List of colors to be used in the color palette in linear form.

    Returns:
        cmap: LinearSegmentedColormap function for color maps.
    """    
    c = ColorConverter().to_rgb
    clrs = [c(i) for i in clist]
    rvb = LinearSegmentedColormap.from_list(
        "hexMap", 
        clrs
    )
    return rvb