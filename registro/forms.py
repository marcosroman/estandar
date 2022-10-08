from django.forms import ModelForm
from django.forms.formsets import formset_factory

from .models import *

class RegistroForm(ModelForm):
    class Meta:
        model = Estandar
        fields = '__all__'

class ComentariosForm(ModelForm):
    class Meta:
        model = Comentarios
        #fields = '__all__'
        exclude = ['codigo']

    def save(self, codigo, commit=True):
        self.instance.codigo = Estandar.objects.get(codigo=codigo)#Estandar.objects.first() #just testing...
        self.instance.save()
        return super(ComentariosForm, self).save(commit=commit)

