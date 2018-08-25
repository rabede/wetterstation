#!/usr/bin/env python3

from datetime import datetime
import requests

from flask import Flask, request
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource

from models import MeasureModel
import status



class MeasureManager():
    
    def __init__(self):
        self.measures = {}

    def insert_measure(self, measure):
        try:
            if measure.sensor_id == '1497627':
                requests.get("https://api.thingspeak.com/update?api_key=TSENL6QISWDJOSK2&field5=" + str(measure.p10)
                         + "&field6=" + str(measure.p2))
        except:
            pass
        
        #self.measures[measure.timestamp] = measure
        
    def get_measure(self, timestamp):
        return self.measures[timestamp]

    def delete_measure(self, timestamp):
        del self.measures[timestamp]


measure_fields = {
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

measure_manager = MeasureManager()


class Measure(Resource):
    
    def abort_if_measure_doesnt_exist(self, timestamp):
        if timestamp not in measure_manager.measures:
            abort(
                status.HTTP_404_NOT_FOUND,
                measure="Measure {0} doesn't exist".format(timestamp))
            
    @marshal_with(measure_fields)
    def get(self, timestamp):
        self.abort_if_measure_doesnt_exist(timestamp)
        return measure_manager.get_measure(timestamp)

    def delete(self, timestamp):
        self.abort_if_measure_doesnt_exist(timestamp)
        measure_manager.delete_measure(timestamp)
        return '', status.HTTP_204_NO_CONTENT


'''
    @marshal_with(measure_fields)
    def patch(self, timestamp):
        self.abort_if_measure_doesnt_exist(timestamp)
        measure = measure_manager.get_measure(timestamp)
        parser = reqparse.RequestParser()
        parser.add_argument('measure', type=str)
        parser.add_argument('duration', type=int)
        parser.add_argument('printed_times', type=int)
        parser.add_argument('printed_once', type=bool)
        args = parser.parse_args()
        if 'measure' in args:
            measure.measure = args['measure']
        if 'duration' in args:
            measure.duration = args['duration']
        if 'printed_times' in args:
            measure.printed_times = args['printed_times']
        if 'printed_once' in args:
            measure.printed_once = args['printed_once']
        return measure
'''

   
class MeasureList(Resource):

    @marshal_with(measure_fields)
    def get(self):
        return [v for v in measure_manager.measures.values()]

    @marshal_with(measure_fields)
    def post(self):
        args = {}
        json_data = request.get_json(force=True)
        args['sensor_id'] = json_data['esp8266id']
        args['software_version'] = json_data['software_version']
        
        for sensor in json_data['sensordatavalues']:
            # print(sensor['value_type'] + ': ' +  sensor['value'])
            args[sensor['value_type']] = sensor['value']

        measure = MeasureModel(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            sensor_id=args['sensor_id'],
            software_version=args['software_version'],
            p10=args['SDS_P1'],
            p2=args['SDS_P2'],
            temperature=args['BME280_temperature'],
            humidity=args['BME280_humidity'],
            pressure=args['BME280_pressure']
            )
        measure_manager.insert_measure(measure) 
        return measure, status.HTTP_201_CREATED   
            

app = Flask(__name__)
api = Api(app)
api.add_resource(MeasureList, '/api/measures/')
api.add_resource(Measure, '/api/measure/<timestamp>', endpoint='measure_endpoint')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
