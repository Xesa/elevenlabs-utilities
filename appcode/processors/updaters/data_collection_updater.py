"""
Módulo para actualizar variables de Data Collection de agentes en ElevenLabs.

Permite definir una variable, su tipo y prompt, seleccionar agentes o grupos
de agentes, y actualizar la configuración de cada agente de forma programática.

Clase:
    - DataCollectionUpdater: Implementa un patrón tipo Builder para configurar
      y actualizar variables de Data Collection en los agentes.
"""

from elevenlabs import LiteralJsonSchemaProperty

from appcode.connections.agent_connection import AgentConnection
from appcode.common.enums import AgentGroup
from appcode.common.enums import VariableType


class DataCollectionUpdater:
    """
    Clase para construir y aplicar actualizaciones de Data Collection a agentes.

    Esta clase implementa un patrón tipo Builder, permitiendo configurar:
        - Nombre de la variable
        - Tipo de variable (`VariableType`)
        - Prompt de la variable
        - Agentes específicos o grupos de agentes

    Después de configurar los parámetros, se llama a `update()` para aplicar
    los cambios a los agentes seleccionados.

    Métodos de configuración (pueden encadenarse):
        - `set_variable_name(name: str)`       : Define el nombre de la variable.
        - `set_variable_type(type: VariableType)` : Define el tipo de la variable.
        - `set_variable_prompt(prompt: str)`   : Define el prompt de la variable.
        - `set_agent_group(group: AgentGroup)` : Selecciona un grupo de agentes.
        - `set_all_agents()`                   : Selecciona todos los agentes.
        - `build()`                            : Finaliza la configuración.

    Ejemplo de uso:
    ::
        updater = (
            DataCollectionUpdater()
            .set_variable_name("customer_feedback")
            .set_variable_type(VariableType.STRING)
            .set_variable_prompt("Ingrese el feedback del cliente")
            .set_agent_group(AgentGroup.ELENA)
            .build()
        )

        updater.update()
    """

    connection : AgentConnection

    variable_name : str
    variable_type : str
    variable_prompt : str

    agent_ids = []
    upload_json : {}


    def __init__(self):
        self.connection = AgentConnection()


    def set_variable_name(self, name : str):
        """
        Define el nombre de la variable de Data Collection.

        Args:
            name (str): Nombre de la variable.
        """
        self.variable_name = name
        return self


    def set_variable_type(self, _variable_type : VariableType):
        """
        Define el tipo de la variable.

        Args:
            _variable_type (`VariableType`): Tipo de la variable (`STRING`, `BOOLEAN`, `FLOAT`, `INTEGER`)
        """
        self.variable_type = _variable_type.value
        return self


    def set_variable_prompt(self, prompt : str):
        """
        Define el prompt o descripción de la variable.

        Args:
            prompt (str): Texto que describe la variable.
        """
        self.variable_prompt = prompt
        return self


    def set_agent_group(self, agent_group : AgentGroup):
        """
        Selecciona todos los agentes pertenecientes a un grupo específico.

        Args:
            agent_group (`AgentGroup`): Grupo de agentes que se actualizarán.
        """
        self.agent_ids.extend(self.connection.get_agent_group_ids(agent_group))
        return self


    def set_all_agents(self):
        """
        Selecciona todos los agentes disponibles para aplicar la actualización.
        """
        self.agent_ids = self.connection.get_all_agent_ids()
        return self


    def build(self):
        """
        Finaliza la configuración de la variable y agentes.
        """
        return self


    def update(self):
        """
        Aplica la actualización de la variable a todos los agentes seleccionados.

        Para cada agente, se actualiza la Data Collection con:
            - Nombre de variable (`variable_name`)
            - Tipo de variable (`variable_type`)
            - Prompt (`variable_prompt`)

        Imprime un mensaje por cada agente actualizado.
        """

        # Itera cada agente
        for agent_id in self.agent_ids:

            # Obtiene la configuración original del agente
            agent = self.connection.get_agent(agent_id)
            data_collection = agent.platform_settings.data_collection

            # Sobreescribe la variable con la nueva configuración
            variable_settings = LiteralJsonSchemaProperty(
                type=self.variable_type,
                description=self.variable_prompt
            )

            data_collection[self.variable_name] = variable_settings

            # Vuelve a cargar toda la configuración de data collection con los cambios
            platform_settings = {"data_collection" : data_collection}

            self.connection.client.conversational_ai.agents.update(
                agent_id=agent_id,
                platform_settings=platform_settings
            )

            print(f'Updated agent with ID: {agent_id}')


