"""
operacion directa en el map PROBE
"""
from DISClib.DataStructures import liststructure as lt


def operationSet(mp, operation, returnEntry):
    """
    Retorna una lista con todas las llaves de la tabla de hash

    Args:
        mp: El map
        returnEntry: formato del retorno
        operation: operacion a realizar
    Returns:
        lista de llaves
    Raises:
        Exception
    """
    if mp['type'] == 'CHAINING':
        return operationSetChaining(mp, operation, returnEntry)
    else:
        return operationSetProbe(mp, operation, returnEntry)


def operationSetProbe(mp, operation, returnEntry={}):
    """

    Args:
        operation:
        mp:
        returnEntry: formato del retorno
    Returns:
        returnEntry actualizado
    Raises:
        Exception
    """

    for pos in range(lt.size(mp['table'])):
        entry = lt.getElement(mp['table'], pos + 1)
        if entry['key'] is not None and entry['key'] != '__EMPTY__':
            operation(entry, returnEntry)
    return returnEntry


def operationSetChaining(mp, operation, returnEntry):
    """
    Retorna una lista con todas las llaves de la tabla de hash

    Args:
        mp: El map
        returnEntry:
        operation:
    Returns:
        lista de llaves
    Raises:
        Exception
    """
    for pos in range(lt.size(mp['table'])):
        bucket = lt.getElement(mp['table'], pos + 1)
        for element in range(lt.size(bucket)):
            entry = lt.getElement(bucket, element + 1)
            operation(entry, returnEntry)
    return returnEntry
