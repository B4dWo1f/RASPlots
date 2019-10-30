#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt

def header():
   html = '<html lang="en">\n<head>'
   html += '  <meta charset="utf-8">\n'
   html += '  <title>DNN RASP Sistema Central</title>\n'
   html += '  <meta name="description" content="RASPuri">\n'
   html += '  <meta name="author" content="SitePoint">\n'
   html += '  <link rel="stylesheet" href="css/styles.css?v=1.0">\n'
   html += '</head>\n'
   return html

def html_image(url,domain,prop,hour,sc,w0=1000):
   sz = {'w2':{'SC2':  (w0,w0*666.666/1000), 'SC2+1':(w0,w0*666.666/1000),
               'SC4+2':(w0,w0*863.724/1000), 'SC4+3':(w0,w0*863.723/1000)},
         'd2':{'SC2':  (w0,w0*0.8), 'SC2+1':(w0,w0*0.8),
               'SC4+2':(w0,w0*0.8), 'SC4+3':(w0,w0*0.8)}}
   #sz = {'SC2':  (1000,666.666), 'SC2+1':(1000,666.666),
   #      'SC4+2':(1000,863.724), 'SC4+3':(1000,863.723)}
   resol = {'A':(w0,w0*1000/1325),'B':(w0,w0*900/1420),'C':(w0,w0*900/1565)}
   html = f'   <p align="center">\n'
   if len(z) == 0:  # full map
      html += f'   <img src="{url}" alt="{prop} {hour}" width="{sz[domain][sc][0]}" height="{sz[domain][sc][1]}" align="center" usemap="#zones">\n'
      html += f'   <map name="zones">\n'
      html += f'      <area shape="rect" coords="670,45,980,345"  href="/{domain}/{sc}/A/{prop}_{hour}.html" alt="Arcones">\n'
      html += f'      <area shape="rect" coords="450,250,800,500" href="/{domain}/{sc}/B/{prop}_{hour}.html" alt="Cebreros">\n'
      html += f'      <area shape="rect" coords="100,300,600,593" href="/{domain}/{sc}/C/{prop}_{hour}.html" alt="Pedro bernardo">\n'
      html += f'   </map>\n'
   else:
      w,h = resol[z]
      html += f'   <img src="../{url}" alt="{prop} {hour}" width="{w}" height="{h}" align="center" usemap="#zones">\n'
      html += f'   <map name="zones">\n'
      html += f'      <area shape="rect" coords="0,0,1056,627"  href="../{prop}_{hour}.html">\n'
      html += f'   </map>\n'
   html += f'   </p>\n\n'
   return html

def footer_hours(UTCshift,domain,sc,z,prop):
   foot = f'   <p align="center">\n'
   foot += f'   <font size="+1">\n'
   for h in range(8,20):
      futc = '%04d'%((h-UTCshift)*100)
      foot += f'   <a href="/{domain}/{sc}/{z}/{prop}_{futc}.html">{h}:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_0700.html">9:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_0800.html">10:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_0900.html">11:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1000.html">12:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1100.html">13:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1200.html">14:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1300.html">15:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1400.html">16:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1500.html">17:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1600.html">18:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1700.html">19:00</a> | \n'.replace('//','/')
   #html += f'   <a href="/{domain}/{sc}/{z}/{prop}_1800.html">20:00</a>\n'.replace('//','/')
   foot += f'   </font>\n'
   foot += f'   </p>\n'
   return foot

def body(hour,domain,prop,url,UTCshift,sc,z='',w0=1000):
   """
   w0: width to be displayed in the web
   """
   html = f'<body>\n'
   html += f'<p align="center">\n'
   html += f'  <table>\n'
   html += f'    <tr>\n'
   html += f'      <td align="right">'
   html += f'<a href="http:///www.denubeanube.com/"><img src="/dnn.svg" alt="De Nube a Nube" width="150" height="81" align="center"></a></td>\n'
   html += f'      <td align="left">\n'
   html += f'        <font size="+3">'
   html += f'<b>RASP</b> Sistema Central'
   html += f'</font><br>\n'
   html += f'        <a href="http:///www.drjack.info/RASP/">RASP</a> '
   html += f'by Dr. Jack, local site by '
   html += f'<a href="http:///raspuri.mooo.com/RASP/index.php">Oriol</a>'
   html += f' & Noel\n'
   html += f'      </td>\n'
   html += f'    </tr>\n'
   html += f'</p>\n'
   html += f'  </table>\n'


   #html += f'  <p align="center">\n'
   #html += '  <font size="+3">\n'
   #html += '  <b>RASP</b> Sistema Central\n'
   #html += '  </font><br>\n'
   #html += '  <a href="http://www.drjack.info/RASP/">RASP</a> by Dr. Jack,'
   #html += ' local site by '
   #html += '<a href="http://raspuri.mooo.com/RASP/index.php">Oriol</a> & Noel\n'
   #html += '  </p>\n'
   html += f'   <p align="center">\n'
   html += f'   <a href="/w2/{sc}/{z}/{prop}_{hour}.html">Sistema Central</a> | \n'
   html += f'   <a href="/d2/{sc}/{z}/{prop}_{hour}.html">Península</a>\n'
   html += f'   </p>\n'
   html += f'   <p align="center">\n'
   html += f'   <font size="+1">\n'
   html += f'   <a href="/{domain}/{sc}/{z}/sfcwind_{hour}.html">Sfc wind</a> | \n'
   html += f'   <a href="/{domain}/{sc}/{z}/blwind_{hour}.html">BL wind</a> | \n'
   html += f'   <a href="/{domain}/{sc}/{z}/bltopwind_{hour}.html">BL top wind</a> | \n'
   html += f'   <a href="/{domain}/{sc}/{z}/cape_{hour}.html">CAPE</a> | \n'
   html += f'   <a href="/{domain}/{sc}/{z}/hbl_{hour}.html">Height BL</a> | \n'
   html += f'   <a href="/{domain}/{sc}/{z}/wstar_{hour}.html">Thermals</a> | \n'
   html += f'   <a href="/{domain}/{sc}/{z}/bsratio_{hour}.html">B/S Ratio</a> | \n'
   html += f'   <a href="/{domain}/{sc}/{z}/blcloudpct_{hour}.html">Clouds</a>\n'
   #html += f'   <a href="/{sc}/{z}/rain1_{hour}.html">Rain</a>\n'
   html = html.replace('//','/')
   html += f'   </font>\n'
   html += f'   </p>\n\n'
   html +=  html_image(url,domain,prop,hour,sc,w0=w0)
   html += footer_hours(UTCshift,domain,sc,z,prop)
   html += f'   <p align="center">\n'
   html += f'   <font size="+1">\n'
   html += f'   <a href="/{domain}/SC2/{z}/{prop}_{hour}.html">Hoy</a> | \n'.replace('//','/')
   html += f'   <a href="/{domain}/SC2+1/{z}/{prop}_{hour}.html">Mañana</a> | \n'.replace('//','/')
   html += f'   <a href="/{domain}/SC4+2/{z}/{prop}_{hour}.html">Pasado</a> | \n'.replace('//','/')
   html += f'   <a href="/{domain}/SC4+3/{z}/{prop}_{hour}.html">Al Otro</a>\n'.replace('//','/')
   html += f'   </p>\n'
   html += f'</body>\n'
   return html

def closing():
   return '</html>\n'

def url_img(folder,sc,hour,prop,z=''):
   if len(z)==0: return folder + f'/{domain}/{sc}/{hour}_{prop}.jpg'
   else: return folder + f'/{domain}/{sc}/{z}/{hour}_{prop}.jpg'


if __name__ == '__main__':
   UTCshift = dt.datetime.now()-dt.datetime.utcnow()
   UTCshift = round(UTCshift.total_seconds()/3600)
   root_folder = '/var/www/html'
   folder = '../../data/PLOTS'
   for sc in ['SC2','SC2+1','SC4+2','SC4+3']:
      for domain in ['w2','d2']:
         #folder = plots+domain+'/'
         for prop in ['sfcwind', 'blwind', 'bltopwind',
                     'cape', 'wstar', 'hbl', 'bsratio', 'blcloudpct']:
            for hora in range(8,21):
               hour = '%04d'%(hora*100)
               for z in ['','A','B','C']:
                  html = header()
                  url = url_img(folder,sc,hour,prop,z)
                  html += body(hour,domain,prop,url,UTCshift,sc,z,w0=950)
                  html += closing()
                  if len(z)>0: fname = f'{root_folder}/{domain}/{sc}/{z}/{prop}_{hour}.html'
                  else: fname = f'{root_folder}/{domain}/{sc}/{prop}_{hour}.html'
                  with open(fname,'w') as f:
                     f.write(html)
