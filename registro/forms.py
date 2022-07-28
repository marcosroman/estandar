from django.forms import ModelForm
from django.forms.formsets import formset_factory

from .models import *

class RegistroForm(ModelForm):
    class Meta:
        model = Estandar
        fields = '__all__'

class ComentariosEstandarForm(ModelForm):
    class Meta:
        model = ComentariosEstandar
        fields = '__all__'


#RegistroFormSet = formset_factory(Estandar,ComentariosEstandar,form=ComentariosEstandarForm)
RegistroFormSet = formset_factory(ComentariosEstandar)


