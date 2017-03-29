# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import serial
import datetime
import time
from django.shortcuts import render_to_response
from SmartFICApp.models import Ambiente,Ambiente2,AmbienteStats,Ambiente1m,Ajustes
from chartit import DataPool, Chart
from pytz import timezone, utc
from django.conf import settings
from django.db.models import Avg,Max,Min
from datetime import timedelta
from xbee import ZigBee
from django.core.management import call_command
from django.template.context_processors import csrf
from forms import AjustesForm



####
def home(request):
	temperatura = Ambiente1m.objects.values_list('Temperatura1',flat=True)
	humedad = Ambiente1m.objects.values_list('Humedad1',flat=True)
	led1State = Ambiente1m.objects.values_list('Led1State',flat=True)
	activado = Ambiente1m.objects.values_list('Activado',flat=True)
	mediaT = Ambiente.objects.aggregate(Avg('Temperatura'),Avg('Humedad'),Max('Temperatura'),Max('Humedad'),Min('Temperatura'),Min('Humedad'))
 	graf = grafico_ambiente()
	return render_to_response('home.html', {
	'humedad': humedad[0],
	'led1State':led1State[0],
	'activado': activado[0],
	'temperatura': temperatura[0],
	'mediaT': round(mediaT['Temperatura__avg']),
	'mediaH': round(mediaT['Humedad__avg']),
	'maxT': mediaT['Temperatura__max'],
	'maxH': mediaT['Humedad__max'],
	'minT': mediaT['Temperatura__min'],
	'minH': mediaT['Humedad__min'],
	'weatherchart': graf })

def presentacion(request):
        return render_to_response('presentacion.html')

####

def grafico_ambiente():
	#Step 1: Create a DataPool with the data we want to retrieve.
	dias = Ajustes.objects.values_list('Dias',flat=True).order_by("-id")[0]
	if dias == 0 :
		weatherdata = DataPool(
			series=[{'options': {
				'source': Ambiente.objects.all()},
				'terms': [ 'Timestamp','Temperatura','Humedad']
			}]
		)
	else:	
		weatherdata = DataPool(
			series=[{'options': {
				'source': Ambiente.objects.filter(Timestamp__range=(datetime.date.today() - timedelta(dias), datetime.date.today() )).all()},
				'terms': [ 'Timestamp','Temperatura','Humedad']
			}]
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
			chart_options ={'title': {'text': 'Ambiente'},'xAxis': {'title': {'text': 'Dia'} ,'minTickInterval': 20, 'type':'datetime'




		       }}
	)
#Step 3: Send the chart object to the template.
	return cht

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
		'source': AmbienteStats.objects.filter(Zona=1).all()},
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
		'source': AmbienteStats.objects.filter(Zona=1).filter(Fecha__range=(datetime.date.today() - timedelta(7), datetime.date.today() )).all()},
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
		
	return HttpResponse(content_type = "application/json",status = 200)
	
	#xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
	#NODO:   '\x00\x13\xa2\x00@Hl`'  
	#ROUTER: '\x00\x13\xa2\x00@:\x8a\xde'


def ACon(request):
	activado = Ambiente1m.objects.values_list('Activado',flat=True)
	if activado[0] == 0:
		Ambiente1m.objects.all().update(Activado=1)
	else:
		Ambiente1m.objects.all().update(Activado=0)
	call_command('ledAmbiente')
		
	return HttpResponse(content_type = "application/json",status = 200)
	
	#xbee.tx(dest_addr='\x00\x01', data='H',dest_addr_long='\x00\x13\xa2\x00@Hl`')
	#NODO:   '\x00\x13\xa2\x00@Hl`'  
	#ROUTER: '\x00\x13\xa2\x00@:\x8a\xde'

def ajustes(request):
	temp = Ajustes.objects.values_list('Temperatura',flat=True).order_by("-id")[0]
	hum = Ajustes.objects.values_list('Humedad',flat=True).order_by("-id")[0]
	dias = Ajustes.objects.values_list('Dias',flat=True).order_by("-id")[0]
	if request.POST:
		form = AjustesForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/home')
	else:
		form = AjustesForm()

	args = {}
	args.update(csrf(request))
	args['temp'] = temp
	args['hum'] = hum
	args['dias'] = dias
	args['form'] = form
	return render_to_response('ajustes.html', args)

