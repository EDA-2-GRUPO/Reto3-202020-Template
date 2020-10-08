"""
operacion directa en el map
"""
from DISClib.DataStructures import liststructure as lt


def operationSet(mp, operation, returnEntry={}):
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
        if entry['key'] and entry['key'] != '__EMPTY__':
            operation(entry, returnEntry)
    return returnEntry
