import config
from DISClib.Utils import error as error
assert config

"""
Se crearon nuevos "metodos" siguiendo la logica de recorrido in-order y siguiendo las 
implementacion hechas en el dataStructure, se creo las funciones con sus variantes y combinaciones:
Before: recorre los valores antes de una key
Operation: realiza alguna operacion con la rama mientras la recorre

Para los requerimientos solo se utiliza las funciones Operation y sus variantes, Set, Before, Range

Tal como se realizaron las implementaciones  es posible utilizar las funciones tanto en BST como RBT
"""


# se crea las funciones Operation


def operationSet(omap, operation, returnEntry={}):
    """
    Realiza la operation indicada en todas las ramas del order map
    y retorna el entry modificado con las operaciones realizadas
    Args:
        omap: mapa ordenado
        operation: funcion a ejecutar en las ramas
        returnEntry: formato del retorno

    Returns:
        entry modificado
    """
    try:
        root = omap['root']
        return operationSetTree(root, operation, returnEntry)
    except Exception as exp:
        error.reraise(exp, 'NOM: iteration')


def operationRange(omap, keylo, keyhi, operation, returnEntry={}):
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


def operationBefore(omap, key_bef, operation, returnEntry={}):
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
            operationSetTree(root['left'], operation, returnEntry)
            operation(root, returnEntry)
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
