from django import forms
from django.contrib.auth.models import User
from models import * 
from django.forms.extras.widgets import SelectDateWidget
import datetime

class RespuestaInlineForm(forms.ModelForm):
    pregunta = forms.ModelChoiceField(queryset = Pregunta.objects.all(), 
                                      widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(RespuestaInlineForm, self).__init__(*args, **kwargs)
        self.fields['respuesta'] = forms.ModelChoiceField(queryset = Opcion.objects.filter(pregunta=self.instance.pregunta), 
                                      widget=forms.RadioSelect(), empty_label=None, required=False)
    
    class Meta:
        model = Respuesta

class EncuestaForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset = User.objects.all(),
                                     widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(EncuestaForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['organizacion'] = forms.ModelChoiceField(queryset = Organizacion.objects.filter(creado_por=self.instance.usuario))
    
    class Meta:
        model = Encuesta

YEAR_CHOICES = ('2009','2010','2011', '2012', '2013','2014', '2015', '2016','2017', '2018', '2019')
hoy = datetime.date.today()

class OrganizacionForm(forms.ModelForm):
    creado_por = forms.ModelChoiceField(queryset = User.objects.all(),
                                     widget=forms.HiddenInput)
    fecha_fundacion = forms.DateField(label="Fecha fundacion",widget=SelectDateWidget(years=YEAR_CHOICES), initial=hoy)

    class Meta:
        model = Organizacion
        widgets = {    
            'municipio' : forms.Select(attrs={'class':'chosen'})
            }

class BuscarForm(forms.Form):
    municipio = forms.ModelChoiceField(queryset = Municipio.objects.all(), required=False)
    tipo = forms.ChoiceField(choices = TIPOS_ORG, required=False)

class BuscarResultadoForm(forms.Form):
    tipo = forms.ChoiceField(choices = TIPOS_ORG, required=False)
    municipio = forms.ModelChoiceField(queryset = Municipio.objects.all(), required=False)

class AdjuntoForm(forms.ModelForm):
    encuesta = forms.ModelChoiceField(queryset = Encuesta.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Adjunto
