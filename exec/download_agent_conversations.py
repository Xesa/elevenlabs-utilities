from appcode.common.enums import AgentGroup
from appcode.common.enums import VariableType
import appcode.processors.exporters.conversation_exporter as ConversationExporter

MARIA = AgentGroup.MARIA
ELENA = AgentGroup.ELENA
ELENA_AFFA = AgentGroup.ELENA_AFFA
ELENA_NOAFFA = AgentGroup.ELENA_NOAFFA
COACH = AgentGroup.COACH
ARTESAN = AgentGroup.ARTESAN
OTHER = AgentGroup.OTHER

# Edita esta lista de parámetros si lo necesitas
parameters = {
    "agent_ids": None,
    "agent_groups": None,
    "start_date" : None,
    "end_date": None,
}

# Cambia la función por alguna de las que están comentadas, si lo necesitas
ConversationExporter.download_transcriptions_combined(**parameters)

# ConversationExporter.download_transcriptions_separated(**parameters)
# ConversationExporter.download_data_collection(**parameters)