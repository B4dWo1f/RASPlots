#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import datetime as dt
from random import choice
import os
here = os.path.dirname(os.path.realpath(__file__))


params = {'figure.dpi': 150,
          'font.family': 'serif',
          'font.size': 30.0,
          'mathtext.rm': 'serif',
          'mathtext.fontset': 'cm',
          'axes.grid': True,
          'figure.figsize': (9.6, 7.2),
          'figure.dpi': 150}
matplotlib.rcParams.update(params)
figsize=(32,19)
fs = 35   # fontsize



def border():
   """
     P0-------------P3
     |              |
     |              |
     P1-------------P2
   """
   P0 = (-6.230882, 41.588094)
   P1 = (-6.232133, 39.866217)
   P2 = (-3.022456, 39.861002)
   P3 = (-3.025468, 41.595428)

   # 41.727515,-6.825019        41.722646,-2.781653
   # 39.590629,-6.787157        39.582791,-2.692100
   #P0 = (-6.825019, 41.727515)
   #P1 = (-6.787157, 39.590629)
   #P2 = (-2.692100, 39.582791)
   #P3 = (-2.781653, 41.722646)
   return P0,P1,P2,P3


def plot_background(img,ext,pueblos,ax=None):
   """
    Sets an image as background for other plots. It also marks the villages
   stored in pueblos.csv
   """
   if ax is None: ax = plt.gca()
   img = mpimg.imread(img) #here+'/Gmap1.jpg')
   #yshape,xshape,_ = img.shape
   ax.imshow(img, aspect='equal', extent=ext,zorder=1,origin='lower')
   ## Pueblos
   px,py = [],[]
   for line in open(pueblos,'r').read().strip().splitlines():
      ll = line.split()
      #a_x,a_y = mapP([float(ll[1]),float(ll[0])],img.shape)
      a_x,a_y = float(ll[1]),float(ll[0])
      px.append(a_x)
      py.append(a_y)
      nam = ' '.join(ll[2:])
      ax.text(a_x,a_y,nam,bbox=dict(facecolor='white', alpha=0.5),
                                                      fontsize=fs, zorder=13)
   ax.scatter(px,py,c='r',s=200,zorder=11)


def plot_scalar(X,Y,S,fig=None,ax=None,lim=36,cmap='Paired',cbar=True):
   """
   X: longitude of the data
   Y: latitude of the data
   S: data to plot
   """
   if fig is None: fig = plt.figure()
   if ax is None: ax = plt.gca()
   C = ax.contourf(X,Y,S, levels=range(0,lim,2), extend='max',
                   antialiased=True,
                   cmap=cmap,
                   vmin=0, vmax=40,
                   zorder=10,alpha=0.3)
   if cbar:
      divider = make_axes_locatable(ax)
      cax = divider.append_axes("right", size="1.5%", pad=0.2)
      cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
      cbar.set_clim(0, lim)
      cbar.ax.set_ylabel('Km/h',fontsize=fs)
      ticklabs = cbar.ax.get_yticklabels()
      cbar.ax.set_yticklabels(ticklabs, fontsize=fs)

def plot_vector(X,Y,U,V,ax=None):
   """
   ** X,Y must be the (n,) arrays that would be passed to np.meshgrid(x,y)
   X: longitude of the data
   Y: latitude of the data
   U: longitudinal components of the vector field
   V: latitudinal components of the vector field
   """
   if ax is None: ax = plt.gca()
   ax.streamplot(X,Y, U,V, color='k',linewidth=1., density=3.5,
                           arrowstyle='->',arrowsize=5,
                           zorder=12)

def plot_wind(fol,tail):
   fol_save = fol.replace('DATA','PLOTS')
   os.system('mkdir -p %s'%(fol_save))

   spd = fol +  tail  + 'spd.data'
   dire = fol + tail  + 'dir.data'
   blcloud = fol + tail.replace('sfcwind','blcloudpct.data')
   cape = fol + tail.replace('sfcwind','cape.data')

   #dire = fol + '/sfcwinddir.' + tail

   # Forecast valid for day:
   date = open(spd,'r').read().strip().splitlines()[1].split()
   date = ' '.join(date[11:14]) + ' ' + date[7]
   date = dt.datetime.strptime(date, '%d %b %Y %H%M')

   # Read latitude and longitude info
   # convert lat,lon to pixel
   f = '/'.join(fol.split('/')[:-4])
   X = np.load(f+'/lons.npy')
   Y = np.load(f+'/lats.npy')
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)


   # Calculate Vx and Vy
   S = np.loadtxt(spd, skiprows=4) * 3.6 # km/h
   D = np.radians(np.loadtxt(dire, skiprows=4))  
   cloud_cover = np.loadtxt(blcloud, skiprows=4)
   cape = np.loadtxt(cape, skiprows=4)

   U = -S*np.sin(D)
   V = -S*np.cos(D)

   # Prepare streamplot
   x = np.linspace(mx,Mx,X.shape[1])
   y = np.linspace(my,My,X.shape[0])

   # Create Plot
   fig, ax = plt.subplots(figsize=figsize)
   ax.xaxis.tick_top()

   # Background Image
   p0,p1,p2,p3 = border()
   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]

   plot_background(here+'/Gmap1.jpg',ext,here+'/pueblos.csv',ax)
   plot_vector(x,y,U,V)
   plot_scalar(X,Y,S,fig,ax,cmap = 'Paired')
   from matplotlib.colors import LinearSegmentedColormap
   color_array = [(0,0,0,a) for a in np.linspace(0,0.9,100)]
   greys = LinearSegmentedColormap.from_list(name='cloud_cover',colors=color_array)
   color_array = [(1,0,0,a) for a in np.linspace(0,0.9,100)]
   reds = LinearSegmentedColormap.from_list(name='cape',colors=color_array)

   #ax.contourf(X,Y,cloud_cover,cmap=greys,vmin=40,vmax=100,zorder=20)
   if np.max(cape)>1000:
      ax.contourf(X,Y,cape,cmap=reds,zorder=20)
   #plot_scalar(X,Y,cloud_cover,fig,ax,cmap='Greys',cbar=False)
   #plot_scalar(X,Y,cloud_cover,fig,ax,cmap=map_object,cbar=False)

   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])
   ax.set_xlim([mx,Mx])
   ax.set_ylim([my,My])


   ax.set_title(date.strftime('Surface Wind for - %d/%m/%Y %H:%M'),fontsize=50)
   fig.tight_layout()
   fsave = fol_save + tail + '.jpg'
   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
   #plt.show()
   plt.close('all')



if __name__ == '__main__':
   import sys
   try:
      fnam = sys.argv[1]
      if fnam[-1] != '/': fnam += '/'
   except IndexError:
      print('File not specified')
      exit()
   now = dt.datetime.now()
   folders = [x[0].split('/')[-3:] for x in os.walk(fnam)]
   fols = []
   for f in folders:
      try:
         y,m,d = map(int,f)
         fols.append(dt.datetime(y,m,d))
      except ValueError: pass
   fname = fnam + max(fols).strftime('%Y/%m/%d/')
   #fname = fnam+'FCST' +'/'+ now.strftime('%Y/%m/%d')
   print('Plotting data from',fname)
   com = 'ls %s/*sfcwindspd*.data'%(fname)
   files = os.popen(com).read().strip().split()
   files = [f.replace('spd','') for f in files]
   for f in files:
      tail = f.split('/')[-1].split('.')[0]
      plot_wind(fname,tail)
