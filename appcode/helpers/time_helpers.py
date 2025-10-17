"""
Módulo de ayuda para conversión de fechas y tiempos.

Este módulo proporciona funciones para convertir entre objetos `date`,
timestamps UNIX y representaciones de tiempo legibles, así como para
formatear duraciones en segundos como timestamps.

Funciones principales:
    - `date_to_unix(raw_date)`: Convierte un objeto `date` a timestamp UNIX.
    - `unix_to_date(ts)`: Convierte un timestamp UNIX a un objeto `date`.
    - `unix_to_time(ts)`: Convierte un timestamp UNIX a un string con hora.
    - `seconds_to_timestamp(seconds)`: Convierte una cantidad de segundos a formato `MM:SS`.

Ejemplo de uso:
::
    >>> import appcode.helpers.time_helpers as TimeHelper
    >>> TimeHelper.date_to_unix(date(2025, 10, 17))
    1766275200
    >>> TimeHelper.unix_to_time(1766278800)
    '10:00:00'
"""

from datetime import date, datetime


def date_to_unix(raw_date : date):
    """
    Convierte un objeto `date` a un timestamp UNIX (segundos desde epoch).

    Args:
        raw_date (date): Fecha a convertir.

    Returns:
        int: Timestamp UNIX correspondiente a la fecha a las 00:00:00.

    Example:
    ::
        >>> date_to_unix(date(2025, 10, 17))
        1766275200
    """
    dt = datetime.combine(raw_date, datetime.min.time())
    return int(dt.timestamp())


def unix_to_date(ts : int):
    """
    Convierte un timestamp UNIX a un objeto `date`.

    Args:
        ts (int): Timestamp UNIX.

    Returns:
        date: Fecha correspondiente al timestamp.

    Example:
    ::
        >>> unix_to_date(1766275200)
        datetime.date(2025, 10, 17)
    """
    dt = datetime.fromtimestamp(ts)
    return dt.date()


def unix_to_time(ts : int):
    """
    Convierte un timestamp UNIX a un string de hora en formato 'HH:MM:SS'.

    Args:
        ts (int): Timestamp UNIX.

    Returns:
        str: Hora en formato 'HH:MM:SS'.

    Example:
    ::
        >>> unix_to_time(1766278800)
        '10:00:00'
    """
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%H:%M:%S")


def seconds_to_timestamp(seconds : int):
    """
    Convierte una duración en segundos a un string en formato 'MM:SS'.

    Args:
        seconds (int): Duración en segundos.

    Returns:
        str: Tiempo formateado como 'MM:SS'.

    Example:
    ::
        >>> seconds_to_timestamp(125)
        '02:05'
    """
    mm, ss = divmod(seconds, 60)
    return f"{mm:02}:{ss:02}"