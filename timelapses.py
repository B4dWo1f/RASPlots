#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
from random import shuffle
################################## LOGGING #####################################
import logging
import log_help
log_file = here+'/'+'.'.join( __file__.split('/')[-1].split('.')[:-1] ) + '.log'
lv = logging.INFO
logging.basicConfig(level=lv,
                 format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                 datefmt='%Y/%m/%d-%H:%M',
                 filename = log_file, filemode='w')
LG = logging.getLogger('main')
log_help.screen_handler(LG, lv=lv)
################################################################################
import datetime as dt
import layers as L
import common

C = common.load(here+'/full.ini')
if C == None:
   LG.critical('No full.ini')
   exit()

UTCshift = dt.datetime.now()-dt.datetime.utcnow()
UTCshift = dt.timedelta(hours = round(UTCshift.total_seconds()/3600))

## Curate properties
root_folder = C.plot_folder
## Sort properties to plot
# unify wind
props = C.props
winds = [p for p in C.props if 'wind' in p]
winds = [p.replace('winddir','wind') for p in winds]
winds = [p.replace('windspd','wind') for p in winds]
winds = sorted(list(set(winds)))   # XXX Dangerous
rest = [p for p in C.props if 'wind' not in p]
# remove masks
rest = [p for p in rest if 'dif' not in p]
try: 
   rest.remove('mslpress')
   rest.remove('blcloudpct')
   rest.remove('hwcrit')
   rest.remove('dwcrit')
except: pass
props = winds+rest
props = sorted(set(props))

SCs = {0:'SC2', 1:'SC2+1', 2:'SC4+2', 3:'SC4+3'}


all_inps = []
for dom in ['w2']:    # C.domains:
   for fscalar in props:
      if 'wind' in fscalar: fvector = fscalar
      else: fvector = 'sfcwind'
      for isc in C.run_days:
         sc = SCs[isc]
         if C.parallel: all_inps.append( (root_folder,dom,sc,fscalar,fvector,UTCshift) )
         else:
            vid = L.make_timelapse((root_folder,dom,sc,fscalar,fvector,UTCshift))

shuffle(all_inps)
if C.parallel:
   import multiprocessing as sub
   pool = sub.Pool(4)
   Res = pool.map(L.make_timelapse, all_inps)

