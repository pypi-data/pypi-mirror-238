graph_call = {
    "MAIN_TABLE": "SIIU_CONVOCATORIA",
    "CHECKPOINT": {"DB": "BUPP", "KEYS": ["IDENTIFICADOR"]},
    "SCHEMA_VERSION": 0.1,
    "GRAPH": [
        {
            "SIIU_CONVOCATORIA": [
                {
                    "KEYS": ["IDENTIFICADOR/CONVOCATORIA"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_PROYECTO": [{
                            "KEYS": ["MODALIDAD_CONVOCATORIA/IDENTIFICADOR"],
                            "DB":"BUPP",
                            "TABLES":[
                                {"SIIU_MODALIDAD_CONVOCATORIA": None}
                            ]
                        }
                        ]}
                    ]
                },
                {
                    "KEYS": ["IDENTIFICADOR/CONVOCATORIA"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_FECHA_INTERMEDIA": [{
                            "KEYS": ["IDENTIFICADOR"],
                            "DB":"BUPP",
                            "TABLES":[
                                {"SIIU_FECHA_PROCESO_SELECCION": [{
                                    "KEYS": ["ETAPA_PROCESO_SELECCION/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES":[
                                        {"SIIU_ETAPA_PROCESO_SELECCION": [{
                                            "KEYS": ["INSTANCIA_ADMINISTRATIVA/IDENTIFICADOR"],
                                            "DB":"BUPP",
                                            "TABLES":[
                                                {"SIIU_INSTANCIA_ADMINISTRATIVA": [{
                                                    "KEYS": ["INSTANCIA_SUPERIOR/IDENTIFICADOR"],
                                                    "DB":"BUPP",
                                                    "TABLES":[{
                                                        "SIIU_INSTANCIA_ADMINISTRATIVA": [{
                                                            "KEYS": ["INSTANCIA_SUPERIOR/IDENTIFICADOR"],
                                                            "DB":"BUPP",
                                                            "TABLES":[{
                                                                "SIIU_INSTANCIA_ADMINISTRATIVA": [{
                                                                    "KEYS": ["INSTANCIA_SUPERIOR/IDENTIFICADOR"],
                                                                    "DB":"BUPP",
                                                                    "TABLES":[{
                                                                        "SIIU_INSTANCIA_ADMINISTRATIVA": None
                                                                    }]
                                                                }]
                                                            }]
                                                        }]
                                                    }]
                                                }]
                                                }]
                                        }]
                                        }]
                                }]
                                }]
                        }]
                        }]
                },
                {
                    "KEYS": ["IDENTIFICADOR"],
                    "DB":"BUPP",
                    "TABLES":[{
                        "SIIU_CONVOCA_DISPONIBILIDAD": [{  # this part is not documented in the ER diagram
                            # I dont want just to leave a table with numbers and not relations
                            "KEYS": ["SUBTIPO"],
                            "DB":"BUPP",
                            "TABLES":[{
                                "SIIU_SUBTIPO_DISPONIBILIDAD": [{
                                    "KEYS": ["TIPO"],
                                    "DB":"BUPP",
                                    "TABLES":[{
                                        "SIIU_TIPO_DISPONIBILIDAD": None
                                    }]
                                },
                                    {
                                    "KEYS": ["APLICACION"],
                                    "DB":"BUPP",
                                    "TABLES":[{
                                        "SIIU_APLICACION_DISPONIBILIDAD": None
                                    }]
                                }, {
                                    "KEYS": ["PERFIL"],
                                    "DB":"BUPP",
                                    "TABLES":[{
                                        "SIIU_PERFIL_AUTORIZACION": None
                                    }]
                                }]
                            }]
                        }]
                    }]
                },
                {
                    "KEYS": ["IDENTIFICADOR/CONVOCATORIA"],
                    "DB":"BUPP",
                    "TABLES":[{
                        "SIIU_COMPROMISO": [{
                            "KEYS": ["IDENTIFICADOR/COMPROMISO"],
                            "DB":"BUPP",
                            "TABLES":[{"SIIU_COMPROMISO_POR_PROYECTO": None}]
                        }]
                    }]
                },
                {
                    "KEYS": ["IDENTIFICADOR"],
                    "DB":"BUPP",
                    "TABLES":[{
                        "SIIU_CONVOCATORIA_INSTANCIA": [{
                            "KEYS": ["INSTANCIA/IDENTIFICADOR"],
                            "DB":"BUPP",
                            "TABLES":[{
                                "SIIU_INSTANCIA_ADMINISTRATIVA": [{
                                    "KEYS": ["INSTANCIA_SUPERIOR/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES":[{
                                        "SIIU_INSTANCIA_ADMINISTRATIVA": [{
                                            "KEYS": ["INSTANCIA_SUPERIOR/IDENTIFICADOR"],
                                            "DB":"BUPP",
                                            "TABLES":[{
                                                "SIIU_INSTANCIA_ADMINISTRATIVA": [{
                                                    "KEYS": ["INSTANCIA_SUPERIOR/IDENTIFICADOR"],
                                                    "DB":"BUPP",
                                                    "TABLES":[{
                                                        "SIIU_INSTANCIA_ADMINISTRATIVA": None
                                                    }]
                                                }]
                                            }]
                                        }]
                                    }]
                                }]
                            }]
                        }]
                    }]
                },
            ]
        }
    ]
}
