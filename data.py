#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import common
import random
import string
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import datetime as dt
import os
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
################################## LOGGING #####################################
import logging
import log_help
lv = logging.INFO
logging.basicConfig(level=lv,
                 format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                 datefmt='%Y/%m/%d-%H:%M:%S',
                 filename = here+'/data.log', filemode='w')
LG = logging.getLogger('main')
log_help.screen_handler(LG, lv=lv)
LG.info(f'Starting: {__file__}')
################################################################################


def make_request(url):
   """ Make http request """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   html_doc = urlopen(req)
   html_doc= html_doc.read()
   return html_doc

def randomString(stringLength=10):
   """Generate a random string of fixed length """
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(stringLength))

import re
def get_and_place(url,base='RASP'):
   sc = url.split('/')[4]
   ftemp = '/tmp/'+ randomString(5) + '.data'  #'/tmp/temporal.data'
   urlretrieve(url, ftemp)
   date = open(ftemp,'r').read().strip().splitlines()[3]
   pattern = r'Day= ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ValidLST= ([ ^\W\w\d_ ]*) ([ ^\W\w\d_ ]*) ValidZ= ([ ^\W\w\d_ ]*) Fcst= ([ ^\W\w\d_ ]*)'
   match = re.search(pattern, date)
   year, month, day, _, hour, tz, validz,_ = match.groups()
   t = [year, month, day, hour]
   valid_date = dt.datetime.strptime(' '.join(t),'%Y %m %d %H%M')
   #XXX Manual offset for UTC
   offset = {'CES':2, 'CET':1}   # hours
   UTCshift_manual = dt.timedelta(hours=offset[tz])
   UTCshift = dt.datetime.now()-dt.datetime.utcnow()
   UTCshift = dt.timedelta(hours = round(UTCshift.total_seconds()/3600))
   if UTCshift != UTCshift_manual: # in order to be in sync with Oriol
      LG.critical(f'UTC shift is wrong [{sc}, {valid_date.date()}]')
      UTCshift = UTCshift_manual
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
   LG.debug('saved %s'%('/'.join(fname.split('/')[-7:])))

if __name__ == '__main__':
   from threading import Thread

   C = common.load(here+'/full.ini')
   if C == None:
      LG.critical('No full.ini')
      exit()

   fol = C.root_folder
   props = C.props
   domains = C.domains
   LG.info(f'Storing data in {fol}')
   LG.info( 'Downloading ' + ', '.join([str(p) for p in props]) )

   if fol[-1] == '/': fol = fol[:-1]

   folder_index = {0:'SC2', 1:'SC2+1', 2:'SC4+2', 3:'SC4+3'}
   sounding_index= {'arcones': 1, 'bustarviejo': 2, 'cebreros': 3, 'abantos': 4,
                    'piedrahita': 5, 'pedro bernardo': 6, 'lillo': 7,
                    'fuentemilanos': 8, 'candelario': 10, 'pitolero': 11,
                    'pegalajar': 12,'otivar': 13}

   def bring(f):
      LG.info(f'Going for {f}')
      url = 'http://raspuri.mooo.com/RASP/%s/FCST/'%(f)
      LG.debug(f'Downloading from {url}')
      html_doc = make_request(url)
      S = BeautifulSoup(html_doc, 'html.parser')
      table = S.find('table')
      data_files,soundings,cape = [],[],[]
      all_rows = table.find_all('tr')[3:-1]
      for irow in range(len(all_rows)):
         row = all_rows[irow]
         col = row.find_all('td')[1]
         l = col.find('a')
         l = l['href']
         if '.data' == l[-5:]:
            if 'curr' in l:
               if l.split('.')[0] in props:
                  for domain in domains:
                     if domain in l: get_and_place(url+l, fol)
                  else: pass
         if irow%(len(all_rows)//10) == 0:
            LG.info(f'{f}: {int(100*irow/len(all_rows))}% done')

   tday = dt.datetime.now().date()
   folders = [folder_index[x] for x in C.run_days]

   threads = []
   for f in folders:
      if C.parallel:
         T = Thread(target=bring, args=[f])
         T.start()
         threads.append(T)
      else: bring(f)
   for T in threads:
      T.join()
   LG.info('Done!')
