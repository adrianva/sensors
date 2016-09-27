from __future__ import unicode_literals
from django.db import models


class Signal(models.Model):
    id = models.IntegerField(primary_key=True)
    sensor_id = models.CharField(max_length=20)
    signal_id = models.CharField(max_length=20)
    date = models.DateField()
    date_acquisition = models.DateField()
    value = models.FloatField()

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
