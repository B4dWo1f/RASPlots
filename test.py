#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from pyproj import Proj

P = Proj(proj='lcc', R=6371200, lat_0=41.0, lat_1=39.872,lon_0=-3.107)

x,y = P(40.0,-3.)
print(x,y)
utmProj = Proj(proj='utm', zone=30, ellps='WGS84')

x,y = utmProj(x,y)
print(x,y)
