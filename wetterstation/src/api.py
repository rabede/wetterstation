#!/usr/bin/env python3

from datetime import datetime
import logging

from flask import Flask, request
from flask_restful import abort, Api, fields, marshal_with, Resource
import requests

import keys
from models import AirrohrModel, SoilMoistureModel
import status


logging.basicConfig(filename= keys.DIR + 'api.log', 
                    level=logging.WARN,
                    format='[%(asctime)s] %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p')
                    
class AirrohrManager():
    
    def __init__(self):
        self.measures = {}

    def insert_measure(self, measure):
        logging.info(measure.sensor_id + ' empfangen')
        logging.debug("Airrohr.inseart_measure: " + str(measure))
        try:
            if measure.sensor_id == '1497627':
                requests.get("https://api.thingspeak.com/update?api_key=TSENL6QISWDJOSK2&field5=" + str(measure.p10)
                         + "&field6=" + str(measure.p2))
        except:
            pass
       
    def get_measure(self, timestamp):
        logging.debug("Airrohr.get_measure: " + str(self.measures))
        return self.measures[timestamp]

    def delete_measure(self, timestamp):
        logging.debug("Airrohr.delete_measure: " + str(self.measures))
        del self.measures[timestamp]

airrohr_fields = {
    'timestamp': fields.String,
    'sensor_id': fields.Integer,
    'uri': fields.Url('measure_endpoint'),
    'software_version': fields.String,
    'p10': fields.Float,
    'p2': fields.Float,
    'temperature': fields.Float,
    'humidity': fields.Float,
    'pressure': fields.Float
}

airrohr_manager = AirrohrManager()

class Airrohr(Resource):
    
    def abort_if_measure_doesnt_exist(self, timestamp):
        if timestamp not in airrohr_manager.measures:
            abort(
                status.HTTP_404_NOT_FOUND,
                measure="Airrohr {0} doesn't exist".format(timestamp))
            
    @marshal_with(airrohr_fields)
    def get(self, timestamp):
        logging.debug("Airrohr.get " + str(self.measures))
        self.abort_if_measure_doesnt_exist(timestamp)
        return airrohr_manager.get_measure(timestamp)

    def delete(self, timestamp):
        logging.debug("Airrohr.delete: " + str(self.measures))
        self.abort_if_measure_doesnt_exist(timestamp)
        airrohr_manager.delete_measure(timestamp)
        return '', status.HTTP_204_NO_CONTENT

class AirrohrList(Resource):

    @marshal_with(airrohr_fields)
    def get(self):
        logging.debug("AirrohrList.get: " + str(airrohr_manager.measures.values()))
        return [v for v in airrohr_manager.measures.values()]

    @marshal_with(airrohr_fields)
    def post(self):
        args = {}
        json_data = request.get_json(force=True)
        logging.debug("AirrohrList.post: " + str(json_data))
        args['sensor_id'] = json_data['esp8266id']
        args['software_version'] = json_data['software_version']
        
        for sensor in json_data['sensordatavalues']:
            logging.info(sensor['value_type'] + ': ' +  sensor['value'])
            args[sensor['value_type']] = sensor['value']

        try:
            temperature=args['BME280_temperature']
        except:
            temperature=None
        try:
            humidity=args['BME280_humidity']
        except:
            humidity=None
        try:
            pressure=args['BME280_pressure']            
        except:
            pressure=None         

        measure = AirrohrModel(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            sensor_id=args['sensor_id'],
            software_version=args['software_version'],
            p10=args['SDS_P1'],
            p2=args['SDS_P2'],
            temperature=temperature,
            humidity=humidity,
            pressure=pressure
        )
        airrohr_manager.insert_measure(measure) 
        return measure, status.HTTP_201_CREATED   

class MoistureManager():
    
    def __init__(self):
        self.measures = {}

    def insert_measure(self, measure):
        try:
            if measure.sensor_id == '1497627':
                requests.get("https://api.thingspeak.com/update?api_key=TSENL6QISWDJOSK2&field5=" + str(measure.p10)
                         + "&field6=" + str(measure.p2))
        except:
            pass

moisture_fields = {
    'timestamp': fields.String,
    'temperature': fields.Float,
    'humidity': fields.Float,
}

moisture_manager = MoistureManager()

class MoistureList(Resource):

    @marshal_with(moisture_fields)
    def get(self):
        logging.debug("MoistureList.get: " + str(moisture_manager.measures.values()))
        return [v for v in moisture_manager.measures.values()]

    @marshal_with(moisture_fields)
    def post(self):
        args = {}
        json_data = request.get_json(force=True)
        logging.debug("MoistureList.post: " + str(json_data))
        args['sensor_id'] = json_data['esp8266id']
        args['software_version'] = json_data['software_version']
        
        for sensor in json_data['sensordatavalues']:
            # print(sensor['value_type'] + ': ' +  sensor['value'])
            args[sensor['value_type']] = sensor['value']

        measure = AirrohrModel(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            temperature=args['BME280_temperature'],
            humidity=args['BME280_humidity'],
            )
        moisture_manager.insert_measure(measure) 
        return measure, status.HTTP_201_CREATED

app = Flask(__name__)
api = Api(app)
api.add_resource(AirrohrList, '/api/measures/')
api.add_resource(Airrohr, '/api/measure/<timestamp>', endpoint='measure_endpoint')

api.add_resource(MoistureList, '/api/soilmoisture/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)    logging.info('Start Server')