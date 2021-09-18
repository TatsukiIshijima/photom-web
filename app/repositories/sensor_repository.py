from app.rpz_sensor.rpz_sensor_wrapper import RpzSensorWrapper

class SensorRepository:
    def __init__(self):
        self.rpz_sensor = RpzSensorWrapper()

    def fetch_mock_sensor_data(self):
        return self.rpz_sensor.mock_measure()

    def fetch_sensor_data(self):
        return self.rpz_sensor.measure()