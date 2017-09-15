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

for data in cur.execute('select date, time, temperatur, humidity, windspeed, downfall, rain from  wetter'):
    print(data)
    timestamp = data[0] + ' ' + data[1]
    cur2.execute(
            'INSERT IGNORE into wetter ' 
            ' (timestamp, temperatur, humidity, windspeed, downfall, rain) VALUES (%s,%s,%s,%s,%s,%s)',
            (timestamp, data[2], data[3], data[4], data[5], data[6]) 
            )
    con2.commit()

con2.close()

conn.close()




