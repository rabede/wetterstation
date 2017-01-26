'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import pandas as pd
from datetime import date 
import matplotlib.pyplot as plt

conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()

start = input("Anfangsdatum eingeben: (YYYY-MM-DD)") or '2017-01-01' #or date.today()
ende  = input("Endedatum eingeben: (YYYY-MM-DD)") or '9999-12-31'

def read_data(cur):
    try:
        cur.execute('select timestamp, temperatur, humidity, windspeed, downfall from  wetter where timestamp between ? and ? ', (start, ende))
    except:
        print('Error: ')
    return cur

df = pd.DataFrame( read_data(cur).fetchall(), columns = ['Timestamp', 'temp', 'hum', 'wind', 'rain'])
#df.set_index(['Timestamp'], drop=True, inplace=True)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Datum'] = df['Timestamp'].dt.date
df['Zeit'] = df['Timestamp'].dt.time

df = df.drop(['Timestamp'], axis=1)#.groupby(by='Datum')

print(df.nsmallest(15, ['temp']))
print(df.nlargest(15, ['temp']))
print(df.loc[df['rain'] < 0 ])
'''
plt.plot(df['temp'])
plt.show()
'''