#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import datetime as dt
from configparser import ConfigParser, ExtendedInterpolation
from os.path import expanduser
from os import listdir
from os.path import isfile, join
import os
here = os.path.dirname(os.path.realpath(__file__))
import logging
import log_help
LG = logging.getLogger(__name__)
import json


now = dt.datetime.now

class Config(object):
   #def __init__(self,Rfolder,lats,lons,hagl,run_days=[], date='', props=[],
   def __init__(self,Rfolder,Dfolder,Pfolder,lims,background,frunning,Ncores=4,
                     run_days=[], date='', domains=[], props=[],
                     parallel=True,zoom=True,ve=100,path_web='../'):
      """
      Rfolder
      Dfolder
      Pfolder
      lims: limits file containing a json dictionary with the following informtion:
            {lims:    {domian: {sc: [mx,Mx,my,My]}},
             aspects: {domain: {sc: x}}}
      background: bool to re-plot terrain or not
      """
      if Rfolder[-1] == '/': Rfolder = Rfolder[:-1]
      self.root_folder = Rfolder.replace('//','/')
      self.data_folder = Dfolder.replace('//','/')
      self.plot_folder = Pfolder.replace('//','/')
      self.ncores = Ncores
      self.frunning = frunning
      self.background = background
      self.lims_file = lims
      try:
         data = json.load( open(self.lims_file) )
         self.lims = data['lims']
         self.aspect = data['aspects']
      except:
         self.lims = {}
         self.aspect = {}
         self.background = True
      self.run_days = run_days
      self.date = date
      self.domains = domains
      self.props = props
      self.parallel = parallel
      self.zoom = zoom
      self.ve = ve
      self.path_web = path_web
   def __str__(self):
      msg =  f'Data stored in: {self.root_folder}\n'
      msg += f'Terrain files:  {self.lats}  {self.lons}  {self.hagl}\n'
      if len(self.run_days) != 0: msg += f'Run for: {self.run_days}\n'
      if len(self.domains)!=0: msg += 'Domains: ' + ', '.join(self.domains)
      if len(self.props)!=0: msg += 'Properties: ' + ', '.join(self.props)
      return msg

def load(fname='config.ini'):
   """
   Load the config options and return it as a class
   """
   if not os.path.isfile(fname): return None
   config = ConfigParser(inline_comment_prefixes='#')
   config._interpolation = ExtendedInterpolation()
   config.read(fname)
   # System
   Rfolder = expanduser(config['system']['root_folder'])
   Dfolder = expanduser(config['system']['data_folder'])
   Pfolder = expanduser(config['system']['plot_folder'])
   Ncores = int(config['system']['ncores'])
   frunning = expanduser(config['system']['frunning'])
   if not frunning.startswith('/'): frunning = f'{here}/{frunning}'
   # Run
   background = eval(config['run']['plot_background'].capitalize())
   lims = config['run']['lims_aspect']
   if lims[0] in ['.','/']: pass
   else: lims = here + '/'+lims
   try:
      run = eval(config['run']['days'])
      #run = config['run']['days']
      #run = list(map(int,run.split(',')))
   except KeyError: run = []
   try:
      date = config['run']['date']
      date = dt.datetime.strptime(date, '%Y/%m/%d')
   except KeyError: date = dt.datetime.now().date()  # XXX
   #props = [x.strip() for x in config['run']['props'].split(',')]
   domains = eval(config['run']['domains'])
   props = eval(config['run']['props'])
   parallel = eval(config['run']['parallel'].capitalize())
   zoom = eval(config['run']['zoom'].capitalize())
   ve = int(config['plots']['ve'])
   path_web = expanduser(config['fixer']['path_web'])
   if path_web[0] in ['/']: pass
   else: path_web = here +'/'+ path_web
   path_web = os.path.abspath(path_web)
   return Config(Rfolder,Dfolder,Pfolder,lims,background,frunning,Ncores,run,date,domains,props,parallel,zoom,ve, path_web)

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

def find_best_fcst(date,Rfolder,domain):
   for f in ['SC2','SC2+1','SC4+2','SC4+3']:
      fol = f'{Rfolder}/DATA/{domain}/{f}/'+date.strftime('%Y/%m/%d')
      if os.path.isdir(fol): return fol

def listfiles(folder):
   return [join(folder,f) for f in listdir(folder) if isfile(join(folder, f))]

def check_folders(folders):
   for folder in folders:
      LG.warning(f'Creating folder {folder}')
      os.system(f'mkdir -p {folder}')

def callback_error():
   pass

if __name__ == '__main__':
   C = load()
   print(C)
   root = C.root_folder
   f = find_data(root,time=dt.datetime(2019,6,23,11,0))
   print(f)
