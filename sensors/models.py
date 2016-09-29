from __future__ import unicode_literals, division
from django.db import models
import sys
import csv
import re
import datetime


class SignalManager(models.Manager):
    def process_csv(self, csvfile):
        """
        Process the CSV file uploaded by the user. If the signal is temperature, we get the average temperature of
        the day. If it is rainfall, we simply sum all the values of the day.
        :param csvfile: The CSV file object.
        :return: Whether the process ended ok or not.
        """
        try:
            data = {}
            sensor_id, date_acquisition = self.parse_csv_filename(csvfile.name)

            Sensor.objects.create(sensor_id=sensor_id)

            content = csv.reader(csvfile)
            for row in content:
                signal_id = row[0]
                timestamp = row[1]
                value = float(row[2])
                date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

                # If the date and the signal type already exists, we update the values of the day
                if date in data and signal_id in data[date]:
                    data[date][signal_id]["value"] += float(row[2])
                    data[date][signal_id]["n"] += 1
                else:
                    data[date][signal_id] = {"sensor_id": sensor_id,
                                             "date_acquisition": date_acquisition,
                                             "value": value,
                                             "n": 1
                                             }

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
    def calculate_temperature_avg(data):
        for key in data.keys():
            if 'temperature' in data[key]:
                data[key]['temperature']["value"] = data[key]["temperature"]["value"] / data[key]["temperature"]["n"]
        return data

    @staticmethod
    def insert_signals(signals):
        for key, value in signals.items():
            Signal.objects.create(
                sensor_id=value["sensor_id"],
                signal_id=value["signal_id"],
                date=value["date"],
                date_acquisition=key,
                value=value["value"]
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
