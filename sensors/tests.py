from django.test import TestCase
from sensors.models import Signal
import reports


class SignalTestCase(TestCase):
    def setUp(self):
        Signal.objects.create(id=1,
                              sensor_id='sensor-1',
                              signal_id='temperature',
                              date='2016-09-20',
                              date_acquisition='2016-09-21',
                              value=32.5)

        Signal.objects.create(id=2,
                              sensor_id='sensor-1',
                              signal_id='temperature',
                              date='2016-09-21',
                              date_acquisition='2016-09-21',
                              value=34.7)

        Signal.objects.create(id=3,
                              sensor_id='sensor-2',
                              signal_id='rain',
                              date='2016-09-21',
                              date_acquisition='2016-09-21',
                              value=34.7)

    def test_convert_to_json(self):
        expected_data = {'dates': ['09-20', '09-21'], 'temperature': [32.5, 34.7], 'signal': 'temperature'}

        signals = Signal.objects.filter(sensor_id='sensor-1')
        report_data = reports.ChartData.convert_data_to_json(signals)

        self.assertEqual(expected_data, report_data)
