#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from layers import params
import numpy as np
import colormaps
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import BoundaryNorm

COLOR = '#e0e0e0'
COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
mpl.rcParams['axes.edgecolor'] = COLOR

#fig.colorbar(c)
#plt.show()

def plot_colorbar(cmap,delta=4,vmin=0,vmax=60,levels=None,name='cbar',
                                        units='',fs=18,norm=None,extend='max'):
   fig, ax = plt.subplots()
   img = np.random.uniform(vmin,vmax,size=(4,4))
   if levels == None:
      levels=np.arange(vmin,vmax,delta)
   img = ax.contourf(img, levels=levels,
                          extend=extend,
                          antialiased=True,
                          cmap=cmap,
                          norm=norm,
                          vmin=vmin, vmax=vmax)
   plt.gca().set_visible(False)
   divider = make_axes_locatable(ax)
   cax = divider.new_vertical(size="2.95%", pad=0.25, pack_start=True)
   fig.add_axes(cax)
   cbar = fig.colorbar(img, cax=cax, orientation="horizontal")
   cbar.ax.set_xlabel(units,fontsize=fs)
   fig.savefig(f'{name}_light.png', transparent=True,
                              bbox_inches='tight', pad_inches=0)

if __name__ == '__main__':
   name = 'sfcwind'
   for name in ['sfcwind','blwind','bltopwind']:
      P = params[name]
      delta = P['delta']
      vmin  = P['vmin']
      vmax  = P['vmax']
      # delta = 4
      # vmin = 0
      # vmax = 56+delta
      levels = None
      cmap = colormaps.WindSpeed
      units = 'Km/h'
      plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  = 'cape'
   P = params[name]
   delta = P['delta']
   vmin  = P['vmin']
   vmax  = P['vmax']
   # delta = 100
   # vmin  = 0
   # vmax  = 6000 + delta
   levels = None
   cmap  = colormaps.CAPE
   units = 'J/Kg'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  = 'bsratio'
   P = params[name]
   delta = P['delta']
   vmin  = P['vmin']
   vmax  = P['vmax']
   # delta = 2
   # vmin  = 0
   # vmax  = 26+delta
   levels = None
   cmap  = colormaps.WindSpeed
   units = ''
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)
   
   name  ='wstar'
   P = params[name]
   delta = P['delta']
   vmin  = P['vmin']
   vmax  = P['vmax']
   # delta = 0.25
   # vmin  = 0
   # vmax  = 3.5 + delta
   levels = None
   cmap  = colormaps.WindSpeed
   units = 'm/s'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  = 'hbl'
   P = params[name]
   delta = P['delta']
   vmin  = P['vmin']
   vmax  = P['vmax']
   # delta = 200
   # vmin  = 800
   # vmax  = 3600 + delta
   levels = None
   cmap  = colormaps.WindSpeed
   units = 'm'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  = 'rain1'
   levels = [0,1,2,4,6,8,10,15,20,25,30,40,50,60,70]
   delta = 200
   vmin  = min(levels)
   vmax  = max(levels)
   norm  = BoundaryNorm(levels,len(levels))
   cmap  = colormaps.Rain
   units = 'mm'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units,norm=norm)

   name  = 'hglider'
   P = params[name]
   delta = P['delta']
   vmin  = P['vmin']
   vmax  = P['vmax']
   # delta = 240
   # vmin  = 200
   # vmax  = 3800
   levels = None
   cmap  = colormaps.WindSpeed
   units = 'm'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  ='wblmaxmin'
   P = params[name]
   delta = P['delta']
   vmin  = P['vmin']
   vmax  = P['vmax']
   levels = P['levels'] # [-3,-2, -1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1, 2, 3]
   norm  = BoundaryNorm(levels,len(levels))
   cmap  = colormaps.Convergencias
   units = 'm/s'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units,norm=norm,extend='both')

   name  ='zsfclcl'
   delta = 280
   vmin  = 1200
   vmax  = 5400 + delta
   levels = None
   cmap = colormaps.WindSpeed
   units = 'm'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  ='zblcl'
   delta = 280
   vmin  = 1200
   vmax  = 5400 + delta
   levels = None
   cmap = colormaps.WindSpeed
   units = 'm'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)
