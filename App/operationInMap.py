"""
operacion directa en el map PROBE, aunque es meterme directamente con la esctructura, igual es
posible realizarlo y deje comentada la opción
"""
from DISClib.DataStructures import liststructure as lt
# from DISClib.DataStructures import listiterator as it
# from DISClib.DataStructures import mapstructure as mp


def operationSet(mp, operation, returnEntry):
    """
    Retorna una lista con todas las llaves de la tabla de hash

    Args:
        mp: El map
        returnEntry: formato del retorno
        operation: operacion a realizar
    Returns:
    Raises:
        Exception
    """
    if mp['type'] == 'CHAINING':
        for pos in range(lt.size(mp['table'])):
            bucket = lt.getElement(mp['table'], pos + 1)
            for element in range(lt.size(bucket)):
                entry = lt.getElement(bucket, element + 1)
                operation(entry, returnEntry)

        return returnEntry
    else:
        for pos in range(lt.size(mp['table'])):
            entry = lt.getElement(mp['table'], pos + 1)
            if entry['key'] is not None and entry['key'] != '__EMPTY__':
                operation(entry, returnEntry)
        return returnEntry




# def operationSet(nmp, operation, returnEntry):
#     keys = nmp.keySet(nmp)
#     iterK = it.newIterator(keys)
#     for _ in range(lt.size(keys)):
#         nk = it.next(iterK)
#         entry = nmp.get(nmp, nk)
#         operation(entry, returnEntry)
#     return returnEntry
