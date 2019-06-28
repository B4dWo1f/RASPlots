#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np

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
   C = ax.scatter(x,y,c=y,s=40,cmap=cm)
   fig.colorbar(C)
   plt.show()
