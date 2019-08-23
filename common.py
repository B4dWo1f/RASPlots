#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import datetime as dt
from configparser import ConfigParser, ExtendedInterpolation
from os.path import expanduser
import os
here = os.path.dirname(os.path.realpath(__file__))

now = dt.datetime.now

class Config(object):
   def __init__(self,Rfolder,lats,lons,hagl,run_days=[], date='', props=[]):
      if Rfolder[-1] != '/': Rfolder += '/'
      self.root_folder = Rfolder
      self.lats = lats
      self.lons = lons
      self.hagl = hagl
      self.run_days = run_days
      self.date = date
      self.props = props
   def __str__(self):
      msg =  f'Data stored in: {self.root_folder}\n'
      msg += f'Terrain files:  {self.lats}  {self.lons}  {self.hagl}\n'
      if len(self.run_days) != 0: msg += f'Run for: {self.run_days}\n'
      if len(self.props) != 0: msg += 'Properties: ' + ', '.join(self.props)
      return msg

def load(fname='config.ini'):
   """
   Load the config options and return it as a class
   """
   config = ConfigParser(inline_comment_prefixes='#')
   config._interpolation = ExtendedInterpolation()
   config.read(fname)
   # System
   Rfolder = expanduser(config['system']['root_folder'])
   ## Background
   lats = config['background']['lats']
   lons = config['background']['lons']
   hagl = config['background']['hagl']
   try:
      run = config['run']['days']
      run = list(map(int,run.split(',')))
   except KeyError: run = []
   try:
      date = config['run']['date']
      date = dt.datetime.strptime(date, '%Y/%m/%d')
   except KeyError: date = dt.datetime.now()  # XXX
   props = [x.strip() for x in config['run']['props'].split(',')]
   return Config(Rfolder,lats,lons,hagl,run,date,props)

def find_data(root='../../Documents/RASP/',data='DATA',grid='w2',time=now()):
   if root[-1] != '/': root += '/'
   fcst_time = time.replace(minute=0,second=0,microsecond=0)
   if fcst_time.date() == now().date(): fol = 'SC2'
   elif fcst_time.date() == now().date() + dt.timedelta(days=1): fol = 'SC2+1'
   elif fcst_time.date() == now().date() + dt.timedelta(days=2): fol = 'SC4+2'
   elif fcst_time.date() == now().date() + dt.timedelta(days=3): fol = 'SC4+3'
   else:
      if fcst_time.date() < now().date(): fol = 'SC2'  # for past forecasts
      else:
         print('Not available')
         return None
   root_folder = root + data+'/'+grid+'/'+fol
   return root_folder+'/'+fcst_time.strftime('%Y/%m/%d/%H%M_')

def find_best_fcst(date,Rfolder):
   for f in ['SC2','SC2+1','SC4+2','SC4+3']:
      fol = Rfolder+'DATA/w2/'+f+'/'+date.strftime('%Y/%m/%d')
      if os.path.isdir(fol): return fol

if __name__ == '__main__':
   C = load()
   print(C)
   root = C.root_folder
   f = find_data(root,time=dt.datetime(2019,6,23,11,0))
   print(f)
