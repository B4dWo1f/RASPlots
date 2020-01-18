#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
try: f_ini = sys.argv[1]
except IndexError:
   print('File not specified')
   exit()

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dense, Flatten, Reshape
from tensorflow.keras.callbacks import ModelCheckpoint
import RASPmodels
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime as dt
from random import shuffle
from tqdm import tqdm
import data


C = data.load_run(f_ini)
root = C.root
domains = C.domains
fmodel = C.fmodel
Ndays = C.Ndays
epochs = C.epochs
nd = C.nd

now = dt.datetime.now() - dt.timedelta(days=nd)  # to avoid midnight error


start = now - dt.timedelta(days=Ndays)
dates = [start+dt.timedelta(days=i) for i in range(Ndays)]
hours = list(range(7,19))
in_props  = C.in_props   #['sfcwindspd', 'sfcwinddir'] #, 'blcloudpct', 'rain1']
out_props = C.out_props  #['sfcwindspd', 'sfcwinddir']



# Prepare training data files
print('Preparing input/output data')
inputs,outputs,dates_train = [],[],[]
for d in tqdm(dates):
   for domain in domains:
      for h in hours:
         date = d.replace(hour=h)
         try:
            # Inputs
            sc = 'SC2+1'
            Min = data.prepare_data(root,domain,sc,date,in_props)
            # Outputs
            sc = 'SC2'
            Mout = data.prepare_data(root,domain,sc,date,out_props)
            inputs.append(Min)
            outputs.append(Mout)
            dates_train.append(date)
         except: continue
inputs  = np.array(inputs)
outputs = np.array(outputs)

md = min(dates_train)
Md = max(dates_train)

print(md.strftime('%d/%m/%Y-%H:%M'),' --> ',Md.strftime('%d/%m/%Y-%H:%M'))
print(inputs.shape)
print(outputs.shape)


if True:
   print('Shuffling')
   inds = list(range(len(inputs)))
   shuffle(inds)
   inputs = inputs[inds]
   outputs = outputs[inds]


size_in   = inputs[0].shape
size_out  = outputs[0].shape

## Load or Create Model #########################################################
try:
   model = models.load_model(fmodel)
   print(f'\nLoaded Model: {model.name} ({fmodel})')
except OSError:
   print('\n******** Starting new Model ********')
   model = C.model(size_in, size_out)
model.summary()


## Train ########################################################################
print('Starting training')
# fmodel_tmp = fmodel.replace('.h5','_tmp.h5')
# callback = ModelCheckpoint(fmodel_tmp, monitor='accuracy', save_best_only=True,
#                                                            save_freq= 'epoch')

class StopOnConvergence(tf.keras.callbacks.Callback):
   """
   Stops training if the std of the loss in the last N epochs is < threshold
   of if a file STOP is present in the folder
   """
   def __init__(self,N=30,threshold=0.05):
      self.N = N
      self.thres = threshold
      self.loss = []
   def on_epoch_end(self, epoch, logs={}):
      #N = self.N
      #thres = self.thres
      #self.loss.append(logs.get('loss'))
      #self.loss = self.loss[int(-1.2*N):]
      #if len(self.loss) > N:
      #   std = np.std(self.loss[-N:])
      #   print('*********************')
      #   print(self.loss[-N:])
      #   print(f'loss std: {std}\n')
      #   print('*********************')
      #   if std < thres:
      #      print('\n\nConvergence achieved?\n\n')
      #      self.model.stop_training = True
      if os.path.isfile('STOP'): self.model.stop_training = True

history = model.fit(inputs, outputs, validation_split=0.1,
                                     epochs=epochs, verbose=2,
                                     callbacks=[StopOnConvergence(50,0.001)])

M = np.column_stack([history.history['loss'], history.history['val_loss']])
Nover = len(os.popen(f'ls overfit*.dat 2> /dev/null').read().strip().splitlines())
np.savetxt(f'overfit{Nover}.dat',M,fmt='%.7f')

model.save(fmodel)
# os.system(f'rm {fmodel_tmp}')


# Plot history
err = history.history['loss']
val_err = history.history['val_loss']
acc = history.history['accuracy']
fig, ax = plt.subplots()
ax1 = ax.twinx()
ax.plot(err,'C0',label='loss')
ax.plot(val_err,'C0--',label='val_loss')
ax1.plot(acc,'C1',label='accuracy')
ax1.tick_params(axis='y', labelcolor='C1')
ax.set_ylabel('Loss')
ax1.set_ylabel('Acc')
# plt.show()


## Check on un-trained example ##################################################
print()
import results
from random import randint
date = now.replace(hour=randint(9,17))
date = dt.datetime.now().replace(hour=17)
domain = 'w2'


# Inputs
sc = 'SC2+1'
inp = data.prepare_data(root,domain,sc,date,in_props)
# Outputs
sc = 'SC2'
out = data.prepare_data(root,domain,sc,date,out_props)
# Prediction
predict = model.predict(np.array([ inp ]))
pred = predict[0]

UTCshift = dt.datetime.now()-dt.datetime.utcnow()
UTCshift = dt.timedelta(hours = round(UTCshift.total_seconds()/3600))
tit = ['SfcWind',(date+UTCshift).strftime('%d/%m/%Y-%H:00')]
tit = ' '.join(tit)

fname = fmodel.replace('.h5','.png')
results.show_test(inp,out,pred, factor=3.6,vmax=60, title=tit,fname=fname)

