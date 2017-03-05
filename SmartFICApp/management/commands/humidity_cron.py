# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
import serial
import datetime
import time
from SmartFICApp.models import Ambiente,Ambiente2
from pytz import timezone, utc
from django.conf import settings
from xbee import ZigBee
import struct
 
PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
# Show this when the user types help
	help = "Comando que se ejecuta cada X tiempo para inserccion de la tabla que usara el HighChart."

# A command must define handle()
	def handle(self, *args, **options):	
		# Open serial port
		ser = serial.Serial(PORT, BAUD_RATE)
		OK = 0
		previo = 0
		percentRH1= 0
		percentRH2 = 0
		tempC1 = 0
		tempC2 = 0
		# Create API object
		xbee = ZigBee(ser,escaped=True)
		while OK <> 1:
			try:		
				response = xbee.wait_read_frame()
				if response['id'] == 'rx':
					#print ('ZONA' + str(response['rf_data'][0]))
					zona =response['rf_data'][0]
					if (previo == 0):
						previo = response['rf_data'][0]
						temp = ord(response['rf_data'][2]) + (ord(response['rf_data'][1]) * 256);
						voltageT = temp * 5.0
						voltageT /= 1024.0
						if response['rf_data'][0] == '1':
							value2 =  ord(response['rf_data'][4]) + (ord(response['rf_data'][3]) * 256);
							voltage = (value2/1023.0)*5.0
							percentRH1 = (voltage - 0.788) / 0.0314	
							tempC1 = (voltageT - 0.5) * 100 
						else:
							tempC2 = (voltageT - 0.5) * 100 
					elif ((previo <> zona)):
						temp = ord(response['rf_data'][2]) + (ord(response['rf_data'][1]) * 256);
						voltageT = temp * 5.0
						voltageT /= 1024.0
						if response['rf_data'][0] == '1':
							value2 =  ord(response['rf_data'][4]) + (ord(response['rf_data'][3]) * 256);
							voltage = (value2/1023.0)*5.0
							percentRH1 = (voltage - 0.788) / 0.0314	
							tempC1 = (voltageT - 0.5) * 100 
						else:
							tempC2 = (voltageT - 0.5) * 100 
						OK = 1

				elif response['id'] == 'tx_status':
					self.stdout.write('TX_STATUS' + str(response))
				else:
					self.stdout.write('PAQUETE DESCONOCIDO')

			except KeyboardInterrupt:
				break
		ambiente = Ambiente()
		ambiente.Humedad = percentRH1
		ambiente.Temperatura = tempC1
		ambiente.save()
		ambiente2 = Ambiente2()
		ambiente2.Humedad = 0
		ambiente2.Temperatura = tempC2
		ambiente2.save()
		self.stdout.write('Humedad: '+str(percentRH1) + ' ' + str(percentRH2) +' Temperatura: '+ str(tempC1) +' '+ str(tempC2))
		ser.close()
