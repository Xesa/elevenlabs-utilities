"""
Módulo de enumeraciones para agentes y tipos de variables.

Define los grupos de agentes disponibles en la plataforma y los tipos
de variables que pueden ser utilizados en los datos de conversación.

Enumeraciones:
    - AgentGroup: Grupos de agentes conocidos y categorías generales.
    - VariableType: Tipos de variables permitidos en los datos.
"""

from enum import Enum


class AgentGroup(Enum):
    """
    Enumeración de los grupos de agentes disponibles.

    Miembros:
        - `ELENA`        : Agente Elena principal
        - `ELENA_AFFA`   : Elena relacionada con AFFA
        - `ELENA_NOAFFA` : Elena relacionada con NOAFFA
        - `ELENA_BANNER` : Elena con Banner
        - `MARIA`        : Agente María
        - `ARTESAN`      : Agente Artesan
        - `COACH`        : Agente Coach
        - `OTHER`        : Grupo por defecto para agentes no categorizados
    """
    ELENA = "Elena"
    ELENA_AFFA = "Elena AFFA"
    ELENA_NOAFFA = "Elena NOAFFA"
    ELENA_BANNER = "Elena Banner"
    MARIA = "María"
    ARTESAN = "Artesan"
    COACH = "Coach"
    OTHER = "Other"


class VariableType(Enum):
    """
    Enumeración de los tipos de variables que pueden aparecer en los datos
    de conversaciones.

    Miembros:
        - `STRING`  : Cadena de texto
        - `BOOLEAN` : Valor booleano (True/False)
        - `FLOAT`   : Número decimal
        - `INTEGER` : Número entero
    """
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "number"
    INTEGER = "integer"
