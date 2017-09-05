#!/usr/bin/env python3

import sqlite3
import requests

url = 'http://nominatim.openstreetmap.org/reverse'

conn = sqlite3.connect('wetter.sqlite')    
cur = conn.cursor()

cur.execute('select distinct sensor_id, sensor_type, location, lat, lon from  luftdaten_raw where sensor_type = ? group by sensor_id', ['SDS011'])

total = 0
lev = 0
for row in cur:
    sensor_id = row[0]
    lat = row[3]
    lon = row[4]
    total += 1
    if lon > 6.9 and lon < 7.1 and lat > 50.9 and lat < 51.1:
        print(sensor_id, lat, lon)
        params = {'lat':lat, 'lon':lon, 'format':'json'}
        res =  requests.get(url, params = params)
        try:
            if res.json()['address']['city'] == 'Leverkusen':
                print(res.json()['address']['suburb'], res.json()['address']['road'], res.json()['address']['house_number'], res.json()['address']['postcode'])
                lev += 1
        except:
            print(res.text)

print(lev, ' von ', total)