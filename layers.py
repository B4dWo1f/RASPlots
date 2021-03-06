#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
here = os.path.dirname(os.path.realpath(__file__))
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import matplotlib.patheffects as PathEffects
import matplotlib as mpl
if os.getenv('RUN_BY_CRON'): mpl.use('Agg')
import matplotlib.pyplot as plt
try: plt.style.use('mystyle')
except: pass
#COLOR = 'black'
## Dark Theme ###################################################################
COLOR = '#e0e0e0'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['axes.facecolor'] = 'black'
mpl.rcParams['savefig.facecolor'] = 'black'
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
mpl.rcParams['axes.edgecolor'] = COLOR
#################################################################################

import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.image as mpimg
from matplotlib.colors import LightSource, BoundaryNorm
from matplotlib.collections import LineCollection, PolyCollection
import colormaps
from colormaps import WindSpeed, CAPE, TERRAIN3D, Rain, greys, Convergencias
from common import listfiles
import datetime as dt
from random import random
import log_help
import logging
LG = logging.getLogger(__name__)


params= {'sfcwind':   {'factor':3.6, 'delta':4, 'vmin':0, 'vmax':60,
                       'cmap':WindSpeed},
         'blwind':    {'factor':3.6, 'delta':4, 'vmin':0, 'vmax':60,
                       'cmap':WindSpeed},
         'bltopwind': {'factor':3.6, 'delta':4, 'vmin':0, 'vmax':60,
                       'cmap':WindSpeed},
         'cape':      {'factor':1, 'delta':100, 'vmin':0, 'vmax':6100,
                       'cmap':CAPE},
         'bsratio':   {'factor':1, 'delta':2, 'vmin':0, 'vmax':28,
                       'cmap':WindSpeed},
         'wstar':     {'factor':1/100, 'delta':0.25, 'vmin':0, 'vmax':3.75,
                       'cmap':WindSpeed},
         'hbl':       {'factor':1, 'delta':200,'vmin':800,'vmax':3800,
                       'cmap':WindSpeed},
         'blcloudpct':{'factor':1, 'delta':7,'vmin':0,'vmax':98+7,
                       'cmap':greys},
         'rain1':     {'factor':1, 'delta':200,'vmin':800,'vmax':3800,
                       'levels': [0,1,2,4,6,8,10,15,20,25,30,40,50,60,70],
                       'cmap':None},  # dummy, it is overriden
         'mslpress':  {'factor':1, 'delta':200,'vmin':800,'vmax':3800,
                       'cmap':None},
         'hglider' :  {'factor':1, 'delta':240,'vmin':200,'vmax':3800,
                       'cmap':WindSpeed},
         'hwcrit' :  {'factor':1, 'delta':240,'vmin':200,'vmax':3800,
                       'cmap':WindSpeed},
         'dwcrit' :  {'factor':1, 'delta':200,'vmin':0,'vmax':2000,
                       'cmap':WindSpeed},
         'wblmaxmin': {'factor':1/100, 'delta':0.1,'vmin':-3,'vmax':3,
                       'levels':[-3,-2, -1, -0.8, -0.6, -0.4, -0.2, 0,
                                 0.2, 0.4, 0.6, 0.8, 1, 2, 3],
                       'cmap':Convergencias},
         'zsfclcl' :  {'factor':1, 'delta':240,'vmin':200,'vmax':3800,
                       'cmap':WindSpeed,'levels':None},
         # 'zsfclcl': {'factor':1, 'delta':280,'vmin':1200,'vmax':5400,
         #             'cmap':WindSpeed},
         # 'zsfclcldif': {'factor':1, 'delta':280,'vmin':1200,'vmax':5400,
         #                'cmap':WindSpeed},
         'zblcl' :  {'factor':1, 'delta':240,'vmin':200,'vmax':3800,
                     'cmap':WindSpeed,'levels':None}
         # 'zblcl': {'factor':1, 'delta':280,'vmin':1200,'vmax':5400,
         #           'cmap':WindSpeed},
         # 'zblcldif': {'factor':1, 'delta':280,'vmin':1200,'vmax':5400,
         #               'cmap':WindSpeed},
         }

def super_plot(args):
   hour,prop,Dfolder, curr_date, Pfolder, domain, sc, prop,l,a = args
   LG.debug(f'Plotting {sc} {domain} {hour.strftime("%Y/%m/%d-%H%M")} {prop}')
   with open(f'{Pfolder}/{domain}/{sc}/valid_date.txt','w') as f:
      f.write(curr_date.strftime('%d/%m/%Y\n'))
   try:
      if 'wind' in prop:
         all_vector(Dfolder, curr_date, Pfolder, domain, sc, hour, prop,l,a)
      all_scalar(Dfolder, curr_date, Pfolder, domain, sc, hour, prop,l,a)
      LG.debug(f'plotted: {domain} {sc} {hour} {prop}')
   except OSError:
      msg = f'missing {sc} {domain} {hour.strftime("%Y/%m/%d-%H%M")} {prop}'
      LG.critical(msg)


def plot_background(grid,cmap='gray',ve=100,fig=None,ax=None):
   """
   grid: folder containing the lats,lons,hasl files
   ve: vertical exageration. The higher the number the more accused the
       shadows are
   """
   if grid[-1] == '/': grid = grid[:-1]
   if ax == None: fig, ax = plt.subplots()
   dom,sc = grid.split('/')[-2:]
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
   aspects = {'w2':{'SC2':2.25, 'SC2+1':2.25, 'SC4+2':1.7, 'SC4+3':1.7},
              'd2':{'SC2':1.9, 'SC2+1':1.9, 'SC4+2':1.9, 'SC4+3':1.9}}
   aspect = aspects[dom][sc]*d_y/d_x #1.75*d_y/d_x   # 2.25 for almost mercator
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
   ccaa = f'{here}/ccaa/'
   prov = f'{here}/provincias/'
   files = listfiles(f'{ccaa}')
   verts = [np.load(fccaa) for fccaa in files]
   coll = LineCollection(verts, color='k',lw=1.5,zorder=10)
   ax.add_collection(coll)
   files = listfiles(f'{prov}')
   verts = [np.load(fccaa) for fccaa in files]
   coll = LineCollection(verts, color='k',lw=1,zorder=10)
   ax.add_collection(coll)

def rivers(fig,ax):
   rivers = f'{here}/rios/'
   files = listfiles(f'{rivers}')
   verts = [np.load(friver) for friver in files]
   coll = LineCollection(verts, color='C0',lw=0.75,zorder=1)
   ax.add_collection(coll)
#def lakes(fig,ax):
   lakes = f'{here}/lagos/'
   files = listfiles(f'{lakes}') #+ listfiles(f'{damns}')
   verts = [np.load(flake) for flake in files]
   coll = PolyCollection(verts, color='C0',zorder=1)
   ax.add_collection(coll)

def roads(fig,ax):
   # Roads
   roads = f'{here}/roads/'
   files = listfiles(f'{roads}')
   for froad in files:
      Xroad,Yroad = np.loadtxt(froad,unpack=True)
      lws = {'A':6, 'E':6, 'M':5, 'AV':5, 'SG':5, 'CL':5, 'EX':5, 'N':4}
      key = froad.split('/')[-1].replace('.csv','')
      key = " ".join(re.findall("[a-zA-Z]+", key))
      lw = max((lws[key] -3)/2,0.1)
      ax.plot(Xroad, Yroad,'k',lw=lw+2,zorder=2)
      ax.plot(Xroad, Yroad,'w',lw=lw,zorder=3)

def takeoffs(fig,ax):
   f_takeoffs = f'{here}/takeoffs.csv'
   Yt,Xt = np.loadtxt(f_takeoffs,usecols=(0,1),delimiter=',',unpack=True)
   ax.scatter(Xt,Yt, c='C3',s=50,zorder=20)

def names(fig,ax):
   f_takeoffs = f'{here}/takeoffs.csv'
   Yt,Xt = np.loadtxt(f_takeoffs,usecols=(0,1),delimiter=',',unpack=True)
   names = np.loadtxt(f_takeoffs,usecols=(2,),delimiter=',',dtype=str)
   for x,y,name in zip(Xt,Yt,names):
      txt = ax.text(x,y,name, horizontalalignment='center',
                              verticalalignment='center',
                              color='k',
                              fontsize=13)
      txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
   f_cities = f'{here}/cities.csv'
   Yt,Xt = np.loadtxt(f_cities,usecols=(0,1),delimiter=',',unpack=True)
   names = np.loadtxt(f_cities,usecols=(2,),delimiter=',',dtype=str)
   for x,y,name in zip(Xt,Yt,names):
      txt = ax.text(x,y,name, horizontalalignment='center',
                              verticalalignment='center',
                              color='k',fontsize=13)
      txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])

def cities(fig,ax):
   f_cities = f'{here}/cities.csv'
   Yt,Xt = np.loadtxt(f_cities,usecols=(0,1),delimiter=',',unpack=True)
   names = np.loadtxt(f_cities,usecols=(2,),delimiter=',',dtype=str)
   ax.scatter(Xt,Yt, c='C3',s=90, marker='x',zorder=20)

def manga(fig,ax):
   f_manga = f'{here}/task.gps'
   try:
      y,x,Rm = np.loadtxt(f_manga,usecols=(0,1,2),delimiter=',',unpack=True)
      # spacing of arrows
      scale = 2
      aspace = .18 # good value for scale of 1
      aspace *= scale

      # r is the distance spanned between pairs of points
      r = [0]
      for i in range(1,len(x)):
          dx = x[i]-x[i-1]
          dy = y[i]-y[i-1]
          r.append(np.sqrt(dx*dx+dy*dy))
      r = np.array(r)

      # rtot is a cumulative sum of r, it's used to save time
      rtot = []
      for i in range(len(r)):
          rtot.append(r[0:i].sum())
      rtot.append(r.sum())

      arrowData = [] # will hold tuples of x,y,theta for each arrow
      arrowPos = 0   # current point on walk along data
      rcount = 1
      while arrowPos < r.sum():
          x1,x2 = x[rcount-1],x[rcount]
          y1,y2 = y[rcount-1],y[rcount]
          da = arrowPos-rtot[rcount]
          theta = np.arctan2((x2-x1),(y2-y1))
          X = np.sin(theta)*da+x1
          Y = np.cos(theta)*da+y1
          arrowData.append((X,Y,theta))
          arrowPos+=aspace
          while arrowPos > rtot[rcount+1]:
              rcount+=1
              if arrowPos > rtot[-1]: break

      # could be done in above block if you want
      for X,Y,theta in arrowData:
          # use aspace as a guide for size and length of things
          # scaling factors were chosen by experimenting a bit
          ax.arrow(X,Y,
                     np.sin(theta)*aspace/10,np.cos(theta)*aspace/10,
                     head_width=aspace/8, color='r')
      # ax.plot(x,y)
      ax.plot(x,y, 'r-', lw=4) #c='C4',s=50,zorder=20)
   except: pass

def vector_layer(fig,ax,grid,fbase,factor,dens=2):
   """ Specific code to plot the wind (either surface, avg, ot top BL) """
   if grid[-1] != '/': grid += '/'
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')
   # # Opt 0
   # mx,Mx = np.min(X),np.max(X)
   # my,My = np.min(Y),np.max(Y)
   # Opt 1
   Mx = np.mean([np.max(X), np.min(X[:,-1])])  # right bound
   mx = np.mean([np.min(X), np.max(X[:,0])])   # left bound
   My = np.mean([np.max(Y), np.min(Y[-1,:])])  # upper bound
   my = np.mean([np.min(Y), np.max(Y[0,:])])   # lower bound
   # # Opt 2
   # Mx = np.min(X[:,-1])  # right bound
   # mx = np.max(X[:,0])  # left bound
   # My = np.min(Y[-1,:])  # upper bound
   # my = np.max(Y[0,:])  # lower bound

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

def scalar_layer(fig,ax,grid,fbase,factor,delta,vmin,vmax,cmap,levels=[]):
   """ Specific code to plot the wind (either surface, avg, ot top BL) """
   if grid[-1] != '/': grid += '/'
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')

   # Read wind files and build UV arrays
   S = fbase+'.data'
   S = np.loadtxt(S, skiprows=4) * factor

   if len(levels) > 0:
      norm = BoundaryNorm(levels,len(levels))
   else:
      levels = np.arange(vmin,vmax,delta)
      norm = None
   Cf = ax.contourf(X,Y,S, levels=levels, extend='max',
                           antialiased=True, norm=norm,
                           cmap=cmap, vmin=vmin, vmax=vmax)
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

def cloud_base_layer(fig,ax,grid,fbase,factor,delta,vmin,vmax,cmap):
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')
   cu_base = fbase+'.data'
   cu_pote = fbase+'dif.data'
   cu_base = np.loadtxt(cu_base, skiprows=4)*factor
   cu_pote = np.loadtxt(cu_pote, skiprows=4)*factor
   null = 0. * cu_base
   cu_base_pote = np.where(cu_pote>0,cu_base,null)
   Cf = ax.contourf(X,Y,cu_base_pote, levels=range(vmin,vmax,delta),
                                      antialiased=True,
                                      extend='max', cmap=cmap,
                                      vmin=vmin, vmax=vmax)

def overcast_development_layer(fig,ax,grid,fbase,factor,delta,vmin,vmax,cmap):
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')
   od_base = fbase+'.data'
   od_pote = fbase+'dif.data'
   od_base = np.loadtxt(od_base, skiprows=4)*factor
   od_pote = np.loadtxt(od_pote, skiprows=4)*factor
   null = 0. * od_base
   od_base_pote = np.where(od_pote>0,od_base,null)
   Cf = ax.contourf(X,Y,od_base_pote, levels=range(vmin,vmax,delta),
                                      antialiased=True,
                                      extend='max', cmap=cmap,
                                      vmin=vmin, vmax=vmax)

def press_layer(fig,ax,grid,fbase,factor,delta,vmin,vmax,cmap):
   X = np.load(grid+'lons.npy')
   Y = np.load(grid+'lats.npy')

   press = fbase+'.data'
   press = np.loadtxt(press, skiprows=4)*factor
   sigma=6
   press3 = gaussian_filter(press, sigma)
   # mp, Mp = int(np.min(press3)-1), int(np.max(press3)+1)+1
   # levels = list( range(mp,Mp,max(1,int((Mp-mp)/10))) )
   levels = list(range(964,1040,4))
   Cf = ax.contour(X,Y,press3,levels=levels,colors='k',linewidths=3,zorder=0)
   plt.clabel(Cf, inline=True,fmt='%1d',fontsize=20)  #,zorder=1)


def all_background_layers(folder,domain,sc):
   ves = {'w2':{'SC2':100,'SC2+1':100,'SC4+2':40,'SC4+3':40},
          'd2':{'SC2':2.5,'SC2+1':2.5,'SC4+2':9.5,'SC4+3':9.5}}
   ve=ves[domain][sc]
   final_folder = f'{folder}/{domain}/{sc}'
   com = f'mkdir -p {final_folder}'
   os.system(com)
   # Terrain
   grid = f'{here}/terrain/{domain}/{sc}/'
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

   # Names
   fname = f'{final_folder}/names.png'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   names(fig,ax)
   strip_plot(fig,ax,lims,aspect,fname)

   # Cities
   fname = f'{final_folder}/cities.png'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   cities(fig,ax)
   strip_plot(fig,ax,lims,aspect,fname)

   # Manga
   fname = f'{final_folder}/manga.png'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   manga(fig,ax)
   strip_plot(fig,ax,lims,aspect,fname)

   plt.close('all')
   return lims,aspect


def all_vector(Dfolder, date, Pfolder, domain, sc, hour, prop,lims,aspect,dpi=65):
   hour = hour.strftime('%H%M')
   densities = {'w2':{'SC2':1.8,'SC2+1':1.8,'SC4+2':2.5,'SC4+3':2.5},
                'd2':{'SC2':2,'SC2+1':2,'SC4+2':2,'SC4+3':2}}
   P = params[prop]
   final_folder = f'{Pfolder}/{domain}/{sc}'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   grid = f'{here}/grids/{domain}/{sc}/'
   #froot = f'{Dfolder}/{domain}/{sc}/{hour}_{prop}'
   froot =  f'{Dfolder}/{domain}/{sc}/'
   froot += f'{date.year}/{date.month:02d}/{date.day:02d}/{hour}_{prop}'
   factor = P['factor']
   vector_layer(fig,ax,grid,froot,factor,dens=densities[domain][sc])
   fname = f'{final_folder}/{hour}_{prop}_vec.png'
   strip_plot(fig,ax,lims,aspect,fname,dpi=dpi)
   plt.close('all')

def all_scalar(Dfolder, date, Pfolder, domain, sc, hour, prop,lims,aspect,dpi=65):
   hour = hour.strftime('%H%M')
   final_folder = f'{Pfolder}/{domain}/{sc}'
   fig, ax = plt.subplots(figsize=(10,10),frameon=False)
   grid = f'{here}/grids/{domain}/{sc}/'
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
   try: levels = P['levels']
   except KeyError: levels = []
   if prop == 'rain1':
      rain_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap)
   elif prop == 'mslpress':
      press_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap)
   elif prop == 'zsfclcl':
      cloud_base_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap)
   elif prop == 'zsfclcldif': return
   elif prop == 'zblcl':
      overcast_development_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap)
   elif prop == 'zblcldif': return
   else:
      scalar_layer(fig,ax,grid,froot,factor,delta,vmin,vmax,cmap,levels=levels)
   fname = f'{final_folder}/{hour}_{prop}.png'
   strip_plot(fig,ax,lims,aspect,fname,dpi=dpi)
   plt.close('all')


def strip_plot(fig,ax,lims,aspect,fname,dpi=65):
   ax.set_aspect(aspect)
   ax.set_xlim(lims[0:2])
   ax.set_ylim(lims[2:4])
   ax.get_xaxis().set_visible(False)
   ax.get_yaxis().set_visible(False)
   plt.axis('off')
   fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
   fig.savefig(fname, transparent=True, bbox_inches='tight', pad_inches=0,
                      dpi=dpi, quality=90)   # compression



props = {'sfcwind':'Viento Superficie', 'blwind':'Viento Promedio',
         'bltopwind':'Viento Altura', 'hglider':'Techo (azul)',
         'wstar':'Térmica', 'zsfclcl':'Base nube', 'zblcl':'Cielo cubierto',
         'cape':'CAPE', 'wblmaxmin':'Convergencias',
         'hbl': 'Altura Capa Convectiva', 'bsratio': 'B/S ratio',
         'rain1': 'Lluvia', 'blcloudpct':'Nubosidad (%)'}

def timelapse(args):
   """
   merge all the png into a mp4 video suitable for Telegram
   """
   save_fol,tmp_folder,prop,fps,N,ext = args
   f_out = f'{save_fol}/{prop}.mp4'
   files = os.popen(f'ls {tmp_folder}/*_{prop}.{ext}').read()
   files = files.strip().splitlines()
   files = sorted(files,key=lambda x:float(x.split('/')[-1].split('_')[0]))
   tmp_file = f'{tmp_folder}/video{int(1+1000*random())}.txt'
   with open(tmp_file,'w') as f:
      for fname in files:
         for _ in range(N):
            f.write(fname+'\n')
   com = f'mencoder -quiet -nosound -ovc lavc -lavcopts vcodec=mpeg4'
   com += f' -o {tmp_folder}/{prop}_temp.mp4'
   com += f' -mf type=png:fps={int(N/fps)} mf://@{tmp_file}'
   com += ' > /dev/null 2> /dev/null'
   LG.debug(com)
   os.system(com)
   com = f'ffmpeg -y -i {tmp_folder}/{prop}_temp.mp4 -vcodec mpeg4 -threads 2 -b:v 1500k -acodec libmp3lame -ab 160k {f_out}'
   com += ' > /dev/null 2> /dev/null'
   LG.debug(com)
   os.system(f'rm {f_out}')  # clean previuos plot
   os.system(com)
   os.system(f'rm {tmp_file}')
   os.system(f'rm {tmp_folder}/{prop}_temp.mp4')
   os.popen(f'rm {tmp_folder}/*_{prop}.png').read()
   LG.info(f'Saved in {save_fol}/{prop}.mp4')
   return f'{save_fol}/{prop}.mp4'


def make_timelapse(args):
   """
   UTCshift = hours between UTC and local time
   """
   root_folder,dom,sc,fscalar,fvector,UTCshift = args
   tmp_folder = f'/tmp/{dom}/{sc}'
   os.system(f'mkdir -p {tmp_folder}')
   LG.debug(f'{dom},{sc},{fscalar},{fvector}')
   com = f'ls {root_folder}/{dom}/{sc}/*00_{fscalar}.png'
   LG.debug(com)
   hours = os.popen(com).read().strip().splitlines()
   hours = [int(h.split('/')[-1].split('_')[0]) for h in hours]
   for hora in hours:
      f_tmp  = f'{tmp_folder}/{hora:04d}_{fscalar}.png'
      f_tmp1 = f'{tmp_folder}/{hora:04d}_{fscalar}1.png'
      grids_fol = f'{here}/grids/{dom}/{sc}/'
      fol = f'{root_folder}/{dom}/{sc}'
      date = open(f'{fol}/valid_date.txt', 'r').read().strip()
      date = dt.datetime.strptime(date,'%d/%m/%Y')
      dateUTC = date.replace(hour=hora//100)   # UTC
      date = dateUTC + UTCshift
      # scalar = 'sfcwind'
      # vector = 'sfcwind'
      title = f"{date.strftime('%d/%m/%Y-%H:%M')} {props[fscalar]}"

      lats = f'{grids_fol}/lats.npy'
      lons = f'{grids_fol}/lons.npy'

      terrain = f'{fol}/terrain.png'
      rivers = f'{fol}/rivers.png'
      ccaa = f'{fol}/ccaa.png'
      takeoffs = f'{fol}/takeoffs.png'
      manga = f'{fol}/manga.png'
      cities = f'{fol}/cities.png'
      bar = f'{root_folder}/{fscalar}.png'  #_light.png'

      if fvector != 'none': vector = f'{fol}/{hora:04d}_{fvector}_vec.png'
      else: vector = None
      scalar = f'{fol}/{hora:04d}_{fscalar}.png'

      # Read Images
      terrain = mpimg.imread(terrain)
      rivers = mpimg.imread(rivers)
      ccaa = mpimg.imread(ccaa)
      takeoffs = mpimg.imread(takeoffs)
      try: manga = mpimg.imread(manga)
      except: pass
      cities = mpimg.imread(cities)
      if fvector != None: img_vector = mpimg.imread(vector)
      img_scalar = mpimg.imread(scalar)
      bar = mpimg.imread(bar)
      # Output Images
      aspect=1.
      fig = plt.figure()
      gs = gridspec.GridSpec(2, 1, height_ratios=[7.2,1])
      fig.subplots_adjust(wspace=0.,hspace=0.)
      ax1 = plt.subplot(gs[0,0])
      ax2 = plt.subplot(gs[1,0])
      ax1.imshow(terrain,aspect=aspect,interpolation='lanczos',zorder=0)
      ax1.imshow(rivers,aspect=aspect,interpolation='lanczos',zorder=0)
      ax1.imshow(ccaa,aspect=aspect,interpolation='lanczos',zorder=20)
      ax1.imshow(takeoffs,aspect=aspect,interpolation='lanczos',zorder=20)
      try: ax1.imshow(manga, aspect=aspect, interpolation='lanczos',zorder=21)
      except: pass
      ax1.imshow(cities,aspect=aspect,interpolation='lanczos',zorder=20)
      if vector != None:
         ax1.imshow(img_vector, aspect=aspect, interpolation='lanczos',
                                zorder=11, alpha=0.75)
      ax1.imshow(img_scalar, aspect=aspect, interpolation='lanczos',
                             zorder=10, alpha=0.5)
      ax1.set_xticks([])
      ax1.set_yticks([])
      ax1.set_title(title)
      ax1.axis('off')
      ax2.imshow(bar)
      ax2.set_xticks([])
      ax2.set_yticks([])
      ax2.axis('off')
      fig.tight_layout()
      fig.savefig(f_tmp)
      # plt.show()
      os.system(f'convert {f_tmp} -trim {f_tmp1}')
      os.system(f'mv {f_tmp1} {f_tmp}')
   plt.close('all')
   out_folder = f'{root_folder}/{dom}/{sc}'
   vid = timelapse((out_folder,tmp_folder,fscalar,2,10,'png'))
   return vid

# if __name__ == '__main__':
#    # Terrain
#    fig, ax = plt.subplots(figsize=(10,10),frameon=False)
#    grid = f'{here}/terrain/d2/sc2/'
#    lims,aspect = plot_background(grid,cmap='gray',ve=5,fig=fig,ax=ax)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('terrain.png', transparent=True,
#                            bbox_inches='tight',
#                            pad_inches=0)
#    plt.close('all')

#    # Vector Layer
#    fig, ax = plt.subplots(figsize=(10,10),frameon=False)
#    grid = 'grids/d2/sc2/'
#    froot = '../../Documents/RASP/DATA/d2/SC2/2019/10/28/1300_sfcwind'
#    vector_layer(fig,ax,grid,froot)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('sfcwind_vec.png', transparent=True,
#                                   bbox_inches='tight',
#                                   pad_inches=0)

#    # Scalar Layer
#    fig, ax = plt.subplots(figsize=(10,10),frameon=False)
#    grid = 'grids/d2/sc2/'
#    froot = '../../Documents/RASP/DATA/d2/SC2/2019/10/28/1300_sfcwindspd'
#    delta = 4
#    vmin,vmax = 0,56+delta
#    cmap = colormaps.WindSpeed
#    scalar_layer(fig,ax,grid,froot,delta,vmin,vmax,colormaps.WindSpeed)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('sfcwind_scalar.png', transparent=True,
#                                      bbox_inches='tight',
#                                      pad_inches=0)
#    froot = '../../Documents/RASP/DATA/d2/SC2/2019/10/28/1300_cape'
#    delta = 100
#    vmin,vmax=0,6000+delta
#    cmap = colormaps.CAPE
#    scalar_layer(fig,ax,grid,froot,delta,vmin,vmax,colormaps.WindSpeed)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('cape.png', transparent=True,
#                                      bbox_inches='tight',
#                                      pad_inches=0)


#    # CCAA
#    fig, ax = plt.subplots(figsize=(10,10),frameon=False)
#    provincias(fig,ax)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('ccaa.png', transparent=True,
#                            bbox_inches='tight',
#                            pad_inches=0)

#    # Rivers
#    fig, ax = plt.subplots(figsize=(10,10),frameon=False)
#    rivers(fig,ax)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('rivers.png', transparent=True,
#                              bbox_inches='tight',
#                              pad_inches=0)

#    # Roads
#    fig, ax = plt.subplots(figsize=(10,10),frameon=False)
#    roads(fig,ax)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('roads.png', transparent=True,
#                              bbox_inches='tight',
#                              pad_inches=0)

#    # Takeoffs
#    fig, ax = plt.subplots(figsize=(10,10),frameon=False)
#    takeoffs(fig,ax)
#    strip_plot(fig,ax,lims,aspect)
#    fig.savefig('takeoffs.png', transparent=True,
#                                bbox_inches='tight',
#                                pad_inches=0)
