from django.test import TestCase
from sensors.models import Signal, Sensor
import os
import datetime
import reports


class SignalTestCase(TestCase):
    def setUp(self):
        Signal.objects.create(sensor_id='sensor-1',
                              signal_id='temperature',
                              date='2016-09-20',
                              date_acquisition='2016-09-21',
                              value=32.5)

        Signal.objects.create(sensor_id='sensor-1',
                              signal_id='temperature',
                              date='2016-09-21',
                              date_acquisition='2016-09-21',
                              value=34.7)

        Signal.objects.create(sensor_id='sensor-2',
                              signal_id='rain',
                              date='2016-09-21',
                              date_acquisition='2016-09-21',
                              value=34.7)

    def test_convert_to_json(self):
        expected_data = {'dates': ['09-20', '09-21'], 'temperature': [32.5, 34.7], 'signal': 'temperature'}

        signals = Signal.objects.filter(sensor_id='sensor-1')
        report_data = reports.ChartData.convert_data_to_json(signals)

        self.assertEqual(expected_data, report_data)

    def test_parse_csv_filename(self):
        filename = "sensor1-20092016.csv"

        sensor_id, date = Signal.objects.parse_csv_filename(filename)

        self.assertEqual("sensor1", sensor_id)
        self.assertEqual(datetime.datetime(2016, 9, 20), date)

    def test_process_csv(self):
        os.chdir("tests/")
        with open("test-20092016.csv", "rb") as csvfile:
            Signal.objects.process_csv(csvfile)

        self.assertEqual(True, Sensor.objects.filter(sensor_id="test").count() == 1)

        signal_temperature = Signal.objects.get(signal_id="temperature", date="2016-09-26")
        self.assertEqual(30, signal_temperature.value)

        signal_temperature = Signal.objects.get(signal_id="temperature", date="2016-09-27")
        self.assertEqual(27, signal_temperature.value)

        signal_rainfall = Signal.objects.get(signal_id="rainfall", date="2016-09-26")
        self.assertEqual(400, signal_rainfall.value)

        signal_rainfall = Signal.objects.get(signal_id="rainfall", date="2016-09-27")
        self.assertEqual(480.4, signal_rainfall.value)
