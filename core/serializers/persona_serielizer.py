from rest_framework import serializers
from core.entities.persona_model import Persona
from core.entities.region_model import Region
from core.entities.provincia_model import Provincia
from core.entities.comuna_model import Comuna
from core.utils.rut_utils import validar_rut
from rut_chile import rut_chile

        
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
    
    
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'    


class PersonaSerializer(serializers.ModelSerializer):
    # rut = serializers.CharField(source="formatted_rut", read_only=True)
    comuna = serializers.CharField(source="comuna.nombre", read_only=True)
    # provincia = serializers.CharField(source="comuna.provincia.nombre", read_only=True)

    
    class Meta:
        model = Persona
        fields = '__all__'
        
    def format_rut(self, instance):
        data = super().format_rut(instance)
        if data.get('rut'):
            data['rut'] = rut_chile.format_rut_without_dots(data['rut'])
        return data        
        