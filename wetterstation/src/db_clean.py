#!/usr/bin/env python3
'''
Created on 16.01.2017

@author: bell
'''
import sqlite3

import mysql.connector

import keys
import pandas as pd


conns = sqlite3.connect(**keys.SQLITECONFIG)
curs = conns.cursor()
connm = mysql.connector.connect(**keys.SQLCONFIG)
curm = connm.cursor()


def read_data(curs):
    ''' Read rawdata to be cleaned'''
    curs.execute('select id, timestamp, temperatur, humidity, windspeed, downfall, rain from  wetter_raw ')
    return curs

def del_data(curs, ind):
    '''Delete entry from raw data table'''
    curs.execute('delete from wetter_raw where id = ?', (ind,)) #make sure parameter is a tuple!
    return curs

def print_data(data):
    print(data['date'], data['time'], data['temp'], data['hum'], data['wind'], data['down'], data['rain'])

def save_data(curs, data, table='wetter'):
    ''' Save refined data into final table, implausible data into errortable, then delete from raw_data'''        
    curs.execute( 
            'INSERT OR IGNORE into ' + table + 
            ' (date, time, temperatur, humidity, windspeed, downfall, rain) VALUES (?,?,?,?,?,?,?)', 
            (str(data['date']), str(data['time']), data['temp'], data['hum'], data['wind'], data['down'], data['rain'])
            )
    del_data(curs, data['id'])
    if table == 'wetter':
        #timestamp = data['date'] + ' ' + data['time']
        curm.execute(
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
    save_data(curs, data, table)   

df = pd.DataFrame( read_data(curs).fetchall(), columns = ['id', 'timestamp', 'temp', 'hum', 'wind', 'down', 'rain'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['time'] = df['timestamp'].dt.time
#df = df.drop(['timestamp'], axis=1)

df.apply(check_data, axis=1)

conns.commit()
conns.close()
connm.commit()
connm.close()