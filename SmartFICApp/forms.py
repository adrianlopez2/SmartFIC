from django import forms
from models import Ajustes

class AjustesForm(forms.ModelForm):

	class Meta:
		model = Ajustes
		fields = ('Temperatura', 'Humedad','Dias')
