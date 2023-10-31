# ArtSciColor

[![PyPI version](https://badge.fury.io/py/ArtSciColor.svg)](https://badge.fury.io/py/ArtSciColor)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Chipdelmal/ArtSciColor)
[![DOI](https://zenodo.org/badge/321399050.svg)](https://zenodo.org/doi/10.5281/zenodo.10011483)



Creating a [python](https://www.python.org/) package with color palettes and utilities for their use in [matplotlib](https://matplotlib.org/), [seaborn](https://seaborn.pydata.org/), [plotly](https://plotly.com/python/), and others.

:construction: **WORK IN PROGRESS** :construction:


[R users](https://www.r-project.org/) or [Python users](https://www.python.org/) who don't want to install the package but still want to use the palettes, can download them in CSV form from the dataset's [permalink](https://raw.githubusercontent.com/Chipdelmal/ArtSciColor/main/ArtSciColor/data/DB.csv)!


## Installation

The package is available through [pypi](https://pypi.org/project/ArtSciColor/), so it can be installed by running:

```bash
pip install ArtSciColor
```

## Usage

To use a color palette simply load the package and run:

```bash
import ArtSciColor as art

hexPalette = art.getSwatch(SWATCH_ID)
```

<a href='https://github.com/Chipdelmal/ArtSciColor/blob/main/ArtSciColor/swatches/Art.md'>
    <img src="https://github.com/Chipdelmal/ArtSciColor/raw/main/ArtSciColor/media/demo_id.png" width='100%' align="middle">
</a>

where the `SWATCH_ID` should match one of the [palettes available](#available-palettes) in our package (see the following section for more info).


## Available Swatches

Have a look at currently-available palettes by selecting your favorite artist or category, and use one through its `ID`!

### [Art](./ArtSciColor/swatches/Art.md)

[Miro](./ArtSciColor/swatches/Miro.md), [Kandinsky](./ArtSciColor/swatches/Kandinsky.md), [Kirchner](./ArtSciColor/swatches/Kirchner.md), [Matisse](./ArtSciColor/swatches/Matisse.md), [Picasso](./ArtSciColor/swatches/Picasso.md),  [Signac](./ArtSciColor/swatches/Signac.md), [Warhol](./ArtSciColor/swatches/Kirchner.md), [Nolde](./ArtSciColor/swatches/Nolde.md), [Monet](./ArtSciColor/swatches/Monet.md), [VanGogh](./ArtSciColor/swatches/VanGogh.md), [EdnaAndrade](./ArtSciColor/swatches/EdnaAndrade.md)
<img src="https://github.com/Chipdelmal/ArtSciColor/raw/main/ArtSciColor/media/swatches/Art.png" height="100px" width='100%' align="middle"><br>


### [Movies](./ArtSciColor/swatches/Movies.md)

[Studio Ghibli](./ArtSciColor/swatches/Ghibli.md)
<img src="https://github.com/Chipdelmal/ArtSciColor/raw/main/ArtSciColor/media/swatches/Movies.png" height="50px" width='100%' align="middle"><br>


### [Gaming](./ArtSciColor/swatches/Gaming.md)

[Splatoon1](./ArtSciColor/swatches/Splatoon1.md), [Splatoon2](./ArtSciColor/swatches/Splatoon2.md), [Splatoon3](./ArtSciColor/swatches/Splatoon3.md)
<img src="https://github.com/Chipdelmal/ArtSciColor/raw/main/ArtSciColor/media/swatches/Gaming.png" height="50px" width='100%' align="middle"><br>

### [Other](./ArtSciColor/swatches/Other.md)

[chipdelmal](./ArtSciColor/swatches/chipdelmal.md), [coolors](./ArtSciColor/swatches/coolors.md), [lospec](./ArtSciColor/swatches/lospec.md)
<img src="https://github.com/Chipdelmal/ArtSciColor/raw/main/ArtSciColor/media/swatches/Other.png" height="50px" width='100%' align="middle"><br>

Full dataframe in CSV for available for download [here](./ArtSciColor/data/DB.csv)!

## How are the palettes generated?

Getting palette colors is a common exercise for people getting started into clustering methods. The most widely-used algorithm for this task is [k-means](https://scikit-learn.org/stable/modules/clustering.html#k-means), but in this package the algorithm and its parameters can be provided as long as they adhere to [scikit-learn's](https://scikit-learn.org/) standards. Most of the curated palettes were calculated through the [agglomerative clustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html#sklearn.cluster.AgglomerativeClustering) algorithm as follows:

```python
from sklearn.cluster import AgglomerativeClustering
# Read image and setup number of desired clusters
img = art.readCV2Image(fPath)
CLST_NUM=4
# Clustering algorithm
CLUSTERING = {
    'algorithm': AgglomerativeClustering, 
    'params': {'n_clusters': CLST_NUM} 
}
(pixels, labels) = art.calcDominantColors(
    img, 
    cFun=CLUSTERING['algorithm'], 
    cArgs=CLUSTERING['params']
)
```

Other algorithms such as [DBSCAN](https://scikit-learn.org/stable/modules/clustering.html#dbscan) and [HDBSCAN](https://scikit-learn.org/stable/modules/clustering.html#hdbscan), [Spectral Clustering](https://scikit-learn.org/stable/modules/clustering.html#spectral-clustering), [OPTICS](https://scikit-learn.org/stable/modules/clustering.html#optics), etc; can also be used.

<a href="https://www.nga.gov/collection/art-object-page.48530.html"><img src="https://github.com/Chipdelmal/ArtSciColor/raw/main/ArtSciColor/media/DB4E776DB0F5524EE128.jpg" width='200%' align="middle"></a>


# Notes and Sources

This package was initially inspired by [Blake R Mills'](https://github.com/BlakeRMills/MetBrewer) [R](https://www.r-project.org/about.html) packages ([MoMA Colors](https://github.com/BlakeRMills/MoMAColors) and [MetBrewer](https://github.com/BlakeRMills/MetBrewer)). Most palettes or original artworks are sourced from: [NGA](https://www.nga.gov/collection/), [wikiart](https://www.wikiart.org/), [staedelemuseum](https://sammlung.staedelmuseum.de/), [filmartgallery](https://filmartgallery.com/products/), [coolors](https://coolors.co/palettes/), [inkipedia](https://splatoonwiki.org/wiki/Ink), [lospec](https://lospec.com/); so please visit and support their work!


<img src="https://github.com/Chipdelmal/ArtSciColor/raw/main/ArtSciColor/media/about-pusheen.jpg" height="125px" align="middle"><br>

Coded by: [Héctor M. Sánchez C.](https://chipdelmal.github.io/)
