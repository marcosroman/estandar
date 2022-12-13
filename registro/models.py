from django.db.models import *
from django.contrib.auth.models import User # https://learndjango.com/tutorials/django-best-practices-referencing-user-model

class Categoria(Model):
    categoria = CharField(max_length=50)

    def __str__(self):
        return self.categoria

class Estandar(Model):
    #codigo = models.CharField(max_length=20)
    codigo = SlugField(unique=True)
    imagen = ImageField(upload_to='imagenes/estandar')
    categoria = ForeignKey(Categoria, on_delete=CASCADE)
    autor = ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return self.codigo

class Comentarios(Model):
    codigo=ForeignKey(Estandar, on_delete=CASCADE)
    #numerolinea=models.IntegerField() # * hacer que se autoincremente
    comentario=CharField(max_length=100)
    autor = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        constraints=(
                UniqueConstraint(fields=['codigo','comentario'],
                                        name='unique_comentario'),)

class Plano(Model):
    planoid = AutoField(primary_key=True)
    fecha = DateTimeField()
    ot = IntegerField()
    #vendedor = CharField(max_length=100)
    #cliente = CharField(max_length=100)
    #obra = CharField(max_length=100)
    autor = ForeignKey(User, on_delete=CASCADE)

class DetallePlano(Model):
    planoid = ForeignKey(Plano, on_delete=CASCADE)
    codigo = ForeignKey(Estandar, on_delete=CASCADE)
    tipo  = CharField(max_length=15)
    cantidad = IntegerField()
    ancho_mm = IntegerField()
    alto_mm = IntegerField()
    autor = ForeignKey(User, on_delete=CASCADE)

