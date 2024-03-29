from django.db.models import *
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model
from django.contrib.auth.models import User
from django.core.validators import *


class Categoria(Model):
    categoria = CharField(max_length=50)

    def __str__(self):
        return self.categoria


class Estandar(Model):
    codigo = SlugField(unique=True)
    imagen = ImageField(upload_to='estandar')
    categoria = ForeignKey(Categoria, on_delete=CASCADE)
    autor = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.codigo


class Comentarios(Model):
    codigo = ForeignKey(Estandar, on_delete=CASCADE)
    comentario = CharField(max_length=100)
    autor = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        constraints = (
                UniqueConstraint(fields=['codigo', 'comentario'],
                                 name='unique_comentario'),)


class Tipos(Model):
    codigo = CharField(max_length=15, unique=True, blank=False)
    descripcion = CharField(max_length=50, blank=False)

    def __str__(self):
        # avoid long descriptions
        descripcion = self.descripcion[:12]  # avoid long descriptions
        if len(self.descripcion) > 12:
            descripcion += "..."
        return self.codigo + " (" + self.descripcion+ ")"


class Plano(Model):
    planoid = AutoField(primary_key=True)
    fecha = DateTimeField()
    ot = IntegerField(validators=[MinValueValidator(0)])
    autor = ForeignKey(User, on_delete=CASCADE)
    ultima_generacion_imagen = DateTimeField(default=None, null=True)


class DetallePlano(Model):
    planoid = ForeignKey(Plano, on_delete=CASCADE)
    codigo = ForeignKey(Estandar, on_delete=CASCADE)
    tipo = ForeignKey(Tipos, on_delete=CASCADE)
    cantidad = IntegerField(validators=[MinValueValidator(1),
                                        MaxValueValidator(20)])
    ancho_mm = IntegerField(validators=[MinValueValidator(100),
                                        MaxValueValidator(4000)])
    alto_mm = IntegerField(validators=[MinValueValidator(100),
                                       MaxValueValidator(4000)])
    comentario = CharField(max_length=30, blank=True, default="")

    class Meta:
        constraints = [
                UniqueConstraint(fields=['planoid', 'codigo', 'tipo',
                                         'ancho_mm', 'alto_mm', 'comentario'],
                                 name='all_unique'),
        ]
