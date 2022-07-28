from django.db import models

# Create your models here.
class Estandar(models.Model):
    codigo=models.CharField(max_length=20)
    imagen=models.ImageField(upload_to='imagenes')

class ComentariosEstandar(models.Model):
    codigo=models.ForeignKey(Estandar, on_delete=models.CASCADE)
    numerolinea=models.IntegerField() # * hacer que se autoincremente
    comentario=models.CharField(max_length=20)
