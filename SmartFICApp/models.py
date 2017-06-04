from __future__ import unicode_literals
from django.db import models
from django_unixdatetimefield import UnixDateTimeField
import datetime

# Create your models here.

#Recoge los datos medidos en la Zona1
class Ambiente(models.Model):
	Timestamp = models.DateTimeField(default=datetime.datetime.now)
	Temperatura = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad = models.DecimalField(max_digits=5, decimal_places=2)

#Recoge los datos medidos en la Zona2
class Ambiente2(models.Model):
	Timestamp = models.DateTimeField(default=datetime.datetime.now)
	Temperatura = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad = models.DecimalField(max_digits=5, decimal_places=2)

#Informa los datos medidos con un corto periodo de tiempo 
#para simular mediciones en tiempo real, asi como posibles estados necesarios
#Como el estado de Zona1 o Zona2 o si el usuario tiene activado el termostato
class Ambiente1m(models.Model):
	Timestamp = models.DateTimeField(default=datetime.datetime.now)
	Temperatura1 = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad1 = models.DecimalField(max_digits=5, decimal_places=2)
	Temperatura2 = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad2 = models.DecimalField(max_digits=5, decimal_places=2)
	Led1State = models.IntegerField(default = 0)
	Led2State = models.IntegerField(default = 0)
	Activado = models.IntegerField(default = 0)

#Modelo que recoge los agregados de cada dia
class AmbienteStats(models.Model):
	Zona = models.CharField(max_length=10,default=0)
	Fecha = models.DateField(("Date"))
	TemperaturaMax = models.DecimalField(max_digits=5, decimal_places=2)
	TemperaturaMin = models.DecimalField(max_digits=5, decimal_places=2)
	TemperaturaMed = models.DecimalField(max_digits=5, decimal_places=2)

#Modelo que recoge los ajustes del usuario realizados en /ajustes
#Este modelo se usa en el fichero forms.py
class Ajustes(models.Model):
	Temperatura = models.DecimalField(max_digits=5, decimal_places=2)
	Humedad = models.DecimalField(max_digits=5, decimal_places=2)
	Dias = models.IntegerField(default=0)
