from django.core.management import BaseCommand
import serial
import datetime
import time
from SmartFICApp.models import Ambiente1m
from pytz import timezone, utc
from django.conf import settings
from xbee import ZigBee
import struct
 
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
		self.stdout.write(str(humedad))
		if activado == 1:
			if temperatura < 13 and humedad > 60 and led2State == 0:
				xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
				Ambiente1m.objects.all().update(Led2State=1)
				self.stdout.write('Encendiendo AC.')
		else:
			xbee.tx(dest_addr='\x00\x01', data='L',dest_addr_long='\x00\x13\xa2\x00@Hl`')
			Ambiente1m.objects.all().update(Led2State=0)
			self.stdout.write('Apagando AC.')

	#xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
	#NODO:   '\x00\x13\xa2\x00@Hl`'  
	#ROUTER: '\x00\x13\xa2\x00@:\x8a\xde'

		self.stdout.write('Humedad: '+str(hum[0]) + ' Temperatura: '+str(temp[0]))
		ser.close()
