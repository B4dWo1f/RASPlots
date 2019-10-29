#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
import datetime as dt
import common
import json
import layers as L
import matplotlib.pyplot as plt

C = common.load(here+'/full.ini')

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



#def super_plot(args):
#   hora,prop,Dfolder, curr_date, Pfolder, domain, sc, hora, prop,l,a = args
#   if 'wind' in prop: func = L.all_vector
#   else: func = L.all_scalar
#   func(Dfolder, curr_date, Pfolder, domain, sc, hora, prop,l,a)

parallel = True
from tqdm import tqdm
for domain in C.domains:
   print('-->',domain)
   for isc in tqdm(C.run_days):
      curr_date = now + dt.timedelta(days=isc)
      sc = SCs[isc]
      print('  -->',sc)
      if C.background:
         l,a = L.all_background_layers(C.plot_folder, domain, sc)
         C.lims[domain]   = {sc: l}
         C.aspect[domain] = {sc: a}
      else: l,a = C.lims[domain][sc], C.aspect[domain][sc]
      all_inputs = []
      for hora in range(8,19):
         for prop in props:
            inps = [hora,prop,C.data_folder, curr_date, C.plot_folder, domain,
                    sc, f'{100*hora:04d}', prop,l,a]
            if parallel: all_inputs.append(inps)
            else: L.super_plot(inps)
      if parallel:
         print('parallel launch')
         Res = pool.map(L.super_plot, all_inputs)




         #Res = pool.map(f,range(8))
if C.background:
   print('here')
   print(C.lims)
   print(C.aspects)
   print(type(C.lims))
   print(type(C.aspects))
   json.dump( {'lims':C.lims,'aspects':C.aspect}, open( C.lims, 'w' ) )
