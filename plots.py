#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LightSource
from matplotlib.collections import PolyCollection, LineCollection
import re
import datetime as dt
import os
here = os.path.dirname(os.path.realpath(__file__))
import logging
import log_help
LG = logging.getLogger(__name__)
import colormaps
from common import listfiles, find_best_fcst, check_folders, callback_error



params = {'figure.dpi': 150,
          'font.family': 'serif',
          'font.size': 30.0,
          'mathtext.rm': 'serif',
          'mathtext.fontset': 'cm',
          'axes.grid': True,
          'figure.figsize': (9.6, 7.2),
          'figure.dpi': 150}
mpl.rcParams.update(params)
figsize=(30,20)
fs = 35      # fontsize legends
fs_st = 55   # fontsize suptitle
fs_t = 40   # fontsize title

figsizes = {'SC2':(30,20),'SC2+1':(30,20),'SC4+2':(30,25),'SC4+3':(30,25)}
crops = {'SC2':  '1563x1054+220+118', 'SC2+1':'1563x1054+220+118',
         'SC4+2':'1563x1335+220+149', 'SC4+3':'1563x1335+220+149'}

titles= {'blwind':'BL Wind', 'bltopwind':'BL Top Wind',
         'sfcwind':'Surface Wind', 'cape': 'CAPE',
         'wstar':'Thermal Updraft Velocity', 'hbl':'Height of BL Top',
         'bsratio':'Buoyancy/Shear Ratio'}

#def plot_all_properties(C,date_run,hora,UTCshift=2,ve=100,zoom=True,ck=True):
def plot_all_properties(args):
   """
   This function should plot all properties for a given time and date
   In the case of missing data it should return:
      - FileNotFoundError: for missing specific file
      - OSError: for missing folder
   """
   LG.info(f"Starting plots for hour: {hora} UTC")
   C,date_run,hora,UTCshift,ve,zoom,ck = args
   fol = find_best_fcst(date_run,C.root_folder)
   save_fol = fol.replace('DATA','PLOTS')
   save_fol = '/'.join(save_fol.split('/')[:-3])
   sc = save_fol.split('/')[-1]
   if ck: check_folders([save_fol, save_fol+'/A', save_fol+'/B', save_fol+'/C'])
   figsize = figsizes[sc]

   # Set time and date for forecat
   H,M = map(int,hora.split(':'))
   date = date_run.replace(hour=H, minute=M)

   # Terrain files
   hasl = here + f'/terrain/{sc.lower()}_hasl.npy'
   lats = here + f'/terrain/{sc.lower()}_lats.npy'
   lons = here + f'/terrain/{sc.lower()}_lons.npy'
   
   # Sort properties to plot
   props = C.props
   winds = [p for p in C.props if 'wind' in p]
   winds = [p.replace('winddir','wind') for p in winds]
   winds = [p.replace('windspd','wind') for p in winds]
   winds = sorted(list(set(winds)))   # XXX Dangerous
   rest = [p for p in C.props if 'wind' not in p]
   props = winds+rest

   #Start plotting
   fig, ax = plt.subplots(figsize=figsize)
   ## Plot background
   plot_background(ve=ve, ax=ax,lats=lats, lons=lons, hasl=hasl)
   remove_wind = True
   for prop in props:
      if prop == 'sfcwind': remove_wind = False  #keep the sfcwind lines
      ## Check integrity of data before plotting anything
      fbase = fol+date.strftime('/%H%M_')+prop
      if 'wind' in prop: data_file = fbase+'spd.data'
      else: data_file = fbase+'.data'
      if not os.path.isfile(data_file):
         LG.error(f'Missing file {data_file}')
         continue

      ## PLOT the data
      fig.set_size_inches(figsize)
      LG.info(f'Plotting {prop}')
      sp,cf,cb = plot_prop(fol, hora, prop, fig=fig,ax=ax)   #streamplot, contourf, cbar
      ## Plot settings
      date_title = date.replace(hour=H+UTCshift, minute=M)
      title = date_title.strftime('%a %d/%m/%Y %H:%M')
      ax.set_title(title, fontsize=fs_t)
      x0 = (fig.subplotpars.left + fig.subplotpars.right)/2
      fig.suptitle(titles[prop], x=x0, y=0.906, horizontalalignment='center',
                   fontsize=fs_st)
      ## Save plot
      fname =  save_fol + '/' + hora.replace(':','')+'_'+prop+'.jpg'
      fig.savefig(fname, dpi=65, quality=90)
      LG.debug(f'Saved to {fname}')
      ## fix cropping
      com_crop = f'convert {fname} -crop {crops[sc]} {fname}'
      os.system(com_crop)
      if zoom: zooms(save_fol,hora,prop,fig,ax)
      LG.debug(f'Ploted {prop}')

      ## Clean up
      for coll in cf.collections:
         #plt.gca().collections.remove(coll)
         coll.remove()
      if remove_wind:
         if sp != None:
            sp.lines.remove()
            # Remove arrows
            keep = lambda x: not isinstance(x, mpl.patches.FancyArrowPatch)
            ax.patches = [patch for patch in ax.patches if keep(patch)]
      cb.remove()
   plt.close('all')
   LG.debug(f"Done for hour: {date_run.strftime('%d/%m/%Y')}-{hora}")



def plot_prop(folder,time,prop,fig=None,ax=None):
   """
     This function
   """
   date = '/'.join(folder.split('/')[-3:]) + '/' + time
   date = dt.datetime.strptime(date, '%Y/%m/%d/%H:%M')
   sc = folder.split('/')[-4].lower()
   X = np.load(here + f'/grids/{sc}_lons.npy')
   Y = np.load(here + f'/grids/{sc}_lats.npy')
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)

   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])
   ax.set_xlim([mx,Mx])
   ax.set_ylim([my,My])

   #_, valid_date = get_valid_date(date)
   #ax.set_title(fbase.split('/')[-1]+valid_date.date.strftime('%d/%m/%Y ')+hora, fontsize=50)
   if 'wind' in prop:
      return wind(X,Y,folder+date.strftime('/%H%M_')+prop,fig=fig,ax=ax)
   elif prop == 'cape':
      return cape(X,Y,folder+date.strftime('/%H%M_')+prop,fig=fig,ax=ax)
   elif prop == 'wstar':
      return wstar(X,Y,folder+date.strftime('/%H%M_')+prop,fig=fig,ax=ax)
   elif prop == 'hbl':
      return hbl(X,Y,folder+date.strftime('/%H%M_')+prop,fig=fig,ax=ax)
   elif prop == 'bsratio':
      return bsratio(X,Y,folder+date.strftime('/%H%M_')+prop,fig=fig,ax=ax)
   else: 
      LG.critical(f'{prop} not implemented')
      return None

def my_cbar(fig,ax,img,units,fs):
   divider = make_axes_locatable(ax)
   cax = divider.new_vertical(size="2.95%", pad=0.25, pack_start=True)
   fig.add_axes(cax)
   cbar = fig.colorbar(img, cax=cax, orientation="horizontal")
   cbar.ax.set_xlabel(units,fontsize=fs)
   return cbar

@log_help.timer(LG)
def cape(X,Y,fbase,fig=None,ax=None):
   """
    Specific code to plot the CAPE
   """
   CAPE = fbase+'.data'
   if not os.path.isfile(CAPE):
      LG.error('Missing file {CAPE}')
      raise FileNotFoundError
   else: CAPE = np.loadtxt(CAPE,skiprows=4)
   delta = 100
   vmin,vmax=0,6000+delta
   Cf = ax.contourf(X,Y,CAPE, levels=range(vmin,vmax,delta), extend='max',
                   antialiased=True,
                   cmap=colormaps.CAPE,
                   vmin=vmin, vmax=vmax,
                   zorder=12,alpha=0.3)
   cbar = my_cbar(fig,ax,Cf,'J/Kg',fs)
   return None,Cf,cbar

@log_help.timer(LG)
def wind(X,Y,fbase,fig=None,ax=None):
   """
    Specific code to plot the wind (either surface, avg, ot top BL)
   """
   mx,Mx = np.min(X),np.max(X)
   my,My = np.min(Y),np.max(Y)
   x = np.linspace(mx,Mx,X.shape[1])
   y = np.linspace(my,My,X.shape[0])

   # Checking integrity of data
   spd = fbase+'spd.data'
   ori = fbase+'dir.data'
   #if not os.path.isfile(spd):
   #   LG.error('Missing file {spd}')
   #   raise FileNotFoundError
   #elif not os.path.isfile(ori):
   #   LG.error('Missing file {ori}')
   #   raise FileNotFoundError

   S = np.loadtxt(spd,skiprows=4) * 3.6
   D = np.radians(np.loadtxt(ori,skiprows=4))
   U = -S*np.sin(D)
   V = -S*np.cos(D)
   
   Sp = ax.streamplot(x,y, U,V, color='k',linewidth=1., density=3.5,
                                arrowstyle='->',arrowsize=5,
                                zorder=11)
   delta = 4
   vmin,vmax = 0,56+delta
   Cf = ax.contourf(X,Y,S, levels=range(vmin,vmax,delta), extend='max',
                           antialiased=True,
                           cmap=colormaps.WindSpeed,
                           vmin=vmin, vmax=vmax,
                           zorder=10,alpha=0.3)
   cbar = my_cbar(fig,ax,Cf,'Km/h',fs)
   return Sp, Cf, cbar

@log_help.timer(LG)
def bsratio(X,Y,fbase,fig=None,ax=None):
   BSratio = fbase+'.data'
   if not os.path.isfile(BSratio):
      LG.error('Missing file {BSratio}')
      raise FileNotFoundError
   else: BSratio = np.loadtxt(BSratio,skiprows=4)
   delta=2
   vmin,vmax = 0,28+delta
   Cf = ax.contourf(X,Y,BSratio, levels=np.arange(vmin,vmax,delta),
                   extend='max', antialiased=True,
                   cmap=colormaps.WindSpeed,
                   vmin=vmin, vmax=vmax,
                   zorder=12,alpha=0.3)
   cbar = my_cbar(fig,ax,Cf,'',fs)
   return None,Cf,cbar


@log_help.timer(LG)
def wstar(X,Y,fbase,fig=None,ax=None):
   Wstar = fbase+'.data'
   if not os.path.isfile(Wstar):
      LG.error('Missing file {Wstar}')
      raise FileNotFoundError
   else: Wstar = np.loadtxt(Wstar,skiprows=4) /100
   delta=0.25
   vmin,vmax = 0,3.5+delta
   Cf = ax.contourf(X,Y,Wstar, levels=np.arange(vmin,vmax,delta),
                   extend='max', antialiased=True,
                   cmap=colormaps.WindSpeed,
                   vmin=vmin, vmax=vmax,
                   zorder=12,alpha=0.3)
   cbar = my_cbar(fig,ax,Cf,'m/s',fs)
   return None,Cf,cbar

@log_help.timer(LG)
def hbl(X,Y,fbase,fig=None,ax=None):
   Hbl = fbase+'.data'
   if not os.path.isfile(Hbl):
      LG.error('Missing file {Hbl}')
      raise FileNotFoundError
   else: Hbl = np.loadtxt(Hbl,skiprows=4)
   delta=200
   vmin,vmax = 800, 3600+delta
   Cf = ax.contourf(X,Y,Hbl, levels=range(vmin,vmax,delta), extend='both',
                   antialiased=True,
                   cmap=colormaps.WindSpeed,  #'Paired',
                   vmin=vmin, vmax=vmax,
                   zorder=12,alpha=0.3)
   cbar = my_cbar(fig,ax,Cf,'m',fs)
   return None,Cf,cbar


#def border():
#   """
#     Obsolete!
#     P0-------------P3
#     |              |
#     |              |
#     P1-------------P2
#   """
#   P0 = (-6.230882, 41.588094)
#   P1 = (-6.232133, 39.866217)
#   P2 = (-3.022456, 39.861002)
#   P3 = (-3.025468, 41.595428)
#
#   # 41.727515,-6.825019        41.722646,-2.781653
#   # 39.590629,-6.787157        39.582791,-2.692100
#   #P0 = (-6.825019, 41.727515)
#   #P1 = (-6.787157, 39.590629)
#   #P2 = (-2.692100, 39.582791)
#   #P3 = (-2.781653, 41.722646)
#   return P0,P1,P2,P3

def get_valid_date(line):
   """
   Regex the data files looking for the valid date of the forecast. Ex:
   Day= 2019 8 23 FRI ValidLST= 1200 CES ValidZ= 1000 Fcst= 10.0 Init= 0 Param= sfcwinddir Unit= deg Mult= 1 Min= 0 Max= 360
   """
   pattern = r'([ ^\W\w\d_ ]*) Valid (\S+) ([ ^\W\w\d_ ]*) ~Z75~([ ^\W\w\d_ ]*)~Z~ ([ ^\W\w\d_ ]*) ~Z75~([ ^\W\w\d_ ]*)'
   match = re.search(pattern, line)
   prop,h,Z,_,date,rest = match.groups()
   date = ' '.join(date.split()[1:]) + ' ' + h + ' ' + Z+'T'
   return prop,dt.datetime.strptime(date,'%d %b %Y %H%M %Z')


@log_help.timer(LG)
def plot_background(lats=here+'/lats.npy',lons=here+'/lons.npy',
                    hasl=here+'/hasl.npy',
                    ve=100, cmap='gray',
                    roads=here+'/roads', lakes=here+'/lagos',
                    damns=here+'/embalses', rivers=here+'/rios',
                    poblaciones=here+'/poblaciones',
                    ccaa=here+'/ccaa', provincias=here+'/provincias',
                    takeoffs=here+'/takeoffs.csv',
                    cities=here+'/cities.csv',
                    ax=None):
   """
    Plots the terrain data stored in the hasl file. lats and lons files are
    only used to extract the geographic limits of the grid, but in principle
    they could have a different size, just make sure that the min/max are
    correct
    ve: vertical exageration. The higher the number the more accused the
        shadows are
   """
   if ax == None: fig, ax = plt.subplots()
   X = np.load(lons)
   Y = np.load(lats)
   Z = np.load(hasl)
   m,n = Z.shape

   d_x = np.max(X)-np.min(X)
   d_y = np.max(Y)-np.min(Y)
   dy,dx = X.shape

   ls = LightSource(azdeg=315, altdeg=50)
   ext = [np.min(X), np.max(X), np.min(Y), np.max(Y)]
   ax.imshow(ls.hillshade(Z, vert_exag=ve, dx=dx, dy=dy),aspect=d_y/d_x,origin='lower',interpolation='lanczos', cmap=cmap, extent=ext,zorder=0)
   # Provincias
   files = listfiles(f'{ccaa}')
   verts = [np.load(fccaa) for fccaa in files]
   coll = LineCollection(verts, color='k',lw=3,zorder=4)
   ax.add_collection(coll)
   files = listfiles(f'{provincias}')
   verts = [np.load(fccaa) for fccaa in files]
   coll = LineCollection(verts, color='k',lw=2,zorder=4)
   ax.add_collection(coll)
     ## poblaciones
     #files = listfiles(f'{poblaciones}') + listfiles(f'{damns}')
     #verts = [np.load(flake) for flake in files]
     #coll = PolyCollection(verts, color='C7',zorder=1,alpha=0.9)
     #ax.add_collection(coll)
   # Lakes
   files = listfiles(f'{lakes}') + listfiles(f'{damns}')
   verts = [np.load(flake) for flake in files]
   coll = PolyCollection(verts, color='C0',zorder=1)
   ax.add_collection(coll)
   # Rivers
   files = listfiles(f'{rivers}')
   verts = [np.load(friver) for friver in files]
   coll = LineCollection(verts, color='C0',lw=1.5,zorder=1)
   ax.add_collection(coll)
   # Roads
   files = listfiles(f'{roads}')
   for froad in files:
      Xroad,Yroad = np.loadtxt(froad,unpack=True)
      lws = {'A':6, 'E':6, 'M':5, 'AV':5, 'SG':5, 'CL':5, 'EX':5, 'N':4}
      key = froad.split(f'{roads}/')[-1].replace('.csv','')
      key = " ".join(re.findall("[a-zA-Z]+", key))
      lw = lws[key]
      ax.plot(Xroad, Yroad,'k',lw=lw+2,zorder=2)
      ax.plot(Xroad, Yroad,'w',lw=lw,zorder=3)

   # Takeoffs
   Yt,Xt = np.loadtxt(takeoffs,usecols=(0,1),delimiter=',',unpack=True)
   ax.scatter(Xt,Yt, c='C3',s=300,zorder=20)
   txt = np.loadtxt(takeoffs,usecols=(2,),delimiter=',',dtype=str)
   for i in range(len(txt)):
      ax.text(Xt[i]+0.025,Yt[i],str(i+1),bbox=dict(facecolor='white',
                                                   alpha=0.5),
                                                   fontsize=fs, zorder=33)
   msg = ''
   for i in range(len(txt)):
      msg += f'{i+1}: {txt[i]}\n'
   msg = msg[:-1]
   ## Legend for takeoffs
   ax.text(0.01,0.584,msg,bbox=dict(facecolor='white', alpha=0.7),
                               transform=ax.transAxes, fontsize=fs, zorder=33)

   # Cities
   Yt,Xt = np.loadtxt(cities,usecols=(0,1),delimiter=',',unpack=True)
   names = np.loadtxt(cities,usecols=(2,),delimiter=',',dtype=str)
   for i in range(len(names)):
      ax.text(Xt[i]-0.09*len(names[i])/6, Yt[i]-0.01, names[i],
              bbox=dict(facecolor='white', alpha=0.4), fontsize=fs-3, zorder=13)
   #ax.scatter(Xt,Yt, c='C3',s=900,zorder=20, marker='*')


def zooms(save_fol,hora,prop,fig,ax,figsize=figsize):
   """
    Apply the harcoded lims for the plots
    Arcones
           +------------------ 41.428272,-3.027596
           |                            |
           |                            |
    40.711015,-4.302319 ----------------+
    Cebreros
           +------------------ 40.946453,-3.564694
           |                            |
           |                            |
    40.171926,-5.079508 ----------------+
    Pedro Bernardo
           +------------------ 40.733445,-4.393813
           |                            |
           |                            |
    39.972178,-6.030375 ----------------+
   """
   #ARCONES
   ax.set_xlim([-4.302319,-3.2])
   ax.set_ylim([40.711015,41.428272])
   fsz = figsize[0]/1.2,figsize[1]
   fig.set_size_inches(fsz)  #igsize[0]/1.2,figsize[1])
   fname =  save_fol + '/A/' + hora.replace(':','')+'_'+prop+'.jpg'
   fig.savefig(fname, dpi=65, quality=90)
   os.system(f'convert {fname} -crop 1325x1000+170+165 {fname}')
   # CEBREROS
   ax.set_xlim([-5.079508,-3.564694])
   ax.set_ylim([40.171926,40.946453])
   fsz = figsize[0]/1.1,figsize[1]/1.2
   fig.set_size_inches(fsz)  #igsize[0]/1.1,figsize[1]/1.2)
   fname =  save_fol + '/B/' + hora.replace(':','')+'_'+prop+'.jpg'
   fig.savefig(fname, dpi=65, quality=90)
   os.system(f'convert {fname} -crop 1420x900+200+100 {fname}')
   # PEDRO BERNARDO
   ax.set_xlim([-6.030375,-4.393813])
   ax.set_ylim([39.972178,40.733445])
   fsz = figsize[0],figsize[1]/1.2
   fig.set_size_inches(fsz)  #igsize[0],figsize[1]/1.2)
   fname =  save_fol + '/C/' + hora.replace(':','')+'_'+prop+'.jpg'
   fig.savefig(fname, dpi=65, quality=90)
   os.system(f'convert {fname} -crop 1565x900+220+95 {fname}')



#def plot_background_google(img,ext,pueblos,takeoffs,ax=None):
#   """
#    obsolete
#    Sets an image as background for other plots. It also marks the villages
#   stored in pueblos.csv
#   """
#   if ax is None: ax = plt.gca()
#   img = mpimg.imread(img) #here+'/Gmap1.jpg')
#   #yshape,xshape,_ = img.shape
#   ax.imshow(img, aspect='equal', extent=ext,zorder=1,origin='lower')
#   ## Pueblos
#   px,py = [],[]
#   villages = open(pueblos,'r').read().strip().splitlines()
#   txt = ''
#   for i in range(len(villages)):
#      line = villages[i]
#      ll = line.split()
#      a_x,a_y = float(ll[1]),float(ll[0])
#      px.append(a_x)
#      py.append(a_y)
#      nam = ' '.join(ll[2:])
#      ax.text(a_x+0.025,a_y,str(i),bbox=dict(facecolor='white', alpha=0.5),
#                                                      fontsize=fs, zorder=13)
#      txt += f'{i}: {nam}\n'
#   txt = txt[:-1]
#   ax.text(0.01,0.665,txt,bbox=dict(facecolor='white', alpha=0.7),
#                               transform=ax.transAxes, fontsize=fs, zorder=13)
#   ax.scatter(px,py,c='r',s=200,zorder=11)
#   px,py = [],[]
#   villages = open(takeoffs,'r').read().strip().splitlines()
#   for i in range(len(villages)):
#      line = villages[i]
#      ll = line.split()
#      a_x,a_y = float(ll[1]),float(ll[0])
#      px.append(a_x)
#      py.append(a_y)
#   ax.scatter(px,py,c='r',s=1500,zorder=13,marker='*')
#
#
#def plot_wind(fol,tail,prop=''):
#   """
#   Obsolete?
#   """
#   fol_save = fol.replace('DATA','PLOTS')
#   os.system('mkdir -p %s'%(fol_save))
#
#   spd = fol +  tail  + 'spd.data'
#   dire = fol + tail  + 'dir.data'
#
#   # Forecast valid for day:
#   date = open(spd,'r').read().strip().splitlines()[1]
#   _, date = get_valid_date(date)
#
#   # Read latitude and longitude info
#   # convert lat,lon to pixel
#   sc = fol.split('/')[-5].lower()
#   X = np.load(here+f'/{sc}_lons.npy')
#   Y = np.load(here+f'/{sc}_lats.npy')
#   mx,Mx = np.min(X),np.max(X)
#   my,My = np.min(Y),np.max(Y)
#
#
#   # Calculate Vx and Vy
#   S = np.loadtxt(spd, skiprows=4) * 3.6 # km/h
#   D = np.radians(np.loadtxt(dire, skiprows=4))  
#   U = -S*np.sin(D)
#   V = -S*np.cos(D)
#
#   # Prepare streamplot
#   x = np.linspace(mx,Mx,X.shape[1])
#   y = np.linspace(my,My,X.shape[0])
#
#   # Create Plot
#   fig, ax = plt.subplots(figsize=figsize)
#   ax.xaxis.tick_top()
#
#   # Background Image
#   p0,p1,p2,p3 = border()
#   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
#          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]
#
#   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
#   # vector field
#   ax.streamplot(x,y, U,V, color='k',linewidth=1., density=3.5,
#                           arrowstyle='->',arrowsize=5,
#                           zorder=12)
#   # scalar field
#   delta = 4
#   vmin,vmax = 0,56+delta
#   C = ax.contourf(X,Y,S, levels=range(vmin,vmax,delta), extend='max',
#                   antialiased=True,
#                   cmap=colormaps.WindSpeed,
#                   vmin=vmin, vmax=vmax,
#                   zorder=10,alpha=0.3)
#   divider = make_axes_locatable(ax)
#   cax = divider.append_axes("right", size="1.5%", pad=0.2)
#   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
#   cbar.set_clim(vmin, vmax-delta)
#   cbar.ax.set_ylabel('Km/h',fontsize=fs)
#   ticklabs = cbar.ax.get_yticklabels()
#   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)
#
#   ax.set_aspect('equal')
#   ax.set_xticks([])
#   ax.set_yticks([])
#   ax.set_xlim([mx,Mx])
#   ax.set_ylim([my,My])
#
#
#   ax.set_title(date.strftime(prop+' for - %d/%m/%Y %H:%M'),fontsize=50)
#   fig.tight_layout()
#   fsave = fol_save + tail + '.jpg'
#   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
#   #plt.show()
#   plt.close('all')
#
#
#
#def plot_cape(fol,tail):
#   fol_save = fol.replace('DATA','PLOTS')
#   os.system('mkdir -p %s'%(fol_save))
#
#   cape = fol + tail + '.data'
#
#   # Forecast valid for day:
#   date = open(cape,'r').read().strip().splitlines()[1]
#   _, date = get_valid_date(date)
#
#   # Read latitude and longitude info
#   # convert lat,lon to pixel
#   sc = fol.split('/')[-5].lower()
#   X = np.load(here+f'/{sc}_lons.npy')
#   Y = np.load(here+f'/{sc}_lats.npy')
#   mx,Mx = np.min(X),np.max(X)
#   my,My = np.min(Y),np.max(Y)
#
#
#   ## Read CAPE data
#   cape = np.loadtxt(cape, skiprows=4)
#
#   # Prepare XY grid
#   x = np.linspace(mx,Mx,X.shape[1])
#   y = np.linspace(my,My,X.shape[0])
#
#   # Create Plot
#   fig, ax = plt.subplots(figsize=figsize)
#   ax.xaxis.tick_top()
#
#   # Background Image
#   p0,p1,p2,p3 = border()
#   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
#          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]
#
#   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
#   delta = 100
#   vmin,vmax=0,6000+delta
#   C = ax.contourf(X,Y,cape, levels=range(vmin,vmax,delta), extend='max',
#                   antialiased=True,
#                   cmap=colormaps.CAPE,
#                   vmin=vmin, vmax=vmax,
#                   zorder=10,alpha=0.3)
#   divider = make_axes_locatable(ax)
#   cax = divider.append_axes("right", size="1.5%", pad=0.2)
#   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
#   cbar.set_clim(vmin, vmax)
#   cbar.ax.set_ylabel('J/Kg',fontsize=fs)
#   ticklabs = cbar.ax.get_yticklabels()
#   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)
#
#   ax.set_aspect('equal')
#   ax.set_xticks([])
#   ax.set_yticks([])
#   ax.set_xlim([mx,Mx])
#   ax.set_ylim([my,My])
#
#
#   ax.set_title(date.strftime('CAPE for - %d/%m/%Y %H:%M'),fontsize=50)
#   fig.tight_layout()
#   fsave = fol_save + tail + '.jpg'
#   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
#   #plt.show()
#   plt.close('all')
#
#
#
#def plot_thermal_height(fol,tail):
#   fol_save = fol.replace('DATA','PLOTS')
#   os.system('mkdir -p %s'%(fol_save))
#
#   thermal_height = fol + tail + '.data'
#
#   # Forecast valid for day:
#   date = open(thermal_height,'r').read().strip().splitlines()[1]
#   _, date = get_valid_date(date)
#
#   # Read latitude and longitude info
#   # convert lat,lon to pixel
#   sc = fol.split('/')[-5].lower()
#   X = np.load(here+f'/{sc}_lons.npy')
#   Y = np.load(here+f'/{sc}_lats.npy')
#   mx,Mx = np.min(X),np.max(X)
#   my,My = np.min(Y),np.max(Y)
#
#
#   ## Read Thermal Height data
#   thermal_height = np.loadtxt(thermal_height, skiprows=4) / 100  # m/s
#
#   # Prepare XY grid
#   x = np.linspace(mx,Mx,X.shape[1])
#   y = np.linspace(my,My,X.shape[0])
#
#   # Create Plot
#   fig, ax = plt.subplots(figsize=figsize)
#   ax.xaxis.tick_top()
#
#   # Background Image
#   p0,p1,p2,p3 = border()
#   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
#          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]
#
#   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
#   #bgr = colormaps.bgr
#   delta=0.2
#   vmin,vmax = 0,3.4+delta
#   C = ax.contourf(X,Y,thermal_height, levels=np.arange(vmin,vmax,delta),
#                   extend='max', antialiased=True,
#                   cmap=colormaps.Thermals,
#                   vmin=vmin, vmax=vmax,
#                   zorder=10,alpha=0.3)
#   divider = make_axes_locatable(ax)
#   cax = divider.append_axes("right", size="1.5%", pad=0.2)
#   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
#   cbar.set_clim(vmin, vmax-delta)
#   cbar.ax.set_ylabel('m/s',fontsize=fs)
#   ticklabs = cbar.ax.get_yticklabels()
#   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)
#
#   ax.set_aspect('equal')
#   ax.set_xticks([])
#   ax.set_yticks([])
#   ax.set_xlim([mx,Mx])
#   ax.set_ylim([my,My])
#
#
#   ax.set_title(date.strftime('Thermal Height for - %d/%m/%Y %H:%M'),fontsize=50)
#   fig.tight_layout()
#   fsave = fol_save + tail + '.jpg'
#   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
#   #plt.show()
#   plt.close('all')
#
#
#def plot_BL_height(fol,tail):
#   fol_save = fol.replace('DATA','PLOTS')
#   os.system('mkdir -p %s'%(fol_save))
#
#   BL_height = fol + tail + '.data'
#
#   # Forecast valid for day:
#   date = open(BL_height,'r').read().strip().splitlines()[1]
#   _, date = get_valid_date(date)
#
#   # Read latitude and longitude info
#   # convert lat,lon to pixel
#   sc = fol.split('/')[-5].lower()
#   X = np.load(here+f'/{sc}_lons.npy')
#   Y = np.load(here+f'/{sc}_lats.npy')
#   mx,Mx = np.min(X),np.max(X)
#   my,My = np.min(Y),np.max(Y)
#
#
#   ## Read CAPE data
#   BL_height = np.loadtxt(BL_height, skiprows=4)
#
#   # Prepare XY grid
#   x = np.linspace(mx,Mx,X.shape[1])
#   y = np.linspace(my,My,X.shape[0])
#
#   # Create Plot
#   fig, ax = plt.subplots(figsize=figsize)
#   ax.xaxis.tick_top()
#
#   # Background Image
#   p0,p1,p2,p3 = border()
#   ext = [np.mean([p1[0],p0[0]]), np.mean([p2[0],p3[0]]),
#          np.mean([p1[1],p2[1]]), np.mean([p0[1],p3[1]])]
#
#   plot_background(here+'/Gmap1.jpg',ext,here+'/takeoffs.csv',here+'/cities.csv',ax)
#   bgr = colormaps.bgr
#   delta=200
#   vmin = 800
#   vmax = 3600
#   C = ax.contourf(X,Y,BL_height, levels=range(vmin,vmax,delta), extend='both',
#                   antialiased=True,
#                   cmap='Paired',
#                   vmin=vmin, vmax=vmax,
#                   zorder=10,alpha=0.3)
#   divider = make_axes_locatable(ax)
#   cax = divider.append_axes("right", size="1.5%", pad=0.2)
#   cbar = fig.colorbar(C, cax=cax) #,boundaries=range(0,lim_wind,5))
#   cbar.set_clim(vmin, vmax-2*delta)
#   cbar.ax.set_ylabel('m',fontsize=fs)
#   ticklabs = cbar.ax.get_yticklabels()
#   cbar.ax.set_yticklabels(ticklabs, fontsize=fs)
#
#   ax.set_aspect('equal')
#   ax.set_xticks([])
#   ax.set_yticks([])
#   ax.set_xlim([mx,Mx])
#   ax.set_ylim([my,My])
#
#
#   ax.set_title(date.strftime('BL Height for - %d/%m/%Y %H:%M'),fontsize=50)
#   fig.tight_layout()
#   fsave = fol_save + tail + '.jpg'
#   fig.savefig(fsave, dpi=65, quality=90) #,dpi=80,quality=100)
#   #plt.show()
#   plt.close('all')

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
