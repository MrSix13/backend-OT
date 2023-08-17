pref = "public.core_"




table_query = [
    {
        "table_name": pref + "usuarios U",
        "entidad": "usuarios",
       "query": [],
        "params": ["_p1", "_p2", "_p3"],
        "def": ["", "0", ""],
         "query01":  
        """SELECT 1, U.id, U.nombre, U.telefono, U.correo, 
             CASE
             WHEN U.estado = 1 THEN 'Activo'
             WHEN U.estado = 2 THEN 'Suspendido'
             ELSE 'Sin estado'
              END AS estado, U.cargo, C.nombre 
             FROM """ + pref + """Usuarios U
             JOIN """ + pref + """Cargos C 
               ON C.id = U.cargo
            WHERE (LOWER(U.nombre) LIKE LOWER('%_p1%') OR '_p1' = '') 
              AND (U.cargo = _p2 OR _p2 = 0) 
            ORDER BY U.nombre""",
       "query02": "SELECT id, nombre FROM " + pref + "Usuarios ORDER BY 2",
       "query03": """INSERT INTO """ + pref + """Usuarios (nombre, password, cargo, telefono, correo, estado) VALUES(_p1);""",
       "query04": """UPDATE """ + pref + """Usuarios SET _p3 WHERE id = _p1;""",
       "query05": "DELETE FROM " + pref + "Usuarios " + 
                  "WHERE id IN (_p1)",
    },
    {
        "table_name": pref + "cargos",
        "entidad": "cargos",
        "params": ["_p1"],
        "def":[""],
        "query01": """SELECT 1, id, nombre FROM """ + pref + """Cargos"""
        """ WHERE LOWER(nombre) LIKE LOWER('%_p1%')""",
        "query02": "SELECT id, nombre FROM " + pref + "Cargos ORDER BY 2",
        "query03": [],
    },
    {
        "table_name": pref + "comunas",
        "entidad": "comunas",
        "params": ["_p1"],
        "def":[""],
        "query01": "",
        "query02": "SELECT id, nombre FROM " + pref + "comunas ORDER BY 2",
        "query03": [],
    },
    {
        "table_name": pref + "permisos",
        "entidad": "permisos",
        "fields": "",
        "join": "",
        "where": "",
    },
    {
        "table_name": "public.core_perfiles",
        "entidad": "perfiles",
        "fields": "",
    },
]

# sql query SELECT 1, u.id, u.nombre, u.telefono, u.correo, u.estado, u.cargo, C.nombre  FROM public.core_usuarios U JOIN public.core_cargos C ON C.id = U.id WHERE (u.nombre = 'Sandra')

# SELECT u.id, u.nombre, u.telefono, u.estado, u.cargo, C.nombre FROM public.core_usuarios u JOIN public.core_cargos C on C.id = u.id WHERE 1=1
