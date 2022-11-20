from django.urls import path
from . import views

app_name='registro'

urlpatterns = [
        path('', views.buscador, name='buscador'),
        path('nuevo/codigo', views.nuevo_codigo, name='nuevo-codigo'),
        path('nuevo/codigo/comentarios', views.nuevo_codigo_comentarios, name='nuevo-codigo-comentarios'),
        path('nuevo/plano', views.nuevo_plano, name='nuevo-plano'),
        path('nuevo/plano/detalle', views.nuevo_plano_detalle, name='nuevo-plano-detalle'),
        path('codigos',views.EstandarLista.as_view(),name='codigos-listview'),
        path('codigos/<slug>',views.EstandarDetalle.as_view(),name='codigos-detailview'),
        #path('codigos-alt',views.codigos_alt,name='codigos-alt'),
        path('codigos-porcategoria',views.listacodigosporcategoria,name='codigosporcategoria'),
        ]
