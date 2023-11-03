# notas:
# 1. COD_NIVEL_FORMACION: no funciona tomandolo de la tabla EN_RECURSO_HUMANO
# 2. tabla EN_RECURSO_HUMANO_GR no exsite apesar de que aparece en el diagrama y la doc
# la relación entre grupo y autor sale por la tabla RE_GRUPO_RH usando el campo NRO_ID_CNPQ
# 3. en EN_ACT_* el campo COD_INST no se usa, solo INSTITUCION OTRA
# no implementar
# {"KEYS": ["COD_INST"], # este campo no se usa en el aplicativo segun la doc
#   "DB": "__CVLAC__",
#   "TABLES": [
#      # institution
#      {'EN_INSTITUCION': None
#       }]},
# 4. EN_ACTIVIDAD es recursiva a 3 niveles
# 5. muchas instituciones no tienen pais, aparace SGL_PAIS = "1"

graph_author = {"MAIN_TABLE": "EN_RECURSO_HUMANO",
                "CHECKPOINT": {"DB": "__CVLAC__", "KEYS": ["COD_RH"]},
                "SCHEMA_VERSION": 0.1,
                "GRAPH": [{"EN_RECURSO_HUMANO": [
                    # municipio
                    {"KEYS": ["COD_RH_MUN_NACIM/COD_RH_MUNICIPIO", "COD_MUN_NACIM/COD_MUNICIPIO"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_MUNICIPIO': [
                          # departamento
                          {"KEYS": ["SGL_PAIS", "SGL_DEPARTAMENTO"],
                           "DB": "__CVLAC__",
                           "TABLES": [{'EN_DEPARTAMENTO': [
                               # pais
                               {"KEYS": ["SGL_PAIS"],
                                "DB": "__CVLAC__",
                                "TABLES": [{'EN_PAIS': None}]},

                           ]}]},
                          ]}]},
                    # nationality
                    {"KEYS": ["TPO_NACIONALIDAD"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_TIPO_NACIONALIDAD': None}]},
                    # studies trajectory
                    {"KEYS": ["COD_RH"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_TRAYECTORIA_ESCOLAR': [
                         {"KEYS": ["COD_RH_PROG_ACAD/COD_RH", "COD_PROGRAMA_ACADEMICO"],
                           "DB": "__CVLAC__",
                           "TABLES": [
                             # academic program
                             {'EN_PROGRAMA_ACADEMICO': [
                                 {"KEYS": ["COD_NIVEL_FORMACION"],
                                  "DB": "__CVLAC__",
                                  "TABLES": [
                                     # studies level
                                     {'EN_NIVEL_FORMACION': None}
                                 ]}
                             ]}
                         ]},
                         # institution
                         {"KEYS": ["COD_INSTITUCION/COD_INST"],
                          "DB": "__CVLAC__",
                          "TABLES": [
                             # institution
                             {'EN_INSTITUCION': None
                              }]},
                         # municipio
                         {"KEYS": ["COD_RH_MUNICIPIO", "COD_MUNICIPIO"],
                             "DB": "__CVLAC__",
                             "TABLES": [{'EN_MUNICIPIO': [
                                 # departamento
                                 {"KEYS": ["SGL_PAIS", "SGL_DEPARTAMENTO"],
                                  "DB": "__CVLAC__",
                                  "TABLES": [{'EN_DEPARTAMENTO': [
                                   # pais
                                   {"KEYS": ["SGL_PAIS"],
                                    "DB": "__CVLAC__",
                                    "TABLES": [{'EN_PAIS': None}]},

                                  ]}]},
                             ]}]},
                         # relation application sector
                         {"KEYS": ["COD_RH", "COD_TRAY_ESCOLAR"],
                          "DB": "__CVLAC__",
                          "TABLES": [{'RE_TRAY_ESCOLAR_SECTOR_APL': [
                              # sector aplicación nivel 2
                              {"KEYS": ["COD_SECTOR_APLIC/COD_SECTOR_APLICACION"],
                               "DB": "__CVLAC__",
                               "TABLES": [{'EN_SECTOR_APLICACION': [
                                   # sector aplicación nivel 1
                                   {"KEYS": ["COD_SECT_APLIC_PADRE/COD_SECTOR_APLICACION"],
                                    "DB": "__CVLAC__",
                                    "TABLES": [{'EN_SECTOR_APLICACION': None}
                                               ]}
                               ]}
                              ]}
                          ]
                          }]},
                         # Re-Palabra clave
                         {"KEYS": ["COD_RH", "COD_TRAY_ESCOLAR"],
                          "DB": "__CVLAC__",
                          "TABLES": [{'RE_TRAY_ESCOLAR_PALABRA_CLA': [
                              # Palabra clave
                              {"KEYS": ["COD_RH", "COD_PALABRA_CLAVE"],
                               "DB": "__CVLAC__",
                               "TABLES": [{'EN_PALABRA_CLAVE': None}
                                          ]}
                          ]}

                         ]},



                     ]},
                    ]},
                    # profesinal trajectory
                    {"KEYS": ["COD_RH"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_TRAYECTORIA_PROFESIONAL': [
                         # admin activities
                         {"KEYS": ["COD_RH", "COD_TRAY_PROFESIONAL"],
                           "DB": "__CVLAC__",
                           "TABLES": [{'EN_ACT_ADMINISTRACION': [

                               {"KEYS": ["COD_RH", "COD_INST_OTRO/COD_INST"],
                                "DB": "__CVLAC__",
                                "TABLES": [
                                   # institution other
                                   {'EN_INSTITUCION_OTRA': [
                                       {"KEYS": ["COD_INSTITUCION/COD_INST"],
                                        "DB": "__CVLAC__",
                                        "TABLES": [
                                           # institution
                                           {"EN_INSTITUCION": [
                                               # pais
                                               {"KEYS": ["SGL_PAIS"],
                                                "DB": "__CVLAC__",
                                                "TABLES": [{'EN_PAIS': None}]},
                                           ]}

                                       ]}
                                   ]
                                   }]},

                               {"KEYS": ["COD_ACTIVIDAD"],
                                "DB": "__CVLAC__",
                                "TABLES": [
                                   # activity level 1
                                   {'EN_ACTIVIDAD': [
                                       {"KEYS": ["COD_PADRE/COD_ACTIVIDAD"],
                                        "DB": "__CVLAC__",
                                        "TABLES": [
                                           # activity level 2
                                           {'EN_ACTIVIDAD': [
                                               {"KEYS": ["COD_PADRE/COD_ACTIVIDAD"],
                                                "DB": "__CVLAC__",
                                                "TABLES": [
                                                   # activity level 3
                                                   {'EN_ACTIVIDAD': None}
                                               ]}

                                           ]}

                                       ]}
                                   ]
                                   }]},


                           ]}]},
                         # research activities
                         {"KEYS": ["COD_RH", "COD_TRAY_PROFESIONAL"],
                          "DB": "__CVLAC__",
                          "TABLES": [{'EN_ACT_INVESTIGACION': [
                              {"KEYS": ["COD_RH", "COD_INST_OTRO/COD_INST"],
                               "DB": "__CVLAC__",
                               "TABLES": [
                                  # institution other
                                  {'EN_INSTITUCION_OTRA': [
                                      {"KEYS": ["COD_INSTITUCION/COD_INST"],
                                       "DB": "__CVLAC__",
                                       "TABLES": [
                                          # institution
                                          {"EN_INSTITUCION": [
                                              # pais
                                              {"KEYS": ["SGL_PAIS"],
                                               "DB": "__CVLAC__",
                                               "TABLES": [{'EN_PAIS': None}]},
                                          ]}

                                      ]}
                                  ]
                                  }]},
                              {"KEYS": ["COD_ACTIVIDAD"],
                               "DB": "__CVLAC__",
                               "TABLES": [
                                  # activity level 1
                                  {'EN_ACTIVIDAD': [
                                      {"KEYS": ["COD_PADRE/COD_ACTIVIDAD"],
                                       "DB": "__CVLAC__",
                                       "TABLES": [
                                          # activity level 2
                                          {'EN_ACTIVIDAD': [
                                              {"KEYS": ["COD_PADRE/COD_ACTIVIDAD"],
                                               "DB": "__CVLAC__",
                                               "TABLES": [
                                                  # activity level 3
                                                  {'EN_ACTIVIDAD': None}
                                              ]}

                                          ]}

                                      ]}
                                  ]
                                  }]},
                              {"KEYS": ["COD_RH", "COD_ACT_INVESTIGACION"],
                               "DB": "__CVLAC__",
                               "TABLES": [
                                  {"RE_ACT_INV_LINEA_INV": [
                                      {"KEYS": ["COD_RH", "COD_LINEA"],
                                       "DB": "__CVLAC__",
                                       "TABLES": [
                                          {"EN_LINEA_INV": None}
                                      ]}
                                  ]}

                              ]},
                          ]}]},
                         # teaching activities
                         {"KEYS": ["COD_RH", "COD_TRAY_PROFESIONAL"],
                          "DB": "__CVLAC__",
                          "TABLES": [{'EN_ACT_DOCENCIA': [

                              {"KEYS": ["COD_RH", "COD_INST_OTRO/COD_INST"],
                               "DB": "__CVLAC__",
                               "TABLES": [
                                  # institution other
                                  {'EN_INSTITUCION_OTRA': [
                                      {"KEYS": ["COD_INSTITUCION/COD_INST"],
                                       "DB": "__CVLAC__",
                                       "TABLES": [
                                          # institution
                                          {"EN_INSTITUCION": [
                                              # pais
                                              {"KEYS": ["SGL_PAIS"],
                                               "DB": "__CVLAC__",
                                               "TABLES": [{'EN_PAIS': None}]},
                                          ]}

                                      ]}
                                  ]
                                  }]},

                              {"KEYS": ["COD_ACTIVIDAD"],
                               "DB": "__CVLAC__",
                               "TABLES": [
                                  # activity level 1
                                  {'EN_ACTIVIDAD': [
                                      {"KEYS": ["COD_PADRE/COD_ACTIVIDAD"],
                                       "DB": "__CVLAC__",
                                       "TABLES": [
                                          # activity level 2
                                          {'EN_ACTIVIDAD': [
                                              {"KEYS": ["COD_PADRE/COD_ACTIVIDAD"],
                                               "DB": "__CVLAC__",
                                               "TABLES": [
                                                  # activity level 3
                                                  {'EN_ACTIVIDAD': None}
                                              ]}

                                          ]}

                                      ]}
                                  ]
                                  }]},
                          ]}]},

                     ]}]},
                    # relación entre grupo and autor.
                    # los autores pueden estar en varios grupos.
                    # la tabla EN_RECURSO_HUMANO_GR no exsite,
                    # apesar de que aparece en el diagrama y la doc
                    {"KEYS": ["NRO_ID_CNPQ"],
                     "DB": "__GRUPLAC__",
                     "TABLES": [{'RE_GRUPO_RH': [
                         # group
                         {"KEYS": ["NRO_ID_GRUPO"],
                          "DB": "__GRUPLAC__",
                          "TABLES": [{'EN_GRUPO_PESQUISA': None}]},

                     ]}]},
                    # product
                    {"KEYS": ["COD_RH"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_PRODUCTO': [

                         # Grupo x Producto
                         {"KEYS": ["COD_RH", "COD_PRODUCTO"],
                          "DB": "__GRUPLAC__",
                          "TABLES": [{'EN_PRODUCTO_GR': [
                              # Grupo
                              {"KEYS": ["NRO_ID_GRUPO"],
                               "DB": "__GRUPLAC__",
                               "TABLES": [{"EN_GRUPO_PESQUISA": [
                                   # re_institucion
                                   {"KEYS": ["NRO_ID_GRUPO"],
                                    "DB": "__GRUPLAC__",
                                    "TABLES": [{'RE_GRUPO_INSTITUCION': [
                                        # institucion
                                        {"KEYS": ["COD_INST"],
                                         "DB": "__CVLAC__",
                                         "TABLES": [{'EN_INSTITUCION': [
                                             # pais
                                             {"KEYS": ["SGL_PAIS"],
                                              "DB": "__CVLAC__",
                                              "TABLES": [{'EN_PAIS': None}]},
                                         ]}
                                        ]}
                                    ]}
                                   ]},
                                   # Area reconocimiento level 2 (tiene 3 niveles máximo) (es con COD_RH_AREA???)
                                   {"KEYS": ['COD_RH_AREA/COD_RH', 'COD_AREA_CONHEC/COD_AREA_CONOCIMIENTO'],
                                    "DB": "__CVLAC__",
                                    "TABLES": [
                                       {"EN_AREA_CONOCIMIENTO": [
                                           # Area reconocimiento level 1
                                           {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                            "DB": "__CVLAC__",
                                            "TABLES": [{'EN_AREA_CONOCIMIENTO': [
                                                # Area reconocimiento level 0
                                                {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                 "DB": "__CVLAC__",
                                                 "TABLES": [{'EN_AREA_CONOCIMIENTO': None}]},
                                            ]}
                                           ]},

                                       ]}
                                   ]},
                               ]},
                              ]},
                          ]}
                         ]},
                     ]}]},

                    # project
                    {"KEYS": ["COD_RH"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_PROYECTO': [

                                 # Grupo x Proyecto
                                 {"KEYS": ["COD_RH", "COD_PROYECTO"],
                                  "DB": "__GRUPLAC__",
                                  "TABLES": [{'EN_PROYECTO_GR': [
                                      # Grupo
                                      {"KEYS": ["NRO_ID_GRUPO"],
                                       "DB": "__GRUPLAC__",
                                       "TABLES": [{"EN_GRUPO_PESQUISA": [
                                           # re_institucion
                                           {"KEYS": ["NRO_ID_GRUPO"],
                                            "DB": "__GRUPLAC__",
                                            "TABLES": [{'RE_GRUPO_INSTITUCION': [
                                                # institucion
                                                {"KEYS": ["COD_INST"],
                                                 "DB": "__CVLAC__",
                                                 "TABLES": [{'EN_INSTITUCION': [
                                                     # pais
                                                     {"KEYS": ["SGL_PAIS"],
                                                      "DB": "__CVLAC__",
                                                      "TABLES": [{'EN_PAIS': None}]},
                                                 ]}
                                                ]}
                                            ]}
                                           ]},
                                           # Area reconocimiento level 2 (tiene 3 niveles máximo) (es con COD_RH_AREA???)
                                           {"KEYS": ['COD_RH_AREA/COD_RH', 'COD_AREA_CONHEC/COD_AREA_CONOCIMIENTO'],
                                               "DB": "__CVLAC__",
                                               "TABLES": [
                                               {"EN_AREA_CONOCIMIENTO": [
                                                   # Area reconocimiento level 1
                                                   {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                    "DB": "__CVLAC__",
                                                    "TABLES": [{'EN_AREA_CONOCIMIENTO': [
                                                        # Area reconocimiento level 0
                                                        {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                         "DB": "__CVLAC__",
                                                         "TABLES": [{'EN_AREA_CONOCIMIENTO': None}]},
                                                    ]}
                                                   ]},

                                               ]}
                                           ]},
                                       ]},
                                      ]},
                                  ]}
                                 ]},

                                 ]}]},

                    # event
                    {"KEYS": ["COD_RH"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_EVENTO': [

                         # Re-Grupo
                         {"KEYS": ["COD_RH", "COD_EVENTO"],
                          "DB": "__GRUPLAC__",
                          "TABLES": [{'RE_GRUPO_RH_EVENTO': [
                              # Grupo
                              {"KEYS": ["NRO_ID_GRUPO"],
                               "DB": "__GRUPLAC__",
                               "TABLES": [{"EN_GRUPO_PESQUISA": [
                                   # re_institucion
                                   {"KEYS": ["NRO_ID_GRUPO"],
                                    "DB": "__GRUPLAC__",
                                    "TABLES": [{'RE_GRUPO_INSTITUCION': [
                                        # institucion
                                        {"KEYS": ["COD_INST"],
                                         "DB": "__CVLAC__",
                                         "TABLES": [{'EN_INSTITUCION': None}
                                                    ]}
                                    ]}
                                   ]},
                                   # Area reconocimiento level 2 (tiene 3 niveles máximo) (es con COD_RH_AREA???)
                                   {"KEYS": ['COD_RH_AREA/COD_RH', 'COD_AREA_CONHEC/COD_AREA_CONOCIMIENTO'],
                                    "DB": "__CVLAC__",
                                    "TABLES": [
                                       {"EN_AREA_CONOCIMIENTO": [
                                           # Area reconocimiento level 1
                                           {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                            "DB": "__CVLAC__",
                                            "TABLES": [{'EN_AREA_CONOCIMIENTO': [
                                                # Area reconocimiento level 0
                                                {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                 "DB": "__CVLAC__",
                                                 "TABLES": [{'EN_AREA_CONOCIMIENTO': None}]},
                                            ]}
                                           ]},

                                       ]}
                                   ]},
                               ]},
                              ]}
                          ]}

                         ]},

                     ]}]},

                    # network
                    {"KEYS": ["COD_RH"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_RED': [

                                 # Re-Grupo
                                 {"KEYS": ["COD_RH", "COD_RED"],
                                  "DB": "__GRUPLAC__",
                                  "TABLES": [{'RE_GRUPO_RH_RED': [
                                      # Grupo
                                      {"KEYS": ["NRO_ID_GRUPO"],
                                       "DB": "__GRUPLAC__",
                                       "TABLES": [
                                           {"EN_GRUPO_PESQUISA": [
                                               # re_institucion
                                               {"KEYS": ["NRO_ID_GRUPO"],
                                                "DB": "__GRUPLAC__",
                                                "TABLES": [{'RE_GRUPO_INSTITUCION': [
                                                    # institucion
                                                    {"KEYS": ["COD_INST"],
                                                     "DB": "__CVLAC__",
                                                     "TABLES": [{'EN_INSTITUCION': [
                                                         # pais
                                                         {"KEYS": ["SGL_PAIS"],
                                                          "DB": "__CVLAC__",
                                                          "TABLES": [{'EN_PAIS': None}]},
                                                     ]}
                                                    ]}
                                                ]}
                                               ]},
                                               # Area reconocimiento level 2 (tiene 3 niveles máximo) (es con COD_RH_AREA???)
                                               {"KEYS": ['COD_RH_AREA/COD_RH', 'COD_AREA_CONHEC/COD_AREA_CONOCIMIENTO'],
                                                "DB": "__CVLAC__",
                                                "TABLES": [
                                                   {"EN_AREA_CONOCIMIENTO": [
                                                       # Area reconocimiento level 1
                                                       {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                        "DB": "__CVLAC__",
                                                        "TABLES": [{'EN_AREA_CONOCIMIENTO': [
                                                            # Area reconocimiento level 0
                                                            {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                             "DB": "__CVLAC__",
                                                             "TABLES": [{'EN_AREA_CONOCIMIENTO': None}]},
                                                        ]}
                                                       ]},

                                                   ]}
                                               ]},
                                           ]},
                                      ]}
                                  ]}

                                 ]},

                                 ]}]},
                    # patente
                    {"KEYS": ["COD_RH"],
                     "DB": "__CVLAC__",
                     "TABLES": [{'EN_PATENTE': [

                         # Grupo x patente
                         {"KEYS": ["COD_RH", "COD_PRODUCTO"],
                             "DB": "__GRUPLAC__",
                             "TABLES": [{'EN_PRODUCTO_GR': [
                                 # Grupo
                                 {"KEYS": ["NRO_ID_GRUPO"],
                                   "DB": "__GRUPLAC__",
                                   "TABLES": [{"EN_GRUPO_PESQUISA": [
                                       # re_institucion
                                       {"KEYS": ["NRO_ID_GRUPO"],
                                        "DB": "__GRUPLAC__",
                                        "TABLES": [{'RE_GRUPO_INSTITUCION': [
                                            # institucion
                                            {"KEYS": ["COD_INST"],
                                             "DB": "__CVLAC__",
                                             "TABLES": [{'EN_INSTITUCION': [
                                                 # pais
                                                 {"KEYS": ["SGL_PAIS"],
                                                  "DB": "__CVLAC__",
                                                  "TABLES": [{'EN_PAIS': None}]},
                                             ]}
                                            ]}
                                        ]}
                                       ]},
                                       # Area reconocimiento level 2 (tiene 3 niveles máximo) (es con COD_RH_AREA???)
                                       {"KEYS": ['COD_RH_AREA/COD_RH', 'COD_AREA_CONHEC/COD_AREA_CONOCIMIENTO'],
                                           "DB": "__CVLAC__",
                                           "TABLES": [
                                           {"EN_AREA_CONOCIMIENTO": [
                                               # Area reconocimiento level 1
                                               {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                "DB": "__CVLAC__",
                                                "TABLES": [{'EN_AREA_CONOCIMIENTO': [
                                                    # Area reconocimiento level 0
                                                    {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                                     "DB": "__CVLAC__",
                                                     "TABLES": [{'EN_AREA_CONOCIMIENTO': None}]},
                                                ]}
                                               ]},

                                           ]}
                                       ]},
                                   ]},
                                 ]}
                             ]}
                         ]},

                     ]}]},

                ]}
                ]}
