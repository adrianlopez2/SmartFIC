from django import forms
from models import Ajustes

#Formulario que cubre los campos
#Temperatura y humedad minima para activar el termostato
#Y numero de ultimos dias a mostrar en el grafico principal
class AjustesForm(forms.ModelForm):

	class Meta:
		model = Ajustes
		fields = ('Temperatura', 'Humedad','Dias')
