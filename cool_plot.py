#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import numpy as np
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import datetime as dt
from random import choice
import colormaps
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

def get_valid_date(line):
   pattern = r'([ ^\W\w\d_ ]*) Valid (\S+) ([ ^\W\w\d_ ]*) ~Z75~([ ^\W\w\d_ ]*)~Z~ ([ ^\W\w\d_ ]*) ~Z75~([ ^\W\w\d_ ]*)'
   match = re.search(pattern, line)
   prop,h,Z,_,date,rest = match.groups()
   date = ' '.join(date.split()[1:]) + ' ' + h + ' ' + Z+'T'
   return prop,dt.datetime.strptime(date,'%d %b %Y %H%M %Z')


def plot_background(img,ext,pueblos,takeoffs,ax=None):
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
   villages = open(pueblos,'r').read().strip().splitlines()
   txt = ''
   for i in range(len(villages)):
      line = villages[i]
      ll = line.split()
      a_x,a_y = float(ll[1]),float(ll[0])
      px.append(a_x)
      py.append(a_y)
      nam = ' '.join(ll[2:])
      ax.text(a_x+0.025,a_y,str(i),bbox=dict(facecolor='white', alpha=0.5),
                                                      fontsize=fs, zorder=13)
      txt += f'{i}: {nam}\n'
   txt = txt[:-1]
   ax.text(0.01,0.665,txt,bbox=dict(facecolor='white', alpha=0.7),
                               transform=ax.transAxes, fontsize=fs, zorder=13)
   ax.scatter(px,py,c='r',s=200,zorder=11)
   px,py = [],[]
   villages = open(takeoffs,'r').read().strip().splitlines()
   for i in range(len(villages)):
      line = villages[i]
      ll = line.split()
      a_x,a_y = float(ll[1]),float(ll[0])
      px.append(a_x)
      py.append(a_y)
   ax.scatter(px,py,c='r',s=1500,zorder=13,marker='*')


def plot_wind(fol,tail,prop=''):
   fol_save = fol.replace('DATA','PLOTS')
   os.system('mkdir -p %s'%(fol_save))

   spd = fol +  tail  + 'spd.data'
   dire = fol + tail  + 'dir.data'

   # Forecast valid for day:
   date = open(spd,'r').read().strip().splitlines()[1]
   _, date = get_valid_date(date)

   # Read latitude and longitude info
   # convert lat,lon to pixel
   sc = fol.split('/')[-5].lower()
   X = np.load(here+f'/{sc}_lons.npy')
   Y = np.load(here+f'/{sc}_lats.npy')
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)


   # Calculate Vx and Vy
   S = np.loadtxt(spd, skiprows=4) * 3.6 # km/h
   D = np.radians(np.loadtxt(dire, skiprows=4))  
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

   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
   # vector field
   ax.streamplot(x,y, U,V, color='k',linewidth=1., density=3.5,
                           arrowstyle='->',arrowsize=5,
                           zorder=12)
   # scalar field
   delta = 4
   vmin,vmax = 0,56+delta
   C = ax.contourf(X,Y,S, levels=range(vmin,vmax,delta), extend='max',
                   antialiased=True,
                   cmap=colormaps.WindSpeed,
                   vmin=vmin, vmax=vmax,
                   zorder=10,alpha=0.3)
   divider = make_axes_locatable(ax)
   cax = divider.append_axes("right", size="1.5%", pad=0.2)
   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
   cbar.set_clim(vmin, vmax-delta)
   cbar.ax.set_ylabel('Km/h',fontsize=fs)
   ticklabs = cbar.ax.get_yticklabels()
   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)

   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])
   ax.set_xlim([mx,Mx])
   ax.set_ylim([my,My])


   ax.set_title(date.strftime(prop+' for - %d/%m/%Y %H:%M'),fontsize=50)
   fig.tight_layout()
   fsave = fol_save + tail + '.jpg'
   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
   #plt.show()
   plt.close('all')



def plot_cape(fol,tail):
   fol_save = fol.replace('DATA','PLOTS')
   os.system('mkdir -p %s'%(fol_save))

   cape = fol + tail + '.data'

   # Forecast valid for day:
   date = open(cape,'r').read().strip().splitlines()[1]
   _, date = get_valid_date(date)

   # Read latitude and longitude info
   # convert lat,lon to pixel
   sc = fol.split('/')[-5].lower()
   X = np.load(here+f'/{sc}_lons.npy')
   Y = np.load(here+f'/{sc}_lats.npy')
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)


   ## Read CAPE data
   cape = np.loadtxt(cape, skiprows=4)

   # Prepare XY grid
   x = np.linspace(mx,Mx,X.shape[1])
   y = np.linspace(my,My,X.shape[0])

   # Create Plot
   fig, ax = plt.subplots(figsize=figsize)
   ax.xaxis.tick_top()

   # Background Image
   p0,p1,p2,p3 = border()
   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]

   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
   delta = 100
   vmin,vmax=0,6000+delta
   C = ax.contourf(X,Y,cape, levels=range(vmin,vmax,delta), extend='max',
                   antialiased=True,
                   cmap=colormaps.bgr,
                   vmin=vmin, vmax=vmax,
                   zorder=10,alpha=0.3)
   divider = make_axes_locatable(ax)
   cax = divider.append_axes("right", size="1.5%", pad=0.2)
   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
   cbar.set_clim(vmin, vmax)
   cbar.ax.set_ylabel('Km/h',fontsize=fs)
   ticklabs = cbar.ax.get_yticklabels()
   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)

   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])
   ax.set_xlim([mx,Mx])
   ax.set_ylim([my,My])


   ax.set_title(date.strftime('CAPE for - %d/%m/%Y %H:%M'),fontsize=50)
   fig.tight_layout()
   fsave = fol_save + tail + '.jpg'
   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
   #plt.show()
   plt.close('all')



def plot_thermal_height(fol,tail):
   fol_save = fol.replace('DATA','PLOTS')
   os.system('mkdir -p %s'%(fol_save))

   thermal_height = fol + tail + '.data'

   # Forecast valid for day:
   date = open(thermal_height,'r').read().strip().splitlines()[1]
   _, date = get_valid_date(date)

   # Read latitude and longitude info
   # convert lat,lon to pixel
   sc = fol.split('/')[-5].lower()
   X = np.load(here+f'/{sc}_lons.npy')
   Y = np.load(here+f'/{sc}_lats.npy')
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)


   ## Read Thermal Height data
   thermal_height = np.loadtxt(thermal_height, skiprows=4) / 100  # m/s

   # Prepare XY grid
   x = np.linspace(mx,Mx,X.shape[1])
   y = np.linspace(my,My,X.shape[0])

   # Create Plot
   fig, ax = plt.subplots(figsize=figsize)
   ax.xaxis.tick_top()

   # Background Image
   p0,p1,p2,p3 = border()
   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]

   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
   #bgr = colormaps.bgr
   delta=0.2
   vmin,vmax = 0,3.4+delta
   C = ax.contourf(X,Y,thermal_height, levels=np.arange(vmin,vmax,delta),
                   extend='max', antialiased=True,
                   cmap=colormaps.Thermals,
                   vmin=vmin, vmax=vmax,
                   zorder=10,alpha=0.3)
   divider = make_axes_locatable(ax)
   cax = divider.append_axes("right", size="1.5%", pad=0.2)
   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
   cbar.set_clim(vmin, vmax-delta)
   cbar.ax.set_ylabel('m/s',fontsize=fs)
   ticklabs = cbar.ax.get_yticklabels()
   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)

   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])
   ax.set_xlim([mx,Mx])
   ax.set_ylim([my,My])


   ax.set_title(date.strftime('Thermal Height for - %d/%m/%Y %H:%M'),fontsize=50)
   fig.tight_layout()
   fsave = fol_save + tail + '.jpg'
   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
   #plt.show()
   plt.close('all')


def plot_BL_height(fol,tail):
   fol_save = fol.replace('DATA','PLOTS')
   os.system('mkdir -p %s'%(fol_save))

   BL_height = fol + tail + '.data'

   # Forecast valid for day:
   date = open(BL_height,'r').read().strip().splitlines()[1]
   _, date = get_valid_date(date)

   # Read latitude and longitude info
   # convert lat,lon to pixel
   sc = fol.split('/')[-5].lower()
   X = np.load(here+f'/{sc}_lons.npy')
   Y = np.load(here+f'/{sc}_lats.npy')
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)


   ## Read CAPE data
   BL_height = np.loadtxt(BL_height, skiprows=4)

   # Prepare XY grid
   x = np.linspace(mx,Mx,X.shape[1])
   y = np.linspace(my,My,X.shape[0])

   # Create Plot
   fig, ax = plt.subplots(figsize=figsize)
   ax.xaxis.tick_top()

   # Background Image
   p0,p1,p2,p3 = border()
   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]

   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
   bgr = colormaps.bgr
   delta=200
   vmin = 800
   vmax = 3600
   C = ax.contourf(X,Y,BL_height, levels=range(vmin,vmax,delta), extend='both',
                   antialiased=True,
                   cmap='Paired',
                   vmin=vmin, vmax=vmax,
                   zorder=10,alpha=0.3)
   divider = make_axes_locatable(ax)
   cax = divider.append_axes("right", size="1.5%", pad=0.2)
   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
   cbar.set_clim(vmin, vmax-2*delta)
   cbar.ax.set_ylabel('m/s',fontsize=fs)
   ticklabs = cbar.ax.get_yticklabels()
   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)

   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])
   ax.set_xlim([mx,Mx])
   ax.set_ylim([my,My])


   ax.set_title(date.strftime('BL Height for - %d/%m/%Y %H:%M'),fontsize=50)
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
      plot_wind(fname,tail, prop='Surface wind')   # surface wind
      plot_wind(fname,tail.replace('sfcwind','blwind'), prop='BL wind')
      plot_wind(fname,tail.replace('sfcwind','bltopwind'), prop='top BL wind')
      plot_cape(fname,tail.replace('sfcwind','cape'))
      plot_thermal_height(fname,tail.replace('sfcwind','wstar'))
      plot_BL_height(fname,tail.replace('sfcwind','hbl'))
