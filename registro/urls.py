from django.urls import path
from . import views

app_name='registro'

urlpatterns = [
        path('', views.buscador, name='buscador'),
        path('nuevo', views.registro, name='registro'),
        #path('comentarios', views.comentarios, name='comentarios'),
        path('comentarios', views.comentarios, name='comentarios'),
        path('codigos',views.EstandarList.as_view(),name='codigos-list'),
        #path('codigos/<slug:codigo>',views.EstandarDetail.as_view(),name='codigos-detalle'),
        path('codigos/<int:pk>',views.EstandarDetail.as_view(),name='codigos-detalle'),
        path('codigos-alt',views.codigos_alt,name='codigos-alt'),
        #path('<str:codigo>', views.vercodigo, name='vercodigo')
        ]
