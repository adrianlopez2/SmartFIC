from django.core.management import BaseCommand 
import serial 
import datetime 
import time 
from SmartFICApp.models import Ambiente1m,Ajustes 
from pytz import timezone, utc 
from django.conf import settings 
from xbee import ZigBee 
import struct

#Variable donde se encuentra el nodo COORDINADOR 
PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600



#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
# Show this when the user types help
	help = "Comando para interactuar con el ledAmbiente."

# A command must define handle()
	def handle(self, *args, **options):	
		# Open serial port
		ser = serial.Serial(PORT, BAUD_RATE)
		#Obtenemos los datos para guardar su estado en la siguiente  modificacion
		ambiente = Ambiente1m()
		led2State = Ambiente1m.objects.values_list('Led2State',flat=True)
		led2State = led2State[0]
		activado = Ambiente1m.objects.values_list('Activado',flat=True)
		activado = activado[0]
		hum = Ambiente1m.objects.values_list('Humedad1',flat=True)
		temp = Ambiente1m.objects.values_list('Temperatura1',flat=True)
		# Create API object
		xbee = ZigBee(ser,escaped=True)
		humedad = hum[0]
		temperatura = temp[0]
		temp_min = Ajustes.objects.values_list('Temperatura',flat=True).order_by("-id")[0]
		hum_min = Ajustes.objects.values_list('Humedad',flat=True).order_by("-id")[0]
		
		#Validaciones para comprobar si se cumple la configuracion en la activacion del termostato
		if activado == 1:
			if temperatura < temp_min and humedad > hum_min:
				xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
				Ambiente1m.objects.all().update(Led2State=1)
				self.stdout.write('Encendiendo AC.')
			else:
				xbee.tx(dest_addr='\x00\x01', data='L',dest_addr_long='\x00\x13\xa2\x00@Hl`')
				Ambiente1m.objects.all().update(Led2State=0)
				self.stdout.write('Apagando AC Activado = 1.')
		else:
			xbee.tx(dest_addr='\x00\x01', data='L',dest_addr_long='\x00\x13\xa2\x00@Hl`')
			Ambiente1m.objects.all().update(Led2State=0)
			self.stdout.write('Apagando AC Activado = 0.')

	#xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
	#NODO:   '\x00\x13\xa2\x00@Hl`'  
	#ROUTER: '\x00\x13\xa2\x00@:\x8a\xde'
		
		#Debug en terminal para informar posibles medidas erroneas
		self.stdout.write('Humedad: '+str(hum[0]) + ' Temperatura: '+str(temp[0]))
		self.stdout.write('Humedad_min: '+str(hum_min) + ' Temperatura_min: '+str(temp_min))

		#Cerramos el serial
		ser.close()
