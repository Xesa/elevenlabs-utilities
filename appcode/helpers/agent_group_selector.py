"""
Módulo de ayuda para la gestión de grupos de agentes.

Este módulo proporciona funciones para clasificar agentes según su nombre,
generar diccionarios de grupos y obtener los grupos como objetos `AgentGroup`
o como cadenas de texto.

Funciones principales:
    - `generate_dictionary_keys()`: Genera un diccionario con claves para todos los grupos de agentes.
    - `get_agent_groups(agent_name)`: Devuelve una lista de objetos `AgentGroup` según el nombre del agente.
    - `get_agent_groups_as_strings(agent_name)`: Devuelve los nombres de los grupos como strings.

Ejemplo de uso:
::
    >>> from appcode.helpers import agent_group_selector as ags
    >>> ags.get_agent_groups("Elena_AFFA")
    [AgentGroup.ELENA, AgentGroup.ELENA_AFFA]

See also:
    - `AgentGroup`: Enum que define todos los grupos posibles de agentes.
"""

from appcode.common.enums import AgentGroup

def generate_dictionary_keys():
    """
    Genera un diccionario con claves para cada grupo de agentes definido
    en el enum `AgentGroup`, inicializando cada valor como una lista vacía.

    Returns:
        dict: Diccionario con formato {grupo.value: []} para todos los grupos.

    Example:
    ::
        >>> generate_dictionary_keys()
        {
            "ELENA": [],
            "ELENA_AFFA": [],
            "ELENA_NOAFFA": [],
            "ELENA_BANNER": [],
            "MARIA": [],
            "COACH": [],
            "ARTESAN": [],
            "OTHER": []
        }

    See also:
        AgentGroup: Enum que define los grupos posibles de agentes.
    """
    dictionary = {}
    for group in AgentGroup:
        dictionary[group.value] = []
    return dictionary


def get_agent_groups(agent_name : str):
    """
    Determina a qué grupo(s) pertenece un agente según su nombre.

    La función analiza el nombre del agente y devuelve una lista de objetos
    `AgentGroup` que corresponden a los grupos a los que pertenece.

    Args:
        agent_name (str): Nombre del agente.

    Returns:
        list[AgentGroup]: Lista de grupos a los que pertenece el agente.

    Example:
    ::
        >>> get_agent_groups("Elena_AFFA")
        [AgentGroup.ELENA, AgentGroup.ELENA_AFFA]

    See also:
        AgentGroup: Enum de referencia para los grupos posibles.
        get_agent_groups_as_strings: Para obtener los grupos como strings.
    """

    name = agent_name.lower()
    groups = []

    if "elena" in name:
        groups.append(AgentGroup.ELENA)

        if "affa" in name and not "noaffa" in name:
            groups.append(AgentGroup.ELENA_AFFA)

        if "noaffa" in name:
            groups.append(AgentGroup.ELENA_NOAFFA)

        if "banner" in name:
            groups.append(AgentGroup.ELENA_BANNER)

    elif "maría" in name or "maria" in name:
        groups.append(AgentGroup.MARIA)

    elif "coach" in name:
        groups.append(AgentGroup.COACH)

    elif "artesan" in name:
        groups.append(AgentGroup.ARTESAN)

    else:
        groups.append(AgentGroup.OTHER)

    return groups


def get_agent_groups_as_strings(agent_name : str):
    """
    Devuelve los nombres de los grupos a los que pertenece un agente como strings.

    Args:
        agent_name (str): Nombre del agente.

    Returns:
        list[str]: Lista de nombres de grupos (strings) del agente.

    Example:
    ::
        >>> get_agent_groups_as_strings("Elena_Banner")
        ["ELENA", "ELENA_BANNER"]

    See also:
        get_agent_groups: Para obtener los grupos como objetos `AgentGroup`.
    """
    agent_groups = get_agent_groups(agent_name)

    agent_groups_strings = []
    for group in agent_groups:
        agent_groups_strings.append(group.value)

    return agent_groups_strings