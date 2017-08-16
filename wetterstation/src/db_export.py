#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import csv
import datetime


start = input("Anfangsdatum eingeben: (YYYY-MM-DD)") or datetime.date.today()
ende = input("Endedatum eingeben: (YYYY-MM-DD)") or '9999-12-31'

conn = sqlite3.connect('wetter.sqlite')
    
cur = conn.cursor()

cur.execute('select date, time, temperatur, humidity, windspeed, downfall, rain from  wetter where date between ? and ? ', (start, ende))
    
csv.register_dialect('wetterdialect', delimiter=';', quoting=csv.QUOTE_NONE)        
with open('wetter.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, dialect='wetterdialect')
    for tup in cur:
        row  = list(tup)
        tst = row[0] + ' ' + row[1]
        row.insert(0, tst)
        row.pop(1)
        row.pop(1)
        writer.writerow(row)
