# from core.entities.persona_model import Persona
# from django.core.paginator import Paginator
# from graphene import Int
# from core.serializers.persona_serielizer import PersonaSerializer


# def resolve_all_personas_with_locations(self, info, page=1, page_size=10):
#         personas  = Persona.objects.select_related('comuna__provincia__region').all()
#         paginator = Paginator(personas, page_size)
        
#         if page < 1 or page > paginator.num_pages:
#             page = 1
            
#         personas_page = paginator.get_page(page)    
#         personas_data = []
        
#         for persona in personas_page:
#             comuna    = persona.comuna
#             provincia = comuna.provincia
#             region    = provincia.region
            
#             persona_data = {
#                 "nombre"    : persona.nombre,
#                 "rut"       : persona.rut,
#                 "comuna"    : comuna.nombre,
#                 "provincia" : provincia.nombre,
#                 "region"    : region.nombre
#             }
            
#             personas_data.append(persona_data)
        
#         return {
#             "results"      : personas_data,
#             "count"        : paginator.count,
#             "num_pages"    : paginator.num_pages,
#             "current_page" : personas_page.number
#         }