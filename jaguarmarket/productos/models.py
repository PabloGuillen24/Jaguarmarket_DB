from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

CARRERAS = [
    ('Medicina', 'Medicina'),
    ('Veterinaria', 'Veterinaria'),
    ('Arquitectura', 'Arquitectura'),
    ('Lenguas', 'Lenguas'),
    ('Derecho', 'Derecho'),
    ('Ingeniería', 'Ingeniería'),
    ('Otra', 'Otra'),
]

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    carrera = models.CharField(max_length=100, blank=True)
    foto     = models.ImageField(upload_to='perfiles/', blank=True, null=True)  


    def clean(self):
        if self.telefono:
            if not re.match(r'^52\d{10,13}$', self.telefono):
                raise ValidationError("El número debe estar en formato internacional (ej. 521234567890).")


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    publicado_por = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
 
 
class Mensaje(models.Model):
    producto     = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='mensajes')
    emisor       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido    = models.TextField()
    timestamp    = models.DateTimeField(auto_now_add=True)
    leido        = models.BooleanField(default=False)    # <-- nuevo campo

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.producto.nombre}] {self.emisor.username} → {self.receptor.username}"

    


    


