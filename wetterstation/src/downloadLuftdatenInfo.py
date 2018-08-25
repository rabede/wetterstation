#!/usr/bin/env python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

import datetime
import os, csv, sqlite3
from urllib.request import urlretrieve

from dateutil.rrule import rrule, DAILY
import mysql.connector

import keys


conns = sqlite3.connect(**keys.SQLITECONFIG)
curs = conns.cursor()

connm = mysql.connector.connect(**keys.SQLCONFIG)
curm = connm.cursor()

cntsql = 0
cntdow = 0
cntntf = 0

ende = datetime.date.today()
url = 'http://archive.luftdaten.info/'  # starting url
localDir = '../data/'

os.makedirs(localDir, exist_ok=True)  # store data in ./luftdaten
    
# Alle Sensoren aus DB holen:
curm.execute('Select sensor_id, sensor_type from luftdaten_lev')  # where sensor_type = "DHT22"')
sensors = curm.fetchall()
#sensors = [('3081', 'SDS011')]
for sensor in sensors:
    sensor_type = sensor[1]
    sensor_id = sensor[0]
    print(sensor_type, sensor_id, end=' ')
    
# Letzten Eintrag aus MySQL-DB holen:
    curm.execute('Select max( timestamp ) from luftdaten where sensor_id = "{}"'.format(sensor_id))
    start = curm.fetchone()[0]
    #start = datetime.datetime.strptime('2018-02-09', '%Y-%m-%d')
    print(start)
    if start == None:
        start = datetime.datetime.today() - datetime.timedelta(days=3)
    else:
        start = start + datetime.timedelta(hours=1)

    for dt in rrule(DAILY, dtstart=start, until=ende):
        downDate = dt.strftime("%Y-%m-%d")
        fileName = downDate + '_' + sensor_type.lower() + '_sensor_' + sensor_id + '.csv'
        dst = localDir + fileName
        sensorUrl = url + downDate + '/' + fileName  # Download the page.
        try:
            if os.path.isfile(dst):
                print('%s already downloaded' % fileName)
                continue
            else:
                urlretrieve(sensorUrl, dst)
                print('%s downloading ' % fileName)
            
            with open(dst, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
                for row in reader:
                    try:
                        if row['sensor_type'] == 'BME280':
                            curs.execute('''INSERT or IGNORE into luftdaten_raw 
                                (timestamp, sensor_id, sensor_type, location, lat, lon, pressure, temperature, humidity ) 
                                VALUES (?,?,?,?,?,?,?,?,?)''',
                                (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['pressure'], row['temperature'], row['humidity']))

                            curm.execute('''INSERT IGNORE into luftdaten  
                                (timestamp, sensor_id, sensor_type, location, lat, lon, pressure, temperature, humidity ) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['pressure'], row['temperature'], row['humidity']))
                        
                        elif row['sensor_type'] == 'DHT22':
                            curs.execute('''INSERT or IGNORE into luftdaten_raw 
                                (timestamp, sensor_id, sensor_type, location, lat, lon, temperature, humidity )       
                                VALUES (?,?,?,?,?,?,?,?)''',
                                (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['temperature'], row['humidity']))

                            curm.execute('''INSERT IGNORE into luftdaten  
                                (timestamp, sensor_id, sensor_type, location, lat, lon, temperature, humidity ) 
                                VALUES (%s,%s,%s,%s,%s,%s, %s, %s)''',
                                (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['temperature'], row['humidity']))
                        
                        elif row['sensor_type'] == 'SDS011':
                            curs.execute('''INSERT or IGNORE into luftdaten_raw 
                                (timestamp, sensor_id, sensor_type, location, lat, lon, p1, p2 )       
                                VALUES (?,?,?,?,?,?,?,?)''',
                                (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['P1'], row['P2']))
                            
                            curm.execute('''INSERT IGNORE into luftdaten  
                                (timestamp, sensor_id, sensor_type, location, lat, lon, p1, p2 )        
                                VALUES (%s,%s,%s,%s,%s,%s, %s, %s)''',
                                (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['P1'], row['P2']))
                            
                        cntsql += 1
                    except:
                        print('Fehler: ', row)
            cntdow += 1
            os.remove(dst)
        except:
            print('%s not found' % fileName)
            cntntf += 1
        conns.commit()
        connm.commit()

connm.close()
conns.close()

print(cntdow, 'files downloded. ', cntntf, ' files not found.', cntsql, ' sets inserted in SQLITEDB and  MySQLDB.')
