#!/usr/bin/env python3
class AirrohrModel:
    def __init__(self, timestamp, sensor_id, software_version, p10, p2, temperature, humidity, pressure):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.software_version = software_version
        self.p10 = p10
        self.p2 = p2
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        
class SoilMoistureModel:
    def __init__(self, timestamp, temp, hum):
        self.timestamp = timestamp
        self.temperature = temp
        self.humidity = hum
