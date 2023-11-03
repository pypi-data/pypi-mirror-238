from .graph_fields_project import project_fields
from .graph_fields_call import call_fields

graph_fields = {}

# adding fields for every main entity
graph_fields["SIIU_PROYECTO"] = project_fields
graph_fields["SIIU_CONVOCATORIA"] = call_fields
