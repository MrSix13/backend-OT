from django.db import connection
from core.views.generic_view import clausula_query
from core.utils.table_query import table_query
import pyexcel as pe

class GenericRepository:
    # Export method

    def listar(
        self,
        query,
    ):
        sql_query = f"{query}"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
        return result
    
    
    def editar(
        self,
        query,
    ):
        sql_query = f"{query}"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
               

    def exportar_a_excel(self, entidad, limit=999):
         entity_info, _ = clausula_query(table_query, entidad, {})

         if not entity_info:
            raise Exception(f"Entidad '{entidad}' no encontrada")

         sql_query = f"{entity_info['query']} LIMIT {limit}"
         with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

         column_headers = entity_info['params']

         data = [column_headers] + [list(item.values()) for item in result]

         sheet_name = entidad.capitalize()

         book = pe.get_book(bookdict={sheet_name: data})
         xls_data = book.save_to_memory("xls")

         return xls_data.getvalue()
        

    # def delete_all(self, entidad, ids):
    #     entity_info = next((item for items in table_query))

    # def create(self, table_name, **data):
    #     columns = ", ".join(data.keys())
    #     placeholders = ", ".join(["%s"] * len(data))
    #     values = tuple(data.values())
    #     sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_query, values)

    # def update(self, table_name, condition_field, condition_value, **data):
    #     set_values = ", ".join([f"{column} = %s" for column in data.keys()])
    #     values = tuple(data.values())
    #     sql_query = f"UPDATE {table_name} SET {set_values} WHERE {condition_field} = %s"
    #     values += (condition_value,)

    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_query, values)
            
                   

    # def delete(self, table_name, condition_field, condition_value):
    #     sql_query = f"DELETE FROM {table_name} WHERE {condition_field} = %s"
    #     values = (condition_value,)

    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_query, values)





    # def delete_all(self, table_name, condition_field, ids):
    #     sql_query = f"DELETE FROM {table_name} WHERE {condition_field} IN ({','.join(['%s'] * len(ids))})"
    #     values = tuple(ids)

    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_query, values)


# CREATE
# INSERT INTO public.core_persona (rut, nombre, direccion, comuna_id, telefono, correo, sexo, fecha_nacimiento, anteojos, estado, dominio_ingles)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

# UPDATE
# query UPDATE public.core_persona SET nombre = %s, comuna_id = %s WHERE rut = %s
# query ('Roberto 2 Alejandro Martinez', 255, '15.827.300-4')


# def listar(
#     self,
#     entidad,
#     condition_field=None,
#     condition_value=None
# ):

#     entity_info = None
#     for query in table_query:
#         if query["table_name"] == entidad:
#             entity_info = query
#             break

#     if not entity_info:
#         return []

#     fields = ", ".join(entity_info["fields"]) if entity_info["fields"] else "*"
#     join = entity_info["join"] if entity_info["join"] else ""
#     where = entity_info["where"] if entity_info["where"] else ""


#     if condition_field and condition_value:
#         sql_query = f"SELECT {fields} FROM {entidad} {join} WHERE {condition_field} = %s {where}"
#         values = (condition_value,)
#     else:
#         sql_query = f"SELECT {fields} FROM {entidad} {join} {where}"
#         values = None

#     with connection.cursor() as cursor:
#         cursor.execute(sql_query, values)
#         result = cursor.fetchall()

#     return result
