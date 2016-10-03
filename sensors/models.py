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
        self.timestamp = None
        self.date = None
        self.date_acquisition = None
        self.value = None

    def __eq__(self, other):
        return self.signal_id == other.signal_id and self.sensor_id == other.sensor_id \
               and self.timestamp == other.timestamp


class SignalTotal:
    def __init__(self):
        self.signal_id = ""
        self.sensor_id = ""
        self.date = None
        self.date_acquisition = None
        self.total = None
        self.n = 1


class SignalManager(models.Manager):
    def process_multiple_csv(self, csvfiles):
        """
        Process the CSV files uploaded by the user. If the signal is temperature, we get the average temperature of
        the day. If it is rainfall, we simply sum all the values of the day.
        :param csvfiles: The CSV files objects.
        :return: Whether the process ended ok or not.
        """
        try:
            data = []
            for csvfile in csvfiles:
                data = self.remove_duplicated_rows(csvfile, data)

            signals = self.obtain_totals(data)
            #data = self.calculate_temperature_avg(data)
            self.insert_signals(signals)

            return "success"
        except AttributeError:
            print(sys.exc_info())
            return "error"

    def remove_duplicated_rows(self, csvfile, data):
        """
        Remove the duplicated rows in the CSV file. One row is duplicated when another one exists with the same
        signal, timestamp and sensor ID. When this happens we keep the most recent data
        :param csvfile: The csv file to be processed
        :param data: The data we have already processed
        :return: The new data
        """
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
            signal_from_csv.timestamp = row[1]
            signal_from_csv.date = datetime.datetime.fromtimestamp(int(signal_from_csv.timestamp)).strftime('%Y-%m-%d')

            if not data:
                data.append(signal_from_csv)
            else:
                found = False
                for signal in data:
                    # If the data already exists we keep the most recent value
                    if signal_from_csv == signal and signal_from_csv.date_acquisition >= signal.date_acquisition:
                        signal.value = signal_from_csv.value
                        found = True
                if not found:
                    data.append(signal_from_csv)
        return data

    def obtain_totals(self, signal_measurements):
        signals = []
        for signal in signal_measurements:
            signal_with_totals = SignalTotal()
            signal_with_totals.signal_id = signal.signal_id
            signal_with_totals.sensor_id = signal.sensor_id
            signal_with_totals.date = signal.date
            signal_with_totals.date_acquisition = signal.date_acquisition
            signal_with_totals.total = signal.value

            if not signals:
                signals.append(signal_with_totals)
            else:
                found = False
                for element in signals:
                    # If the date and the signal type already exists, we update the values of the day
                    if element.date == signal_with_totals.date and element.signal_id == signal_with_totals.signal_id:
                        element.total += signal_with_totals.total
                        element.n += 1
                        found = True
                if not found:
                    signals.append(signal_with_totals)

        signals = self.calculate_temperature_avg(signals)
        return signals

    @staticmethod
    def parse_csv_filename(csv_filename):
        """
        Parse the name of the CSV file un order to get the signal id (temperature, rainfall, etc.) and
        the acquisition date of the data.
        :param csv_filename: The name of the CSV file
        :return: signal_id, date_acquisition

        """
        # Regexp for <sensor_id>-<ddmmyyyy>.csv
        filename_regexp = re.search('(.*)-(\d{2}\d{2}\d{4})\.csv', csv_filename)

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
                signal.total /= float(signal.n)
        return signals

    @staticmethod
    def insert_signals(signals):
        for signal in signals:
            Signal.objects.create(
                sensor_id=signal.sensor_id,
                signal_id=signal.signal_id,
                date=signal.date,
                date_acquisition=signal.date_acquisition,
                value=signal.total
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
