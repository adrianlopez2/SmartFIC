# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
import serial
import datetime
import time
from SmartFICApp.models import Ambiente,Ambiente2,AmbienteStats
from pytz import timezone, utc
from django.conf import settings
from django.db.models import Avg,Max,Min
from datetime import timedelta



#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
# Show this when the user types help
	help = "Comando que se ejecuta cada día para inserccion de temperatura maxima y minima del dia."

# A command must define handle()
	def handle(self, *args, **options):	
#filter(Timestamp__range=(datetime.date.today() - timedelta(1), datetime.date.today() )).
		maxT = Ambiente.objects.filter(Timestamp__range=(datetime.date.today() - timedelta(1), datetime.date.today() )).aggregate(Max('Temperatura'),Min('Temperatura'), Avg('Temperatura'))
		maxT2 = Ambiente2.objects.filter(Timestamp__range=(datetime.date.today() - timedelta(1), datetime.date.today() )).aggregate(Max('Temperatura'),Min('Temperatura'), Avg('Temperatura'))
		ambiente = AmbienteStats()
		ambiente.Fecha =datetime.date.today() - timedelta(1)
		ambiente.Zona = '1'
                ambiente.TemperaturaMax = maxT['Temperatura__max']
                ambiente.TemperaturaMin = maxT['Temperatura__min']
		ambiente.TemperaturaMed = maxT['Temperatura__avg']
                ambiente.save()
		self.stdout.write( "Se ha insertado correctamente los valores de la zona 1: Maxima: "+ str(maxT['Temperatura__max'])+" Minima:"+str(maxT['Temperatura__min'])+" Media:" +str(maxT['Temperatura__avg']))
		ambiente = AmbienteStats()
		ambiente.Fecha =datetime.date.today() #- timedelta(1)
		ambiente.Zona = '2'
                ambiente.TemperaturaMax = maxT2['Temperatura__max']
                ambiente.TemperaturaMin = maxT2['Temperatura__min']
		ambiente.TemperaturaMed = maxT2['Temperatura__avg']
                ambiente.save()
		self.stdout.write( "Se ha insertado correctamente los valores de la zona 2: Maxima: "+ str(maxT2['Temperatura__max'])+" Minima:"+str(maxT2['Temperatura__min'])+" Media:" +str(maxT2['Temperatura__avg']))

