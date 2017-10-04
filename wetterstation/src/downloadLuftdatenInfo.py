#! python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

import os, csv, sqlite3
from urllib.request import urlretrieve
import datetime
from dateutil.rrule import rrule, DAILY
import mysql.connector
from keys import SQLCONFIG

conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()
con2 = mysql.connector.connect(**SQLCONFIG)
cur2 = con2.cursor()

cntsql = 0
cntmys = 0
cntdow = 0
cntntf = 0


def sqlite2mysql(cur, con2, cur2, start):
    global cntmys
# Als Select-Parameter für SQLITE muß eine Liste [] übergeben werden!
    for data in cur.execute('''select id, timestamp, sensor_id, sensor_type, location, 
                                lat, lon, p1, p2, pressure, temperature, humidity
                                from luftdaten_raw where date(timestamp) >= ?  ''', [start]):
#        print(data)
        cur2.execute('''INSERT IGNORE into luftdaten  
                        (timestamp, sensor_id, sensor_type, location, 
                        lat, lon, p1, p2, pressure, temperature, humidity) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]))
        cntmys += 1
    con2.commit()
    

def get_files(conn, cur, start, ende):
    global cntsql, cntdow, cntntf
    #sensorList = SENSORLIST
    cur2.execute('Select sensor_id, sensor_type from luftdaten_lev')
    sensors = cur2.fetchall()
    sensorList = []
    for sensor in sensors:
        sensorList.append('_' + str(sensor[1]).lower() + '_sensor_' + str(sensor[0]))
        
    url = 'http://archive.luftdaten.info/'  # starting url
    localDir = '../data/'
    
    os.makedirs(localDir, exist_ok=True)  # store data in ./luftdaten

    for dt in rrule(DAILY, dtstart=start, until=ende):
        downDate = dt.strftime("%Y-%m-%d")
        for sensor in sensorList:
            fileName = downDate + sensor + '.csv'
            dst = localDir + fileName
            sensorUrl = url + downDate + '/' + fileName  # Download the page.
            try:
                #if os.path.isfile(dst):
                #    print('%s already downloaded' % sensorUrl)
                #else:
                urlretrieve(sensorUrl, dst)
                #    print('Downloading page %s' % sensorUrl)
                
                with open(dst, newline='') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
                    for row in reader:
                        try:
                            if row['sensor_type'] == 'BME280':
                                cur.execute('''INSERT or IGNORE into luftdaten_raw 
                                (timestamp, sensor_id, sensor_type, location, lat, lon, pressure, temperature, humidity ) 
                                VALUES (?,?,?,?,?,?,?,?,?)''', (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['pressure'], row['temperature'], row['humidity']))
                            elif row['sensor_type'] == 'DHT22':
                                cur.execute('''INSERT or IGNORE into luftdaten_raw 
                                (timestamp, sensor_id, sensor_type, location, lat, lon, temperature, humidity )       
                                VALUES (?,?,?,?,?,?,?,?)''', (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['temperature'], row['humidity']))
                            elif row['sensor_type'] == 'SDS011':
                                cur.execute('''INSERT or IGNORE into luftdaten_raw 
                                (timestamp, sensor_id, sensor_type, location, lat, lon, p1, p2 )       
                                VALUES (?,?,?,?,?,?,?,?)''', (row['timestamp'], row['sensor_id'], row['sensor_type'], row['location'], row['lat'], row['lon'], row['P1'], row['P2']))
                            cntsql += 1
                        except:
                            print('Fehler: ', row)
                cntdow += 1
            except:
                print('File not found %s' % sensorUrl)
                cntntf += 1
        conn.commit()

# Letzten Eintrag aus MySQL-DB holen:
cur2.execute('Select max( timestamp ) from luftdaten')
start = cur2.fetchone()[0]
#start = datetime.datetime.strptime('2017-09-27', "%Y-%m-%d")
ende = datetime.date.today()



print('Starttimestamp: ', start)

get_files(conn, cur, start, ende)

sqlite2mysql(cur, con2, cur2, start)

con2.close()
conn.close()

print(cntdow, 'files downloded. ', cntntf, ' files not found.', cntsql, ' sets inserted in SQLITEDB. ', cntmys, ' sets inserted in MySQLDB.')