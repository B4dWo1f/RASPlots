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
import common
import json
import layers as L
import matplotlib.pyplot as plt

C = common.load(here+'/full.ini')
if C == None:
   print('HEREEE')
   LG.critical('No full.ini')
   exit()

UTCshift = dt.datetime.now()-dt.datetime.utcnow()
UTCshift = dt.timedelta(hours = round(UTCshift.total_seconds()/3600))

## Curate properties
# Sort properties to plot
props = C.props
winds = [p for p in C.props if 'wind' in p]
winds = [p.replace('winddir','wind') for p in winds]
winds = [p.replace('windspd','wind') for p in winds]
winds = sorted(list(set(winds)))   # XXX Dangerous
rest = [p for p in C.props if 'wind' not in p]
props = winds+rest



now = dt.datetime.now() - dt.timedelta(hours=5)
today = now.date()

import multiprocessing as sub
pool = sub.Pool(4)


SCs = {0:'SC2', 1:'SC2+1', 2:'SC4+2', 3:'SC4+3'}


parallel = True
from tqdm import tqdm
from random import shuffle
LG.info(f'Plot Background: {C.background}')
for isc in tqdm(C.run_days):
   sc = SCs[isc]
   LG.info(f'Plotting day: {sc}')
   for domain in C.domains:
      LG.info(f'Plotting domain: {domain}')
      curr_date = now + dt.timedelta(days=isc)
      com = f'mkdir -p {C.plot_folder}/{domain}/{sc}'
      LG.warning(com)
      os.system(com)
      if C.background:
         l,a = L.all_background_layers(C.plot_folder, domain, sc)
         try:
            C.lims[domain][sc] = l
            C.aspect[domain][sc] = a
         except KeyError:
            C.lims[domain]   = {sc: l}
            C.aspect[domain] = {sc: a}
      else: l,a = C.lims[domain][sc], C.aspect[domain][sc]
      all_inputs = []
      for hora in range(8,20):           # local time
         hour = dt.datetime.now().replace(hour=hora,minute=0)
         hour -= UTCshift          # UTC time
         for prop in props:
            inps = [hour,prop,C.data_folder, curr_date, C.plot_folder, domain,
                    sc, prop,l,a]
            if parallel: all_inputs.append(inps)
            else: L.super_plot(inps)
      if parallel:
         shuffle(all_inputs)
         Res = pool.map(L.super_plot, all_inputs)

   D = curr_date.strftime('%d/%m/%Y')
   now1 = dt.datetime.now().strftime('%d/%m/%Y-%H:%M')
   #LG.debug(f"Last plot for {D}: {now}")
   LG.info(f'last plot for {SCs[isc]}: {here}/{SCs[isc]}.time')
   with open(here+'/'+SCs[isc]+'.time','w') as myf:
      myf.write(f'{now1}\n')

LG.info('Done!')
if C.background:
   LG.info('Update lims file')
   json.dump( {'lims':C.lims,'aspects':C.aspect}, open( C.lims_file, 'w' ) )
