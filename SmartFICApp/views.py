from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import serial
import datetime
import time
from django.shortcuts import render_to_response
from SmartFICApp.models import Ambiente,Ambiente2,AmbienteStats,Ambiente1m
from chartit import DataPool, Chart
from pytz import timezone, utc
from django.conf import settings
from django.db.models import Avg,Max,Min
from datetime import timedelta
from xbee import ZigBee


####

def home(request):
	temperatura = Ambiente1m.objects.values_list('Temperatura1',flat=True)
	humedad = Ambiente1m.objects.values_list('Humedad1',flat=True)
	led1State = Ambiente1m.objects.values_list('Led1State',flat=True)
	mediaT = Ambiente.objects.aggregate(Avg('Temperatura'),Avg('Humedad'),Max('Temperatura'),Max('Humedad'),Min('Temperatura'),Min('Humedad'))
 	graf = grafico_ambiente()
	return render_to_response('home.html', {
	'humedad': humedad[0],
	'led1State':led1State[0],
	'temperatura': temperatura[0],
	'mediaT': round(mediaT['Temperatura__avg']),
	'mediaH': round(mediaT['Humedad__avg']),
	'maxT': mediaT['Temperatura__max'],
	'maxH': mediaT['Humedad__max'],
	'minT': mediaT['Temperatura__min'],
	'minH': mediaT['Humedad__min'],
	'weatherchart': graf })

def prueba(request):
        return render_to_response('prueba.html')

####

def grafico_ambiente():
		#ts = Ambiente.objects.get()
#Step 1: Create a DataPool with the data we want to retrieve.
	weatherdata = DataPool(
		series=[
		{'options': 
		{
		'source': Ambiente.objects.all()},
		'terms': [ 'Timestamp','Temperatura','Humedad']
		}
		#,
		#{'options': {
        #'source': Ambiente2.objects.all()},
        #'terms': [{'am2_Timestamp': 'Timestamp'},{'am2_Temperatura': 'Temperatura'}]
		#}
		]
	)
#Step 2: Create the Chart object
	cht = Chart(
		datasource = weatherdata,
			series_options =[{'options':{
				'type': 'line','stacking': False},
				'terms':{
						'Timestamp':['Temperatura','Humedad']
						#,'am2_Timestamp':['am2_Temperatura']
						}}],
			chart_options ={'title': {'text': 'Ambiente'},'xAxis': {'title': {'text': 'Dia'}}}
	)
#Step 3: Send the chart object to the template.
	return cht

#######################################
#######################################

def utcisoformat(dt):
    #Return a datetime object in ISO 8601 format in UTC, without microseconds
    #or time zone offset other than 'Z', e.g. '2011-06-28T00:00:00Z'.
    # Convert datetime to UTC, remove microseconds, remove timezone, convert to string
	TZ = timezone(settings.TIME_ZONE)
	return TZ.localize(dt.replace(microsecond=0)).astimezone(utc).replace(tzinfo=None).isoformat() + 'Z'

#######################################
#######################################
def maxmin(request):
	graf = grafico_maxmin()
	return render_to_response('maxmin.html', {
		'weatherchart': graf
		})

def maxmin7dias(request):
 	graf7dias = grafico_maxmin_7dias()
	return render_to_response('maxmin.html', {
		'weatherchart': graf7dias 
		})

def grafico_maxmin():
#Step 1: Create a DataPool with the data we want to retrieve.
	weatherdata = DataPool(
		series=[{'options': {
		'source': AmbienteStats.objects.all()},
		'terms': [ 'Fecha','TemperaturaMax','TemperaturaMin','TemperaturaMed']
		}
		]
	)
#Step 2: Create the Chart object
	cht = Chart(
		datasource = weatherdata,
			series_options =[{'options':{
				'type': 'line','stacking': False},
				'terms':{'Fecha': ['TemperaturaMax','TemperaturaMin','TemperaturaMed']}}],
			chart_options ={'title': {'text': 'Temperatura Max-Min-Med'},'xAxis': {'title': {'text': 'Dia'}},'yAxis': {'title': {'text': ' '}}}
	)
#Step 3: Send the chart object to the template.
	return cht

def grafico_maxmin_7dias():
#Step 1: Create a DataPool with the data we want to retrieve.
	weatherdata = DataPool(
		series=[{'options': {
		'source': AmbienteStats.objects.filter(Fecha__range=(datetime.date.today() - timedelta(7), datetime.date.today() )).all()},
		'terms': [ 'Fecha','TemperaturaMax','TemperaturaMin','TemperaturaMed']
		}
		]
	)
#Step 2: Create the Chart object
	cht = Chart(
		datasource = weatherdata,
			series_options =[{'options':{
				'type': 'column','stacking': False},
				'terms':{'Fecha': ['TemperaturaMax','TemperaturaMin','TemperaturaMed']}}],
			chart_options ={'title': {'text': 'Temperatura Max-Min-Med'},'xAxis': {'title': {'text': 'Dia'}},'yAxis': {'title': {'text': ' '}}}
	)
#Step 3: Send the chart object to the template.
	return cht


#############################################################################################
#ACTUADORES#
#############################################################################################
def on(request):
	ambiente = Ambiente1m()
	PORT = '/dev/ttyUSB0'
	BAUD_RATE = 9600
	led1State = Ambiente1m.objects.values_list('Led1State',flat=True)
	# Open serial port
	ser = serial.Serial(PORT, BAUD_RATE)
	# Create API object
	xbee = ZigBee(ser,escaped=True)
	print led1State
	if led1State[0] == 0:
		xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@:\x8a\xde')
		Ambiente1m.objects.all().update(Led1State=1)
	else:
		xbee.tx(dest_addr='\x00\x01', data='L',dest_addr_long='\x00\x13\xa2\x00@:\x8a\xde')
		Ambiente1m.objects.all().update(Led1State=0)
		
	return HttpResponse( content_type = "application/json",status = 200)
	#time.sleep(3)
	#xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@:\x8a\xde')
		
	
	#xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
	#NODO:   '\x00\x13\xa2\x00@Hl`'  
	#ROUTER: '\x00\x13\xa2\x00@:\x8a\xde'

def off(request):
	PORT = '/dev/ttyUSB0'
	BAUD_RATE = 9600
	# Open serial port
	ser = serial.Serial(PORT, BAUD_RATE) 
	# Create API object
	xbee = ZigBee(ser,escaped=True)
	xbee.tx(dest_addr='\x00\x01', data='L',dest_addr_long='\x00\x13\xa2\x00@:\x8a\xde')	
	ambiente = Ambiente1m()	
	Ambiente1m.objects.all().update(Led1State=0)
	#xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
	#NODO:   '\x00\x13\xa2\x00@Hl`'  
	#ROUTER: '\x00\x13\xa2\x00@:\x8a\xde'


