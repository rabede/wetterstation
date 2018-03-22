#! python3
# downloadLuftdatenInfo.py - Downloads data from http://archive.luftdaten.info/ 

import os
from urllib.request import urlretrieve

down_date = '2018-03-21'
down_sens = 'bme280'

url = 'http://archive.luftdaten.info/'  # starting url
localDir = '../data/'

os.makedirs(localDir, exist_ok=True)  # store data in ./luftdaten
    
for sensor_id in range(10668, 11394):
    fileName = down_date + '_' + down_sens + '_sensor_' + str(sensor_id) + '.csv'
    dst = localDir + fileName
    sensorUrl = url + down_date + '/' + fileName  # Download the page.
    try:
        if os.path.isfile(dst):
            print('%s already downloaded' % fileName)
            continue
        else:
            urlretrieve(sensorUrl, dst)
            print('%s downloading ' % fileName)
    except:
        print('%s not found' % fileName)