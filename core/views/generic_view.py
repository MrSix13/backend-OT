from functools import wraps
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.repositories.generic_repository import GenericDatabaseManager
from core.utils.table_query import table_query

generic_db_manager = GenericDatabaseManager()


def clausula_query(table_query, entidad, setInputValues):
    entidad_info = next(
        (item for item in table_query if item["entidad"] == entidad), None
    )

    if entidad_info:
        default_table = entidad_info["def"]
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
                
                
            setInputValues = request.query_params.dict()
            campos_busqueda = {
                campo: valor for campo, valor in setInputValues.items() if campo != "q"
            }
            clausula_query(table_query, entidad, campos_busqueda)   
            generic_db_manager = GenericDatabaseManager()
            try:
                datos = metodo(
                    generic_db_manager,
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
@with_entidad(metodo=GenericDatabaseManager.listar)
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
@with_entidad(metodo=GenericDatabaseManager.listar)
def eliminar(request,entidad, datos):
    try:
        
        
        print("data", datos)
      
        return Response({"mensaje": "Cargo eliminadas correctamente"}, status= status.HTTP_200_OK)
    except Exception as e:
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@api_view(["POST"])
@parser_classes([JSONParser])
@with_entidad(metodo=GenericDatabaseManager.create)
def crear_view(request, entidad, datos):
    try:
        print("nuevo dato", request.data)
        nuevo_dato = request.data
        generic_db_manager.create(f"public.core_{entidad}", **nuevo_dato)
        # datos.create(f"public.core_{entidad}", **nuevo_dato)
        return Response(status=status.HTTP_201_CREATED)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return Response(
            {"Error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# DECORADOR MOVER A ARCHIVO GENERAL
# def with_entidad(metodo):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, entidad, *args, **kwargs):
#             generic_db_manager = (
#                 GenericDatabaseManager()
#             )  # Crea una instancia de GenericDatabaseManager
#             table_name = f"public.core_{entidad}"
#             try:
#                 datos = metodo(generic_db_manager, table_name)
#                 return view_func(request, entidad, datos, *args, **kwargs)
#             except Exception as e:
#                 print(e)
#                 error_message = str(e)
#                 return Response(
#                     {"Error": error_message},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 )

#         return _wrapped_view

#     return decorator


# # listar listo
# @api_view(["GET"])
# @with_entidad(metodo=GenericDatabaseManager.listar)
# def listar_view(request, entidad, datos):
#     return Response(list(datos), status=status.HTTP_200_OK)


# @api_view(['POST'])
# def crear(request):
#     try:
#         generic_db_manager.create(table_name, **request.data)
#         return Response({"Mensaje": "Creado correctamente"}, status= status.HTTP_201_CREATED)
#     except Exception as e:
#         error_message = str(e)
#         return Response({"error": error_message}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# @with_entidad
# def eliminar_cargo(request):
# try:
#     funcionalidad_id = request.data.get('idDelete',[])
#     generic_db_manager.delete(table_name, 'id', funcionalidad_id)
#     return Response({"Mensaje":"Cargo eliminada correctamente"},  status= status.HTTP_200_OK)
# except Exception as e:
#     error_message = srt(e)
#     return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def eliminar_cargo(request):
#     try:
#         funcionalidad_id = request.data.get('idDelete',[])
#         generic_db_manager.delete(table_name, 'id', funcionalidad_id)
#         return Response({"Mensaje":"Cargo eliminada correctamente"},  status= status.HTTP_200_OK)
#     except Exception as e:
#         error_message = srt(e)
#         return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# def listar_cargos(request):
#     try:
#         funcionalidades = generic_db_manager.listar(table_name, None, None)
#         return Response(list(funcionalidades), status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         error_message = str(e)
#         return Response({"Error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @api_view(['PATCH'])
# def editar_cargo(request, id):
#     try:
#         # print('request', request.data) request {'description': 'editado'}
#         # return Response({'hola mundo', id})
#         generic_db_manager.update(table_name,'id', id, **request.data)
#         return Response({"mensaje":"Cargo editada correctamente"})
#     except Exception as e:
#         error_message = str(e)
#         print(error_message)
