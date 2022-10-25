from django.urls import path
from . import views

app_name='registro'

urlpatterns = [
        path('', views.buscador, name='buscador'),
        path('nuevo', views.registro, name='registro'),
        path('comentarios', views.comentarios, name='comentarios'),
        path('codigos',views.EstandarList.as_view(),name='codigos-list'),
        path('codigos/<slug>',views.EstandarDetail.as_view(),name='codigos-detalle'),
        path('codigos-alt',views.codigos_alt,name='codigos-alt'),
        path('codigos-porcategoria',views.listacodigosporcategoria,name='codigosporcategoria'),
        ]
