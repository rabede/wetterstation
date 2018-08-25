#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import datetime
import sqlite3

import mysql.connector

import keys
import matplotlib.pyplot as plt
import pandas as pd


start = input("Anfangsdatum eingeben: (YYYY-MM-DD)") or datetime.date.today()
ende = input("Endedatum eingeben: (YYYY-MM-DD)") or '9999-12-31'
db = input("[S]qlite oder [M]ySQL?").upper() or 'M'

if db == 'M':
    conns = mysql.connector.connect(**keys.SQLCONFIG)
else:
    conns = sqlite3.connect(**keys.SQLITECONFIG)
    
curs = conns.cursor()

if db == 'M':
    curs.execute('select timestamp, temperatur, humidity, windspeed, downfall, rain from  wetter where timestamp between %s and %s ', (start, ende))
    df = pd.DataFrame(curs.fetchall(), columns=['timestamp', 'temp', 'hum', 'wind', 'down', 'rain'])
else:
    curs.execute('select date, time, temperatur, humidity, windspeed, downfall, rain from  wetter where date between ? and ? ', (start, ende))
    df = pd.DataFrame(curs.fetchall(), columns=['date', 'time', 'temp', 'hum', 'wind', 'down', 'rain'])


df = df.set_index('timestamp')


# df['c'] = df[['a','b']].apply(lambda x: do stuff with x[0] and x[1] here, axis=1) 

# df.apply(print_data, axis=1)

for row in df.itertuples():
    print(row)

#print('Maximaltemperatur: \n', df.nlargest(1, 'temp'))
#print('Minimaltemperatur: \n', df.nsmallest(1, 'temp'))

#print(df.nlargest(5, 'wind'))
#print(df.nlargest(5, 'down'))

# df = df.groupby('date')

#print(df['temp'].agg(min))

plt.plot(df['temp'])
plt.show()
