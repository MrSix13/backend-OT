from django.contrib import admin
from core.entities.persona_model import Personas
from core.entities.comuna_model import Comunas
from core.entities.region_model import Regiones
from core.entities.permisos_model import Usuarios, Cargos


# Register your models here.

admin.site.register(Personas)
admin.site.register(Comunas)
admin.site.register(Regiones)
admin.site.register(Usuarios)
admin.site.register(Cargos)
# admin.site.register(Permisos)
# admin.site.register(Cargo)

