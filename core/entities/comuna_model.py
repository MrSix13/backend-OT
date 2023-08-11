from django.db import models
from .provincia_model import Provincias


class Comunas(models.Model):
    nombre = models.CharField(max_length=64)
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, related_name="comuna_provincia")
    
    def __str__(self):
        return self.nombre
