#! python3 

import json
import os
import requests

import pandas as pd
from sqlalchemy import create_engine
from stationen import LANUV_STATIONEN as lanuvStationen
from stationen import OK_STATIONEN    as okStationen
from stationen import REQUEST_PARAMETERS as params


engine = create_engine('sqlite:///../data/wetter.sqlite')

def downloadFile(dst, sensorUrl):
    try:
        r = requests.get(sensorUrl)
        r.raise_for_status()
        print('Downloading page %s' % sensorUrl)
        with open(dst, 'w') as file:
            file.write(r.text)
    except:
        print('File not found %s' % sensorUrl)

def getLanuvData(localDir):
    # Alle Stationen aus Datei holen:
    url = 'https://www.lanuv.nrw.de/fileadmin/lanuv/luft/temes/365tage/'
    for station in lanuvStationen:
        if station["csv"] == "True":
            fileName = station["Station"] + '.csv'
            dst = localDir + fileName
            sensorUrl = url + fileName
            downloadFile(dst, sensorUrl)

def getOkData(localDir):
    for station in okStationen:
        for i, param in enumerate(params):
            stat = station["Station"]
            value = param["value"]
            time = param["time"]
            dst = localDir + stat + value + '.json'
            url = "http://openair-api.datacolonia.de/?q=SELECT value FROM open_air.. {} WHERE time > now() - {} AND id='{}'".format(value, time, stat)
            #downloadFile(dst, url)
            r = requests.get(url)
            r.raise_for_status()
        
            data = json.loads(r.text)
            if i == 0:
                df = pd.DataFrame(data["results"][0]["series"][0]["values"], columns=["Zeitpunkt", (data["results"][0]["series"][0]["name"])])
            else:
                df = pd.merge(df, pd.DataFrame(data["results"][0]["series"][0]["values"], columns=["Zeitpunkt", (data["results"][0]["series"][0]["name"])]), on = "Zeitpunkt")
        df['sensor_id'] = stat
        df = df.rename(index=str, columns={"Zeitpunkt": 'timestamp'}).set_index('timestamp')
        print(df)
        df.to_sql('noxdaten', engine, if_exists='append')


localDir = '../data/'
os.makedirs(localDir, exist_ok=True)

getLanuvData(localDir)    
getOkData(localDir)

