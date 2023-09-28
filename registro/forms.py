import base64
from django import forms
from django.forms import ModelForm, Form, widgets
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.files.base import ContentFile
from .models import *


class PastedImageWidget(widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:  # though it's always None so far
            html = "<img id='id_imagen' alt='(ctrl+v p/ pegar)'/>"
        else:
            html = "<img id='id_imagen' src='%s'/>" % value
        return mark_safe(html)


class RegistroForm(ModelForm):
    imagen_container = forms.CharField(required=False,
                                       widget=forms.HiddenInput())

    class Meta:
        model = Estandar
        exclude = ['autor']
        widgets = {'imagen': PastedImageWidget()}

    # need this to complain in case no 'imagen' is pasted
    def clean(self):
        # https://github.com/twoscoops/two-scoops-of-django-1.8/issues/64
        # (this is the right way to check fields, when auto-check is off)
        cleaned_data = super(RegistroForm, self).clean()
        imagen_container = cleaned_data.get("imagen_container")
        if imagen_container == "":
            self.add_error('imagen_container', 'Agregar imagen!')

    def save(self, commit=True):
        self.instance.imagen.delete(False)
        self.instance.codigo = self.instance.codigo.lower()  # force lowercase
        imgdata = self.cleaned_data['imagen_container'].split(',')
        try:
            ftype = imgdata[0].split(';')[0].split('/')[1]
            fname = slugify(self.instance.codigo)
            self.instance.imagen.save(
                    '%s.%s' % (fname, ftype),
                    ContentFile(
                        base64.decodebytes(bytes(imgdata[1], 'utf-8'))))
        except:
            raise 
            print('could not save file!')
        return super(RegistroForm, self).save(commit=commit)


class ComentariosForm(ModelForm):
    class Meta:
        model = Comentarios
        exclude = ['codigo', 'autor']

    def save(self, codigo, commit=True):
        self.instance.codigo = Estandar.objects.get(codigo=codigo)
        self.instance.save()
        return super(ComentariosForm, self).save(commit=commit)


# used in self-made list-view to show codigos...
# to filter by category and-or (un)select show-images
class FilterCodigosForm(Form):
    mychoices = [('All', 'Mostrar Todos')]
    try:
        mychoices.extend(list(zip(Categoria.objects.all(),
                                  Categoria.objects.all())))
    except:
        pass
    filtro = forms.ChoiceField(widget=forms.Select(
                                             attrs={'onchange': 'submit()'}),
                               choices=mychoices)
    # https://tuts-station.com/django-form-checkbox-validation-example.html
    mostrarimagenes = forms.BooleanField(label='Mostar imagenes?',
                                         required=False,
                                         widget=forms.CheckboxInput(
                                             attrs={'onchange': 'submit()'}))


class PlanoForm(ModelForm):
    class Meta:
        model = Plano
        exclude = ['fecha', 'autor', 'ultima_generacion_imagen']


class DetallePlanoForm(ModelForm):
    class Meta:
        model = DetallePlano
        exclude = ['planoid', 'autor']
        # https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/#overriding-the-default-fields
        labels = {'comentario': 'Comentario (opcional)'}
        widgets = {'tipo': forms.Select(attrs={"class": "tipo-select"})}
