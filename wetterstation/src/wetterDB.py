import sqlite3

database_name = 'test.sqlite'
table_name = 'wetter'
row_names = 'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, timestamp TIMESTAMP UNIQUE, temperatur FLOAT, humidity INTEGER, windspeed FLOAT, downfall FLOAT, rain BOOLEAN'

conn = sqlite3.connect(database_name)
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS ' + table_name)
cur.execute('CREATE TABLE ' + table_name + ' (' + row_names + ')')

conn.close