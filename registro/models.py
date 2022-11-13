from django.db.models import *

class Categoria(Model):
    categoria = TextField()

    def __str__(self):
        return self.categoria

class Estandar(Model):
    #codigo = models.CharField(max_length=20)
    codigo = SlugField(unique=True)
    imagen = ImageField(upload_to='imagenes')
    categoria = ForeignKey(Categoria, on_delete=CASCADE)
    
    def __str__(self):
        return self.codigo


class Comentarios(Model):
    codigo=ForeignKey(Estandar, on_delete=CASCADE)
    #numerolinea=models.IntegerField() # * hacer que se autoincremente
    comentario=CharField(max_length=100)

    class Meta:
        constraints=(
                UniqueConstraint(fields=['codigo','comentario'],
                                        name='unique_comentario'),)

class Plano(Model):
    planoid = AutoField(primary_key=True)
    fecha = DateTimeField(default=0)
    vendedor = TextField()

class DetallePlano(Model):
    planoid = ForeignKey(Plano, on_delete=CASCADE)
    codigo = ForeignKey(Estandar, on_delete=CASCADE)
    cantidad = IntegerField()
    ancho_mm = IntegerField()
    alto_mm = IntegerField()

