from appcode.processors.updaters.data_collection_updater import DataCollectionUpdater
from appcode.common.enums import AgentGroup
from appcode.common.enums import VariableType

MARIA = AgentGroup.MARIA
ELENA = AgentGroup.ELENA
ELENA_AFFA = AgentGroup.ELENA_AFFA
ELENA_NOAFFA = AgentGroup.ELENA_NOAFFA
COACH = AgentGroup.COACH
ARTESAN = AgentGroup.ARTESAN
OTHER = AgentGroup.OTHER

STRING = VariableType.STRING
BOOLEAN = VariableType.BOOLEAN
FLOAT = VariableType.FLOAT
INTEGER = VariableType.INTEGER

# Modifica el prompt según necesites
variable_prompt = 'Indica "True" si en algún momento de la conversación se ha hablado sobre agendar una demo o una consultoría y el cliente ha aceptado o ha mostrado interés. Marca "False" en caso contrario.'

# Cambia el nombre de la variable, su tipo y los agentes a los que debe aplicarse
updater = DataCollectionUpdater().set_variable_name("demoVerbalizada") \
                                 .set_variable_type(BOOLEAN) \
                                 .set_agent_group(ELENA) \
                                 .set_variable_prompt(variable_prompt) \
                                 .build() \
                                 .update()
