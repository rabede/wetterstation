import json
import os
import requests

import pandas as pd


url = "?timestampStart=2018-09-30&source=sensors_arduino&sensor=348&show=all"

url = 'https://api.hackair.eu/measurements'
timestampStart = '2018-09-21'
timestampEnd = ''
location = '7.0,51.0|7.1,51.1'
source = 'sensors_arduino'
sensor = '348' #'889'
user = '393'
pollutant = ''
#type = '' #Response type
show = 'all'  # Defines how measurements are returned, specifically sensor measurements. Use: 'latest' for the latest measurements, 'hourly_averages' for hourly averages or 'all' for all measurements. Default: 'latest

params = {'timestampStart':timestampStart, 'source':source, 'user': user, 'show': show, 'format': json}

res = requests.get(url, params=params)
js = res.json()
print(js)

