import graphene
from graphene_django.types import DjangoObjectType
from core.entities.persona_model import Persona
from core.entities.region_model import Region
from core.entities.provincia_model import Provincia
from core.entities.comuna_model import Comuna

class SexoEnum(graphene.Enum):
    MASCULINO = 1
    FEMENINO  = 2

class EstadoEnum(graphene.Enum):
    SIN_ESTADO = 0
    ACTIVO     = 1
    SUSPENDIDO = 2
    
class DominioInglesEnum(graphene.Enum):
    SIN_ESTADO = 0
    BASICO     = 1
    MEDIO      = 2
    AVANZADO   = 3
    NATIVO     = 4

class PersonaType(DjangoObjectType):
    sexo           = SexoEnum()
    estado         = EstadoEnum()
    dominio_ingles = DominioInglesEnum()
    
    class Meta:
        model = Persona

class RegionType(DjangoObjectType):
    class Meta:
        model = Region
        
class ProvinciaType(DjangoObjectType):
    class Meta:
        model = Provincia

class ComunaType(DjangoObjectType):
    class Meta:
        model = Comuna
        
class Query(graphene.ObjectType):
    all_personas   = graphene.List(PersonaType)
    all_regions    = graphene.List(RegionType)
    all_provincias = graphene.List(ProvinciaType)
    all_comunas    = graphene.List(ComunaType)

    
    def resolve_all_personas(self, info, **kwargs):
        return Persona.objects.all()
    
    def resolve_all_regions(self, info):
        return Region.objects.all()
    
    def resolve_all_provincias(self, info):
        return Provincia.objects.all()
    
    def resolve_all_comunas(self, info):
        return Comuna.objects.all()
    
schema = graphene.Schema(query=Query)
