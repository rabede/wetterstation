import pandas as pd
import json
import os
import requests

url = "?timestampStart=2018-09-30&source=sensors_arduino&sensor=348&show=all"

url = 'https://api.hackair.eu/measurements'
timestampStart = '2018-09-27'
timestampEnd = ''
location = '7.0,51.0|7.1,51.1'
source = 'sensors_arduino, sensors_bleair'
sensor = '348' #'889'
user = ''
pollutant = ''
#type = '' #Response type
show = 'all'  # Defines how measurements are returned, specifically sensor measurements. Use: 'latest' for the latest measurements, 'hourly_averages' for hourly averages or 'all' for all measurements. Default: 'latest

params = {'timestampStart':timestampStart, 'location':location, 'source':source, 'format':'json'}

res = requests.get(url, params=params)
js = res.json()
print(js)

