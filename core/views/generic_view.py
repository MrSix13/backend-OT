from functools import wraps
from django.db import IntegrityError
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.repositories.generic_repository import GenericRepository
from core.utils.table_query import table_query

generic_repository = GenericRepository()


def clausula_query(table_query, entidad, setInputValues):
    entidad_info = next(
        (item for item in table_query if item["entidad"] == entidad), None
    )
    

    if entidad_info:
        default_table = entidad_info["def"]
        
        
        print('setInputValues', setInputValues)
        entidad_info["query"] = entidad_info["query"+setInputValues["query"]]
        
        
        
        for index, (campo0) in enumerate(entidad_info["params"]):
            found = False

            for name, value in setInputValues.items():
                if campo0 == name:
                    entidad_info["query"] = entidad_info["query"].replace(name, value)
                    found = True
                    break
            if not found:
                entidad_info["query"] = entidad_info["query"].replace(
                    campo0, default_table[index]
                )
    print("entidad_info", entidad_info["query"])
                
    return table_query


def with_entidad(metodo):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, entidad, *args, **kwargs):
            entity_info = None
            
            for query in table_query:
                if query["entidad"] == entidad:
                    entity_info = query
                    break

            if not entity_info:
                return Response(
                    {"error": "Entidad no encontrada"},
                    status=status.HTTP_404_NOT_FOUND,
                )
                
                
            if request.content_type == 'application/json':
                setInputValues = request.data
            else:
                setInputValues = request.query_params.dict()



            campos_busqueda = {
                campo: valor for campo, valor in setInputValues.items() if campo != "q"
            }
            
            
            clausula_query(table_query, entidad, campos_busqueda)   
            generic_repository = GenericRepository()
            
            try:
                datos = metodo(
                    generic_repository,
                    entity_info.get("query")
                )
                return view_func(request, entidad, datos, *args, **kwargs)
            
            except Exception as e:
                print(e)
                error_message = str(e)
                return Response(
                    {"error": error_message},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return _wrapped_view

    return decorator


@api_view(["GET"])
@with_entidad(metodo=GenericRepository.listar)
def listar_view(request, entidad, datos):
    try:
        print('datos', datos)
        return Response(datos, status=status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return Response(
            {"Error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
     
@api_view(['POST'])
@with_entidad(metodo=GenericRepository.editar)
def crear(request, entidad, datos):
    try:
        return Response({"mensaje": "Creado correctamente"}, status= status.HTTP_200_OK)
    except Exception as e:
        error_message= str(e)
        return Response({"error:":error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      
@api_view(['DELETE'])
@with_entidad(metodo=GenericRepository.editar)
def eliminar():
    try:
        return Response({"mensaje": "Eliminado correctamente"}, status= status.HTTP_200_OK)
    except IntegrityError as e:
        error_message = str(e)
        print('Error de integridad:', error_message)
        return Response({"error": "No se puede eliminar debido a restricciones de integridad"}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        error_message = str(e)
        print('error:', error_message)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@with_entidad(metodo=GenericRepository.editar)
def editar():
    try:
            return Response({"mensaje": "Edición realizada exitosamente"})
    except Exception as e:
        error_message= str(e)
        return Response({"error:":error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@with_entidad(metodo=GenericRepository.exportar_a_excel)
def crear_archivo_xls_view(request, entidad, datos):
    try:
        limit = 50 #VARIABLE PARA CREAR PAGINACION

        xls_data = datos(entidad, limit)

        response = HttpResponse(xls_data, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f"attachment; filename={entidad}.xls"
        return response
    except Exception as e:
          error_message= str(e)
          return Response({"error:":error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




