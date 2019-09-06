#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
################################## LOGGING #####################################
import logging
import log_help
logging.basicConfig(level=logging.DEBUG,
                 format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                 datefmt='%Y/%m/%d-%H:%M:%S',
                 filename = here+'/davinci.log', filemode='w')
LG = logging.getLogger('main')
log_help.screen_handler(LG,lv='info')
################################################################################

import numpy as np
import datetime as dt
import matplotlib as mpl
mpl.use('Agg')   # For crontab running
import matplotlib.pyplot as plt
from time import sleep
from random import random
import common
import plots


C = common.load(here+'/full.ini')

C.date = dt.datetime.now() - dt.timedelta(hours = 5)

UTCshift = round((dt.datetime.now()-dt.datetime.utcnow()).total_seconds()/3600)
LG.info(f'UTCshift: {UTCshift}')

titles= {'blwind':'BL Wind','bltopwind':'BL Top Wind','sfcwind':'Surface Wind',
         'cape': 'CAPE', 'wstar':'Thermal Updraft Velocity',
         'hbl':'Height of BL Top'}


import multiprocessing as sub
all_hour = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
            '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']

figsize=(32,19)
ve=100
for day in C.run_days:
   date_run = C.date + day*dt.timedelta(days=1)
   LG.info(f"Starting plots for {date_run.strftime('%d/%m/%Y')}")
   fol = common.find_best_fcst(date_run,C.root_folder)
   save_fol = fol.replace('DATA','PLOTS')
   LG.info(f'Folder: {save_fol}')
   if not os.path.isdir(save_fol):
      LG.warning(f'Creating folder {save_fol}')
      os.system(f'mkdir -p {save_fol}')
      os.system(f'mkdir -p {save_fol}/A')
      os.system(f'mkdir -p {save_fol}/B')
      os.system(f'mkdir -p {save_fol}/C')
   else: pass
   def plotting(hora):
      sleep(5*random())
      LG.info(f"Starting plots for hour: {hora} UTC")
      H,M = map(int,hora.split(':'))
      date = date_run.replace(hour=H+UTCshift, minute=M)
      props = C.props
      try:
         props.remove('blwinddir')
         props.remove('blwindspd')
         props.remove('bltopwinddir')
         props.remove('bltopwindspd')
         props.remove('sfcwindspd')
         props.remove('sfcwinddir')
      except ValueError: pass
      for prop in ['blwind','bltopwind']:
         figsize=(32,19)
         LG.info(f'Plotting {prop}')
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
         fig.savefig(fname, dpi=65, quality=90)
         plots.zooms(save_fol,hora,prop,fig,ax)
         LG.debug(f'Ploted {prop}')
      fig, ax = plt.subplots(figsize=figsize)
      # Plot background
      plots.plot_background(ve=ve, ax=ax)
      for prop in ['sfcwind'] + props:
         #,'cape','wstar','hbl']: # change for resto of C.props
         figsize=(32,19)
         fig.set_size_inches(figsize)
         LG.info(f'Plotting {prop}')
         # Returns streamplot, contourf, cbar
         sp,cf,cb = plots.plot_prop(fol, hora, prop, fig=fig,ax=ax)
         # Plot settings
         title = titles[prop] + ' - ' + date.strftime('%d/%m/%Y %H:%M')
         ax.set_title(title, fontsize=50)
         fig.tight_layout()
         # Save plot
         fname =  save_fol + '/' + hora.replace(':','')+'_'+prop+'.jpg'
         fig.savefig(fname, dpi=65, quality=90)
         plots.zooms(save_fol,hora,prop,fig,ax)
         LG.debug(f'Ploted {prop}')

         # Clean up
         for coll in cf.collections:
            #plt.gca().collections.remove(coll)
            coll.remove()
         #if sp != None:
         #   sp.lines.remove()
         #   sp.arrows.remove()
         cb.remove()
      plt.close('all')
      LG.debug(f"Done for hour: {date_run.strftime('%d/%m/%Y')}-{hora}")
   #for hora in ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
   #             '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']:

   pool = sub.Pool(2)
   Res = pool.map(plotting, all_hour)
   props = list(set([x.replace('spd','').replace('dir','') for x in C.props]))
   for prop in props:
      files = os.popen(f'ls {save_fol}/*_{prop}.jpg').read().strip().splitlines()
      files = sorted(files,key=lambda x:float(x.split('/')[-1].split('_')[0]))
      tmp_file = '/tmp/video.txt'
      with open(tmp_file,'w') as f:
         for fname in files:
            N=10
            for _ in range(N):
               f.write(fname+'\n')
      com = f'mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4'
      com += f' -o {save_fol}/{prop}.mp4'
      com += f' -mf type=jpeg:fps={N} mf://@{tmp_file}'
      os.system(com)

LG.info('Done!')
