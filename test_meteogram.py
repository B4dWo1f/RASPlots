#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt
import numpy as np
from time import time
import numeric as num
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from colormaps import WindSpeed
import matplotlib.colors as colors
mpl.rcParams['grid.linestyle'] = 'dotted'

UTCshift = dt.datetime.now()-dt.datetime.utcnow()
UTCshift = round(UTCshift.total_seconds()/3600)
# UTCshift = dt.timedelta(hours = round(UTCshift.total_seconds()/3600))



def get_meteogram(P0,date,data_fol,N=0):
   lon,lat = P0
   sc = 'SC2'
   dom = 'w2'
   year = date.year
   month = date.month
   day = date.day
   fol = f'{data_fol}/{dom}/{sc}/{year}/{month:02d}/{day:02d}'
   plot_meteogram(lon,lat,fol,N=0)

def plot_meteogram(lon,lat,fol,N=0):
   """
   P0 in format (lon, lat)
   """

   grids = 'grids/w2/SC2'
   lats = np.load(f'{grids}/lats.npy')
   lons = np.load(f'{grids}/lons.npy')

   P0 = lon,lat


   def get_ground(fol,P):
      lats = np.load(f'{fol}/lats.npy')
      lons = np.load(f'{fol}/lons.npy')
      hasl = np.load(f'{fol}/hasl.npy')
      dists = num.dists(lons,lats,P0)
      closest_index = np.unravel_index(np.argmin(dists),dists.shape)
      # dists,inds = [],[]
      # for i in range(lats.shape[0]):
      #    for j in range(lats.shape[1]):
      #       dists.append( points2distance(P0,(lons[i,j],lats[i,j])) )
      #       inds.append( (i,j) )
      # ind = np.argmin(dists)
      # closest_index = inds[ind]
      return hasl[closest_index]



   # told = time()
   # dists_matrix = 0.*lats
   # dists,inds = [],[]
   # for i in range(lats.shape[0]):
   #    for j in range(lats.shape[1]):
   #       d = points2distance(P0,(lons[i,j],lats[i,j]))
   #       dists.append(d)
   #       dists_matrix[i,j] = d
   #       inds.append( (i,j) )
   # print('~~ Python')
   # print(np.unravel_index(np.argmin(dists_matrix),dists_matrix.shape))
   # print('time:',time()-told)
   # print('~~ Fortran')
   told = time()
   dists = num.dists(lons,lats,P0)
   closest_index = np.unravel_index(np.argmin(dists),dists.shape)
   print('******************************')
   print(list(reversed(P0)))
   P0 = lons[closest_index], lats[closest_index]
   print('Real:',list(reversed(P0)))
   print('******************************')
   ground = get_ground('../RASPlots/terrain/w2/SC2',P0)

   if N>0:
      patch = [(closest_index[0]-N,closest_index[0]+N+1),
               (closest_index[1]-N,closest_index[1]+N+1)]
      weights = dists_matrix[patch[0][0]:patch[0][1],patch[1][0]:patch[1][1]]
      weights = 1/(weights+0.1)
      weights *= weights
      weights = np.tanh(weights)
   else:
      patch = [(closest_index[0],closest_index[0]+1), 
                (closest_index[1],closest_index[1]+1)]
      weights = None


   def get_value_err(M,closest,weights):
      N = 0  # closest point
      patch = [(closest[0]-N, closest[0]+N+1),
               (closest[1]-N, closest[1]+N+1)]
      M0 = M[patch[0][0]:patch[0][1],patch[1][0]:patch[1][1]]
      M0 = np.average(M0,weights=weights)
      N = 1  # neighbors
      patch = [(closest[0]-N, closest[0]+N+1),
               (closest[1]-N, closest[1]+N+1)]
      MN = M[patch[0][0]:patch[0][1],patch[1][0]:patch[1][1]]
      MN = np.average(MN,weights=weights)
      return M0,MN

   def get_data(fol,h,prop,closest,weights=None):
      fname = f'{fol}/{h*100:04d}_{prop}.data'
      M = np.loadtxt(fname,skiprows=4)
      return get_value_err(M,closest,weights)

   def get_data_mask(fol,h,prop,closest,weights=None):
      fname = f'{fol}/{h*100:04d}_{prop}'
      prop_base = f'{fname}.data'
      prop_pote = f'{fname}dif.data'
      prop_base = np.loadtxt(prop_base, skiprows=4)
      prop_pote = np.loadtxt(prop_pote, skiprows=4)
      null = 0. * prop_base
      M = np.where(prop_pote>0,prop_base,null)
      return get_value_err(M,closest,weights)

   told = time()
   H = []
   sfcwindspd,sfcwinddir = [],[]
   bltopwindspd,bltopwinddir = [],[]
   hbl,hbl_err = [],[]
   # hwcrit = []
   wstar = []
   dwcrit, dwcrit_err = [],[]
   zsfclcl,zsfclcl_err = [],[]
   zblcl,zblcl_err = [],[]
   for h in range(8,19):   # UTC hours
      H.append(h+UTCshift)
      s,_ = get_data(fol,h,'sfcwindspd',closest_index)
      sfcwindspd.append(s*3.6)
      d,_ = get_data(fol,h,'sfcwinddir',closest_index)
      sfcwinddir.append(d)
      s,_ = get_data(fol,h,'bltopwindspd',closest_index)
      bltopwindspd.append(s*3.6)
      d,_ = get_data(fol,h,'bltopwinddir',closest_index)
      bltopwinddir.append(d)
      hg,e = get_data(fol,h,'hbl',closest_index)
      hbl.append(hg)
      hbl_err.append(abs(hg-e)/2)
      # hwcrit.append(get_data(fol,h,'hwcrit',patch))
      d,e = get_data(fol,h,'dwcrit',closest_index)
      dwcrit.append(d+ground)
      dwcrit_err.append(abs(d-e)/2)
      w,_ = get_data(fol,h,'wstar',closest_index)
      wstar.append(s)
      z,e = get_data_mask(fol,h,'zsfclcl',closest_index)
      zsfclcl.append(z)
      zsfclcl_err.append(abs(z-e)/2)
      z,e = get_data_mask(fol,h,'zblcl',closest_index)
      zblcl.append(z)
      zblcl_err.append(abs(z-e)/2)
   print(f'data: {time()-told}s')

   told = time()
   sfcU,sfcV = [],[]
   for S,D in zip(sfcwindspd,sfcwinddir):
      sfcU.append( -np.sin(np.radians(D)) )
      sfcV.append( -np.cos(np.radians(D)) )
   bltopU,bltopV = [],[]
   for S,D in zip(sfcwindspd,sfcwinddir):
      bltopU.append( -np.sin(np.radians(D)) )
      bltopV.append( -np.cos(np.radians(D)) )
   print(f'wind: {time()-told}s')

   thermal_color = (0.90196078,1., 0.50196078)             # NOT RGB
   thermal_color1 = (0.96862745, 0.50980392, 0.23921569)             # NOT RGB
   terrain_color = (0.78235294, 0.37058824, 0.11568627)   # NOT RGB


   told = time()
   rect = patches.Rectangle((0,0),24,ground,facecolor=terrain_color,zorder=90)
   fig, ax = plt.subplots()
   ax.text(8,ground-80,f'GND:{int(ground)}m',zorder=100)
   sfc_info = ground + 15
   cb = ax.quiver(H,[sfc_info for _ in H],
                  sfcU, sfcV, sfcwindspd,
                  linewidth=1, scale=22,
                  norm=colors.Normalize(vmin=0,vmax=56),
                  headaxislength=3,
                  headlength=3.5,
                  headwidth=3,
                  edgecolor='k',
                  cmap = WindSpeed,
                  pivot='middle',zorder=99)
   for h,v in zip(H,sfcwindspd):
      ax.text(h-0.3,sfc_info+30,f'{v:.1f}',zorder=100,bbox=dict(edgecolor='none',facecolor='white', alpha=0.5))
   wind_info = np.where(hbl>sfc_info+150,hbl,-1e9)
   cb = ax.quiver(H,wind_info, bltopU,bltopV, bltopwindspd,
                  linewidth=1, scale=22,
                  norm=colors.Normalize(vmin=0,vmax=56),
                  headaxislength=3,
                  headlength=3.5,
                  headwidth=3,
                  edgecolor='k',
                  cmap = WindSpeed,
                  pivot='middle',zorder=99)
   for h,v,wi in zip(H,bltopwindspd,wind_info):
      ax.text(h-0.3,wi+25,f'{v:.1f}',zorder=100,bbox=dict(edgecolor='none',facecolor='white', alpha=0.5))
   cb = fig.colorbar(cb, orientation='horizontal')
   cb.set_label('Wind (km/h)')
   error_kw = {'width':2,'capsize':4.0, 'alpha':0.3}
   ax.bar(H,hbl,yerr=hbl_err,width=0.9,color=thermal_color,zorder=0,
                    error_kw=error_kw)
   col1 = np.array([255,191,128])/255
   col2 = np.array([204,41,0])/255
   wstar = np.array(wstar)
   wstar_norm = (wstar-np.min(wstar))/(np.max(wstar)-np.min(wstar))
   w_colors = [col2*c/col1 for c in wstar_norm]
   ax.bar(H,dwcrit,color=thermal_color1,yerr=dwcrit_err,width=0.7,zorder=1,
                   error_kw=error_kw)
   ax.bar(H,90,bottom=zsfclcl,width=1.05,color='gray',zorder=1,
                    error_kw=error_kw)
   ax.bar(H,90,bottom=zblcl,width=1.05,color='k',zorder=1,
                    error_kw=error_kw)
   ax.add_patch(rect)
   ax.set_ylim([0.85*ground,max([2500,1.2*max(hbl)])])
   ax.set_xlabel('Time')
   ax.set_ylabel('Height above sea level (m)')
   fig.tight_layout()
   print(f'plot: {time()-told}s')
   # fig.savefig('test.png')
   plt.show()

if __name__ == '__main__':
   # Embalse Monda
   P0 = -3.662435,40.790458   # Lon, Lat

   ## Segovia
   ## P0 = -4.140895,40.939294   # Lon, Lat


   # grids = '../RASPlots/grids/w2/SC2'
   # lats = np.load(f'{grids}/lats.npy')
   # lons = np.load(f'{grids}/lons.npy')
   # lon = np.random.uniform(np.min(lons),np.max(lons))
   # lat = np.random.uniform(np.min(lats),np.max(lats))
   # P0 = lon,lat

   # Arcones
   # P0 = -3.700872,41.088520   # Lon, Lat
   P0 = -3.709228,41.097472   # Lon, Lat

   # # Pedro Bernardo
   # P0 = -4.889601,40.220667

   # # Piedrahita
   # P0 = -5.33,40.46
   data_fol = '/home/n03l/Documents/RASP/DATA'

   year = '2020'
   month = '02'
   day = '28'
   hoy = dt.datetime.now().date()
   get_meteogram(P0,hoy,data_fol)
