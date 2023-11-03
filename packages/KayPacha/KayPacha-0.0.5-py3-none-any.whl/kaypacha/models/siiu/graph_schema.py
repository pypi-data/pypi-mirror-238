# SIIU data model 2022
# SCHEMA version for modification on the relations, it is vertioned as well
from .graph_schema_project import graph_project
from .graph_schema_call import graph_call

graph_schema = {"SIIU_MODEL": 2022}
graph_schema["MODELS"] = {}

graph_schema["MODELS"]["project"] = graph_project
graph_schema["MODELS"]["call"] = graph_call
