from __future__ import unicode_literals
from django.db import models
import csv
import re
import datetime


class SignalManager(models.Manager):
    def process_csv(self, csvfile):
        try:
            sensor_id, date_acquisition = self.parse_csv_filename(csvfile.name)

            Sensor.objects.create(sensor_id=sensor_id)

            content = csv.reader(csvfile)
            for row in content:
                signal_id = row[0]
                timestamp = row[1]
                date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
                value = row[2]

                Signal.objects.create(
                    sensor_id=sensor_id,
                    signal_id=signal_id,
                    date=date,
                    date_acquisition=date_acquisition,
                    value=value
                )
        except AttributeError:
            return "error"

    def parse_csv_filename(self, csv_fileaname):
        filename_regexp = re.search('(.*)-(\d{2}\d{2}\d{4})\.csv', csv_fileaname)  # Regexp for <sensor_id>-<ddmmyyyy>.csv

        if filename_regexp:
            signal_id = filename_regexp.group(1)
            date_acquisition = filename_regexp.group(2)

            return signal_id, date_acquisition

        raise AttributeError


class Signal(models.Model):
    id = models.IntegerField(primary_key=True)
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
