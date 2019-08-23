#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import os
import datetime as dt
from time import time
import matplotlib.pyplot as plt
import common
import plots
here = os.path.dirname(os.path.realpath(__file__))


C = common.load('full.ini')

C.date = dt.datetime.now() - dt.timedelta(hours = 5)

UTCshift = round((dt.datetime.now()-dt.datetime.utcnow()).total_seconds()/3600)

titles= {'blwind':'BL Wind','bltopwind':'BL Top Wind','sfcwind':'Surface Wind',
         'cape': 'CAPE', 'wstar':'Thermal Updraft Velocity',
         'hbl':'Height of BL Top'}

figsize=(32,19)
ve=200
for day in C.run_days:
   date_run = C.date + day*dt.timedelta(days=1)
   fol = common.find_best_fcst(date_run,C.root_folder)
   save_fol = fol.replace('DATA','PLOTS')
   told = time()
   print(save_fol)
   os.system(f'mkdir -p {save_fol}')
   for hora in ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
                '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']:
      H,M = map(int,hora.split(':'))
      date = date_run.replace(hour=H+UTCshift, minute=M)
      for prop in ['blwind','bltopwind']:
         fig, ax = plt.subplots(figsize=figsize)
         # Plot background
         plots.plot_background(ve=ve, ax=ax)
         # Returns streamplot, contourf, cbar
         sp,cf,cb = plots.plot_prop(fol, hora, prop, fig=fig,ax=ax)
         # Plot settings
         title = titles[prop] + ' - ' + date.strftime('%d/%m/%Y %H:%M')
         ax.set_title(title, fontsize=50)
         fig.tight_layout()
         # Save plot
         fname =  save_fol + '/' + hora.replace(':','')+'_'+prop+'.jpg'
         fig.savefig(fname)
      fig, ax = plt.subplots(figsize=figsize)
      # Plot background
      plots.plot_background(ve=ve, ax=ax)
      for prop in ['sfcwind','cape','wstar','hbl']:
         # Returns streamplot, contourf, cbar
         sp,cf,cb = plots.plot_prop(fol, hora, prop, fig=fig,ax=ax)
         # Plot settings
         title = titles[prop] + ' - ' + date.strftime('%d/%m/%Y %H:%M')
         ax.set_title(title, fontsize=50)
         fig.tight_layout()
         # Save plot
         fname =  save_fol + '/' + hora.replace(':','')+'_'+prop+'.jpg'
         fig.savefig(fname)

         # Clean up
         for coll in cf.collections:
            #plt.gca().collections.remove(coll)
            coll.remove()
         #if sp != None:
         #   sp.lines.remove()
         #   sp.arrows.remove()
         cb.remove()
      plt.close('all')
   print(time()-told)
