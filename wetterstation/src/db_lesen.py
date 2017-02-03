#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()

start = input("Anfangsdatum eingeben: (YYYY-MM-DD)") or '1017-01-25' #or date.today()
ende  = input("Endedatum eingeben: (YYYY-MM-DD)") or '9999-12-31'


def read_data(cur):
    cur.execute('select date, time, temperatur, humidity, windspeed, downfall, rain from  wetter where date between ? and ? ', (start, ende))
    return cur

df = pd.DataFrame( read_data(cur).fetchall(), columns = ['date', 'time', 'temp', 'hum', 'wind', 'down', 'rain'])

#df['c'] = df[['a','b']].apply(lambda x: do stuff with x[0] and x[1] here, axis=1) 

#df.apply(print_data, axis=1)

#for row in df.itertuples():
#    print(row)

print('Maximaltemperatur: \n', df.nlargest(1, 'temp'))
print('Minimaltemperatur: \n', df.nsmallest(1, 'temp'))

print(df.nlargest(5, 'wind'))
print(df.nlargest(5, 'down'))

#df = df.groupby('date')

#print(df['temp'].agg(min))

plt.plot(df['temp'])
plt.show()
