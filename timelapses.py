#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
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
# Sort properties to plot
props = C.props
winds = [p for p in C.props if 'wind' in p]
winds = [p.replace('winddir','wind') for p in winds]
winds = [p.replace('windspd','wind') for p in winds]
winds = sorted(list(set(winds)))   # XXX Dangerous
rest = [p for p in C.props if 'wind' not in p]
props = winds+rest
props = [p.replace('dif','') for p in props]
props.remove('mslpress')
props.remove('blcloudpct')
# props = [p for p in props if 'wind' in p]


SCs = {0:'SC2', 1:'SC2+1', 2:'SC4+2', 3:'SC4+3'}


for isc in C.run_days:
   sc = SCs[isc]
   for dom in ['w2']:    # C.domains:
      for fscalar in props:
         if 'wind' in fscalar: fvector = fscalar
         else: fvector = 'sfcwind'
         vid = L.make_timelapse(root_folder,dom,sc,fscalar,fvector,UTCshift)
