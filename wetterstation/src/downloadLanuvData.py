#! python3 

import os
import json
import requests
import pandas as pd

def getLanuvData(localDir):
    # Alle Stationen aus Datei holen:
    url = 'https://www.lanuv.nrw.de/fileadmin/lanuv/luft/temes/365tage/'
    lanuvStationen = 'lanuv_stationen.json'
    stationen = json.load(open(lanuvStationen))
    for station in stationen:
        fileName = station["Station"] + '.csv'
        dst = localDir + fileName
        sensorUrl = url + fileName
        # Download the page.
        try:
            if os.path.isfile(dst):
                print('%s already downloaded' % sensorUrl)
            else:
                r = requests.get(sensorUrl)
                r.raise_for_status()
                r.encoding = 'UTF-8 with BOM'
                print('Downloading page %s' % sensorUrl)
                with open(dst, 'w') as file:
                    file.write(r.text)
                                        
        except:
            print('File not found %s' % sensorUrl)
            continue
        
        df = pd.read_csv(dst, header=1, delimiter=';')
        print(df.head())
        

localDir = '../data/'
os.makedirs(localDir, exist_ok=True)
    
getLanuvData(localDir)
