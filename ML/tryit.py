#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import tensorflow as tf
from tensorflow.keras import models
import datetime as dt
import data

import sys
try: f_ini = sys.argv[1]
except IndexError: f_ini = 'rasp_cnn.h5'


C = data.load_run(f_ini)
root = C.root
domains = C.domains
fmodel = C.fmodel
Ndays = C.Ndays
epochs = C.epochs
in_props = C.in_props
out_props = C.out_props
nd = C.nd

now = dt.datetime.now() - dt.timedelta(days=nd)  # to avoid midnight error

# root = '../../../Documents/RASP'
# nd = 7
# domain = 'w2'
# in_props  = ['sfcwindspd', 'sfcwinddir', 'blcloudpct','rain1']
# out_props = ['sfcwindspd', 'sfcwinddir']


model = models.load_model(fmodel)
model.summary()


## Check on un-trained example ##################################################
import results
from random import randint
date = now.replace(hour=randint(7,18))
# date = dt.datetime.now().replace(hour=13)
domain = 'w2'


# Inputs
sc = 'SC2+1'
inp = data.prepare_data(root,domain,sc,date,in_props)
# Outputs
sc = 'SC2'
out = data.prepare_data(root,domain,sc,date,out_props)
# Prediction
predict = model.predict(np.array([ inp ]))
pred = predict[0] #,:,:]

UTCshift = dt.datetime.now()-dt.datetime.utcnow()
UTCshift = dt.timedelta(hours = round(UTCshift.total_seconds()/3600))
tit = ['SfcWind',(date+UTCshift).strftime('%d/%m/%Y-%H:00')]
tit = ' '.join(tit)

fname = fmodel.replace('.h5','') + f'_d-{nd}.png'
results.show_test(inp,out,pred, factor=3.6,vmax=60, title=tit,fname=fname)

