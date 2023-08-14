from django.urls import path

# from core.views.cargos_view import listar_cargos, crear_cargo,eliminar_cargo,eliminar_all_cargos,editar_cargo, listar_view
from core.views.generic_view import listar_view, crear, eliminar, editar


urlpatterns = [
    # path('api/cargos/listadoss/', listar_cargos, name="listar_cargos"),
    # path('api/cargos/<str:id>', editar_cargo, name="editar_cargos"),
    # path('api/cargos/crear/', crear_cargo, name="crear_cargos"),
    # path('api/cargos/eliminar/', eliminar_cargo, name="eliminar_cargos"),
    # path('api/cargos/eliminar/all/', eliminar_all_cargos, name="eliminar_cargos"),
    path("api/<str:entidad>/listado/", listar_view, name="listar"),
    path("api/<str:entidad>/crear/", crear, name="crear"),
    path("api/<str:entidad>/editar/", editar, name="editar"),
    path("api/<str:entidad>/eliminar/", eliminar, name="eliminar"),
]
