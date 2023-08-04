from django.db import models
from .provincia_model import Provincia


class Comuna(models.Model):
    nombre = models.CharField(max_length=64)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name="comuna")
    
    def __str__(self):
        return self.nombre
