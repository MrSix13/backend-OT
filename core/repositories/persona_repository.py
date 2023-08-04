from core.entities.persona_model import Persona, GeneroEnum, EstadoEnum, DominioInglesEnum
from core.entities.region_model import Region
from core.entities.provincia_model import Provincia
from core.entities.comuna_model import Comuna
from core.serializers.persona_serielizer import ComunaSerializer
from core.repositories.generic_repository import GenericDatabaseManager
from rut_chile import rut_chile
from django.db.models import Q
from django.db.models import F
from django.db.models.functions import Cast
from django.db import connection

generic_databaseManager = GenericDatabaseManager()

#Persona
class PersonaRepository:
    def get_persona_by_id(self, id):
        return Persona.objects.get(id=id)
    
    def get_comunas_mapping():
        comunas = Comuna.objects.all().values('nombre', 'id')
        mapeo_comunas = {comuna['nombre']: comuna['id'] for comuna in comunas}
        return mapeo_comunas
        
    def get_all_personas(self, query=None, nombre=None, rut=None, limit=10, offset=0):
        sql_query = """
             SELECT
            persona.id,
            persona.nombre,
            persona.rut,
            persona.direccion,
            persona.telefono,
            persona.correo,
            persona.sexo,
            persona.fecha_nacimiento,
            persona.anteojos,
            persona.estado,
            persona.dominio_ingles,
            comuna.nombre as comuna_nombre,
            provincia.nombre as provincia_nombre,
            region.nombre as region_nombre
            FROM public.core_persona persona
            LEFT JOIN public.core_comuna comuna ON persona.comuna_id = comuna.id
            LEFT JOIN public.core_provincia provincia ON comuna.provincia_id = provincia.id
            LEFT JOIN public.core_region region ON provincia.region_id = region.id 
        
        """
        
        params = []
        conditions = []
        
        if query:
            if nombre:
                conditions.append("persona.nombre ILIKE %s")
                search_query_nombre = f"%{nombre}%"
                params.append(search_query_nombre.lower())
            if rut:
                conditions.append("persona.rut ILIKE %s")
                search_query_rut = f"%{rut}%"
                params.append(search_query_rut.lower())
            if conditions:
                sql_query += " WHERE " + " AND ".join(conditions)

    
        if limit is not None:
            sql_query += " LIMIT %s"
            params.append(limit)

        if offset is not None:
            sql_query += " OFFSET %s"
            params.append(offset)
            
        resultGeneric = generic_databaseManager.list(sql_query, params)
        print('result generico',len(resultGeneric))
            
        # with connection.cursor() as cursor:
        #     cursor.execute(sql_query, params)
        #     result = cursor.fetchall()
            
            
            
            
        personas_data = []
        for col in resultGeneric:
            persona = {
                'id':col[0],
                'nombre': col[1],
                'rut': col[2],
                'direccion': col[3],
                'telefono': col[4],
                'correo': col[5],
                'sexo': col[6],
                'fecha_nacimiento': col[7],
                'anteojos': col[8],
                'dominio_ingles': col[9],
                'estado': col[10],
                'comuna_nombre': col[11],
                'provincia_nombre': col[12],
                'region_nombre': col[13],
            }
            persona['sexo'] = GeneroEnum(persona['sexo']).label
            persona['estado'] = EstadoEnum(persona['estado']).label
            persona['dominio_ingles'] = DominioInglesEnum(persona['dominio_ingles']).label

            personas_data.append(persona)

        return personas_data
        
    
    #Crear Persona
    def create_persona(self, rut, nombre, direccion, comuna_id, telefono, correo, sexo, anteojos, estado, dominio_ingles, fecha_nacimiento):
        persona = Persona(rut=rut,nombre=nombre,direccion=direccion,comuna_id=comuna_id, telefono=telefono, correo=correo, sexo=sexo, anteojos=anteojos, estado=estado, dominio_ingles=dominio_ingles)
        persona.set_fecha_nacimiento(fecha_nacimiento)
        persona.save()
        return persona
    
    
    def buscar_personas(self, query, nombre, rut):
        personas_data = self.get_all_personas(query, nombre, rut)
        return personas_data
         
    
    #Eliminar Persona
    def delete_persona(self, rut):
        persona = self.get_persona_by_rut(rut)
        persona.delete()        
        
    def delete_all_personas(self, personas_id):
        query = f"DELETE FROM public.core_persona WHERE id IN ({','.join(['%s'] * len(personas_id))})"
        with connection.cursor() as cursor:
            cursor.execute(query, personas_id)
              
        
        
        
#Region        
class RegionRepository:
    def get_all_regions(self):
        return Region.objects.all()
    
    
    def get_region_by_id(self, id):
        return Region.objects.get(id = id)

    

#Provincia
class ProvinciaRepository:
    def get_provncia_by_id(self, id):
        return Provincia.objects.get(id = id)
    def get_provincia_by_regionID(self,id):
        return Provincia.objects.filter(region__id = id)



#Comuna
class ComunaRepository:
    def get_comuna_by_provinciaID(self, id):
        return Comuna.objects.filter(provincia__id = id)
    
    def get_comuna_by_id(self, id):
        return Comuna.objects.get(id = id)
    
    def get_region_and_provincia_by_comuna_id(self, id):
        try:
            comuna = Comuna.objects.get(id=id)
            serializer = ComunaSerializer(instance=comuna)
            data = serializer.data
            
            provincia_nombre = data.get('provincia', {}).get('nombre')
            region_nombre = data.get('provincia', {}).get('region', {}).get('nombre')
            
            return {
                "region": region_nombre,
                "provincia": provincia_nombre
            }
        except Comuna.DoesNotExist:
            return None
        
        
        
        
        
        
        
        
#  def get_all_personas(self, query=None, nombre=None, rut=None, limit=10, offset=0):
#         print(indice_final)
#         personas = Persona.objects.select_related('comuna__provincia__region').all().filter(
#             Q(nombre__icontains=query) | Q(rut__icontains=query) if query else Q()
#         ).values(
#                 'nombre',
#                 'rut',
#                 'direccion',
#                 'telefono',
#                 'correo',
#                 'sexo',
#                 'fecha_nacimiento',
#                 'anteojos',
#                 'dominio_ingles',
#                 'estado',
#                 comuna_nombre=F('comuna__nombre'),
#                 provincia_nombre=F('comuna__provincia__nombre'),
#                 region_nombre=F('comuna__provincia__region__nombre')
#         )[indice_inicial:indice_final]
        
#         #[indice_inicio : indice_final]
        
#         for persona in personas:
#             persona['sexo'] = GeneroEnum(persona['sexo']).label
#             persona['estado'] = EstadoEnum(persona['estado']).label
#             persona['dominio_ingles'] = DominioInglesEnum(persona['dominio_ingles']).label

        
#         return personas       