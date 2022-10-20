from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory
from . import models
from . import forms
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

def buscador(request):
    # aca quiero poner algo asi como un buscador...
    '''
    que uno pueda buscar por codigo por ejemplo... lo cual se puede lograr con un dropdown nomas
    tambien podria filtrar por categoria, por ejemplo
    incluso hacer un AND u OR (mostrar los que tengan alguna coincidencia con el codigo y/o con la categoria elegida)
    tambien puede ser buscar por comentarios (y mostrar ahi matches)
    '''
    #if (request.method == "POST"):

    return render(request, template_name="registro/buscador.html")


def registro(request):
    if request.method == "POST":
        form=forms.RegistroForm(request.POST, request.FILES)
        form.fields['imagen'].required=False
        if form.is_valid():
            formtosave=form.save()
            codigo=formtosave.codigo
            formtosave.save()
            url="/comentarios?codigo="+codigo
            return redirect(url)
    else:
        form=forms.RegistroForm()

    return render(request,
                  template_name="registro/nuevo.html",
                  context={'form':form})

def comentarios(request):
    ComentariosFormSet = formset_factory(forms.ComentariosForm)
    codigo=request.GET.get('codigo') 
    if request.method == "POST":
        formset=ComentariosFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save(codigo=codigo)
            return HttpResponseRedirect('/codigos/'+codigo)
    else:
        formset = ComentariosFormSet()
        estandarobj=get_object_or_404(models.Estandar, codigo=codigo)
    
    return render(request,
                  template_name="registro/comentariosformset.html",
                  context={'formset':formset,'codigo':codigo})

class EstandarList(ListView):
    model = models.Estandar

class EstandarDetail(DetailView):
    model = models.Estandar
    # https://stackoverflow.com/questions/68512060/slugfield-not-working-if-field-name-is-different-from-slug
    slug_field = 'codigo'
    
    # https://stackoverflow.com/questions/14936160/django-detailview-how-to-display-two-models-at-same-time#14936328
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = models.Estandar.objects.get(id=context['object'].id).comentarios_set.all()
        return context

def codigos_alt(request):
    return render(request,
                  template_name="registro/codigos-alt.html",
                  context = {'estandar':models.Estandar.objects.all()})
