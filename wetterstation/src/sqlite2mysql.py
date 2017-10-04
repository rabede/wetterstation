#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import mysql.connector
from keys import SQLCONFIG

conns = sqlite3.connect('wetter.sqlite')
curs = conns.cursor()

connm = mysql.connector.connect(**SQLCONFIG)
curm = connm.cursor()

for data in curs.execute('select date, time, temperatur, humidity, windspeed, downfall, rain from  wetter'):
    print(data)
    timestamp = data[0] + ' ' + data[1]
    curm.execute(
            'INSERT IGNORE into wetter ' 
            ' (timestamp, temperatur, humidity, windspeed, downfall, rain) VALUES (%s,%s,%s,%s,%s,%s)',
            (timestamp, data[2], data[3], data[4], data[5], data[6]) 
            )
    connm.commit()

connm.close()

conns.close()




