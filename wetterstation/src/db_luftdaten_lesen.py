#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import pandas as pd
import datetime



start = input("Anfangsdatum eingeben: (YYYY-MM-DD)") or datetime.date.today() - datetime.timedelta(days=1)
ende = input("Endedatum eingeben: (YYYY-MM-DD)") or '9999-12-31'

conns = sqlite3.connect('wetter.sqlite')
    
curs = conns.cursor()


def read_data(curs):
    curs.execute('select timestamp, sensor_id, sensor_type, location, lat, lon, p1, p2, pressure, temperature, humidity from  luftdaten_raw where timestamp between ? and ? ', (start, ende))
    return curs

df = pd.DataFrame(read_data(curs).fetchall(), columns=['timestamp', 'sensor_id', 'sensor_type', 'location', 'lat', 'lon', 'p1', 'p2', 'pressure', 'temperature', 'humidity'])

df.to_csv('luftdaten.csv', ';')
