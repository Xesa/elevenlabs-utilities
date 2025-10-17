"""
Módulo para la descarga y procesamiento de conversaciones de ElevenLabs.

Este módulo define la clase `ConversationDownloader`, que permite configurar
filtros, parámetros y tipos de procesamiento para conversaciones de agentes
de manera flexible, siguiendo un patrón Builder.

Se pueden pasar `kwargs` al constructor para inicializar la configuración
y opcionalmente auto-construir la estructura de conversaciones.

Ejemplo de uso:
::
    downloader = ConversationDownloader(
        agent_groups=[AgentGroup.ELENA, AgentGroup.MARIA],
        start_date=date(2025, 10, 1),
        end_date=date(2025, 10, 15),
        process_transcripts=True
    ).build()

Clases:
    - ConversationConnection: Clase subyacente que gestiona la conexión y
      filtrado de conversaciones.

See also:
    - `AgentGroup`: Enum que define todos los grupos posibles de agentes.
"""

from elevenlabs import ElevenLabs
from datetime import date
from appcode.connections.conversation_connection import ConversationConnection

import appcode.helpers.time_helpers as TimeHelper

class ConversationDownloader:
    """
    Clase que descarga conversaciones de agentes y las procesa
    según filtros y tipos de información solicitados.

    Implementa un patrón mixto entre Builder y Kwargs. Puedes utilizar setter methods o
    asignar argumentos opciones vía kwargs.

    Argumentos opcionales vía kwargs:
        - agent_ids: Lista de IDs de agentes.
        - agent_groups: Lista de grupos de agentes.
        - start_date: Fecha mínima de inicio de llamadas.
        - end_date: Fecha máxima de inicio de llamadas.
        - process_summary: Activar/desactivar resúmenes.
        - process_transcripts: Activar/desactivar transcripciones.
        - process_variables: Activar/desactivar variables dinámicas.
        - process_criteria: Activar/desactivar criterios de evaluación.
        - process_data_collection: Activar/desactivar data collection.
        - process_all: Activa todos los tipos de procesamiento.

    Ejemplo de uso:
    ::
        downloader = ConversationDownloader(
            agent_groups=[AgentGroup.ELENA, AgentGroup.MARIA],
            start_date=date(2025, 10, 1),
            end_date=date(2025, 10, 15),
            process_transcripts=True
        ).build()

    See also:
        - `AgentGroup`: Enum que define todos los grupos posibles de agentes.
    """

    connection: ConversationConnection
    client : ElevenLabs

    conversation_details = []

    must_process_summary = False
    must_process_transcripts = False
    must_process_variables = False
    must_process_criteria = False
    must_process_data_collection = False


    def __init__(self, **kwargs):
        self.connection = ConversationConnection()
        self.client = self.connection.client

        # Settea diferentes argumentos según los kwargs
        if kwargs.get("agent_ids"):
            self.set_accepted_agent_ids(kwargs["agent_ids"])

        if kwargs.get("agent_groups"):
            self.set_accepted_agent_groups(kwargs["agent_groups"])

        if kwargs.get("start_date"):
            self.set_start_date(kwargs["start_date"])

        if kwargs.get("end_date"):
            self.set_end_date(kwargs["end_date"])

        if kwargs.get("process_summary"):
            self.toggle_process_summary(kwargs["process_summary"])

        if kwargs.get("process_transcripts"):
            self.toggle_process_transcripts(kwargs["process_transcripts"])

        if kwargs.get("process_variables"):
            self.toggle_process_variables(kwargs["process_variables"])

        if kwargs.get("process_criteria"):
            self.toggle_process_criteria(kwargs["process_criteria"])

        if kwargs.get("process_data_collection"):
            self.toggle_process_data_collection(kwargs["process_data_collection"])

        if kwargs.get("process_all"):
            self.toggle_process_all(kwargs["process_all"])


    def build(self):
        """
        Construye la estructura de conversaciones obtenidas de ElevenLabs.
        Esta función debe ser llamada después de usar todos los setter methods.
        Consulta la documentación de la clase para más información.
        """

        # Construye la connection y recibe los IDs de las conversaciones esperadas
        self.connection.build()
        conversations = self.connection.get_all_conversations_info()

        # Itera cada conversación y obtiene los detalles
        for conversation in conversations.values():
            conv_id = conversation["conversation_id"]

            raw_details = self.client.conversational_ai.conversations.get(conversation_id=conv_id)

            # Fija los detalles básicos
            details = {
                "conversation_id" : conv_id,
                "agent_id" : conversation["agent_id"],
                "agent_name" : conversation["agent_name"],
                "agent_groups" : conversation["agent_groups"],
                "start_date" : conversation["start_date"],
                "start_time": conversation["start_time"],
                "call_duration_secs" : conversation["call_duration_secs"],
                "call_duration_timestamp" : conversation["call_duration_timestamp"],
                "status": conversation["status"],
                "successful": conversation["successful"],
                "direction": conversation["direction"],
            }

            # Obtiene las variables dinámicas comunes a todos los agentes
            details = self.process_basic_variables(details, raw_details)

            # Obtiene otros datos opcionales
            if self.must_process_summary:
                details["summary"] = self.process_summary(raw_details)

            if self.must_process_variables:
                details["dynamic_variables"] = self.process_dynamic_variables(raw_details)

            if self.must_process_criteria:
                details["criteria"] = self.process_criteria(raw_details)

            if self.must_process_data_collection:
                details["data_collection"] = self.process_data_collection(raw_details)

            if self.must_process_transcripts:
                details["transcript"] = self.process_transcript(raw_details)

            self.conversation_details.append(details)
            print(details)

        return self


#region SetterMethods

    def set_accepted_agent_ids(self, agent_ids):
        """Define la lista de agentes aceptados para filtrar conversaciones."""
        self.connection.set_accepted_agent_ids(agent_ids)
        return self


    def set_accepted_agent_groups(self, agent_groups):
        """Define la lista de grupos de agentes aceptados."""
        self.connection.set_accepted_agent_groups(agent_groups)
        return self


    def set_start_date(self, start_date : date):
        """Define la fecha mínima de inicio de conversación."""
        self.connection.set_start_date(start_date)
        return self


    def set_end_date(self, end_date : date):
        """Define la fecha máxima de inicio de conversación."""
        self.connection.set_end_date(end_date)
        return self


    def toggle_process_summary(self, toggle : bool):
        """Activa o desactiva el procesamiento de resúmenes."""
        self.must_process_summary = toggle
        return self


    def toggle_process_transcripts(self, toggle : bool):
        """Activa o desactiva el procesamiento de transcripciones."""
        self.must_process_transcripts = toggle
        return self


    def toggle_process_variables(self, toggle : bool):
        """Activa o desactiva el procesamiento de variables dinámicas."""
        self.must_process_variables = toggle
        return self


    def toggle_process_criteria(self, toggle : bool):
        """Activa o desactiva el procesamiento de criterios de evaluación."""
        self.must_process_criteria = toggle
        return self


    def toggle_process_data_collection(self, toggle : bool):
        """Activa o desactiva el procesamiento de data collection."""
        self.must_process_data_collection = toggle
        return self


    def toggle_process_all(self, toggle : bool):
        """Activa todos los tipos de procesamiento si toggle es True."""
        if toggle:
            self.toggle_process_summary(True)
            self.toggle_process_transcripts(True)
            self.toggle_process_variables(True)
            self.toggle_process_criteria(True)
            self.toggle_process_data_collection(True)

#endregion


#region ProcessMethods

    def process_summary(self, raw_details):
        """Extrae el resumen de la transcripción si existe."""
        if raw_details.analysis is None or raw_details.analysis.transcript_summary is None:
            return ""
        else:
            return raw_details.analysis.transcript_summary


    def process_transcript(self, raw_details):
        """Extrae la transcripción completa en formato estructurado."""
        transcript = []
        turn_index = 0

        for turn in raw_details.transcript:
            turn_index += 1
            timestamp = TimeHelper.seconds_to_timestamp(turn.time_in_call_secs)

            transcript.append({
                "turn" : turn_index,
                "time" : timestamp,
                "role" : turn.role,
                "turn_agent_id" : turn.agent_metadata["agent_id"] if turn.agent_metadata else "",
                "message" : turn.message
            })

        return transcript


    def process_dynamic_variables(self, raw_details):
        """Extrae las variables dinámicas, ignorando las variables de sistema y la información del cliente."""

        if raw_details.conversation_initiation_client_data is None \
        or raw_details.conversation_initiation_client_data.dynamic_variables is None:
            return {}

        raw_dynamic_variables = raw_details.conversation_initiation_client_data.dynamic_variables.copy()
        dynamic_variables = raw_details.conversation_initiation_client_data.dynamic_variables.copy()

        # Ignora las variables del sistema y la información del cliente ya que se extraen por otro lado
        for key in raw_dynamic_variables.keys():
            if key.startswith("system"):
                dynamic_variables.pop(key)

            if key == "email" or key == "phone" or key == "secret_user_id" or key == "secret_object_id":
                dynamic_variables.pop(key)

        return dynamic_variables


    def process_criteria(self, raw_details):
        """Extrae los criterios de evaluación de la conversación."""

        if raw_details.analysis is None or raw_details.analysis.evaluation_criteria_results is None:
            return {}

        criteria = {}
        for result in raw_details.analysis.evaluation_criteria_results.values():
            criteria_id = result.criteria_id

            criteria[criteria_id] = {
                "result": result.result,
                "rationale": result.rationale
            }

        return criteria


    def process_data_collection(self, raw_details):
        """Extrae la data collection de la conversación si existe."""

        if raw_details.analysis is None or raw_details.analysis.data_collection_results is None:
            return {}

        data_collection = {}
        for data in raw_details.analysis.data_collection_results.values():
            data_collection_id = data.data_collection_id

            data_collection[data_collection_id] = {
                "value" : data.value,
                "rationale" : data.rationale
            }

        return data_collection


    def process_basic_variables(self, details, raw_details):
        """Agrega variables básicas (email, phone, Salesforce IDs) a los detalles de la conversación."""

        details["email"] = ""
        details["phone"] = ""
        details["salesforce_user_id"] = ""
        details["salesforce_object_id"] = ""

        # Si no existen las variables dinámicas hace un return
        if raw_details.conversation_initiation_client_data is None \
        or raw_details.conversation_initiation_client_data.dynamic_variables is None:
            return details

        # Obtiene las variables dinámicas comunes a todos los agentes
        dynamic_variables = raw_details.conversation_initiation_client_data.dynamic_variables

        if dynamic_variables.get("email"):
            details["email"] = dynamic_variables["email"]

        if dynamic_variables.get("phone"):
            details["phone"] = dynamic_variables["phone"]

        if dynamic_variables.get("secret_user_id"):
            details["salesforce_user_id"] = dynamic_variables["secret_user_id"]

        if dynamic_variables.get("secret_object_id"):
            details["salesforce_object_id"] = dynamic_variables["secret_object_id"]

        return details

#endregion