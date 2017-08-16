#! python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/

import os, csv, sqlite3
from urllib.request import urlretrieve
from pip._vendor.distlib.util import CSVReader


conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()

downDate = '2017-08-15'

sensorList = {'_bme280_sensor_3082', '_bme280_sensor_4977', '_dht22_sensor_4834', '_sds011_sensor_3081', '_sds011_sensor_4833', '_sds011_sensor_4975'}

url = 'http://archive.luftdaten.info/' # starting url
localDir = 'luftdaten/'
os.makedirs(localDir, exist_ok=True) # store data in ./luftdaten

for sensor in sensorList:
    fileName = downDate + sensor + '.csv'
    dst = localDir + fileName
    sensorUrl = url + downDate + '/' + fileName
    # Download the page.
    try:
        urlretrieve(sensorUrl, dst)
        print('Downloading page %s...' % sensorUrl)
    
        with open(dst, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
            for row in reader:
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
                    print('Fehler: ', row)
    
        conn.commit()
    except: 
        print('File not found %s...' % sensorUrl)


print('Done.')
conn.close()
