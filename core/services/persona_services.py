from core.repositories.persona_repository import PersonaRepository, RegionRepository, ProvinciaRepository, ComunaRepository
from core.entities.persona_model import Persona

class PersonaService:
    def __init__(self):
        self.personas_repository = PersonaRepository()
        
    def get_all_personas(self, limit, offset):
        print('limit:',limit)
        print('offset:', offset)
        return self.personas_repository.get_all_personas(limit=limit, offset=offset)
    
    def get_persona_by_id(self, id):
        persona = self.personas_repository.get_persona_by_id(id)
        if not persona:
            raise ValueError(f"No se encontro ninguna persona con el Rut especificado")
        return persona 
    
    def buscar_persona(self, query, nombre, rut):
        return self.personas_repository.buscar_personas(query, nombre, rut)
    
    
    def create_persona(self, data):
        rut = data['rut']
        nombre = data['nombre']
        direccion = data['direccion']
        comuna_id = int(data['comuna_id'])
        telefono = data['telefono']
        correo = data['correo']
        sexo = data['sexo']
        anteojos = data['anteojos']
        estado = data['estado']
        dominio_ingles = data['dominio_ingles']
        fecha_nacimiento = data['fecha_nacimiento']
        persona = self.personas_repository.create_persona(
            rut=rut,
            nombre=nombre,
            direccion=direccion,
            comuna_id=comuna_id,
            telefono=telefono,
            correo=correo,
            sexo=sexo,
            anteojos=anteojos,
            estado=estado,
            dominio_ingles=dominio_ingles,
            fecha_nacimiento=fecha_nacimiento
        )
        return persona
        
    def update_persona(self, rut,data):
        return self.personas_repository.update_persona(rut, data)
        
    def delete_persona(self, rut):
        persona = self.get_persona_by_rut(rut)
        persona.delete()
    
    
    def delete_all_personas(self, personas_id):
        return self.personas_repository.delete_all_personas(personas_id)
    # def get_all_information():
    #     personas_relacionada = Persona.objects.select_related('comuna__provincia__region').all()
        
    #     for persona in personas_relacionada:
    #         nombre_persona = persona.nombre
    #         nombre_comuna = persona.comuna.nombre
    #         nombre_provicnia = persona.comuna.provicnia.nombre
    #         nombre_region = persona.comuna.provincia.region.nombre
            
    #     return personas_relacionada
        
class RegionService:
    def __init__(self):
        self.region_repository = RegionRepository()
        
    def get_all_regiones(self):
        return self.region_repository.get_all_regions()
    
    def get_region_by_id(self, id):
        return self.region_repository.get_region_by_id(id)
    

class ProvinciaService:
    def __init__(self):
        self.provincia_repository = ProvinciaRepository()
    
    def get_provincia_by_region_id(self, id):
        return self.provincia_repository.get_provincia_by_regionID(id)
    
    def get_provincia_by_id(self,id):
        return self.provincia_repository.get_provncia_by_id(id)
    

class ComunaService:
    def __init__(self):
        self.comuna_repository = ComunaRepository()   
    
    def get_comuna_by_id(self, id):
        return self.comuna_repository.get_comuna_by_id(id)
    
    def get_comuna_by_provincia_id(self, id):
        return self.comuna_repository.get_comuna_by_provinciaID(id)
    
    def get_region_and_provincia_by_id(self, id):
        return self.comuna_repository.get_region_and_provincia_by_id(id)
