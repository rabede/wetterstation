#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3
import pandas as pd
import mysql.connector
from keys import SQLCONFIG


conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()
con2 = mysql.connector.connect(**SQLCONFIG)
cur2 = con2.cursor()


def read_data(cur):
    ''' Read rawdata to be cleaned'''
    cur.execute('select id, timestamp, temperatur, humidity, windspeed, downfall, rain from  wetter_raw ')
    return cur

def del_data(cur, ind):
    '''Delete entry from raw data table'''
    cur.execute('delete from wetter_raw where id = ?', (ind,)) #make sure parameter is a tuple!
    return cur

def print_data(data):
    print(data['date'], data['time'], data['temp'], data['hum'], data['wind'], data['down'], data['rain'])

def save_data(cur, data, table='wetter'):
    ''' Save refined data into final table, implausible data into errortable, then delete from raw_data'''        
    cur.execute( 
            'INSERT OR IGNORE into ' + table + 
            ' (date, time, temperatur, humidity, windspeed, downfall, rain) VALUES (?,?,?,?,?,?,?)', 
            (str(data['date']), str(data['time']), data['temp'], data['hum'], data['wind'], data['down'], data['rain'])
            )
    del_data(cur, data['id'])
    if table == 'wetter':
        #timestamp = data['date'] + ' ' + data['time']
        cur2.execute(
                'INSERT IGNORE into wetter ' 
                ' (timestamp, temperatur, humidity, windspeed, downfall, rain) VALUES (%s,%s,%s,%s,%s,%s)',
                (str(data['timestamp']), data['temp'], data['hum'], data['wind'], data['down'], data['rain']) 
                )


def check_data(data):
    table = 'wetter_errors'
    if (
            (50 > float(data['temp']) < -20) or  #zu Heiß oder zu kalt 
            (100 > float(data['hum']) < 0 ) or   #Luftfeuchtikgeit zu groß oder klein
            (float(data['down']) < 0) or         #Negativer Niederschlag
            (float(data['wind']) < 0)            #Negative Windgeschwindigkeit
         ):
        print_data(data)
    else:
        table = 'wetter'
    save_data(cur, data, table)   

df = pd.DataFrame( read_data(cur).fetchall(), columns = ['id', 'timestamp', 'temp', 'hum', 'wind', 'down', 'rain'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['time'] = df['timestamp'].dt.time
#df = df.drop(['timestamp'], axis=1)

df.apply(check_data, axis=1)

conn.commit()
conn.close()
con2.commit()
con2.close()