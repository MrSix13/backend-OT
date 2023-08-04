from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length=50)
    ordinal = models.CharField(max_length=4)
    
    def __str__(self):
        return self.nombre