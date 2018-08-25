#! python3
import json
import os, requests

import pandas as pd


# Hole Geodaten zu gegebenr Länge/Breite
def get_geodata(row, osmdata):
    url = 'http://nominatim.openstreetmap.org/reverse'
    lat = row['lat']
    lon = row['lon']
    
    params = {'lat':lat, 'lon':lon, 'format':'json'}
    res = requests.get(url, params=params)
    
    try:
        city = res.json()['address']['city']
        if city != 'Leverkusen':
            print(row['sensor_id'] + ' in ' +  city)
            return
        
        row['ort'] = res.json()['address']['suburb']
        
        try:
            stn = res.json()['address']['road'] 
        except:
            stn = res.json()['address']['footway']
        
        try:
            hnr = res.json()['address']['house_number']
        except:
            hnr = ''
    
        row['adresse'] = stn + ' ' + hnr                    
        row['plz'] = res.json()['address']['postcode']
    except:
        osmdata[str(row['sensor_id'])] = res.json()    
        

if __name__ == '__main__':
    
    osmdata = {}
    for file in os.listdir('../data'):
        if file.endswith('.csv') and file.startswith('2018-03-21'):
    
            sensor = pd.read_csv('../data/' + file, header=0, delimiter=';')
            row = sensor.iloc[0]
        
            if row['lon'] >= 6.89 and row['lon'] <= 7.12  and row['lat'] >= 51.01 and row['lat'] <= 51.1:
                get_geodata(row, osmdata)
                print(row)
                print('\n\n')
            else:
                os.remove('../data/' + file)
    
    with open('../data/osmdata.json', 'w') as outfile:
        json.dump(osmdata, outfile, ensure_ascii=False)
        
                
