#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join
from os.path import expanduser


###############################################################################
# Paths for Palettes and Data
###############################################################################
PTH_DATA = expanduser('~/Documents/GitHub/ArtSciColor/ArtSciColor/data')
(PTH_DBDF, PTH_DBBZ, PTH_SWBZ, PTH_SRCS) = (
    join(PTH_DATA, 'DB.csv'),
    join(PTH_DATA, 'DB.bz'),
    join(PTH_DATA, 'SWATCHES.bz'),
    join(PTH_DATA, 'sources')
)
###############################################################################
# Paths for Media Outputs
###############################################################################
PTH_MDIA = expanduser('~/Documents/GitHub/ArtSciColor/ArtSciColor/media')
(PTH_SWCH) = join(PTH_MDIA, 'swatches') 
###############################################################################
# Paths for MD/HTML
###############################################################################
PTH_SWRM = expanduser('~/Documents/GitHub/ArtSciColor/ArtSciColor/swatches')
