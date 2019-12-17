#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import data
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from colormaps import WindSpeed

def plot_wind(ax,img,factor,vmin,vmax,cmap,ext,dens=1.5,stream=True):
   Wspd = img[:,:,0] * data.norms['sfcwindspd'] * factor
   print('Max/min:',np.max(Wspd),np.min(Wspd))
   # Contour
   ax.imshow(Wspd, origin='lower', vmin=vmin, vmax=vmax,
                                   interpolation='lanczos',
                                     cmap=cmap, extent=ext) #,alpha=0.7)
   if stream:
      # Streamplot
      Wdir = img[:,:,1] * data.norms['sfcwinddir']
      mx,Mx,my,My = ext
      x = np.linspace(mx,Mx,Wspd.shape[1])
      y = np.linspace(my,My,Wspd.shape[0])
      U = -Wspd*np.sin(np.radians(Wdir))
      V = -Wspd*np.cos(np.radians(Wdir))
      ax.streamplot(x,y, U,V, color='k',linewidth=0.7, density=dens,
                                         arrowstyle='->',arrowsize=1.5)


def show_prediction(inp,pred,factor=1,vmin=0,vmax=60,title='',fname='',sh=True):
   fig = plt.figure()
   spec = gridspec.GridSpec(1,2, wspace=0.05, hspace=-0.2)
   ax0 = fig.add_subplot(spec[0, 0])
   ax1 = fig.add_subplot(spec[0, 1])

   cmap = WindSpeed
   ext = get_ext('SC4+3')
   print('inp')
   plot_wind(ax0,inp*factor,vmin,vmax,cmap,ext,dens=2)

   ext = get_ext('SC2')
   print('pred')
   plot_wind(ax1,pred*factor,vmin,vmax,cmap,ext)

   titles = ['SC4+3', 'NN']
   for ax,tit in zip([ax0,ax1],titles):
      set_axes(ax,ext,tit)
   if len(title) > 0:
      fig.suptitle(title)
   if len(fname) > 0: fig.savefig(fname,dpi=90)
   if sh: plt.show()


def show_test(inp,out,pred,factor=1,vmin=0,vmax=60,title='',fname='',sh=True):
   """
    Plos an input, expected output, predicted output
    and difference (exp-pred)
   factor: change units
   """
   fig = plt.figure(figsize=(13,8))
   gs = gridspec.GridSpec(2,2, wspace=0.05, hspace=0.18)

   ax0 = fig.add_subplot(gs[0, 0])
   ax1 = fig.add_subplot(gs[0, 1])
   ax2 = fig.add_subplot(gs[1, 0])
   ax3 = fig.add_subplot(gs[1, 1])

   ext = get_ext('SC4+3')
   cmap = WindSpeed
   factor = 3.6
   print('inp')
   plot_wind(ax0,inp,factor,vmin,vmax,cmap,ext,dens=2.25)

   ext = get_ext('SC2')
   print('out')
   plot_wind(ax2,out,factor,vmin,vmax,cmap,ext)

   print('pred')
   plot_wind(ax3,pred,factor,vmin,vmax,cmap,ext)

   diff0 = pred - inp
   diff1 = pred - out
   print('------------------------------')
   print('RASP error:',np.min(diff0),np.max(diff0))
   print('CNN  error:',np.min(diff1),np.max(diff1))
   diff = diff0 - diff1
   plot_wind(ax1,diff,1,-10,10,'PRGn_r',ext,stream=False)

   titles = ['Input (SC4+3)','diff (SC2-NN)',
             'Expected (SC2)','Neural Network']
   for ax,tit in zip([ax0,ax1,ax2,ax3],titles):
      set_axes(ax,ext,tit)

   if len(title) > 0: fig.suptitle(title)
   if len(fname) > 0: fig.savefig(fname, dpi=90)
   ##############
   # Error
   print('Error:')
   fig = plt.figure()
   gs = gridspec.GridSpec(1,2) #, wspace=0.1, hspace=0.18)
   ax0 = fig.add_subplot(gs[0, 0])
   ax1 = fig.add_subplot(gs[0, 1])
   v_diff = diff[:,:,0].flatten() * data.norms['sfcwindspd'] * factor
   values, bins, _ = ax0.hist(v_diff,bins=100)
   ax0.set_xlim([-36,36])
   area = np.sum(np.diff(bins)*values)/v_diff.shape[0]
   print('speed->',area)
   v_diff = diff[:,:,1].flatten() * data.norms['sfcwinddir'] * factor
   values, bins, _ = ax1.hist(v_diff,bins=100)
   ax1.set_xlim([-360,360])
   area = np.sum(np.diff(bins)*values)/v_diff.shape[0]
   print('dir->',area)
   print('------------------------------')
   ##############
   if sh: plt.show()


def set_axes(ax,ext,title=''):
   mx,Mx,my,My = ext
   ax.set_xlim([mx,Mx])
   ax.set_ylim([my,My])
   ax.set_xticks([])
   ax.set_yticks([])
   if len(title) > 0:
      ax.set_title(title)


def get_ext(sc):
   # lat/lon
   lat = np.load(f'../grids/w2/{sc}/lats.npy')
   lon = np.load(f'../grids/w2/{sc}/lons.npy')
   ext = [np.min(lon), np.max(lon), np.min(lat), np.max(lat)]
   return ext
