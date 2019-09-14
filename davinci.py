#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import datetime as dt
import multiprocessing as sub
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
import common
import plots


C = common.load(here+'/full.ini')

#C.date = dt.datetime.now() - dt.timedelta(hours = 5)

UTCshift = round((dt.datetime.now()-dt.datetime.utcnow()).total_seconds()/3600)
LG.info(f'UTCshift: {UTCshift}')

all_hour = ['%02d:00'%(i) for i in range(6,18)]

for day in C.run_days:
   date_run = C.date + day*dt.timedelta(days=1)
   LG.info(f"Plotting {date_run.strftime('%d/%m/%Y')}")

   if C.parallel:
      LG.debug('Running in parallel')
      all_inputs = []
      ck = True
      for hora in all_hour:
         all_inputs.append( (C, date_run, hora, UTCshift, C.ve, C.zoom, ck) )
         ck = False
      pool = sub.Pool(2)
      Res = pool.map(plots.plot_all_properties, all_inputs)
   else:
      ck = True
      for hora in all_hour:
         LG.info(f"Plotting {date_run.strftime('%d/%m/%Y-%H:%M')}")
         plots.plot_all_properties((C,date_run,hora,UTCshift,C.ve, C.zoom, ck))
         ck = False

   props = list(set([x.replace('spd','').replace('dir','') for x in C.props]))

LG.info('Done!')
