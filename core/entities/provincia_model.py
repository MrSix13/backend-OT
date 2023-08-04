from django.db import models
from .region_model import Region

class Provincia(models.Model):
    nombre  = models.CharField(max_length=64)
    region = models.ForeignKey(Region,on_delete=models.CASCADE, related_name='provincia')
    
    def __str__(self):
        return self.nombre
