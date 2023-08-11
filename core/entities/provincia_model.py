from django.db import models
from .region_model import Regiones

class Provincias(models.Model):
    nombre  = models.CharField(max_length=64)
    region = models.ForeignKey(Regiones,on_delete=models.CASCADE, related_name='provincia_region')
    
    def __str__(self):
        return self.nombre
