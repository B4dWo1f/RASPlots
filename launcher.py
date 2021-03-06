#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import common
import os
here = os.path.dirname(os.path.realpath(__file__))
is_cron = os.getenv('RUN_BY_CRON')
import datetime as dt
full = here+'/full.ini'

os.system(f'rm {full} 2> /dev/null')

import re
from urllib.request import Request, urlopen
from urllib.error import URLError
from configparser import ConfigParser, ExtendedInterpolation
import subprocess as sub
from time import sleep,time
################################## LOGGING #####################################
import logging
import log_help
log_file = here+'/'+'.'.join( __file__.split('/')[-1].split('.')[:-1] ) + '.log'
lv = logging.INFO
logging.basicConfig(level=lv,
                 format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                 datefmt='%Y/%m/%d-%H:%M',
                 filename = log_file, filemode='w')
LG = logging.getLogger('main')
if not is_cron: log_help.screen_handler(LG, lv=lv)
LG.info(f'Starting: {__file__}')
################################################################################


def make_request(url):
   """ Make http request """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   out = False
   while not out:
      try:
         html = urlopen(req)
         out = True
      except URLError:
         LG.error(f'URLError: {url}')
         out = False
   html_doc = html.read()
   try: html_doc = html_doc.decode(html.headers.get_content_charset())
   except TypeError: html_doc = html_doc.decode()
   return html_doc


def get_latest_run(url):
   """ Check time of latest runs from Oriol's RASP """
   html_doc = make_request(url)

   p = r'([ ^\w ]*) (\S+) ([ ^\w ]*) (\S+)\: (\S+)\:'
   p += r' (\S+) - (\S+) = (\S+) (\w+)'
   n=50

   html_doc = html_doc.splitlines()
   html_doc.reverse()

   for l in html_doc:
      try:
         m = re.search(p, l)
         wday,day,month,year,st,Hstart,Hend,dur,unit = m.groups()
         date = dt.datetime.strptime(' '.join([day,month,year]),'%d %b %Y')
         tstart = dt.datetime.strptime(Hstart,'%H:%M').time()
         tend = dt.datetime.strptime(Hend,'%H:%M').time()
         start = dt.datetime.combine(date, tstart)
         end = dt.datetime.combine(date, tend)
         return end
      except AttributeError: pass
   LG.critical('Unable to get last run')   #TODO
   return None


C = common.load(here+'/template.ini')

# frunning = f'{here}/RUNNING'
if os.path.isfile(C.frunning):
   LG.critical('Already running')
   exit()
dummy = open(C.frunning,'w')

SCs = ['SC2','SC2+1','SC4+2','SC4+3']
twait = 7   # minutes to check for new data
toffset = twait # the reported time accounts only for WRF, toffset estimates
                # the delay required for NCL to make the plots and data files

# Look for days to run
run_days = []
for i in range(len(SCs)):
   sc = SCs[i]
   LG.info(f'Checking fodler {sc}')
   url = f'http://raspuri.mooo.com/RASP/{sc}/FCST/gridcalctimes.txt'
   end = get_latest_run(url)
   try:
      last_plot = open(f'{here}/{sc}.time','r').read().strip()
      last_plot = dt.datetime.strptime(last_plot,'%d/%m/%Y-%H:%M')
   except FileNotFoundError:
      LG.info(f"last update file '{here}/{sc}.time' not found")
      last_plot = dt.datetime.now() - dt.timedelta(days=20)
   LG.info(f"last update {end.strftime('%d/%m/%Y %H:%M')}")
   LG.info(f"last plot {last_plot.strftime('%d/%m/%Y %H:%M')}")

   if (last_plot-end).total_seconds() < toffset*60: run_days.append(i)

if len(run_days) == 0:
   LG.info(f'No new data, skipping')
   #told = time()
   #while time()-told < twait*60 and not os.path.isfile('STOP'):
   #   sleep(0.5)
   LG.info('Done!')
   exit()
else: LG.info(f'New data in ' + ','.join([SCs[i] for i in run_days]))

# Save ini file for next run
config = ConfigParser(inline_comment_prefixes='#')
config._interpolation = ExtendedInterpolation()
config.read(here+'/template.ini')
config['run']['days'] = str(run_days)

with open(full, 'w') as configfile:
   config.write(configfile)

### Launch processes
## Data
#LG.info('Running data')
#p = sub.run(here+'/data.py', stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
#out = p.stdout.decode('utf-8').strip()
#err = p.stderr.decode('utf-8').strip()
#if err != '':
#   LG.critical('Error running data.py:')
#   LG.critical(err)
#
## Ploter
#LG.info('Running ploter')
#p = sub.run(here+'/ploter.py', stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
#out = p.stdout.decode('utf-8').strip()
#err = p.stderr.decode('utf-8').strip()
#if err != '':
#   LG.critical('Error running ploter.py:')
#   LG.critical(err)
#
### Davinci
##LG.info('Running davinci')
##p = sub.run(here+'/davinci.py', stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
##out = p.stdout.decode('utf-8').strip()
##err = p.stderr.decode('utf-8').strip()
##if err != '':
##   LG.critical('Error running davinci.py:')
##   LG.critical(err)
##
### Timelapses
##LG.info('Running timelapses')
##p = sub.run(here+'/timelapses.py', stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
##out = p.stdout.decode('utf-8').strip()
##err = p.stderr.decode('utf-8').strip()
##if err != '':
##   LG.critical('Error running davinci.py:')
##   LG.critical(err)
#
LG.info('Done!')
#os.system(f"rm {run_file}")
dummy.close()
