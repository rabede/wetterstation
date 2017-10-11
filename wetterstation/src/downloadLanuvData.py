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
        if station["csv"] == "True":
            fileName = station["Station"] + '.csv'
            dst = localDir + fileName
            sensorUrl = url + fileName
            # Download the page.
            try:
                r = requests.get(sensorUrl)
                r.raise_for_status()
                print('Downloading page %s' % sensorUrl)
                with open(dst, 'w') as file:
                    file.write(r.text)
                                            
            except:
                print('File not found %s' % sensorUrl)
                continue

localDir = '../data/'
os.makedirs(localDir, exist_ok=True)
    
#getLanuvData(localDir)

url = 'http://openair-api.datacolonia.de/?q=SELECT%20value%20FROM%20open_air..r_no%20WHERE%20time%20%3E%20now()%20-%201h%20AND%20id=%27F68654%27'
r = requests.get(url)
print(r.text)
