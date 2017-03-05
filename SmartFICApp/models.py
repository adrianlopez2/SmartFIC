from __future__ import unicode_literals
from django.db import models
from django_unixdatetimefield import UnixDateTimeField
import datetime

# Create your models here.

class Ambiente(models.Model):
	Timestamp = models.DateTimeField(default=datetime.datetime.now)
	Temperatura = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad = models.DecimalField(max_digits=5, decimal_places=2)

class Ambiente2(models.Model):
	Timestamp = models.DateTimeField(default=datetime.datetime.now)
	Temperatura = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad = models.DecimalField(max_digits=5, decimal_places=2)

class Ambiente1m(models.Model):
	Timestamp = models.DateTimeField(default=datetime.datetime.now)
	Temperatura1 = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad1 = models.DecimalField(max_digits=5, decimal_places=2)
	Temperatura2 = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad2 = models.DecimalField(max_digits=5, decimal_places=2)

class AmbienteStats(models.Model):
	Zona = models.CharField(max_length=10,default=0)
	Fecha = models.DateField(("Date"))
	TemperaturaMax = models.DecimalField(max_digits=5, decimal_places=2)
	TemperaturaMin = models.DecimalField(max_digits=5, decimal_places=2)
	TemperaturaMed = models.DecimalField(max_digits=5, decimal_places=2)
