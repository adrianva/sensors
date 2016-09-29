from __future__ import unicode_literals, division
from django.db import models, IntegrityError, transaction
import sys
import csv
import re
import datetime


class SignalCSV:
    def __init__(self):
        self.signal_id = ""
        self.sensor_id = ""
        self.date = None
        self.date_acquisition = None
        self.value = None
        self.n = 1


class SignalManager(models.Manager):
    def process_csv(self, csvfile):
        """
        Process the CSV file uploaded by the user. If the signal is temperature, we get the average temperature of
        the day. If it is rainfall, we simply sum all the values of the day.
        :param csvfile: The CSV file object.
        :return: Whether the process ended ok or not.
        """
        try:
            data = []
            sensor_id, date_acquisition = self.parse_csv_filename(csvfile.name)

            try:
                with transaction.atomic():
                    Sensor.objects.create(sensor_id=sensor_id)
            except IntegrityError:
                pass

            content = csv.reader(csvfile)
            for row in content:
                signal_from_csv = SignalCSV()
                signal_from_csv.signal_id = row[0]
                signal_from_csv.sensor_id = sensor_id
                signal_from_csv.date_acquisition = date_acquisition
                signal_from_csv.value = float(row[2])
                timestamp = row[1]
                signal_from_csv.date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

                if not data:
                    data.append(signal_from_csv)
                else:
                    for signal in data:
                        # If the date and the signal type already exists, we update the values of the day
                        if signal.date == signal_from_csv.date and signal.signal_id == signal_from_csv.signal_id:
                            signal.value += signal_from_csv.value
                            signal.n += 1
                        else:
                            data.append(signal_from_csv)

            data = self.calculate_temperature_avg(data)
            self.insert_signals(data)

            return "success"
        except AttributeError:
            print(sys.exc_info())
            return "error"

    @staticmethod
    def parse_csv_filename(csv_filename):
        """
        Parse the name of the CSV file un order to get the signal id (temperature, rainfall, etc.) and
        the acquisition date of the data.
        :param csv_filename: The name of the CSV file
        :return: signal_id, date_acquisition

        """
        filename_regexp = re.search('(.*)-(\d{2}\d{2}\d{4})\.csv', csv_filename)  # Regexp for <sensor_id>-<ddmmyyyy>.csv

        if filename_regexp:
            signal_id = filename_regexp.group(1)
            date_acquisition = filename_regexp.group(2)
            date_acquisition = datetime.datetime.strptime(date_acquisition, '%d%m%Y')

            return signal_id, date_acquisition

        raise AttributeError

    @staticmethod
    def calculate_temperature_avg(signals):
        for signal in signals:
            if signal.signal_id == "temperature":
                signal.value /= float(signal.n)
        return signals

    @staticmethod
    def insert_signals(signals):
        for signal in signals:
            Signal.objects.create(
                sensor_id=signal.sensor_id,
                signal_id=signal.signal_id,
                date=signal.date,
                date_acquisition=signal.date_acquisition,
                value=signal.value
            )


class Signal(models.Model):
    sensor_id = models.CharField(max_length=20)
    signal_id = models.CharField(max_length=20)
    date = models.DateField()
    date_acquisition = models.DateField()
    value = models.FloatField()

    objects = SignalManager()

    class Meta:
        db_table = "signal"


class Sensor(models.Model):
    sensor_id = models.CharField(max_length=20, primary_key=True)

    class Meta:
        db_table = "sensor"


class SignalType(models.Model):
    signal_type = models.CharField(max_length=20, primary_key=True)

    class Meta:
        db_table = "signal_type"
