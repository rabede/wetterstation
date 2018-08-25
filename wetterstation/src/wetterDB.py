#!/usr/bin/env python3
import sqlite3

import keys


database_name = keys.SQLITECONFIG

def create_tables(database, table, rows):
    conns = sqlite3.connect(database)
    curs = conns.cursor()
#    curs.execute('DROP TABLE IF EXISTS ' + table)
    curs.execute('CREATE TABLE ' + table + ' (' + rows + ')')
    conns.close

#table_name = 'wetter_raw'
#row_names = 'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, timestamp TIMESTAMP UNIQUE, temperatur FLOAT, humidity INTEGER, windspeed FLOAT, downfall FLOAT, rain BOOLEAN'

#table_name = 'wetter'
#row_names = 'date TEXT, time TEXT, temperatur FLOAT, humidity INTEGER, windspeed FLOAT, downfall FLOAT, rain BOOLEAN, Primary Key (date, time)'

#table_name = 'wetter_errors'


table_name = 'luftdaten_lev'
row_names = 'sensor_id string NOT NULL PRIMARY KEY UNIQUE, sensor_type STRING, location INTEGER, lat FLOAT, lon FLOAT, adresse string, plz string, ort string' 

create_tables(database_name, table_name, row_names)
