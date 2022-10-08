from django.db import models

class Categoria(models.Model):
    categoria = models.TextField()

    def __str__(self):
        return self.categoria

class Estandar(models.Model):
    #codigo = models.CharField(max_length=20)
    codigo = models.SlugField()
    imagen = models.ImageField(upload_to='imagenes')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.codigo

    class Meta:
        constraints=(models.UniqueConstraint(fields=['codigo'],name='unique_codigo'),)

class Comentarios(models.Model):
    codigo=models.ForeignKey(Estandar, on_delete=models.CASCADE)
    #numerolinea=models.IntegerField() # * hacer que se autoincremente
    comentario=models.CharField(max_length=100)

    class Meta:
        constraints=(models.UniqueConstraint(fields=['codigo','comentario'], name='unique_comentario'),)
