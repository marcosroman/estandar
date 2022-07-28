from django.urls import path
from . import views

app_name='registro'

urlpatterns = [
        path('', views.registro, name='registro'),
        #path('<str:codigo>', views.vercodigo, name='vercodigo')
        ]
