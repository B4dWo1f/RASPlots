#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np


def mycmap(stops,Ns=[]):
   """
    This function returns a matplorlib colormap object.
    stops: color steps
    Ns: list of colors between steps len(Ns) = len(stops)-1
    if Ns is not provided. then Ns = [100 for _ in range(len(stops)-1)] is used
    ** alpha is allowed
   """
   if isinstance(Ns,int): Ns = [Ns for _ in range(len(stops)-1)]
   if isinstance(Ns,list):
      if len(Ns) == 0: Ns = [100 for _ in range(len(stops)-1)]
      else: pass
   if len(stops) != len(Ns)+1:
      print('Error making mycmap')
      return None
   cols = []
   for i in range(len(Ns)):
      N = Ns[i]
      col0 = stops[i]
      col1 = stops[i+1]
      for j in range(N):
         a = j/N
         c = (1-a)*col0 + a*col1
         #print(a,c)
         cols.append( tuple((1-a)*col0 + a*col1) )
   return ListedColormap(cols)


# Blue-Green-Red
cdict={'red': ((0., 0., 0.),(0.6, 0.0, 0.0),(1.0, 1.0, 1.0)),
       'green': ((0., 0.0, 0.0),(0.4, 1.0, 1.0),(0.6, 1.0, 1.0),(1., 0.0, 0.0)),
       'blue': ((0., 1.0, 1.0),(0.4, 0.0, 0.0),(1.0, 0.0, 0.0))}
bgr = LinearSegmentedColormap('bgr',cdict,256)

# Grey scale from black to transparent along black-white direction
color_array = [(0,0,0,a) for a in np.linspace(0,0.9,100)]
greys = LinearSegmentedColormap.from_list(name='cloud_cover',colors=color_array)
   
# Red scale from red to transparent along red-white direction
color_array = [(1,0,0,a) for a in np.linspace(0,0.9,100)]
reds = LinearSegmentedColormap.from_list(name='cape',colors=color_array)

## Wind Speed ##################################################################
col0 = np.array([178, 223, 138])
col1 = np.array([ 51, 160,  44])
col2 = np.array([166, 206, 227])
col3 = np.array([ 31, 120, 180])
col4 = np.array([253, 191, 111])
col5 = np.array([255, 127,   0])
col6 = np.array([251, 154, 153])
col7 = np.array([227,  26,  28])
col8 = np.array([202, 178, 214])
col9 = np.array([106,  61, 154])
col10 = np.array([255, 255, 153])
col11 = np.array([177,  89,  40])
col12 = np.array([ 90, 219, 229])
col13 = np.array([  0, 158, 170])

cols = [col0,col1,col2,col3,col4,col5] #,col6,col7,col8,col9,col9]

stops = [C/255 for C in cols]
Ns = [3, 7, 15, 28, 28]
CAPE = mycmap(stops, Ns)
################################################################################

## Wind Speed ##################################################################
col0 = np.array([178, 223, 138])
col1 = np.array([ 51, 160,  44])
col2 = np.array([166, 206, 227])
col3 = np.array([ 31, 120, 180])
col4 = np.array([253, 191, 111])
col5 = np.array([255, 127,   0])
col6 = np.array([251, 154, 153])
col7 = np.array([227,  26,  28])
col8 = np.array([202, 178, 214])
col9 = np.array([106,  61, 154])
col10 = np.array([255, 255, 153])
col11 = np.array([177,  89,  40])
col12 = np.array([ 90, 219, 229])
col13 = np.array([  0, 158, 170])

cols = [col0,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11]
cols += [col12,col13,col13]

stops = [C/255 for C in cols]
WindSpeed1 = mycmap(stops,1)
################################################################################

## Thermals_uri ################################################################
col0 = np.array([  0,   0, 255])
col1 = np.array([  0,  93, 255])
col2 = np.array([  0, 193, 255])
col3 = np.array([  1, 246, 225])
col4 = np.array([  4, 215, 131])
col5 = np.array([  6, 187,  44])
col6 = np.array([ 66, 197,  10])
col7 = np.array([160, 225,   6])
col8 = np.array([248, 252,   0])
col9 = np.array([255, 224,   0])
col10 = np.array([255, 189,   0])
col11 = np.array([255, 149,   0])
col12 = np.array([255,  84,   0])
col13 = np.array([255,  24,   0])
col14 = np.array([219,   0,  29])
col15 = np.array([153,   0,  82])
col16 = np.array([ 92,   0, 132])

cols = [col0,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11]
cols += [col12,col13,col14,col15,col16,col16]

stops = [C/255 for C in cols]
Thermals_uri = mycmap(stops,1)
################################################################################

## Thermals ####################################################################
col0 = np.array([178, 223, 138])
col1 = np.array([115, 192,  91])
col2 = np.array([ 51, 160,  44])
col3 = np.array([166, 206, 227])
col4 = np.array([ 99, 163, 203])
col5 = np.array([ 31, 120, 180])
col6 = np.array([253, 191, 111])
col7 = np.array([254, 159,  56])
col8 = np.array([255, 127,   0])
col9 = np.array([251, 154, 153])
col10 = np.array([239,  90,  91])
col11 = np.array([227,  26,  28])
col12 = np.array([202, 178, 214])
col13 = np.array([154, 120, 184])
col14 = np.array([106,  61, 154])
col15 = np.array([ 90, 219, 229])
col16 = np.array([  0, 158, 170])

cols = [col0,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11]
cols += [col12,col13,col14,col15,col16,col16]

stops = [C/255 for C in cols]
Thermals = mycmap(stops,1)
################################################################################

## Wind Speed 1 ################################################################
col0 = np.array([239, 239, 239])
col1 = np.array([166, 206, 227])
col2 = np.array([ 31, 120, 180])
col3 = np.array([178, 223, 138])
col4 = np.array([ 51, 160,  44])
col5 = np.array([248, 253, 133])
col6 = np.array([255, 228,   0])
col7 = np.array([253, 191, 111])
col8 = np.array([255, 127,   0])
col9 = np.array([251, 154, 153])
col10 = np.array([227,  26,  28])
col11 = np.array([202, 178, 214])
col12 = np.array([106,  61, 154])
col13 = np.array([148,  0, 87])
col14 = np.array([148,  0, 87])

cols = [col0,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11]
cols += [col12,col13,col14]

stops = [C/255 for C in cols]
WindSpeed = mycmap(stops,1)

cols = [col0,col2,col4,col6,col8,col10,col12,col13]
color_array = [C/255 for C in cols]
CAPE1 = LinearSegmentedColormap.from_list(name='CAPE1',colors=color_array)
################################################################################

if __name__ == '__main__':
   
   col0 = np.array((25,255,0))
   col1 = np.array((0, 81, 255))
   col2 = np.array((255, 218, 0))
   col3 = np.array((255, 0, 2))
   col4 = np.array((167, 65, 0))
   
   stops = [col0/255,col1/255,col2/255,col3/255,col4/255]
   Ns = [1,1,1,1]
   cm = mycmap(stops,Ns=Ns)
   
   x = np.linspace(0,10,100)
   y = np.sin(x)
   
   fig, ax = plt.subplots()
   C = ax.scatter(x,y,c=y,s=40,cmap=CAPE)
   fig.colorbar(C)
   plt.show()
