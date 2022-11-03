from django.urls import path
from . import views

app_name='registro'

urlpatterns = [
        path('', views.buscador, name='buscador'),
        path('nuevo', views.registro, name='nuevo-codigo'),
        path('comentarios', views.comentarios, name='comentarios'),
        path('codigos',views.EstandarList.as_view(),name='codigos-listview'),
        path('codigos/<slug>',views.EstandarDetail.as_view(),name='codigos-detailview'),
        path('codigos-alt',views.codigos_alt,name='codigos-alt'),
        path('codigos-porcategoria',views.listacodigosporcategoria,name='codigosporcategoria'),
        ]
