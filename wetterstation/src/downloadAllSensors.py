#! python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

from keys import SQLCONFIG
import mysql.connector
import requests
import time
import pandas as pd
from builtins import range
from asyncio.tasks import wait

def get_geodata(row):
    url = 'http://nominatim.openstreetmap.org/reverse'
    lat = row['lat']
    lon = row['lon']
    
    params = {'lat':lat, 'lon':lon, 'format':'json'}
    res =  requests.get(url, params = params)
    
    try:
        row['ort'] = res.json()['address']['suburb']
    except:
        row['ort'] = res.json()['address']['city']
    try: 
        row['adresse'] = res.json()['address']['road'] + ' ' + res.json()['address']['house_number']
    except:
        try:
            row['adresse'] = res.json()['address']['road']
        except:
            row['adresse'] = ''
    row['plz'] = res.json()['address']['postcode']


conn = mysql.connector.connect(**SQLCONFIG)
cur = conn.cursor()

url = 'http://archive.luftdaten.info/'  # starting url

downDate = '2017-09-24'
downloads = 0
start = time.time()

for i in range(4138,5403):
    filename =  downDate + '_sds011_sensor_' + str(i) + '.csv'
    sensorUrl = url + downDate + '/' + filename
    
    # Download the page.
    try:
        r = requests.head(sensorUrl)
        r.raise_for_status()
    except:
        continue

    sensor = pd.read_csv(sensorUrl, header=0, delimiter = ';')
    row = sensor.iloc[0]
    print(row['sensor_id'], row['lon'], row['lat'])
    
    if row['lon'] >= 6.89 and row['lon'] <= 7.12  and row['lat'] >= 51.01 and row['lat'] <= 51.1:
        get_geodata(row)
        cur.execute('''INSERT IGNORE into luftdaten_lev (sensor_id, sensor_type, location, lat, lon, adresse, plz, ort )       
                       VALUES (%s,%s,%s, %s, %s, %s, %s, %s)''', (str(row['sensor_id']), row['sensor_type'], str(row['location']), float(row['lat']), float(row['lon']), row['adresse'], row['plz'], row['ort']))
        
        conn.commit()
        downloads += 1
        wait(5)

end = time.time()

print(downloads, ' done in ', end -start )
conn.close()