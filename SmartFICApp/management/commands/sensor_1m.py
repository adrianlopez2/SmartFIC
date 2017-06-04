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
	help = "Comando que guardar en la BD los valores obtenidos cada X tiempo"

# A command must define handle()
	def handle(self, *args, **options):	
		# Open serial port
		ser = serial.Serial(PORT, BAUD_RATE)
		#Inicializacion de variables para evitar posibles errores en las lecturas
		OK = 0
		previo = 0
		percentRH1= 0
		percentRH2 = 0
		tempC1 = 0
		tempC2 = 0
		ambiente = Ambiente1m()
		led1State = Ambiente1m.objects.values_list('Led1State',flat=True)
		led1State = led1State[0]
		led2State = Ambiente1m.objects.values_list('Led2State',flat=True)
		led2State = led2State[0]
		activado = Ambiente1m.objects.values_list('Activado',flat=True)
		activado = activado[0]

		#Borramos el contenido de la tabla para solo tener la medida mas actual
		Ambiente1m.objects.all().delete()
		# Create API object
		xbee = ZigBee(ser,escaped=True)

		#Bucle que espera por los parametros de cada zona
		while OK <> 1:
			try:		
				response = xbee.wait_read_frame()
				if response['id'] == 'rx':
					#print ('ZONA' + str(response['rf_data'][0]))
					zona =response['rf_data'][0]
					if (previo == 0):
						previo = response['rf_data'][0]
						temp = ord(response['rf_data'][2]) + (ord(response['rf_data'][1]) * 256);
						#Conversiones de datos para obtener una medicion estandar
						# a grados centigrados o porcentajes
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

				#Clasificacion de mensajes para obtener debug del estado del paquete
				elif response['id'] == 'tx_status':
					self.stdout.write('TX_STATUS' + str(response))
				else:
					self.stdout.write('PAQUETE DESCONOCIDO')
				
				#Objeto que se insertara en la tabla con los valores de la medicion
				ambiente.Humedad1 = percentRH1
				ambiente.Temperatura1 = tempC1
				ambiente.Humedad2 = 0
				ambiente.Temperatura2 = tempC2
				ambiente.Led1State = led1State
				ambiente.Led2State = led2State
				ambiente.Activado = activado
				
				#Se guardan en la base de datos dichos valores
				ambiente.save()
			except KeyboardInterrupt:
				break
		#Debug por terminal para mostrar posibles errores en las mediciones de los valores
		self.stdout.write('Humedad: '+str(percentRH1) + ' ' + str(percentRH2) +' Temperatura: '+ str(tempC1) +' '+ str(tempC2))

		#Cerramos el serial
		ser.close()
