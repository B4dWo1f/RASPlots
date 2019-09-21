#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
import multiprocessing as sub
import datetime as dt
from random import random
################################## LOGGING #####################################
import logging
import log_help
logging.basicConfig(level=logging.WARNING,
                 format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                 datefmt='%Y/%m/%d-%H:%M:%S',
                 filename = here+'/timelapse.log', filemode='w')
LG = logging.getLogger('main')
log_help.screen_handler(LG, lv=logging.WARNING)
################################################################################
import common

def timelapse(args):
   save_fol,prop,fps,N = args
   files = os.popen(f'ls {save_fol}/*_{prop}.jpg').read()
   files = files.strip().splitlines()
   files = sorted(files,key=lambda x:float(x.split('/')[-1].split('_')[0]))
   tmp_file = f'/tmp/video{int(1+1000*random())}.txt'
   with open(tmp_file,'w') as f:
      for fname in files:
         for _ in range(N):
            f.write(fname+'\n')
   com = f'mencoder -quiet -nosound -ovc lavc -lavcopts vcodec=mpeg4'
   com += f' -o /tmp/{prop}_temp.mp4'
   com += f' -mf type=jpeg:fps={int(fps/N)} mf://@{tmp_file}'
   com += ' > /dev/null 2> /dev/null'
   LG.debug(com)
   os.system(com)
   com = f'ffmpeg -y -i /tmp/{prop}_temp.mp4 -vcodec mpeg4 -threads 2 -b:v 1500k -acodec libmp3lame -ab 160k {save_fol}/{prop}.mp4'
   com += ' > /dev/null 2> /dev/null'
   LG.debug(com)
   os.system(com)
   os.system(f'rm {tmp_file}')
   os.system(f'rm /tmp/{prop}_temp.mp4')
   LG.info(f'Saved in {save_fol}/{prop}.mp4')


C = common.load(here+'/full.ini')
fps = 20
dens=5

# Sort properties to plot
props = C.props
winds = [p for p in C.props if 'wind' in p]
winds = [p.replace('winddir','wind') for p in winds]
winds = [p.replace('windspd','wind') for p in winds]
winds = sorted(list(set(winds)))   # XXX Dangerous
rest = [p for p in C.props if 'wind' not in p]
props = winds+rest
LG.info( 'Timelapses for: ' + ', '.join([str(p) for p in props]) )


for day in C.run_days:
   date_run = C.date + day*dt.timedelta(days=1)
   fol = common.find_best_fcst(date_run,C.root_folder)
   save_fol = fol.replace('DATA','PLOTS')
   save_fol = '/'.join(save_fol.split('/')[:-3])
   LG.info(f"Timelapses for {date_run.strftime('%d/%m/%Y')}")

   if C.parallel:
      LG.debug('Running in parallel')
      all_inputs = [ (save_fol,prop,fps,dens) for prop in props ]
      pool = sub.Pool(4)
      Res = pool.map(timelapse, all_inputs)
   else:
      for prop in props:
         LG.debug(f'Timelapsing: {prop}')
         timelapse( (save_fol,prop,fps,dens) )

LG.info('Done!')
