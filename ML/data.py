#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from os.path import expanduser
from configparser import ConfigParser, ExtendedInterpolation
import RASPmodels
import numpy as np
import os

norms = {'sfcwindspd':56, 'sfcwinddir':360, 'blcloudpct':100, 'rain1':10}

my_models = {'cnn':RASPmodels.cnn, 'cnn2':RASPmodels.conv2lays,
             'mlp':RASPmodels.mlp}


class ParamsRun(object):
   def __init__(self, data, root, domains, fmodel, Ndays, in_props,
                                                          out_props,
                                                          epochs,
                                                          model,nd):
      self.data = data
      self.root = root
      self.domains = domains
      self.fmodel = fmodel 
      self.Ndays = Ndays 
      self.in_props = in_props 
      self.out_props = out_props 
      self.epochs = epochs
      self.model = model
      self.nd = nd

def sample(root,date,domain,sc,prop):
   """ Get data file """
   d = date.strftime('%Y/%m/%d')
   h = date.hour*100
   return f'{root}/DATA/{domain}/{sc}/{d}/{h:04d}_{prop}.data'

def prepare_data(root,domain,sc,date,props):
   channels = []
   for prop in props:
      f = sample(root,date,domain,sc,prop)
      try: M = np.loadtxt(f, skiprows=4) / norms[prop]
      except OSError: raise #return None
      channels.append( M )
   return np.dstack(channels)

def load_run(fname='run.ini'):
   config = ConfigParser(inline_comment_prefixes='#')
   config._interpolation = ExtendedInterpolation()
   config.read(fname)

   # Data
   data = config['data']
   root = expanduser(data['root'])
   domains = eval(data['domains'])
   fmodel = data['fmodel']
   Ndays = int(data['Ndays'])
   in_props = eval(data['in_props'])
   out_props = eval(data['out_props'])
   epochs = int(data['epochs'])
   # Run
   run = config['run']
   model = my_models[run['model']]
   nd = float(run['nd'])
   return ParamsRun(data,root,domains,fmodel,Ndays,in_props,out_props,epochs,model,nd)
