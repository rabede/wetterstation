#! python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

import sqlite3
import requests
import time
import pandas as pd
from builtins import range


conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()

url = 'http://archive.luftdaten.info/'  # starting url

downDate = '2017-09-03'
start = time.time()

for i in range(35,5480):
    filename =  downDate + '_sds011_sensor_' + str(i) + '.csv'
    sensorUrl = url + downDate + '/' + filename
    
    # Download the page.
    try:
        r = requests.head(sensorUrl)
        r.raise_for_status()
    except:
        continue

    sensor = pd.read_csv(sensorUrl, header=0, delimiter = ';')
    for index, row in sensor.iterrows():
        try:
            if row['sensor_type'] == 'BME280':
                cur.execute('''INSERT or IGNORE into luftdaten_raw (timestamp, sensor_id, sensor_type, location, lat, lon, pressure, temperature, humidity )       
                           VALUES (?,?,?,?,?,?,?,?,?)''', (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['pressure'], row['temperature'], row['humidity']))
            elif row['sensor_type'] == 'DHT22':
                cur.execute('''INSERT or IGNORE into luftdaten_raw (timestamp, sensor_id, sensor_type, location, lat, lon, temperature, humidity )       
                           VALUES (?,?,?,?,?,?,?,?)''', (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['temperature'], row['humidity']))
            elif row['sensor_type'] == 'SDS011':
                cur.execute('''INSERT or IGNORE into luftdaten_raw (timestamp, sensor_id, sensor_type, location, lat, lon, p1, p2 )       
                           VALUES (?,?,?,?,?,?,?,?)''', (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['P1'], row['P2']))
        except:
            sensor.to_csv(filename)

    conn.commit()
    #except: 
    #    

end = time.time()

print('Done in ', end -start )
conn.close()
