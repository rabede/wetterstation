"""
Book: Building RESTful Python Web Services
Chapter 5: Developing RESTful APIs with Flask
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
class MeasureModel:
    def __init__(self, timestamp, sensor_id, software_version, p10, p2, temperature, humidity, pressure):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.software_version = software_version
        self.p10 = p10
        self.p2 = p2
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
