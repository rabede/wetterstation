#! python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

import os, csv
from urllib.request import urlretrieve

url = 'http://archive.luftdaten.info/'  # starting url
localDir = '../data/'

os.makedirs(localDir, exist_ok=True)  # store data in ./luftdaten
    
for sensor_id in range(1, 9010):
    fileName = '2018-01-30_sds011_sensor_' + str(sensor_id) + '.csv'
    dst = localDir + fileName
    sensorUrl = url + '2018-01-30' + '/' + fileName  # Download the page.
    try:
        if os.path.isfile(dst):
            print('%s already downloaded' % fileName)
            continue
        else:
            urlretrieve(sensorUrl, dst)
            print('%s downloading ' % fileName)
    except:
        print('%s not found' % fileName)