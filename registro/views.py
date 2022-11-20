from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import models
from . import forms

def buscador(request):
    # aca quiero poner algo asi como un buscador...
    '''
    que uno pueda buscar por codigo por ejemplo... lo cual se puede lograr con un dropdown nomas
    tambien podria filtrar por categoria, por ejemplo
    incluso hacer un AND u OR (mostrar los que tengan alguna coincidencia con el codigo y/o con la categoria elegida)
    tambien puede ser buscar por comentarios (y mostrar ahi matches)
    '''

    return render(request, template_name='registro/buscador.html')

def nuevo_codigo(request):
    if request.method == "POST":
        form=forms.RegistroForm(request.POST, request.FILES)
        form.fields['imagen'].required=False
        if form.is_valid():
            formtosave=form.save()
            codigo=formtosave.codigo
            formtosave.save()
            url=reverse("registro:nuevo-codigo-comentarios")+"?codigo="+codigo
            return redirect(url)
    else:
        form=forms.RegistroForm()

    return render(request,
                  template_name="registro/nuevo-codigo.html",
                  context={'form':form})

def nuevo_codigo_comentarios(request):
    ComentariosFormSet = formset_factory(forms.ComentariosForm)
    codigo=request.GET.get('codigo') 
    if request.method == "POST":
        formset=ComentariosFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save(codigo=codigo)
            return HttpResponseRedirect(reverse("registro:codigos-detailview",args=[codigo]))
    else:
        formset = ComentariosFormSet()
        estandarobj=get_object_or_404(models.Estandar, codigo=codigo)
    
    return render(request,
                  template_name="registro/nuevo-codigo-comentarios.html",
                  context={'formset':formset,
                           'codigo':codigo})

# another view, little pics included
def codigos_alt(request):
    return render(request,
                  template_name="registro/codigos-alt.html",
                  context = {'estandar':models.Estandar.objects.all()})

def listacodigosporcategoria(request):
    # dirty but works... refactor later (20221030)
    if request.method == "POST":
        filtro_value=request.POST.get('filtro')
        if(filtro_value=="All"): # all categories
            categorias = models.Categoria.objects.all()
            codigos = dict(zip(categorias,
                               map(lambda x: x.estandar_set.all(),
                                   categorias)))
        else: # one category
            categoria=models.Categoria.objects.get(categoria=filtro_value)
            codigos=dict([(categoria,
                           categoria.estandar_set.all())])
        codigosfilter=forms.FilterCodigosForm(request.POST)
        showimages=request.POST.get('mostrarimagenes')
    else: # start
        categorias=models.Categoria.objects.all()
        codigosfilter=forms.FilterCodigosForm()

        codigos=dict(zip(categorias,
                         map(lambda x: x.estandar_set.all(),
                              categorias)))
        showimages=False # hardcoded for now

    return render(request,
                  template_name="registro/listacodigos.html",
                  context = {'codigos':codigos,
                             'selectfilter':codigosfilter,
                             'showimages':showimages})

def nuevo_plano(request):
    if request.method == "POST":
        form=forms.PlanoForm(request.POST, request.FILES)
        #form_detalle=forms.DetallePlanoForm(request.POST, request.FILES)
        #form.fields['imagen'].required=False
        #if form_inicial.is_valid():
        #formtosave=form.save()
        #planoid=formtosave.planoid
        #formtosave.save()
        #url=reverse("registro:nuevo-plano-detalle")+"?planoid="+planoid
        #return redirect(url)
    else:
        form=forms.PlanoForm()

    return render(request,
                  template_name="registro/nuevo-plano.html",
                  context={'form':form})

def nuevo_plano_detalle(request):
    DetallePlanoFormSet = formset_factory(forms.DetallePlanoForm)
    #codigo=request.GET.get('codigo') 
    if request.method == "POST":
        formset=DetallePlanoFormSet(request.POST)
        #if formset.is_valid():
        #    for form in formset:
        #        form.save()#codigo=codigo)
        #        #return HttpResponseRedirect('/codigos/'+codigo)
    else:
        formset = DetallePlanoFormSet()
        #estandarobj=get_object_or_404(models.Estandar, codigo=codigo)
    
    return render(request,
                  template_name="registro/nuevo-plano-detalle.html",
                  context={'formset':formset})#,'codigo':codigo})

class EstandarLista(ListView):
    model = models.Estandar

class EstandarDetalle(DetailView):
    model = models.Estandar
    # https://stackoverflow.com/questions/68512060/slugfield-not-working-if-field-name-is-different-from-slug
    slug_field = 'codigo'
    
    # https://stackoverflow.com/questions/14936160/django-detailview-how-to-display-two-models-at-same-time#14936328
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = models.Estandar.objects.get(id=context['object'].id).comentarios_set.all()
        return context


