#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

def interp(x,x0,x1,y0,y1):
   """
   Linear interpolation for polar quantity
   y0,y1 in degrees
   returns degrees
   """
   return (y0*(x1-x)-y1*(x0-x))/(x1-x0)

def interp_pol(x,x0,x1,y0,y1):
   """
   Linear interpolation for polar quantity
   y0,y1 in degrees
   returns degrees
   """
   Y0 = np.sin(np.radians(y0))
   Y1 = np.sin(np.radians(y1))
   return np.degrees(np.arcsin((Y0*(x1-x)-Y1*(x0-x))/(x1-x0)))

def mean(*vecs):
   """
   Makes a polar average. vecs should be a list of vectors to average:
   average = mean(vec1, vec2, vec3,...)
   """
   avg = np.mean([np.sin(np.radians(V)) for V in vecs])
   return np.degrees(np.arcsin(avg))

d = '2019/07/05/12:30'
R = '../../Documents/RASP/DATA/w2/SC2/'
date_fcst = dt.datetime.strptime(d,'%Y/%m/%d/%H:%M')

X = np.load('sc2_lons.npy')
Y = np.load('sc2_lats.npy')
mx,Mx = np.min(X),np.max(X)
my,My = np.min(Y),np.max(Y)
x = np.linspace(mx,Mx,X.shape[1])
y = np.linspace(my,My,X.shape[0])

date0 = date_fcst.replace(minute=0)
date1 = date_fcst.replace(hour=date_fcst.hour+1,minute=0)

S0 = np.loadtxt(R+date0.strftime('%Y/%m/%d/%H00_sfcwindspd.data'),skiprows=4)
D0 = np.loadtxt(R+date0.strftime('%Y/%m/%d/%H00_sfcwinddir.data'),skiprows=4)
U0 = -S0*np.sin(np.radians(D0))
V0 = -S0*np.cos(np.radians(D0))

S1 = np.loadtxt(R+date1.strftime('%Y/%m/%d/%H00_sfcwindspd.data'),skiprows=4)
D1 = np.loadtxt(R+date1.strftime('%Y/%m/%d/%H00_sfcwinddir.data'),skiprows=4)
U1 = -S1*np.sin(np.radians(D1))
V1 = -S1*np.cos(np.radians(D1))

T = np.linspace(0,1,101)
lim = 40
#for i in range(len(T)):
#   t = round(T[i],2)
for t in [0.25, 0.5, 0.75]:
   delta = date1 - date0
   print('Curr time:',date0+delta*t)
#   S = interp(t,0,1,S0,S1)
#   D = interp_pol(t,0,1,D0,D1)
#   U = -S*np.sin(np.radians(D))
#   V = S*np.cos(np.radians(D))
#   fig, ax = plt.subplots()
#   ax.streamplot(x,y, U,V, color='k',linewidth=1., density=3.5,
#                              arrowstyle='->',arrowsize=5,
#                              zorder=12)
#   ax.contourf(X,Y,S, levels=range(0,lim,4), extend='max',
#                   antialiased=True,
#                   cmap='Paired',
#                   vmin=0, vmax=lim,
#                   zorder=10,alpha=0.3)
#   ax.set_title('t=%s'%(t))
#   fig.savefig('/tmp/test_%s.png'%(i))
#   plt.close('all')
