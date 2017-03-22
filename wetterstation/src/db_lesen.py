#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import keys
import datetime


start = input("Anfangsdatum eingeben: (YYYY-MM-DD)") or datetime.date.today()
ende = input("Endedatum eingeben: (YYYY-MM-DD)") or '9999-12-31'
db = input("[S]qlite oder [M]ySQL?") or 'M'

if db == 'M':
    conn = mysql.connector.connect(**keys.SQLCONFIG)
else:
    conn = sqlite3.connect('wetter.sqlite')
    
cur = conn.cursor()


def read_data(cur):
    cur.execute('select date, time, temperatur, humidity, windspeed, downfall, rain from  wetter where date between %s and %s ', (start, ende))
    return cur

df = pd.DataFrame(read_data(cur).fetchall(), columns=['date', 'time', 'temp', 'hum', 'wind', 'down', 'rain'])

# df['c'] = df[['a','b']].apply(lambda x: do stuff with x[0] and x[1] here, axis=1) 

# df.apply(print_data, axis=1)

# for row in df.itertuples():
#    print(row)

print('Maximaltemperatur: \n', df.nlargest(1, 'temp'))
print('Minimaltemperatur: \n', df.nsmallest(1, 'temp'))

print(df.nlargest(5, 'wind'))
print(df.nlargest(5, 'down'))

# df = df.groupby('date')

# print(df['temp'].agg(min))

plt.plot(df['temp'])
plt.show()
