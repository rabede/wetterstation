#!/usr/bin/env python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

from asyncio.tasks import wait
from builtins import range
import json
import requests
import sys
import time, datetime

import mysql.connector

import check_locality as cl
from keys import SQLCONFIG
import pandas as pd


conns = mysql.connector.connect(**SQLCONFIG)
curs = conns.cursor()

downDate = str(datetime.date.today() - datetime.timedelta(days=10))
downloads = 0
start = time.time()

curs.execute('Select sensor_id from lastcheckedsensor')
maxid = int(curs.fetchone()[0])
#maxid = 22984
newmaxid = maxid
osmdata = {}

#Hole Datei vom luftdaten-Archich:
def get_file(date, nr, typ = 'sds011'):
    global newmaxid, osmdata
    
    url = 'http://archive.luftdaten.info/'  # starting url
    filename =  date + '_' + typ + '_sensor_' + nr + '.csv'
    sensorUrl = url + date + '/' + filename
    
    # Download the page.
    try:
        r = requests.head(sensorUrl)
        r.raise_for_status()
    except:
        print(filename + " not found")
        return
    
    newmaxid = nr
    sensor = pd.read_csv(sensorUrl, header=0, delimiter = ';')
    row = sensor.iloc[0]
    
    if row['lon'] >= 6.89 and row['lon'] <= 7.12  and row['lat'] >= 51.01 and row['lat'] <= 51.1:
        cl.get_geodata(row, osmdata)
        save_data(row)
        print(row)

def save_data(row):    
    global downloads    
    try:
        curs.execute('''INSERT IGNORE into luftdaten_lev (sensor_id, sensor_type, location, lat, lon, adresse, plz, ort )       
                           VALUES (%s,%s,%s, %s, %s, %s, %s, %s)''', (str(row['sensor_id']), row['sensor_type'], str(row['location']), float(row['lat']), float(row['lon']), row['adresse'], row['plz'], row['ort']))
            
        conns.commit()
        downloads += 1
        wait(5)
    except:
        print('SQL-Fehler: ' + str(row))
    
if len(sys.argv) == 2:
    get_file(downDate, sys.argv[1])
else:
    for i in range(maxid + 1, maxid + 100):
        get_file(downDate, str(i))

if osmdata:
    with open('../data/osmdata.' + str(newmaxid) + '.json', 'w') as outfile:
        json.dump(osmdata, outfile, ensure_ascii=False)

curs.execute('''UPDATE lastcheckedsensor SET sensor_id = %s WHERE sensor_id = %s''', (newmaxid, maxid))    

end = time.time()

print(downloads, ' done in ', end -start )
print(newmaxid)
conns.commit()
conns.close()
