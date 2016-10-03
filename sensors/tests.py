from django.test import TestCase
from django.conf import settings
from sensors.models import Signal, Sensor
import os
import datetime
import reports


class SignalTestCase(TestCase):
    def test_convert_to_json(self):
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

        expected_data = {'dates': ['09-20', '09-21'], 'temperature': [32.5, 34.7], 'signal': 'temperature'}

        signals = Signal.objects.filter(sensor_id='sensor-1')
        report_data = reports.ChartData.convert_data_to_json(signals)

        self.assertEqual(expected_data, report_data)

    def test_parse_csv_filename(self):
        filename = "sensor1-20092016.csv"

        sensor_id, date = Signal.objects.parse_csv_filename(filename)

        self.assertEqual("sensor1", sensor_id)
        self.assertEqual(datetime.datetime(2016, 9, 20), date)

    def test_process_csv(self):  # Test where we upload 1 csv file
        os.chdir(settings.BASE_DIR + "/tests/")

        with open("test-20092016.csv", "rb") as csvfile:
            Signal.objects.process_multiple_csv([csvfile])

        self.assertEqual(True, Sensor.objects.filter(sensor_id="test").count() == 1)

        signal_temperature = Signal.objects.get(signal_id="temperature", date="2016-09-26")
        self.assertEqual(30, signal_temperature.value)

        signal_temperature = Signal.objects.get(signal_id="temperature", date="2016-09-27")
        self.assertEqual(27, signal_temperature.value)

        signal_rainfall = Signal.objects.get(signal_id="rainfall", date="2016-09-26")
        self.assertEqual(400, signal_rainfall.value)

        signal_rainfall = Signal.objects.get(signal_id="rainfall", date="2016-09-27")
        self.assertEqual(240.2, signal_rainfall.value)

    def test_process_multiple_csv(self):  # Test where we upload ,ultiple csv files
        os.chdir(settings.BASE_DIR + "/tests/")
        files = []

        with open("test-20092016.csv", "rb") as csvfile_1, open("test-19092016.csv", "rb") as csvfile_2:
            files.append(csvfile_1)
            files.append(csvfile_2)

            Signal.objects.process_multiple_csv(files)

        self.assertEqual(True, Sensor.objects.filter(sensor_id="test").count() == 1)

        signal_temperature = Signal.objects.get(signal_id="temperature", date="2016-09-26")
        self.assertEqual(25, signal_temperature.value)

        signal_rainfall = Signal.objects.get(signal_id="rainfall", date="2016-09-28")
        self.assertEqual(381, signal_rainfall.value)