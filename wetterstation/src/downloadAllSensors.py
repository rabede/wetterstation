#! python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

from keys import SQLCONFIG
import mysql.connector
import requests
import time, datetime
import pandas as pd
from builtins import range
from asyncio.tasks import wait

conns = mysql.connector.connect(**SQLCONFIG)
curs = conns.cursor()

downDate = str(datetime.date.today() - datetime.timedelta(days=1))
downloads = 0
start = time.time()

curs.execute('Select max( sensor_id ) from luftdaten_lev')
maxid = int(curs.fetchone()[0])

#Hole Geodaten zu gegebenr Länge/Breite
def get_geodata(row):
    url = 'http://nominatim.openstreetmap.org/reverse'
    lat = row['lat']
    lon = row['lon']
    
    params = {'lat':lat, 'lon':lon, 'format':'json'}
    res =  requests.get(url, params = params)
    
    try:
        row['ort'] = res.json()['address']['suburb']
    except:
        row['ort'] = res.json()['address']['city']
    try: 
        row['adresse'] = res.json()['address']['road'] + ' ' + res.json()['address']['house_number']
    except:
        try:
            row['adresse'] = res.json()['address']['road']
        except:
            row['adresse'] = ''
    row['plz'] = res.json()['address']['postcode']

#Hole Datei vom luftdaten-Archich:
def get_file(date, nr, typ = 'sds011'):
    url = 'http://archive.luftdaten.info/'  # starting url
    filename =  date + '_' + typ + '_sensor_' + nr + '.csv'
    sensorUrl = url + date + '/' + filename
    
    # Download the page.
    try:
        r = requests.head(sensorUrl)
        r.raise_for_status()
    except:
        return

    sensor = pd.read_csv(sensorUrl, header=0, delimiter = ';')
    row = sensor.iloc[0]
    
    if row['lon'] >= 6.89 and row['lon'] <= 7.12  and row['lat'] >= 51.01 and row['lat'] <= 51.1:
        get_geodata(row)
        save_data(row)


def save_data(row):    
    global downloads    
    curs.execute('''INSERT IGNORE into luftdaten_lev (sensor_id, sensor_type, location, lat, lon, adresse, plz, ort )       
                       VALUES (%s,%s,%s, %s, %s, %s, %s, %s)''', (str(row['sensor_id']), row['sensor_type'], str(row['location']), float(row['lat']), float(row['lon']), row['adresse'], row['plz'], row['ort']))
        
    conns.commit()
    downloads += 1
    wait(5)

for i in range(maxid + 1, maxid + 1000):
    get_file(downDate, str(i))
    

end = time.time()

print(downloads, ' done in ', end -start )
conns.close()