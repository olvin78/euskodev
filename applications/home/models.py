from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.contrib.auth import get_user_model

from tinymce.models import HTMLField



# Se obtiene el modelo de usuario de Django
User = get_user_model()

class Blog(models.Model):
    """Modelo para entradas de blog."""

    fecha_hora = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='media/img', blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    cuerpo = HTMLField()
    resumen = HTMLField( blank=True,null=True)



    def __str__(self):
        """Devuelve el título del post como representación en cadena."""
        return self.titulo

    def get_summary(self):
        """Devuelve un resumen del cuerpo del post (primeras 200 palabras)."""
        return self.cuerpo[:200]
