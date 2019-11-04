#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
here = os.path.dirname(os.path.realpath(__file__))
import datetime as dt
import common

C = common.load(here+'/full.ini')
if C == None:
   #LG.critical('No full.ini')
   exit()

SCs = ['SC2', 'SC2+1', 'SC4+2', 'SC4+3']
domains = ['w2', 'd2']

valid_dates = {}
for sc in SCs:
   valid_dates[sc] = {}
   for domain in domains:
      fname = f"{C.plot_folder}/{domain}/{sc}/valid_date.txt"
      try: date = open(fname,'r').read().strip()
      except: date = ""
      date = dt.datetime.strptime(date,'%d/%m/%Y')
      date = date.strftime('%m/%d/%Y')
      valid_dates[sc][domain] = f"new Date('{date}')"

new_string = f'var valid_dates = {valid_dates};\n'.replace('"','')

fname = f'{C.path_web}/js/valid_dates.js'
with open(fname, "w") as f:
    f.writelines(new_string)
print('fixer Done!')
