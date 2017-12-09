#!/usr/bin/env python

import datetime
import serial
import xively
import logging.handlers
import sys
from time import sleep
#import urllib2
import requests
import keys
import mysql.connector
import dropbox

LOG_FILENAME = keys.DIR + "wetter.log"
LOG_LEVEL = logging.ERROR  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

# api initialisieren
api = xively.XivelyAPIClient(keys.API_KEY)
try:
    feed = api.feeds.get(keys.FEED_ID)
except:
    logger.error("Fehler: api.feeds.get(keys.FEED_ID)")


# Niederschlag total und heutiges Datum merken
total_down = -1
today = -1

def init_serial_port(logger):
# initialize serial port
    try:
        ser = serial.Serial(port='/dev/ttyAMA0', baudrate=4800, bytesize=8, parity="N", stopbits=1)
        ser.write("\x02\x02\xfb\x01")
        ser.write("\x02\x02\xf2\x01")
    except (serial.SerialException) as e:
        logger.error("Error({0}): {1}".format(e.errno, e.strerror))
        return None
    logger.info('Serial Port initialised: ' + ser.name)
    return ser

def update_data(stream, value):
    logger.info(stream + ": " + value) 
    try:
        datastream = feed.datastreams.get(stream)
        datastream.current_value = value
        datastream.max_value = None
        datastream.min_value = None
        datastream.at = datetime.datetime.utcnow()
    except:
        logger.error("Fehler: feed.datastreams.get(stream)")
        return

    try:
        datastream.update()
    except (requests.HTTPError, requests.ConnectionError) as e:
        logger.error("Error({0}): {1}".format(e.errno, e.strerror))

def prepare_value(split, raw):
    value,hexvalue=raw.split(split)
    return value.replace(",",".")


def calc_down(time, value):
    global total_down
    global today

#295ml/m^2 per pulse
    value = float(value) * 0.295

    logger.info("today + total_down + value")
    logger.info(str(today) + " " + str(total_down) + " " +  str(value)) 
#Erster Lauf: aktuellen Wert als Gesamtniederschlag setzen, 
#             Datum merken
#             aktueller Niederschlag auf 0
    if total_down == -1:
        total_down = value
        today = datetime.datetime.now().day
        return "0.0"

#Folgelauf: solange Datum gleich
#           aktuellen Wert von Gesamtniederschlag abziehen
    if today == datetime.datetime.now().day:
        return str(float(value) - float(total_down))

#Datumswechsel: neues Datum merken, Gesamtniederschlag aktualisieren
#               aktueller Niederschlag auf 0
    else:
        upload_Dropbox()
        today = datetime.datetime.now().day
        logger.info('Date change: ' + str(today))
        total_down = value
        return "0.0"
    
def save_sql(data):
    con = mysql.connector.connect(**keys.SQLCONFIG)
    curs = con.cursor()
    datum, zeit = data[0].split(" ")
    curs.execute( 
            'INSERT into wetter ' 
            ' (date, time, temperatur, humidity, windspeed, downfall, rain) VALUES (%s,%s,%s,%s,%s,%s,%s)', 
            (datum, zeit, data[1], data[2], data[3], data[4], data[5])
            )
    con.commit()
    con.close()

def upload_Dropbox():
    try:
        dbx = dropbox.Dropbox(keys.DROPBOX_TOKEN)
        yesterday = datetime.date.today() - datetime.timedelta(1) 
        filename = yesterday.strftime("%Y%m%d") +  '.txt'
        file = keys.DIR + filename
        target = '/' + filename
        with open(file, 'rb') as f:
                dbx.files_upload(f.read(), target)
    except:
        logger.error('Dropbox-Fehler')
            

#Hauptprogramm, Schleife liest von ser und bereitet die Daten auf 
def run():

    dataset = [] 
    ser = init_serial_port(logger)
    while True:
        while ser == None:
            ser = init_serial_port(logger)
            sleep(10)
        line=ser.readline()
        logger.info(line.replace("\n", ""))
        name,value=line.split(": ")
        now = datetime.datetime.now()

        if name == "Temperatur":
            temp = prepare_value(" C", value)
            update_data("Temperatur", temp)
            dataset.append(now.strftime("%Y-%m-%d %H:%M"))
            dataset.append(temp)
    
        elif name == "Luftfeuchtigkeit":
            hum= prepare_value(" %", value)
            update_data("Luftfeuchtigkeit", hum)
            dataset.append(hum)
    
        elif name == "Windgeschw.":
            vel = prepare_value(" k", value)
            update_data("Windgeschwindigkeit", vel)
            dataset.append(vel)
    
        elif name == "Niederschlag":
            down = prepare_value(" (", value)
            down = calc_down(now, down)
            update_data("Niederschlag", down)
            dataset.append(down)
    
        elif name == "Regen":
            value = value.replace("Nein","0")
            value = value.replace("Ja","1")
            rain = prepare_value(" (", value)
            update_data("Regen", rain)
            dataset.append(rain)
            
            file = keys.DIR + str(datetime.datetime.today().strftime("%Y%m%d")) +  '.txt'
            f=open(file,'a')
            logger.info('write to file ' + file)
            print >>f,(dataset)
            f.close()
# 20171029 Sparkfun no longer online            
#            try:
#                urllib2.urlopen("http://data.sparkfun.com/input/" + keys.PUBLIC_KEY + 
#                                "?private_key=" + keys.PRIVATE_KEY + 
#                                "&humidity=" + str(dataset[2]) + 
#                                "&israining=" + str(dataset[5]) + 
#                                "&rainfall=" + str(dataset[4]) + 
#                                "&temp=" + str(dataset[1]) +
#                                "&windspeed=" + str(dataset[3]))
#            except:
#                logger.error("Error sparkfun")
            try:
                save_sql(dataset)
            except Exception as e:
                logger.error("Error MySQL: ", repr(e))
            dataset = []
    
        else:
            logger.info(line)
run()
