"""
Módulo de exportación de datos de conversaciones de ElevenLabs.

Proporciona funciones para exportar en formato .csv transcripciones y datos de
conversaciones, tanto de forma separada por conversación como
combinada, y también para exportar variables dinámicas y resultados
de data collection.

Funciones:
    - download_transcriptions_separated(**kwargs)
    - download_transcriptions_combined(**kwargs)
    - download_data_collection(**kwargs)

Cada función acepta un número arbitrario de kwargs, consulta la documentación de
`ConversationDownloader` para obtener más información.
"""

from pathlib import Path
import pandas as pd
from datetime import datetime
from pandas import json_normalize

from appcode.processors.downloaders.conversation_downloader import ConversationDownloader

FILEPATH = Path("../../../exports/")


def _define_file_path(folder, file_name):
    """
    Genera la ruta completa para guardar un archivo CSV que combina varias conversaciones.
    El nombre irá seguido de un timestamp.

    Args:
        folder (str): Carpeta dentro de FILEPATH donde se guardará el archivo.
        file_name (str): Nombre base del archivo.

    Returns:
        Path: Ruta completa donde se guardará el archivo CSV.
    """
    time = str(datetime.now()).replace(":", "-")
    file_name = f"{file_name} - {time}.csv"
    file_path = FILEPATH / (folder + "/")
    file_path.mkdir(parents=True, exist_ok=True)
    file_path = file_path / file_name
    return file_path


def _define_conversation_file_path(conversation, folder):
    """
    Genera la ruta completa para guardar la transcripción de una conversación.
    El nombre irá seguido de un timestamp.

    Args:
        conversation (dict): Diccionario con los datos de la conversación.
        folder (str): Carpeta dentro de FILEPATH donde se guardará el archivo.

    Returns:
        Path: Ruta completa donde se guardará la transcripción CSV.
    """
    email = conversation["email"] if conversation["email"] != "" else "unknown"
    conversation_id = conversation["conversation_id"]
    start_date = str(conversation["start_date"])
    start_time = str(conversation["start_time"]).replace(":", "-")
    file_name = f"{email} - {start_date}-{start_time} - {conversation_id}.csv"
    file_path = FILEPATH / (folder + "/")
    file_path.mkdir(parents=True, exist_ok=True)
    file_path = file_path / file_name
    return file_path


def download_transcriptions_separated(**kwargs):
    """
    Descarga las transcripciones de cada conversación en archivos CSV separados.

    Args:
        **kwargs: Argumentos que se pasan a ConversationDownloader,
                  por ejemplo `agent_ids`, `agent_groups`, `start_date`, `end_date`.

    Genera:
        Un archivo CSV por cada conversación en la carpeta `transcripts`.
    """
    kwargs["process_transcripts"] = True
    downloader = ConversationDownloader(**kwargs).build()

    for conversation in downloader.conversation_details:
        transcript = conversation["transcript"]
        df = pd.DataFrame(transcript)

        file_path = _define_conversation_file_path(conversation, "transcripts")
        df.to_csv(file_path, index=False, encoding="utf-8", sep=";")


def download_transcriptions_combined(**kwargs):
    """
    Descarga todas las transcripciones y las combina en un solo CSV.

    Args:
        **kwargs: Argumentos que se pasan a ConversationDownloader.

    Genera:
        Un único archivo CSV con todas las transcripciones en la carpeta
        `combined_transcripts`. Se añaden columnas `initiator_agent_id`
        y `conversation_id` para identificar cada conversación.
    """
    kwargs["process_transcripts"] = True
    downloader = ConversationDownloader(**kwargs).build()

    all_transcripts = []

    for conversation in downloader.conversation_details:
        transcript = conversation["transcript"]
        df = pd.DataFrame(transcript)
        df.insert(0, "initiator_agent_id", conversation["agent_id"])
        df.insert(1, "conversation_id", conversation["conversation_id"])
        all_transcripts.append(df)

    if all_transcripts:
        file_path = _define_file_path("combined_transcripts", "Combined Transcripts")
        combined_df = pd.concat(all_transcripts, ignore_index=True)
        combined_df.to_csv(file_path, index=False, encoding="utf-8", sep=";")


def download_data_collection(**kwargs):
    """
    Descarga variables dinámicas, criterios de evaluación y data collection
    de las conversaciones y exporta a un CSV.

    Args:
        **kwargs: Argumentos que se pasan a ConversationDownloader.

    Genera:
        Un archivo CSV en la carpeta `data_collection` con todos los datos
        estructurados a partir de `conversation_details`.
    """
    kwargs["process_variables"] = True
    kwargs["process_data_collection"] = True
    kwargs["process_criteria"] = True
    kwargs["process_transcripts"] = False

    downloader = ConversationDownloader(**kwargs).build()
    df = json_normalize(downloader.conversation_details)

    file_path = _define_file_path("data_collection", "ElevenLabs Data Export")
    df.to_csv(file_path, index=False, encoding="utf-8", sep=";")