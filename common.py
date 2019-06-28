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
   def __init__(self,Rfolder,bck_img,border,run_days=[],props=[]):
      self.root_folder = Rfolder
      self.bck_img = bck_img
      self.border = border
      self.run_days = run_days
      self.props = props
   def __str__(self):
      msg =  f'Data stored in: {self.root_folder}\n'
      msg += f'Img for background: {self.bck_img}\n'
      msg += f'With perimeter:\n'
      for i in range(len(self.border)):
         P = self.border[i]
         msg += f'  P{i} = {P}\n'
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
   # Background
   border = []
   for P in ['P0','P1','P2','P3']:
      p = config['background'][P].replace(')','').replace('(','')
      border.append( np.array( list(map(float,p.split(',')))) )
   bck_img = config['background']['img']
   run = config['run']['days']
   run = list(map(int,run.split(',')))
   props = [x.strip() for x in config['run']['props'].split(',')]
   return Config(Rfolder,bck_img,border,run,props)

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

if __name__ == '__main__':
   C = load()
   print(C)
   root = C.root_folder
   f = find_data(root,time=dt.datetime(2019,6,23,11,0))
   print(f)
