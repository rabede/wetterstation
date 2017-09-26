#!/usr/bin/env python3

import sqlite3
import requests

url = 'http://nominatim.openstreetmap.org/reverse'

conn = sqlite3.connect('wetter.sqlite')    
cur = conn.cursor()
cur2 = conn.cursor()

cur.execute('select sensor_id, lat, lon from  luftdaten_lev ')



for row in cur:
    sensor_id = row[0]
    lat = row[1]
    lon = row[2]
    params = {'lat':lat, 'lon':lon, 'format':'json'}
    res =  requests.get(url, params = params)
    try:
        ort = res.json()['address']['suburb']
    except:
        ort = res.json()['address']['city']
    try: 
        adresse = res.json()['address']['road'] + ' ' + res.json()['address']['house_number']
    except:
        try:
            adresse = res.json()['address']['road']
        except:
            adresse = ''
    plz = res.json()['address']['postcode']
    print(sensor_id, adresse, plz, ort)
    cur2.execute('update luftdaten_lev set adresse = adresse, plz = plz, ort = ort where sensor_id = sensor_id')
    conn.commit()

conn.close()
    