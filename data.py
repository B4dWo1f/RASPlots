#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import common
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import datetime as dt
import os
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')


def make_request(url):
   """ Make http request """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   html_doc = urlopen(req)
   html_doc= html_doc.read()
   return html_doc

import re
def get_and_place(url,base='RASP'):
   ftemp = '/tmp/temporal.data'
   urlretrieve(url, ftemp)
   date = open(ftemp,'r').read().strip().splitlines()[3]
   pattern = r'Day= ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ValidLST= ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ValidZ= ([ ^\W\w\d_ ]*) Fcst= ([ ^\W\w\d_ ]*)'
   match = re.search(pattern, date)
   year, month, day, _, hour, tz, validz,_ = match.groups()
   t = [year, month, day, hour]
   valid_date = dt.datetime.strptime(' '.join(t),'%Y %m %d %H%M')
   #XXX Manual offset for UTC
   offset = {'CES':2*3600, 'DST':3600}   # seconds
   UTCshift = dt.timedelta(seconds=offset[tz])
   valid_date = valid_date - UTCshift

   # http://raspuri.mooo.com/RASP/SC2/FCST/cape.curr.0800lst.w2.data
   # $RASP/DATA/W2/SC2/FCST/2019/05/24/0800_cape.data
   path = '/'.join(url.split('/')[3:-1]) + '/'
   path += '/'.join(url.split('/')[-1].split('.'))
   pattern = r'RASP/([ ^\W\w\d_ ]*)/FCST/([ ^\W\w\d_ ]*)/([ ^\W\w\d_ ]*)/([ ^\W\w\d_ ]*)/([ ^\W\w\d_ ]*)/data'
   match = re.search(pattern, path)
   time,prop,_,_,domain = match.groups()
   date = valid_date.strftime('%Y/%m/%d/%H%M')
   fname = f'{base}/DATA/{domain}/{time}/{date}_{prop}.data'
   com = 'mkdir -p '+'/'.join(fname.split('/')[:-1])
   os.system(com)
   os.rename(ftemp, fname)

if __name__ == '__main__':
   C = common.load(here+'/config.ini')

   fol = C.root_folder
   props = C.props
   if fol[-1] == '/': fol = fol[:-1]

   folder_index = {0:'SC2', 1:'SC2+1', 2:'SC4+2', 3:'SC4+3'}
   sounding_index= {'arcones': 1, 'bustarviejo': 2, 'cebreros': 3, 'abantos': 4,
                    'piedrahita': 5, 'pedro bernardo': 6, 'lillo': 7,
                    'fuentemilanos': 8, 'candelario': 10, 'pitolero': 11,
                    'pegalajar': 12,'otivar': 13}

   tday = dt.datetime.now().date()
   folders = [folder_index[x] for x in C.run_days]

   #props = ['sfcwindspd','sfcwinddir','cape','blcloudpct']
   # + [f'sounding{i}' for i in range(15)]
   for f in folders:
      print('Going for',f)
      url = 'http://raspuri.mooo.com/RASP/%s/FCST/'%(f)
      html_doc = make_request(url)
      S = BeautifulSoup(html_doc, 'html.parser')
      table = S.find('table')
      data_files,soundings,cape = [],[],[]
      for row in table.find_all('tr')[3:-1]:
         col = row.find_all('td')[1]
         l = col.find('a')
         l = l['href']
         if '.data' == l[-5:]:
            if 'curr' in l:
               if l.split('.')[0] in props:
                  if '.w2.' in l: get_and_place(url+l, fol)
                  else: pass
