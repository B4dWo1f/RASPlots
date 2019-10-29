#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, BoundaryNorm
from matplotlib.collections import LineCollection, PolyCollection
import colormaps
from colormaps import WindSpeed, CAPE, TERRAIN3D, Rain, greys
from common import listfiles
import datetime as dt


params= {'sfcwind':  {'factor':3.6, 'delta':4, 'vmin':0, 'vmax':60,
                      'cmap':WindSpeed},
         'blwind':   {'factor':3.6, 'delta':4, 'vmin':0, 'vmax':60,
                      'cmap':WindSpeed},
         'bltopwind':{'factor':3.6, 'delta':4, 'vmin':0, 'vmax':60,
                      'cmap':WindSpeed},
         'cape':     {'factor':1, 'delta':100, 'vmin':0, 'vmax':6100,
                      'cmap':CAPE},
         'bsratio':  {'factor':1, 'delta':2, 'vmin':0, 'vmax':28,
                      'cmap':WindSpeed},
         'wstar':    {'factor':1/100, 'delta':0.25, 'vmin':0, 'vmax':3.75,
                      'cmap':WindSpeed},
         'hbl':      {'factor':1, 'delta':200,'vmin':800,'vmax':3800,
                      'cmap':WindSpeed},
         'blcloudpct':{'factor':1, 'delta':7,'vmin':0,'vmax':98+7,
                      'cmap':greys},
         'rain1':{'factor':1, 'delta':200,'vmin':800,'vmax':3800,
                      'cmap':None},  # dummy, it is overriden
         'mslpress':{'factor':1, 'delta':200,'vmin':800,'vmax':3800,
                      'cmap':None}}

def super_plot(args):
   hour,prop,Dfolder, curr_date, Pfolder, domain, sc, prop,l,a = args
   if 'wind' in prop:
      all_vector(Dfolder, curr_date, Pfolder, domain, sc, hour, prop,l,a)
   all_scalar(Dfolder, curr_date, Pfolder, domain, sc, hour, prop,l,a)


def plot_background(grid,cmap='gray',ve=100,fig=None,ax=None):
   """
   grid: folder containing the lats,lons,hasl files
   ve: vertical exageration. The higher the number the more accused the
       shadows are
   """
   if grid[-1] == '/': grid = grid[:-1]
   if ax == None: fig, ax = plt.subplots()
   X = np.load(grid+'/lons.npy')
   Y = np.load(grid+'/lats.npy')
   Z = np.load(grid+'/hasl.npy')
   m,n = Z.shape

   d_x = np.max(X)-np.min(X)
   d_y = np.max(Y)-np.min(Y)
   dy,dx = X.shape

   ls = LightSource(azdeg=315, altdeg=50)
   ext = [np.min(X), np.max(X), np.min(Y), np.max(Y)]
   if cmap != 'gray': vmin,vmax = 0.4,1
   else: vmin,vmax = None,None
   aspect = 1.75*d_y/d_x
   terrain = ax.imshow(ls.hillshade(Z, vert_exag=ve, dx=dx, dy=dy),
                       aspect=aspect,
                       origin='lower', interpolation='lanczos',
                       vmin=vmin, vmax=vmax,
                       cmap=cmap, extent=ext, zorder=0)
   
   #if True: #domain == 'd2':
   Sea = np.where(Z<1,-10,1)
   if np.max(Sea) != np.min(Sea):
      sea = ax.imshow(Sea, aspect=1.75*d_y/d_x,
                           origin='lower', interpolation='lanczos',
                           vmin=vmin, vmax=vmax,
                           cmap=colormaps.SeaMask, extent=ext, zorder=1)
   else: sea = None
   return ext,aspect #,terrain,sea

def provincias(fig,ax):
   ccaa = 'ccaa/'
   prov = 'provincias/'
   files = listfiles(f'{ccaa}')
   verts = [np.load(fccaa) for fccaa in files]
   coll = LineCollection(verts, color='k',lw=1.5,zorder=10)
   ax.add_collection(coll)
   files = listfiles(f'{prov}')
   verts = [np.load(fccaa) for fccaa in files]
   coll = LineCollection(verts, color='k',lw=1,zorder=10)
   ax.add_collection(coll)

def rivers(fig,ax):
   rivers = '../../test_lagos/old/old1/rivers/'
   rivers = '../../test_lagos/rivers_spain/'
   files = listfiles(f'{rivers}')
   verts = [np.load(friver) for friver in files]
   coll = LineCollection(verts, color='C0',lw=0.75,zorder=1)
   ax.add_collection(coll)
#def lakes(fig,ax):
   lakes = '../../test_lagos/old/old1/lakes/'
   files = listfiles(f'{lakes}') #+ listfiles(f'{damns}')
   verts = [np.load(flake) for flake in files]
   coll = PolyCollection(verts, color='C0',zorder=1)
   ax.add_collection(coll)

def roads(fig,ax):
   # Roads
   roads = 'roads/'
   files = listfiles(f'{roads}')
   for froad in files:
      Xroad,Yroad = np.loadtxt(froad,unpack=True)
      lws = {'A':6, 'E':6, 'M':5, 'AV':5, 'SG':5, 'CL':5, 'EX':5, 'N':4}
      key = froad.split('/')[-1].replace('.csv','')
      key = " ".join(re.findall("[a-zA-Z]+", key))
      lw = lws[key] -3
      ax.plot(Xroad, Yroad,'k',lw=lw+2,zorder=2)
      ax.plot(Xroad, Yroad,'w',lw=lw,zorder=3)

def takeoffs(fig,ax):
   f_takeoffs = 'takeoffs.csv'
   Yt,Xt = np.loadtxt(f_takeoffs,usecols=(0,1),delimiter=',',unpack=True)
   ax.scatter(Xt,Yt, c='C3',s=50,zorder=20)

def vector_layer(fig,ax,grid,fbase,factor,dens=2):
   """ Specific code to plot the wind (either surface, avg, ot top BL) """
   if grid[-1] != '/': grid += '/'
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)
   x = np.linspace(mx,Mx,X.shape[1])
   y = np.linspace(my,My,X.shape[0])

   # Checking integrity of data
   spd = fbase+'spd.data'
   ori = fbase+'dir.data'

   # Read wind files and build UV arrays
   S = np.loadtxt(spd,skiprows=4) * factor
   D = np.radians(np.loadtxt(ori,skiprows=4))
   U = -S*np.sin(D)
   V = -S*np.cos(D)

   Sp = ax.streamplot(x,y, U,V, color='k',linewidth=1, density=dens,
                                arrowstyle='->',arrowsize=2.5,
                                zorder=11)

def scalar_layer(fig,ax,grid,fbase,factor,delta,vmin,vmax,cmap):
   """ Specific code to plot the wind (either surface, avg, ot top BL) """
   if grid[-1] != '/': grid += '/'
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')

   # Read wind files and build UV arrays
   S = fbase+'.data'
   S = np.loadtxt(S, skiprows=4) * factor

   Cf = ax.contourf(X,Y,S, levels=np.arange(vmin,vmax,delta), extend='max',
                           antialiased=True,
                           cmap=cmap, vmin=vmin, vmax=vmax,
                           zorder=10) #,alpha=0.3)
   #cbar = my_cbar(fig,ax,Cf,'Km/h',fs)
   #return Sp, Cf, cbar

def rain_layer(fig,ax,grid,fbase,factor,delta,vmin,vmax,cmap):
   """ Specific code to plot the wind (either surface, avg, ot top BL) """
   if grid[-1] != '/': grid += '/'
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')

   # Read wind files and build UV arrays
   S = fbase+'.data'
   rain = np.loadtxt(S, skiprows=4) * factor

   levels = [0,1,2,4,6,8,10,15,20,25,30,40,50,60,70]
   norm = BoundaryNorm(levels,len(levels))
   vmin = min(levels)
   vmax = max(levels)
   cmap = Rain
   Cf = ax.contourf(X,Y,rain, levels=levels, #range(vmin,vmax,delta),
                              antialiased=True,
                              extend='max', cmap=cmap,
                              norm=norm, vmin=vmin, vmax=vmax)

def press_layer(fig,ax,grid,fbase,factor,delta,vmin,vmax,cmap):
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')

   press = fbase+'.data'
   press = np.loadtxt(press, skiprows=4)*factor
   sigma=6
   press3 = gaussian_filter(press, sigma)
   mp, Mp = int(np.min(press3)-1), int(np.max(press3)+1)+1
   levels = list( range(mp,Mp,max(1,int((Mp-mp)/10))) )
   Cf = ax.contour(X,Y,press3,levels=levels,colors='k',linewidths=3,zorder=0)
   plt.clabel(Cf, inline=True,fmt='%1d',fontsize=20,zorder=1)


def all_background_layers(folder,domain,sc):
   ves = {'w2':{'SC2':100,'SC2+1':100,'SC4+2':90,'SC4+3':90},
          'd2':{'SC2':5,'SC2+1':5,'SC4+2':4,'SC4+3':4}}
   ve=ves[domain][sc]
   final_folder = f'{folder}/{domain}/{sc}'
   com = f'mkdir -p {final_folder}'
   os.system(com)
   # Terrain
   grid = f'terrain/{domain}/{sc}/'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   fname = f'{final_folder}/terrain.png'
   lims,aspect = plot_background(grid,cmap='gray',ve=ve,fig=fig,ax=ax)
   strip_plot(fig,ax,lims,aspect,fname)
   fname = f'{final_folder}/terrain1.png'
   plot_background(grid,cmap=colormaps.TERRAIN3D,ve=ve,fig=fig,ax=ax)
   strip_plot(fig,ax,lims,aspect,fname)

   # CCAA
   fname = f'{final_folder}/ccaa.png'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   provincias(fig,ax)
   strip_plot(fig,ax,lims,aspect,fname)

   # Rivers
   fname = f'{final_folder}/rivers.png'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   rivers(fig,ax)
   strip_plot(fig,ax,lims,aspect,fname)

   # Roads
   fname = f'{final_folder}/roads.png'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   roads(fig,ax)
   strip_plot(fig,ax,lims,aspect,fname)

   # Takeoffs
   fname = f'{final_folder}/takeoffs.png'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   takeoffs(fig,ax)
   strip_plot(fig,ax,lims,aspect,fname)
   plt.close('all')
   return lims,aspect


def all_vector(Dfolder, date, Pfolder, domain, sc, hour, prop,lims,aspect):
   hour = hour.strftime('%H%M')
   densities = {'w2':{'SC2':1.8,'SC2+1':1.8,'SC4+2':2.5,'SC4+3':2.5},
                'd2':{'SC2':2,'SC2+1':2,'SC4+2':2,'SC4+3':2}}
   P = params[prop]
   final_folder = f'{Pfolder}/{domain}/{sc}'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   grid = f'grids/{domain}/{sc}/'
   #froot = f'{Dfolder}/{domain}/{sc}/{hour}_{prop}'
   froot =  f'{Dfolder}/{domain}/{sc}/'
   froot += f'{date.year}/{date.month:02d}/{date.day:02d}/{hour}_{prop}'
   factor = P['factor']
   vector_layer(fig,ax,grid,froot,factor,dens=densities[domain][sc])
   fname = f'{final_folder}/{hour}_{prop}_vec.png'
   strip_plot(fig,ax,lims,aspect,fname)
   plt.close('all')

def all_scalar(Dfolder, date, Pfolder, domain, sc, hour, prop,lims,aspect):
   hour = hour.strftime('%H%M')
   final_folder = f'{Pfolder}/{domain}/{sc}'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   grid = f'grids/{domain}/{sc}/'
   froot =  f'{Dfolder}/{domain}/{sc}/'
   if 'wind' in prop:
      froot += f'{date.year}/{date.month:02d}/{date.day:02d}/{hour}_{prop}spd'
   else:
      froot += f'{date.year}/{date.month:02d}/{date.day:02d}/{hour}_{prop}'
   P = params[prop]
   delta = P['delta']
   factor = P['factor']
   vmin = P['vmin']
   vmax = P['vmax']
   cmap = P['cmap']
   if prop == 'rain1':
      rain_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap)
   elif prop == 'mslpress':
      press_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap)
   else:
      scalar_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap)
   fname = f'{final_folder}/{hour}_{prop}.png'
   strip_plot(fig,ax,lims,aspect,fname)


def strip_plot(fig,ax,lims,aspect,fname):
   ax.set_aspect(aspect)
   ax.set_xlim(lims[0:2])
   ax.set_ylim(lims[2:4])
   ax.get_xaxis().set_visible(False)
   ax.get_yaxis().set_visible(False)
   fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
   fig.savefig(fname, transparent=True, bbox_inches='tight', pad_inches=0)
   plt.axis('off')

if __name__ == '__main__':
   # Terrain
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   grid = 'terrain/d2/sc2/'
   lims,aspect = plot_background(grid,cmap='gray',ve=5,fig=fig,ax=ax)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('terrain.png', transparent=True,
                           bbox_inches='tight',
                           pad_inches=0)
   plt.close('all')

   # Vector Layer
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   grid = 'grids/d2/sc2/'
   froot = '../../Documents/RASP/DATA/d2/SC2/2019/10/28/1300_sfcwind'
   vector_layer(fig,ax,grid,froot)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('sfcwind_vec.png', transparent=True,
                                  bbox_inches='tight',
                                  pad_inches=0)

   # Scalar Layer
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   grid = 'grids/d2/sc2/'
   froot = '../../Documents/RASP/DATA/d2/SC2/2019/10/28/1300_sfcwindspd'
   delta = 4
   vmin,vmax = 0,56+delta
   cmap = colormaps.WindSpeed
   scalar_layer(fig,ax,grid,froot,delta,vmin,vmax,colormaps.WindSpeed)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('sfcwind_scalar.png', transparent=True,
                                     bbox_inches='tight',
                                     pad_inches=0)
   froot = '../../Documents/RASP/DATA/d2/SC2/2019/10/28/1300_cape'
   delta = 100
   vmin,vmax=0,6000+delta
   cmap = colormaps.CAPE
   scalar_layer(fig,ax,grid,froot,delta,vmin,vmax,colormaps.WindSpeed)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('cape.png', transparent=True,
                                     bbox_inches='tight',
                                     pad_inches=0)


   # CCAA
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   provincias(fig,ax)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('ccaa.png', transparent=True,
                           bbox_inches='tight',
                           pad_inches=0)

   # Rivers
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   rivers(fig,ax)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('rivers.png', transparent=True,
                             bbox_inches='tight',
                             pad_inches=0)

   # Roads
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   roads(fig,ax)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('roads.png', transparent=True,
                             bbox_inches='tight',
                             pad_inches=0)

   # Takeoffs
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   takeoffs(fig,ax)
   strip_plot(fig,ax,lims,aspect)
   fig.savefig('takeoffs.png', transparent=True,
                               bbox_inches='tight',
                               pad_inches=0)
