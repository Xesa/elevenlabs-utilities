"""
Módulo para gestionar la conexión con las conversaciones de ElevenLabs.
Proporciona una interfaz simple para obtener las conversaciones de un agente o grupo de agentes.

Clases:
    ConversationConnection: Maneja la conexión con ElevenLabs y agrupa conversaciones por agentes.

"""

from elevenlabs import ElevenLabs
from datetime import date, datetime

from appcode.connections.agent_connection import AgentConnection

import appcode.helpers.agent_group_selector as AgentGroupSelector
import appcode.helpers.time_helpers as TimeHelper

from appcode.common.secrets import API_KEY
from appcode.common.enums import AgentGroup


class ConversationConnection:
    """
    Clase que gestiona la conexión con ElevenLabs para obtener conversaciones
    de agentes y organizarlas por agente o grupo de agentes.

    Instanciar esta clase llamará directamente a la API de ElevenLabs una sola vez y
    almacenará la información en la propia instancia. Por ello, esta clase debe
    tratarse como un singleton.

    Esta clase implementa un patrón tipo Builder, permitiendo configurar
    filtros y parámetros paso a paso antes de construir la estructura final
    de conversaciones.

    Métodos de configuración (pueden encadenarse):
        - `set_accepted_agent_ids(agent_ids)`: Define un array de agentes de los que extraer conversaciones.
        - `set_accepted_agent_groups(agent_groups)`: Define un array de grupos de los que extraer conversaciones.
        - `set_start_date(start_date)`: Filtra conversaciones iniciadas después de esta fecha.
        - `set_end_date(end_date)`: Filtra conversaciones iniciadas antes de esta fecha.

    Finalmente llama a `build()` para cargar los datos.

    Ejemplo de uso:
    ::
        connection = (
            ConversationConnection()
            .set_accepted_agent_groups([AgentGroup.ELENA, AgentGroup.MARIA])
            .set_start_date(date(2025, 10, 1))
            .set_end_date(date(2025, 10, 15))
            .build())


    """

    client : ElevenLabs
    agent_connection : AgentConnection = None

    parameters = {}
    accepted_agent_ids = []

    conversations = {}
    conversation_ids = []
    conversation_ids_per_agent_id = {}
    conversation_ids_per_agent_group = {}


    def __init__(self):
        self.client = ElevenLabs(api_key=API_KEY)


#region BuildMethods

    def build(self):
        """
        Construye la estructura de conversaciones obtenidas de ElevenLabs.
        Esta función debe ser llamada después de usar todos los setter methods.
        Consulta la documentación de la clase para más información.
        """

        # Crea una clave en el diccionario por cada elemento del Enum
        self.conversation_ids_per_agent_group = AgentGroupSelector.generate_dictionary_keys()

        has_more = True
        next_cursor = None

        self.parameters["page_size"] = 100

        # Itera todas las páginas devueltas por la API
        while has_more:

            if next_cursor:
                self.parameters["cursor"] = next_cursor

            response = self.client.conversational_ai.conversations.list(**self.parameters)

            has_more = response.has_more
            next_cursor = response.next_cursor

            # Itera cada conversación presente en la página actual
            for conversation in response.conversations:

                conversation_id = conversation.conversation_id
                agent_id = conversation.agent_id
                agent_name = conversation.agent_name

                # Si el agente no está dentro de los agentes aceptados saltamos la iteración
                if len(self.accepted_agent_ids) > 0 and agent_id not in self.accepted_agent_ids:
                    continue

                # Indicamos cada grupo al que pertenece la conversación
                groups = AgentGroupSelector.get_agent_groups(agent_name)
                group_strings = AgentGroupSelector.get_agent_groups_as_strings(agent_name)

                # Extraemos la info de la conversación
                conversation_info = {
                    "conversation_id" : conversation_id,
                    "agent_id" : agent_id,
                    "agent_name" : agent_name,
                    "start_date" : TimeHelper.unix_to_date(conversation.start_time_unix_secs),
                    "start_time" : TimeHelper.unix_to_time(conversation.start_time_unix_secs),
                    "call_duration_secs" : conversation.call_duration_secs,
                    "call_duration_timestamp" : TimeHelper.unix_to_time(conversation.call_duration_secs),
                    "status" : conversation.status,
                    "successful" : conversation.call_successful,
                    "direction" : conversation.direction,
                    "agent_groups" : group_strings
                }

                # Añadimos la información de la conversación a la clase
                self.conversations[conversation_id] = conversation_info
                self.conversation_ids.append(conversation_id)
                self.conversation_ids_per_agent_id[agent_id] = conversation_id

                # Añadimos la conversación a cada agent group al que pertenece
                for group in groups:
                    self.conversation_ids_per_agent_group[group.value].append(conversation_id)


    def set_accepted_agent_ids(self, agent_ids):
        """
        Define los IDs de agentes que se considerarán en la construcción de conversaciones.

        Args:
            agent_ids (list[str]): Lista de IDs de agentes.

        Returns:
            ConversationConnection: Devuelve la instancia para encadenar llamadas.
        """
        self.accepted_agent_ids.extend(agent_ids)
        return self


    def set_accepted_agent_groups(self, agent_groups):
        """
        Define los grupos de agentes aceptados y actualiza los IDs internos.

        Args:
            agent_groups (list[AgentGroup]): Lista de grupos de agentes.

        Returns:
            ConversationConnection: Devuelve la instancia para encadenar llamadas.
        """
        if self.agent_connection is None:
            self.agent_connection = AgentConnection()

        for group in agent_groups:
            group_ids = self.agent_connection.get_agent_group_ids(group)
            self.set_accepted_agent_ids(group_ids)

        return self


    def set_start_date(self, start_date : date):
        """
        Filtra conversaciones iniciadas después de una fecha específica.

        Args:
            start_date (date): Fecha de inicio.

        Returns:
            ConversationConnection: Devuelve la instancia para encadenar llamadas.
        """
        self.parameters["call_start_after_unix"] = TimeHelper.date_to_unix(start_date)
        return self


    def set_end_date(self, end_date : date):
        """
        Filtra conversaciones iniciadas antes de una fecha específica.

        Args:
            end_date (date): Fecha de fin.

        Returns:
            ConversationConnection: Devuelve la instancia para encadenar llamadas.
        """
        self.parameters["call_start_before_unix"] = TimeHelper.date_to_unix(end_date)
        return self

#endregion

#region GetterMethods

    def get_all_conversations_info(self):
        """Devuelve toda la información de conversaciones cargadas."""
        return self.conversations


    def get_all_conversation_ids(self):
        """Devuelve todos los IDs de conversaciones cargadas."""
        return self.conversation_ids


    def get_conversation_ids_from_agent(self, agent_id):
        """
        Devuelve los IDs de conversaciones asociadas a un agente específico.

        Args:
            agent_id (str): ID del agente.
        """
        return self.conversation_ids_per_agent_id[agent_id]


    def get_conversation_ids_from_agent_group(self, agent_group : AgentGroup):
        """
        Devuelve los IDs de conversaciones asociadas a un grupo de agentes.

        Args:
            agent_group (AgentGroup): Grupo de agentes.
        """
        return self.conversation_ids_per_agent_group[agent_group.value]


    def get_conversation_info_from_agent(self, agent_id):
        """
        Devuelve la información completa de todas las conversaciones de un agente.

        Args:
            agent_id (str): ID del agente.
        """
        selected_conversations = []
        for conv_id in self.get_conversation_ids_from_agent(agent_id):
            selected_conversations.append(self.conversations[conv_id])
        return selected_conversations


    def get_conversation_info_from_agent_group(self, agent_group : AgentGroup):
        """
        Devuelve la información completa de todas las conversaciones de un grupo de agentes.

        Args:
            agent_group (AgentGroup): Grupo de agentes.
        """
        selected_conversations = []
        for conv_id in self.get_conversation_ids_from_agent_group(agent_group):
            selected_conversations.append(self.conversations[conv_id])
        return selected_conversations

#endregion