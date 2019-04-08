#!/usr/bin/env python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

import datetime
import os, csv, sqlite3, sys
import logging.config
import yaml
from urllib.request import urlretrieve

from dateutil.rrule import rrule, DAILY
import mysql.connector

import keys

with open ('config.yaml') as f:
    config_dict = yaml.load(f, Loader=yaml.SafeLoader)
    
logging.config.dictConfig(config_dict)
verbose = logging.getLogger("verbose")
logfile = logging.getLogger("logfile") 

conns = sqlite3.connect(**keys.SQLITECONFIG)
curs = conns.cursor()

connm = mysql.connector.connect(**keys.SQLCONFIG)
curm = connm.cursor()

cntsql = 0
cntdow = 0
cntntf = 0

url = 'http://archive.luftdaten.info/'  # starting url
localDir = '../data/'

os.makedirs(localDir, exist_ok=True)  # store data in ./luftdaten
    
# Alle Sensoren aus DB holen:
curm.execute('Select sensor_id, sensor_type from luftdaten_lev')  # where sensor_type = "DHT22"')
sensors = curm.fetchall()
#sensors = [('16203', 'SDS011')]
for sensor in sensors:
    sensor_type = sensor[1]
    sensor_id = sensor[0]
    
    try:
        start = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
    except:
# Letzten Eintrag aus MySQL-DB holen:
        curm.execute('Select max( timestamp ) from luftdaten where sensor_id = "{}"'.format(sensor_id))
        start = curm.fetchone()[0]
    
        if start == None:
            start = datetime.datetime.today() - datetime.timedelta(days=30)
        elif( datetime.datetime.today() - start > datetime.timedelta(days=3)):
            start = datetime.datetime.today() - datetime.timedelta(days=1)
        else:
            start = start + datetime.timedelta(hours=1)
    try: 
        ende = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
    except:
        ende = datetime.date.today()
    
    '''
    start = datetime.datetime.strptime('2019-03-28', '%Y-%m-%d')
    ende = datetime.datetime.strptime('2019-03-31', '%Y-%m-%d')
    '''
    verbose.info(sensor_type + '\t' +  sensor_id + '\t' + str(start))
    
    for dt in rrule(DAILY, dtstart=start, until=ende):
        downDate = dt.strftime("%Y-%m-%d")
        fileName = downDate + '_' + sensor_type.lower() + '_sensor_' + sensor_id + '.csv'
        dst = localDir + fileName
        sensorUrl = url + downDate + '/' + fileName  # Download the page.
        try:
            if os.path.isfile(dst):
                verbose.info('%s already downloaded' % fileName)
                continue
            else:
                urlretrieve(sensorUrl, dst)
                verbose.info('%s downloading ' % fileName)
            
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
                        logfile.warn('Fehler: ', row)
            cntdow += 1
            os.remove(dst)
        except:
            verbose.info('%s not found' % fileName)
            cntntf += 1
        conns.commit()
        connm.commit()

connm.close()
conns.close()

verbose.info(cntdow, 'files downloded. ', cntntf, ' files not found.', cntsql, ' sets inserted in SQLITEDB and  MySQLDB.')
