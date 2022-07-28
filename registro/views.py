from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.list import ListView

from . import models
from . import forms

# Create your views here.
def registro(request):
    if request.method == "POST":
        form=forms.RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save().save()
            return HttpResponseRedirect('/')
    else:
        form=forms.RegistroForm()

    return render(request,
                  template_name="registro/index.html",
                  context={'form':form})

