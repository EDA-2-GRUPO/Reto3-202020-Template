import config
from DISClib.DataStructures import liststructure as lt
from DISClib.Utils import error as error

assert config
# ======================#
# Para order map
# ======================#

"""
Se crearon nuevos "metodos" siguiendo la logica de recorrido in-order y siguiendo las 
implementacion hechas en el dataStructure, se creo con sus variantes:
Operation: realiza alguna operacion con la rama mientras la recorre
    Set: opera en todo el arbol, inspirada en Keyset
    Before: opera en las ramas con keys antes de una key indicada, inspirada en Keys
    Range: opera en las ramas con Keys en el rango indicado, inspirada en Rank
Para los requerimientos solo se utiliza las funciones Operation Before y Range

Tal como se realizaron las implementaciones  es posible utilizar las funciones tanto en BST como RBT
"""


def operationSetOmp(omap, operation, returnEntry):
    """
    Realiza la operation indicada en todas las ramas del order map
    y retorna el entry modificado con las operaciones realizadas
    Args:
        omap: mapa ordenado
        operation: funcion a ejecutar en las ramas
        returnEntry: formato del retorno

    Returns:
        returnEntry modificado
    """
    try:
        root = omap['root']
        return operationSetTree(root, operation, returnEntry)
    except Exception as exp:
        error.reraise(exp, 'NOM: iteration')


def operationRangeOmp(omap, keylo, keyhi, operation, returnEntry):
    """
    Realiza la operation indicada en las ramas del order map que tengan el
    key el rango de keylo y keyhi y retorna el entry modificado con las operaciones realizadas
    Args:
        omap: mapa ordenado
        keylo: limite inferior
        keyhi: limite superior
        operation: funcion a ejecutar en las ramas
        returnEntry: formato del retorno

    Returns:
        entry modificado
    """
    try:
        root = omap['root']
        cmpfunction = omap['cmpfunction']
        return operationRangeTree(root, keylo, keyhi, operation, returnEntry, cmpfunction)
    except Exception as exp:
        error.reraise(exp, 'NOM: iterationRange')


def operationBeforeOmp(omap, key_bef, operation, returnEntry):
    """
    Realiza la operation indicada en las ramas del order map que tengan la llave
    antes del key_bef ingresado y retorna el entry modificado con las operaciones realizadas
    Args:
        omap: mapa ordenado
        key_bef: llave de limite superior
        operation: funcion a ejecutar en las ramas
        returnEntry: formato del retorno

    Returns:
        entry modificado
    """
    try:
        root = omap['root']
        cmpfunction = omap['cmpfunction']

        return operationBeforeTree(root, key_bef, operation, returnEntry, cmpfunction)
    except Exception as exp:
        error.reraise(exp, 'NOM: iterationBefore')


# funciones en arboles


def operationSetTree(root, operation, returnEntry):
    try:
        if root is not None:
            operation(root, returnEntry)
            operationSetTree(root['left'], operation, returnEntry)
            operationSetTree(root['right'], operation, returnEntry)
        return returnEntry
    except Exception as exp:
        error.reraise(exp, 'NOM:operationSetTree')


def operationRangeTree(root, keylo, keyhi, operation, returnEntry, cmpfunction):
    try:
        if root is not None:
            complo = cmpfunction(keylo, root['key'])
            comphi = cmpfunction(keyhi, root['key'])
            if complo < 0:
                operationRangeTree(root['left'], keylo, keyhi, operation, returnEntry, cmpfunction)
            if (complo <= 0) and (comphi >= 0):
                operation(root, returnEntry)
            if comphi > 0:
                operationRangeTree(root['right'], keylo, keyhi, operation, returnEntry, cmpfunction)
        return returnEntry
    except Exception as exp:
        error.reraise(exp, 'NOM:operationRangeTree')


def operationBeforeTree(root, key_bef, operation, returnEntry, comparefunction):
    try:
        if root is None:
            return returnEntry
        cmp = comparefunction(key_bef, root['key'])
        if cmp < 0:
            return operationBeforeTree(root['left'], key_bef, operation, returnEntry, comparefunction)
        elif cmp > 0:
            operationSetTree(root['left'], operation, returnEntry)
            operation(root, returnEntry)
            operationBeforeTree(root['right'], key_bef, operation, returnEntry, comparefunction)
            return returnEntry
        else:
            return operationSetTree(root['left'], operation, returnEntry)
    except Exception as exp:
        error.reraise(exp, 'NOM:operationBeforeTree')


# ======================#
# Para Hash map
# ======================#
"""
operacion directa en las entrys de un  map PROBE o CHAINING, aunque es meterme directamente con la esctructura 
(al igual que se hiso con order map) igual es posible realizarlo sin acceder directamente (igualmente menos eficiente)
,y deje la opcion comentada
"""


def operationSetMap(hMap, operation, returnEntry):
    """
    Realiza la operation indicada en las entradas del map hash
    Args:
        hMap: El map
        returnEntry: formato del retorno
        operation: operacion a realizar
    Returns:
        returnEntry modificado
    Raises:
        Exception
    """
    if hMap['type'] == 'CHAINING':
        for pos in range(hMap['table']['size']):
            bucket = lt.getElement(hMap['table'], pos + 1)
            for element in range(bucket['size']):
                entry = lt.getElement(bucket, element + 1)
                operation(entry, returnEntry)
    else:
        for pos in range(hMap['table']['size']):
            entry = lt.getElement(hMap['table'], pos + 1)
            if entry['key'] is not None and entry['key'] != '__EMPTY__':
                operation(entry, returnEntry)
    return returnEntry

# from DISClib.DataStructures import listiterator as it
# from DISClib.DataStructures import mapstructure as mp
# def operationSetMap(hMap, operation, returnEntry):
#     keys = mp.keySet(hMap)
#     iterK = it.newIterator(keys)
#     for _ in range(lt.size(keys)):
#         nk = it.next(iterK)
#         entry = nmp.get(nmp, nk)
#         operation(entry, returnEntry)
#     return returnEntry
