from django.contrib import admin
from core.entities.persona_model import Persona
from core.entities.comuna_model import Comuna
from core.entities.region_model import Region
from .models import User

# Register your models here.

admin.site.register(Persona)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(User)
