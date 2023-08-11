from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date, datetime
from core.entities.comuna_model import Comunas
from rut_chile import rut_chile

class EstadoEnum(models.IntegerChoices):
    SIN_ESTADO  = 0, 'Sin estado'
    ACTIVO      = 1, 'Activo'
    SUSPENDIDO  = 2, 'Suspendido'
    SUSPENDI    = 3, 'Suspendido'


class DominioInglesEnum(models.IntegerChoices):
    SIN_ESTADO = 0, 'Sin estado'
    BASICO     = 1, 'Básico'
    MEDIO      = 2, 'Medio'
    AVANZADO   = 3, 'Avanzado'
    NATIVO     = 4, 'Nativo'
    
class GeneroEnum(models.IntegerChoices):
    MASCULINO = 1, 'Masculino'
    FEMENINO  = 2, 'Femenino'


class Personas(models.Model):
    id               = models.AutoField(primary_key=True, default=0)
    rut              = models.CharField(max_length=15)
    nombre           = models.CharField(max_length=50)
    direccion        = models.CharField(max_length=100)
    comuna           = models.ForeignKey(Comunas, on_delete=models.CASCADE, related_name="persona_comuna")
    telefono         = models.IntegerField()
    correo           = models.CharField(max_length=50)
    sexo             = models.IntegerField(choices=GeneroEnum.choices, default=GeneroEnum.MASCULINO)
    fecha_nacimiento = models.DateField(default=date(2000,1,1))
    anteojos         = models.CharField(max_length=10)
    estado           = models.IntegerField(choices=EstadoEnum.choices, default=EstadoEnum.SIN_ESTADO)
    dominio_ingles   = models.IntegerField(choices=DominioInglesEnum.choices, default=DominioInglesEnum.SIN_ESTADO)
    
    def __str__(self):
        return self.rut
    
    def set_fecha_nacimiento(self, fecha_nacimiento):
        self.fecha_nacimiento = datetime.strptime(fecha_nacimiento,'%d-%m-%Y').date()
    
    def formatted_rut(self):
        return rut_chile.format_capitalized_rut_with_dots(self.rut)
    
   

@receiver(pre_save, sender=Personas)
def format_rut_antes_guardar(sender, instance, **kwargs):
    instance.rut = rut_chile.format_capitalized_rut_with_dots(instance.rut)