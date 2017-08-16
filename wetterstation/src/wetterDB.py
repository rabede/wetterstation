#!/usr/bin/env python3
import sqlite3

database_name = 'wetter.sqlite'

def create_tables(database, table, rows):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
#    cur.execute('DROP TABLE IF EXISTS ' + table)
    cur.execute('CREATE TABLE ' + table + ' (' + rows + ')')
    conn.close

#table_name = 'wetter_raw'
#row_names = 'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, timestamp TIMESTAMP UNIQUE, temperatur FLOAT, humidity INTEGER, windspeed FLOAT, downfall FLOAT, rain BOOLEAN'

#table_name = 'wetter'
#row_names = 'date TEXT, time TEXT, temperatur FLOAT, humidity INTEGER, windspeed FLOAT, downfall FLOAT, rain BOOLEAN, Primary Key (date, time)'

#table_name = 'wetter_errors'

table_name = 'luftdaten_raw'
row_names = 'id Integer NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, timestamp TIMESTAMP UNIQUE, sensor_id INTEGER, sensor_type STRING, location INTEGER, lat FLOAT, lon FLOAT, p1 FLOAT, p2 FLOAT, pressure FLOAT, temperature FLOAT, humidity FLOAT' 

create_tables(database_name, table_name, row_names)
