"""
Módulo para gestionar la conexión con los agentes de ElevenLabs.
Proporciona una interfaz simple para categorizar a los agentes y obtener información básica sobre ellos.

Clases:
    AgentConnection: Maneja la conexión con ElevenLabs y agrupa agentes por tipo.

"""

from elevenlabs import ElevenLabs

import appcode.helpers.agent_group_selector as AgentGroupSelector

from appcode.common.secrets import API_KEY
from appcode.common.enums import AgentGroup


class AgentConnection:
    """
    Clase que gestiona la conexión con ElevenLabs y organiza
    los agentes disponibles según los grupos definidos en `AgentGroup`.

    Instanciar esta clase llamará directamente a la API de ElevenLabs una sola vez y
    almacenará la información en la propia instancia. Por ello, esta clase debe
    tratarse como un singleton.
    """

    client : ElevenLabs
    agents = {}
    agents_ids = []
    agent_groups_ids = {}


    def __init__(self):

        # Inicia la conexión con ElevenLabs
        self.client = ElevenLabs(api_key=API_KEY)
        response = self.client.conversational_ai.agents.list()

        # Crea una clave en el diccionario por cada elemento del Enum
        self.agent_groups_ids = AgentGroupSelector.generate_dictionary_keys()

        # Itera cada agente
        for agent in response.agents:
            agent_id : str = agent.agent_id
            agent_name : str = agent.name

            agent_info = self.client.conversational_ai.agents.get(agent_id=agent_id)

            # Indicamos cada grupo al que pertenece el agente
            groups = AgentGroupSelector.get_agent_groups(agent_name)

            # Añadimos la información del agente a la clase
            self.agents[agent_id] = agent_info
            self.agents_ids.append(agent_id)

            # Añadimos el agente a cada uno de los grupos a los que pertenece
            for group in groups:
                self.agent_groups_ids[group.value].append(agent_id)


    def get_all_agents(self) -> dict:
        """
        Devuelve todos los agentes con su información detallada.

        Returns:
            dict: Diccionario con los agentes (clave = agent_id, valor = objeto de agente).
        """
        return self.agents


    def get_all_agent_ids(self) -> list[str]:
        """
        Devuelve la lista de todos los IDs de agentes disponibles.

        Returns:
            list[str]: Lista con los IDs de los agentes.
        """
        return self.agents_ids


    def get_agent_group_ids(self, agent_group: AgentGroup) -> list[str]:
        """
        Devuelve los IDs de agentes que pertenecen a un grupo específico.

        Args:
            agent_group (AgentGroup): Grupo de agentes definido en el Enum `AgentGroup`.

        Returns:
            list[str]: Lista con los IDs de agentes pertenecientes al grupo indicado.
        """
        return self.agent_groups_ids[agent_group.value]


    def get_agent(self, agent_id: str):
        """
        Devuelve la información completa de un agente específico.

        Args:
            agent_id (str): ID del agente.

        Returns:
            object | None: Objeto de agente si existe, o `None` si no se encuentra.
        """
        return self.agents.get(agent_id)