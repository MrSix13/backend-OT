import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from rut_chile import rut_chile
from core.services.persona_services import PersonaService,RegionService, ProvinciaService, ComunaService
from core.serializers.persona_serielizer import PersonaSerializer, RegionSerializer, ProvinciaSerializer, ComunaSerializer
from core.entities.comuna_model import Comunas
from core.entities.persona_model import Personas,GeneroEnum,EstadoEnum,DominioInglesEnum
from django.core.serializers import serialize
from core.repositories.generic_repository import GenericDatabaseManager
import pyexcel as pe

persona_service = PersonaService()
region_service = RegionService()
provincia_service = ProvinciaService()
comuna_service = ComunaService()


generic_db_manager = GenericDatabaseManager()

table_name = "public.core_personas"

#Personas
@api_view(['POST'])
def crear_archivo_xls(request):
    
    limit = int(request.data.get('limit', request.GET.get('limit', 999)))
    print('limit excel',limit)
    offset = 0
    personas_todas = persona_service.get_all_personas(limit, offset)
    encabezados = list(personas_todas[0].keys())
    datos_personas = [encabezados] + [[persona[key] for key in encabezados] for persona in personas_todas]
    
    
    
    book_personas = pe.get_book(bookdict={"Personas": datos_personas })
    xls_data = book_personas.save_to_memory("xls")
     
    response = HttpResponse(xls_data.getvalue(),content_type="application/vnd.ms-excel")

    response["Content-Disposition"] = "attachment; filename=archivo.xls"

    return response


@api_view(['GET'])
def obtener_personas_relacionadas(request):
    try:
        page_number =  int(request.GET.get('page',1))
        num_paginas = page_number
        elementos_por_pagina=10
            
        offset = (num_paginas - 1) * elementos_por_pagina
        limit = num_paginas * elementos_por_pagina

        
        personas = persona_service.get_all_personas(limit,offset)
    
       #repositorio generico
        return Response(list(personas), status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e);
        return Response({"Error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def obtener_todas_personas():
    try:
        limit = 999 #Cambiar mas adelante por tabla parametro
        offset = 0
        
        personas_todas = persona_service.get_all_personas(limit, offset)
        return Response(list(personas_todas), status=status.HTTP_200_OK)   
    except Exception as e:
        error_message = str(e)
        return Response({"Error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['POST'])
def personas_create(request):
    try:
        rut = request.data.get('rut')
        if rut_chile.is_valid_rut(rut):
            # nueva_persona = persona_service.create_persona(request.data)
            # serializer = PersonaSerializer(nueva_persona)
            generic_db_manager.create(table_name,**request.data)
            return Response({"Mensaje":"Persona creada correctamente"}, status=status.HTTP_200_OK)
        return Response({"Error":"Rut Invalido"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        error_message = str(e)
        print(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def personas_update(request, id):
    try:
        persona = persona_service.get_persona_by_id(id)
        rut = persona.rut  
        
        comuna_id = request.data.get('comuna_id')
        comuna = None
        
        if comuna_id is not None:
            try:
                comuna_id = int(comuna_id)
                comuna = Comunas.objects.get(id=comuna_id)
            except comuna.DoesNotExist:
                return Response({"Error": "La comuna especificada no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        data_to_update = {}
        field_to_update = list(request.data.keys())
        for field in field_to_update:
            if field in ['nombre', 'direccion', 'comuna_id', 'telefono', 'correo', 'sexo', 'anteojos', 'estado', 'dominio_ingles']:
                data_to_update[field] = request.data[field]
                
        if comuna_id is not None:
            data_to_update['comuna_id'] = comuna_id
        
        generic_db_manager.update(table_name, 'rut', rut, **data_to_update)
        
        return Response({"message": "Persona actualizada correctamente."}, status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def personas_buscar(request):
    try:
        query = request.query_params.get('q', None)
        nombre = request.query_params.get('nombre', None)
        rut = request.query_params.get('rut', None)
        
        print('nombre', nombre)
        print('rut', rut)
        
        # if not query:
        #     return Response({"Error":"Debe proporcionar un termino de busqueda valido"})
        personas = persona_service.buscar_persona(query,nombre, rut)
        return Response(list(personas), status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"Error":error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
@api_view(['POST'])
def persona_delete(request):
    try:
        # persona = persona_service.get_persona_by_rut(rut)
        # persona.delete()
        persona_id = request.data.get('idDelete',[])
        generic_db_manager.delete(table_name,'id', persona_id)
        
        
        return Response({"Mensaje":"Persona eliminada correctamente"},status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({'error': error_message}, status= status.HTTP_500_INTERNAL_SERVER_ERROR) 
    

@api_view(['POST'])    
def personas_all_delete(request):
    try:
        personas_ids = request.data.get('idsDelete',[])
        print('ids para eliminar',personas_ids)

        generic_db_manager.delete_all(table_name,'id', personas_ids)
        return Response({"mensaje":"Personas Eliminadas correctamente"})
    except Exception as e:
        error_message = str(e)
        return Response({"error": error_message}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

#Regiones
@api_view(['GET'])
def regiones_list(request):
    try:
        regiones = region_service.get_all_regiones()
        serializer = RegionSerializer(regiones, many=True)
        return Response(serializer.data,status= status.HTTP_200_OK )
    except Exception as e:
        error_message = str(e)
        return Response({"Error":error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def region_by_id(request, id):
    try:
        region = region_service.get_region_by_id(id)
        serializer = RegionSerializer(region)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"error":error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Provincias
@api_view(['GET'])
def provincias_list(request, id):
    try:
        provincias = provincia_service.get_provincia_by_region_id(id)
        serializer = ProvinciaSerializer(provincias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def provincia_by_id(request,id):
    try:
        provincia = provincia_service.get_provincia_by_id(id)
        serialier = ProvinciaSerializer(provincia)
        return Response(serialier.data,status = status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def region_provincia_by_comuna_id(request, id):
    try:
        result = comuna_service.get_region_and_provincia_by_id(id)
        comuna = Comunas(**result)
        serializer = ComunaSerializer(comuna)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"Error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Comuas
@api_view(['GET'])
def comunas_list_by_provinciaID(request, id):
    try:
        comunas = comuna_service.get_comuna_by_provincia_id(id)
        serializer =  ComunaSerializer(comunas, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"Error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def comunas_by_id(request,id):
    try:
        comuna = comuna_service.get_comuna_by_id(id)
        serializer = ComunaSerializer(comuna)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"Error":error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


