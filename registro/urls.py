from django.urls import path
from . import views

app_name = 'registro'

urlpatterns = [
        path('', views.inicio, name='inicio'),
        path('ayuda', views.instrucciones, name='instrucciones'),
        path('nuevo/codigo', views.nuevo_codigo, name='nuevo-codigo'),
        path('nuevo/codigo/comentarios', views.nuevo_codigo_comentarios,
             name='nuevo-codigo-comentarios'),
        path('nuevo/plano', views.nuevo_plano, name='nuevo-plano'),
        path('codigos', views.EstandarLista.as_view(),
             name='codigos-listview'),
        path('codigos/<slug>', views.EstandarDetalle.as_view(),
             name='codigos-detailview'),
        path('codigos-porcategoria', views.listacodigosporcategoria,
             name='codigosporcategoria'),
        path('planos', views.plano_lista, name='listaplanos'),
        path('planos/<int:ot>', views.plano_detalle, name='detalleplano'),
        path('catalogo', views.catalogo, name='catalogo'),
        ]
