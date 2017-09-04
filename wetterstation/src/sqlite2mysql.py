#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import mysql.connector
from keys import SQLCONFIG

conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()

con2 = mysql.connector.connect(**SQLCONFIG)
cur2 = con2.cursor()

#Letzten Eintrag aus MySQL-DB holen:
cur2.execute('Select max( timestamp ) from luftdaten')

#Als Select-Parameter für SQLITE muß eine Liste [] übergeben werden!
lastdate = [cur2.fetchone()[0]]

#for data in cur.execute('select date, time, temperatur, humidity, windspeed, downfall, rain from  wetter'):
for data in cur.execute('select id, timestamp, sensor_id, sensor_type, location, lat, lon, p1, p2, pressure, temperature, humidity from luftdaten_raw where timestamp > ?', (lastdate)):
    print(data)
    cur2.execute(
#            'INSERT into wetter ' 
#            ' (date, time, temperatur, humidity, windspeed, downfall, rain) VALUES (%s,%s,%s,%s,%s,%s,%s)',
#            (data[0], data[1], data[2], data[3], data[4], data[5], data[6]) 
            'INSERT into luftdaten ' 
            ' (id, timestamp, sensor_id, sensor_type, location, lat, lon, p1, p2, pressure, temperature, humidity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11])
            )
    con2.commit()

con2.close()

conn.close()




