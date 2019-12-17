#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dense, Flatten, Reshape
import numpy as np


def cnn(size_in,size_out,name='cnn',error='mse'):
   """
   error: mse - mean_squared_error
          mae - mean_absolute_error
   """
   model = models.Sequential(name=name)
   model.add(Conv2D(50, (5,5), activation='relu', input_shape=size_in))
   model.add(MaxPooling2D(5))
   model.add(Conv2D(10, (3,3), activation='relu', input_shape=size_in))
   model.add(MaxPooling2D(2))
   model.add(Flatten())
   model.add(Dense(500, activation='relu'))
   model.add(Dense(np.prod(size_out), activation='relu'))
   model.add(Reshape(target_shape=size_out))
   model.compile(optimizer='adam', metrics=['accuracy'], loss=error)
   return model


def conv2lays(size_in,size_out,name='cnn2',error='mse'):
   """
   error: mse - mean_squared_error
          mae - mean_absolute_error
   """
   model = models.Sequential(name=name)
   model.add(Conv2D(30, (17,17), activation='relu', input_shape=size_in))
   model.add(MaxPooling2D(2))
   model.add(Conv2D(10, (10,10), activation='relu', input_shape=size_in))
   model.add(MaxPooling2D(2))
   model.add(Flatten())
   model.add(Dense(600, activation='relu'))
   model.add(Dense(np.prod(size_out), activation='relu'))
   model.add(Reshape(target_shape=size_out))
   model.compile(optimizer='adam', metrics=['accuracy'], loss=error)
   return model


def mlp(size_in,size_out,name='MLP',error='mae'):
   """
   error: mse - mean_squared_error
          mae - mean_absolute_error
   """
   model = models.Sequential(name=name)
   model.add(Flatten(input_shape=size_in))
   # model.add(Dense(500, activation='relu'))
   model.add(Dense(1000, activation='relu'))
   model.add(Dense(np.prod(size_out), activation='relu', input_shape=size_in))
   model.add(Reshape(target_shape=size_out))
   model.compile(optimizer='adam', metrics=['accuracy'], loss=error)
   return model
