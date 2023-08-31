pref = ""


table_query = [
    {
        "entidad": "tipos",
        "query": [],
        "params": ["_p1"],
        "def": [""],
       "query02": "CALL spTipos('_p1')",
    },
    {
        "entidad": "usuarios",
        "query": [],
        "head": ["","ID","NOMBRE", "TELEFONO", "CORREO","ESTADO", "CARGO ID", "CARGO"],
        "params": ["_p1", "_p2", "_p3","_id"],
        "def": ["", "0", "", "0"],
       "query01": "CALL spUsuarios(1, '_p1', _p2,'', _id, 100)",
       "query02": "CALL spUsuarios(2, '', 0,'', 0, 0)",
       "query03": "CALL spUsuarios(3, \"_p1\", 0, '', 0, 0)",
       "query04": "CALL spUsuarios(4,\"_p1\", _p2,'', 0, 0)",
       "query05": "CALL spUsuarios(5, '_p1', 0, '', 0, 0)",
       "query06": "CALL spUsuarios(6, '_p1', 0, '_p3', 0,0)",
    },
    {
        "entidad": "cargos",
        "query": [],
        "head": ["","ID", "CARGO"],
        "params": ["_p1", "_p2",'_id'],
        "def": ["", "0","0"],
       "query01": "CALL spCargos(1, '_p1', _p2,_id, 100)",
       "query02": "CALL spCargos(2, '', 0, 0, 0)",
       "query03": "CALL spCargos(3, \"_p1\", 0, 0, 0)",
       "query04": "CALL spCargos(4,\"_p1\", _p2, 0, 0)",
       "query05": "CALL spCargos(5, '_p1', 0, 0, 0)",
    },
    {
        "entidad": "funcionalidades",
        "query": [],
        "head": ["","ID", "FUNCIONALIDAD"],
        "params": ["_p1", "_p2",'_id'],
        "def": ["", "0","0"],
       "query01": "CALL spFuncionalidades(1, '_p1', _p2,_id, 100)",
       "query02": "CALL spFuncionalidades(2, '', 0, 0, 0)",
       "query03": "CALL spFuncionalidades(3, \"_p1\", 0, 0, 0)",
       "query04": "CALL spFuncionalidades(4,\"_p1\", _p2, 0, 0)",
       "query05": "CALL spFuncionalidades(5, '_p1', 0, 0, 0)",
    },

    {
        "entidad": "",
        "query": [],
        "params": ["_p1"],
        "def":[""],
        "query01": """""",
        "query02": "SELECT id, nombre FROM " + pref + "Cargos ORDER BY 2",
        "query03": """""",
        "query04": """""",
        "query05": """""",
    },
    {
        "table_name": pref + "comunas",
        "entidad": "comunas",
        "params": ["_p1"],
        "def":[""],
        "query01": "",
        "query02": "SELECT id, nombre FROM " + pref + "comunas ORDER BY 2",
        "query03": [],
    },]

# sql query SELECT 1, u.id, u.nombre, u.telefono, u.correo, u.estado, u.cargo, C.nombre  FROM public.core_usuarios U JOIN public.core_cargos C ON C.id = U.id WHERE (u.nombre = 'Sandra')

# SELECT u.id, u.nombre, u.telefono, u.estado, u.cargo, C.nombre FROM public.core_usuarios u JOIN public.core_cargos C on C.id = u.id WHERE 1=1
