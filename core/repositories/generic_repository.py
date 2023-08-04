from django.db import connection

class GenericDatabaseManager:
    #Export method
    
    
    
    
    
    def list(self, sql_query, params=None):
        
        with connection.cursor() as cursor:
            cursor.execute(sql_query, params)
            result = cursor.fetchall()
        return result
    
    def create(self, table_name, **data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s']*len(data))
        values = tuple(data.values())
        sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            
    def update(self, table_name, condition_field, condition_value, **data):
        set_values = ', '.join([f"{column} = %s" for column in data.keys()])
        values = tuple(data.values())
        sql_query = f"UPDATE {table_name} SET {set_values} WHERE {condition_field} = %s"
        values += (condition_value,)
          
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
        
    def delete(self, table_name, condition_field, condition_value):
        sql_query = f"DELETE FROM {table_name} WHERE {condition_field} = %s"
        values = (condition_value,)  
        
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)  
            
  
    def delete_all(self, table_name, condition_field, ids):
        sql_query = f"DELETE FROM {table_name} WHERE {condition_field} IN ({','.join(['%s'] * len(ids))})"
        values = tuple(ids)
        
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            
            
            
            
            
            
            
#CREATE
# INSERT INTO public.core_persona (rut, nombre, direccion, comuna_id, telefono, correo, sexo, fecha_nacimiento, anteojos, estado, dominio_ingles) 
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

#UPDATE
# query UPDATE public.core_persona SET nombre = %s, comuna_id = %s WHERE rut = %s
# query ('Roberto 2 Alejandro Martinez', 255, '15.827.300-4')
