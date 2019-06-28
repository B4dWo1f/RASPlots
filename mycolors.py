#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from matplotlib.colors import LinearSegmentedColormap

cdict={'red': ((0., 0., 0.),(0.6, 0.0, 0.0),(1.0, 1.0, 1.0)),
       'green': ((0., 0.0, 0.0),(0.4, 1.0, 1.0),(0.6, 1.0, 1.0),(1., 0.0, 0.0)),
       'blue': ((0., 1.0, 1.0),(0.4, 0.0, 0.0),(1.0, 0.0, 0.0))}
bgr = LinearSegmentedColormap('bgr',cdict,256)

