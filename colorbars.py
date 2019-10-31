#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import colormaps
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import BoundaryNorm


#fig.colorbar(c)
#plt.show()

def plot_colorbar(cmap,delta=4,vmin=0,vmax=60,levels=None,
                       name='cbar',units='',fs=18,norm=None):
   fig, ax = plt.subplots()
   img = np.random.uniform(vmin,vmax,size=(4,4))
   if levels == None:
      levels=np.arange(vmin,vmax,delta)
   img = ax.contourf(img, levels=levels,
                          extend='max',
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
   fig.savefig(f'{name}.png', transparent=True,
                              bbox_inches='tight', pad_inches=0)

if __name__ == '__main__':
   name = 'sfcwind'
   for name in ['sfcwind','blwind','bltopwind']:
      delta = 4
      vmin = 0
      vmax = 56+delta
      levels = None
      cmap = colormaps.WindSpeed
      units = 'Km/h'
      plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  = 'cape'
   delta = 100
   vmin  = 0
   vmax  = 6000 + delta
   levels = None
   cmap  = colormaps.CAPE
   units = 'J/Kg'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  = 'bsratio'
   delta = 2
   vmin  = 0
   vmax  = 26+delta
   levels = None
   cmap  = colormaps.WindSpeed
   units = ''
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)
   
   name  ='wstar'
   delta = 0.25
   vmin  = 0
   vmax  = 3.5 + delta
   levels = None
   cmap  = colormaps.WindSpeed
   units = 'm/s'
   plot_colorbar(cmap,delta,vmin,vmax,levels,name,units)

   name  = 'hbl'
   delta = 200
   vmin  = 800
   vmax  = 3600 + delta
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
