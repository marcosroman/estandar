from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone # to fix the "received a naive datetime" warning
# -> https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime#20106079
from . import models
from . import forms
from django.conf import settings

def buscador(request):
    # aca quiero poner algo asi como un buscador...
    '''
    que uno pueda buscar por codigo por ejemplo... lo cual se puede lograr con un dropdown nomas
    tambien podria filtrar por categoria, por ejemplo
    incluso hacer un AND u OR (mostrar los que tengan alguna coincidencia con el codigo y/o con la categoria elegida)
    tambien puede ser buscar por comentarios (y mostrar ahi matches)
    '''

    return render(request, template_name='registro/buscador.html')

@login_required
def nuevo_codigo(request):
    if request.method == "POST":
        form=forms.RegistroForm(request.POST, request.FILES)
        form.fields['imagen'].required=False
        if form.is_valid():
            form.instance.autor=request.user
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

@login_required
def nuevo_codigo_comentarios(request):
    ComentariosFormSet = formset_factory(forms.ComentariosForm)
    codigo=request.GET.get('codigo') 
    if request.method == "POST":
        formset=ComentariosFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.instance.autor=request.user
                form.save(codigo=codigo)
            return HttpResponseRedirect(reverse("registro:codigos-detailview",
                                        args=[codigo]))
    else:
        formset = ComentariosFormSet()
        estandarobj=get_object_or_404(models.Estandar, codigo=codigo)
    
    return render(request,
                  template_name="registro/nuevo-codigo-comentarios.html",
                  context={'formset':formset,
                           'codigo':codigo})

@login_required
def nuevo_plano(request):
    if request.method == "POST":
        form=forms.PlanoForm(request.POST)
        if form.is_valid():
            form.instance.autor=request.user
            form.instance.fecha=datetime.now(tz=timezone.utc)
            formtosave=form.save()
            planoid=formtosave.planoid
            formtosave.save()
            url=reverse("registro:nuevo-plano-detalle")+"?planoid="+str(planoid)
            return redirect(url)
    else:
        form=forms.PlanoForm()

    return render(request,
                  template_name="registro/nuevo-plano.html",
                  context={'form':form})

@login_required
def nuevo_plano_detalle(request):
    DetallePlanoFormSet = formset_factory(forms.DetallePlanoForm)
    planoid=int(request.GET.get('planoid'))
    print("planoid is "+str(planoid))
    if request.method == "POST":
        formset=DetallePlanoFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.instance.planoid=models.Plano.objects.get(planoid=planoid)
                form.instance.autor=request.user

                form.fields['comentario'].required=False
                form.save().save()
            return HttpResponseRedirect("/")
                # form.save()#codigo=codigo)
                # return HttpResponseRedirect('/codigos/'+codigo)
            # generate each 'plano' image...!!!
            # then add them up...!
            # then redirect to the view (showing the image and the details below in table form :D) 
    else:
        formset = DetallePlanoFormSet()
        #estandarobj=get_object_or_404(models.Estandar, codigo=codigo)
    
    return render(request,
                  template_name="registro/nuevo-plano-detalle.html",
                  context={'formset':formset})#,'codigo':codigo})


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
                             'showimages':showimages,
                             'MEDIA_URL':settings.MEDIA_URL})

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

from .utils import generarplanos

# here i'm gonna add a funtionview for plano
# it will list all ot's and link to the last
# plano that was created (highest planoid)
# (so 2 url families here, /plano and /plano/<ot>)
# for the current user

# and maybe if there's no plano, it will render the first one

# in /plano/<ot> i'll add a 'generate plano' button
# (in case there are updates or things needed to be corrected)

# and the controller should also check if there's no such image to create it,
# i guess
# but maybe not necessary since it would be created after the data is saved
# so yes, check or generating at start is not needed
@login_required
def plano_lista(request):
    ots = models.Plano.objects.filter(autor
                                      =request.user.id).values('ot').distinct()

    # no estoy seguro de que esto funcione... ver de cerca primero
    print('request.user =',request.user)
    print('request.user.id =',request.user.id)
    return render(request,
                  template_name="registro/listaplanos.html",
                  context = {'ots':ots})

from .utils import generarplanos
@login_required
def plano_detalle(request, ot):
    plano=models.Plano.objects.filter(ot=ot,autor=request.user.id).first()
    plano_detalle=models.DetallePlano.objects.filter(planoid=plano.planoid)

    # use submit button to regenerate (save again) the plano image
    #if request.method == "GET":
    #print("REGENERAR IMAGEN")
    # REGENERAR IMAGEN
    # ?should i get a plano image check (to see if any exists)
    #print("settings.MEDIA_URL:",settings.MEDIA_URL)
    #print("settings.MEDIA_ROOT:",settings.MEDIA_ROOT)
    generarplanos.generate_and_save_plano(plano.planoid,
                                          plano_detalle,
                                          settings.MEDIA_URL+"/estandar", #input_images_url,
                                          settings.MEDIA_ROOT+"/estandar", #input_images_folder,
                                          settings.MEDIA_ROOT+"/planos")
    # PENDING: SHOULD ALSO CHECK CONDTIONS (MAX GLASSES=20, MAX_WIDHT HEIGHT, ETC (we can add these checks later))

    return render(request,
                  template_name="registro/detalleplano.html",
                  context = {'ot':ot,
                             'plano':plano,
                             'plano_detalle':plano_detalle})

def inicio(request):
    return render(request, 
                  template_name='registro/base.html')

def instrucciones(request):
    return render(request, 
                  template_name='registro/instrucciones.html',
                  context = {'MEDIA_URL':settings.MEDIA_URL})

def catalogo(request):
    return redirect (settings.MEDIA_URL+'/catalogo.pdf')
    
