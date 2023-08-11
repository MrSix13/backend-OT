from rest_framework import serializers
from core.entities.persona_model import Personas
from core.entities.region_model import Regiones
from core.entities.provincia_model import Provincias
from core.entities.comuna_model import Comunas
from core.utils.rut_utils import validar_rut
from rut_chile import rut_chile

        
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiones
        fields = '__all__'
    
    
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincias
        fields = '__all__'

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunas
        fields = '__all__'    


class PersonaSerializer(serializers.ModelSerializer):
    # rut = serializers.CharField(source="formatted_rut", read_only=True)
    comuna = serializers.CharField(source="comuna.nombre", read_only=True)
    # provincia = serializers.CharField(source="comuna.provincia.nombre", read_only=True)

    
    class Meta:
        model = Personas
        fields = '__all__'
        
    def format_rut(self, instance):
        data = super().format_rut(instance)
        if data.get('rut'):
            data['rut'] = rut_chile.format_rut_without_dots(data['rut'])
        return data        
    