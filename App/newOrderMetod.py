import config
from DISClib.Utils import error as error
from DISClib.ADT import list as lt
# from DISClib.DataStructures.rbt import keySetTree

assert config

"""
Se crearon nuevos "metodos" siguiendo la logica de recorrido in-order y siguiendo las implementacion hecha en el 
dataStructure, se creo las funciones con sus variantes y combinaciones:
Before: recorre los valores antes de una key
Pair: Simplemento devuelve el conjunto llave-valor
Operation: realiza alguna operacion con la rama mientras la recorre

Para los requerimientos solo se utiliza las funciones Operation y sus variantes, Set, Before, Range

Tal como se realizaron las implementaciones  es posible utilizar las funciones tanto en BST como RBT
"""

# se crea las funciones Operation


def operationSet(omap, operation, entry={}):
    """
    Realiza la operation indicada en todas las ramas del order map
    y retorna el entry modificado con las operaciones realizadas
    Args:
        omap: mapa ordenado
        operation: funcion a ejecutar en las ramas
        entry: formato del retorno

    Returns:
        entry modificado
    """
    try:
        root = omap['root']
        return operationSetTree(root, operation, entry)
    except Exception as exp:
        error.reraise(exp, 'NOM: iteration')


def operationRange(omap, keylo, keyhi, operation, entry={}):
    """
    Realiza la operation indicada en las ramas del order map que tengan el
    key el rango de keylo y keyhi y retorna el entry modificado con las operaciones realizadas
    Args:
        omap: mapa ordenado
        keylo: limite inferior
        keyhi: limite superior
        operation: funcion a ejecutar en las ramas
        entry: formato del retorno

    Returns:
        entry modificado
    """
    try:
        root = omap['root']
        cmpfunction = omap['cmpfunction']
        return operationRangeTree(root, keylo, keyhi, operation, entry, cmpfunction)
    except Exception as exp:
        error.reraise(exp, 'NOM: iterationRange')


def operationBefore(omap, key_bef, operation, entry={}):
    """
    Realiza la operation indicada en las ramas del order map que tengan la llave
    antes del key_bef ingresado y retorna el entry modificado con las operaciones realizadas
    Args:
        omap: mapa ordenado
        key_bef: llave de limite superior
        operation: funcion a ejecutar en las ramas
        entry: formato del retorno

    Returns:
        entry modificado
    """
    try:
        root = omap['root']
        cmpfunction = omap['cmpfunction']

        return operationBeforeTree(root, key_bef, operation, entry, cmpfunction)
    except Exception as exp:
        error.reraise(exp, 'NOM: iterationBefore')


# funciones en arboles


def operationSetTree(root, operation, entry):
    try:
        if root is not None:
            operationSetTree(root['left'], operation, entry)
            operation(root, entry)
            operationSetTree(root['right'], operation, entry)
        return entry
    except Exception as exp:
        error.reraise(exp, 'NOM:operationSetTree')


def operationRangeTree(root, keylo, keyhi, operation, entry, cmpfunction):
    try:
        if root is not None:
            complo = cmpfunction(keylo, root['key'])
            comphi = cmpfunction(keyhi, root['key'])
            if complo < 0:
                operationRangeTree(root['left'], keylo, keyhi, operation, entry, cmpfunction)
            if (complo <= 0) and (comphi >= 0):
                operation(root, entry)
            if comphi > 0:
                operationRangeTree(root['right'], keylo, keyhi, operation, entry, cmpfunction)
        return entry
    except Exception as exp:
        error.reraise(exp, 'NOM:operationRangeTree')


def operationBeforeTree(root, key, operation, entry, comparefunction):
    try:
        if root is None:
            return entry
        cmp = comparefunction(key, root['key'])
        if cmp < 0:
            return operationBeforeTree(root['left'], key, operation, entry, comparefunction)
        elif cmp > 0:
            operationSetTree(root['left'], operation, entry)
            operation(root, entry)
            operationBeforeTree(root['right'], key, operation, entry, comparefunction)
            return entry
        else:
            return operationSetTree(root['left'], operation, entry)

    except Exception as exp:
        error.reraise(exp, 'NOM:operationBeforeTree')


# se agrega Before
# def keysBefore(omap, key):
#     """
#     Retorna todas las llaves del arbol que se encuentren antes de key
#     Args:
#         key: key a comparar
#         omap: La tabla de simbolos
#
#     Returns:
#         Las llaves en el rago especificado
#     Raises:
#         Exception
#     """
#     try:
#         lstkeys = lt.newList('SINGLELINKED', omap['cmpfunction'])
#         lstkeys = keysBeforeTree(omap['root'], key, omap['cmpfunction'], lstkeys)
#         return lstkeys
#     except Exception as exp:
#         error.reraise(exp, 'RBT:KeysBefore')


# Se agrega el retorno de parejas Pair

# def pairSet(omap):
#     """
#     Retorna una lista con todas las parejas llave-valor de la tabla
#     Args:
#         omap: La tabla de simbolos
#     Returns:
#         Una lista con todas las llaves de la tabla
#     Raises:
#         Exception
#     """
#     try:
#         klist = lt.newList()
#         klist = pairSetTree(omap['root'], klist)
#         return klist
#     except Exception as exp:
#         error.reraise(exp, 'RBT:pairSet')
#
#
# def pairsRange(omap, key1, key2):
#     try:
#         lstpairs = lt.newList('SINGLELINKED', omap['cmpfunction'])
#         lstkeys = pairsRangeTree(omap['root'], key1, key2, omap['cmpfunction'], lstpairs)
#         return lstkeys
#     except Exception as exp:
#         error.reraise(exp, 'RBT:keys')
#
#
# def pairsBefore(omap, key):
#     """
#     Retorna todos las parejas key-value que su llave se encuentre antes que key
#     Args:
#         omap:
#         key:
#     Returns:
#         Las llaves en el rago especificado
#     Raises:
#         Exception
#     """
#     try:
#         lstkeys = lt.newList('SINGLELINKED', omap['cmpfunction'])
#         lstkeys = PairBeforeTree(omap['root'], key, omap['cmpfunction'], lstkeys)
#         return lstkeys
#     except Exception as exp:
#         error.reraise(exp, 'RBT:keys')


# def pairSetTree(root, klist):
#     """
#     Construye una lista con las llaves de la tabla
#     Args:
#         root: El arbol con los elementos
#         klist: La lista de respuesta
#     Returns:
#         Una lista con todos las llaves
#     Raises:
#         Exception
#     """
#     try:
#         if root is not None:
#             pairSetTree(root['left'], klist)
#             lt.addLast(klist, {'key': root['key'], 'value': root['value']})
#             pairSetTree(root['right'], klist)
#         return klist
#     except Exception as exp:
#         error.reraise(exp, 'BST:pairSetTree')
#
#
# def pairsRangeTree(root, keylo, keyhi, cmpfunction, lstpairs):
#     try:
#         if root is not None:
#             complo = cmpfunction(keylo, root['key'])
#             comphi = cmpfunction(keyhi, root['key'])
#
#             if complo < 0:
#                 pairsRangeTree(root['left'], keylo, keyhi, cmpfunction, lstpairs)
#             if (complo <= 0) and (comphi >= 0):
#                 lt.addLast(lstpairs, {'key': root['key'], 'value': root['value']})
#             if comphi > 0:
#                 pairsRangeTree(root['right'], keylo, keyhi, cmpfunction, lstpairs)
#         return lstpairs
#     except Exception as exp:
#         error.reraise(exp, 'RBT:keysRange')
#
#
# def keysBeforeTree(root, key, comparefunction, list_):
#     """
#     Retorna el número de llaves en la tabla estrictamente menores que key
#     Args:
#         root:
#         key: La llave de busqueda
#         comparefunction:
#         list_:
#
#     Returns:
#        El numero de llaves
#     Raises:
#         Exception
#     """
#     try:
#         if root is None:
#             return list_
#         cmp = comparefunction(key, root['key'])
#         if cmp < 0:
#             return keysBeforeTree(root['left'], key, comparefunction, list_)
#         elif cmp > 0:
#             keySetTree(root['left'], list_)
#             lt.addLast(list_, root['key'])
#             keysBeforeTree(root['right'], key, comparefunction, list_)
#             return list_
#         else:
#             return keySetTree(root['left'], list_)
#
#     except Exception as exp:
#         error.reraise(exp, 'RBT:BeforeKeys')
#
#
# def PairBeforeTree(root, key, comparefunction, list_):
#     """
#     Retorna el número de llaves en la tabla estrictamente menores que key
#     Args:
#         root: Arbo binario
#         key: La llave de busqueda
#         comparefunction:
#         list_:
#     Returns:
#        El numero de llaves
#     Raises:
#         Exception
#     """
#     try:
#         if root is None:
#             return list_
#         cmp = comparefunction(key, root['key'])
#         if cmp < 0:
#             return PairBeforeTree(root['left'], key, comparefunction, list_)
#         elif cmp > 0:
#             pairSetTree(root['left'], list_)
#             lt.addLast(list_, {'key': root['key'], 'value': root['value']})
#             PairBeforeTree(root['right'], key, comparefunction, list_)
#             return list_
#         else:
#             return pairSetTree(root['left'], list_)
#
#     except Exception as exp:
#         error.reraise(exp, 'RBT:BeforeValues')
# pruebas
if __name__ == '__main__':
    from DISClib.DataStructures.rbt import newMap, put, keySet, values, valueSet, get
    from DISClib.DataStructures import listiterator as it


    def compare(el1, el2):
        if el1 == el2:
            return 0
        elif el1 < el2:
            return -1
        return 1


    def gen(root, m):
        nw = root['value']
        try:
            ac = m['value']
            if nw > ac:
                m['value'] = nw
                m['key'] = root['key']

        except KeyError:
            m['key'] = root['key']
            m['value'] = nw
            m['total'] = ""


    def gen2(list_):
        iter = it.newIterator(list_)
        el = it.next(iter)
        m = {}
        m['key'] = el['key']
        m['value'] = el['value']
        m['total'] = ""

        for _ in range(lt.size(list_) - 1):
            el = it.next(iter)
            nw = el['value']
            ac = m['value']
            if nw > ac:
                m['value'] = nw
                m['key'] = el['key']

        return m


    def gen3(list_, s):
        iter = it.newIterator(list_)
        el = it.next(iter)
        m = {}
        m['key'] = el
        m['value'] = get(s, el)['value']
        m['total'] = ""

        for _ in range(lt.size(list_) - 1):
            el = it.next(iter)
            nw = get(s, el)['value']
            ac = m['value']
            if nw > ac:
                m['value'] = nw
                m['key'] = el
        return m


    from random import randint
    import time

    s = newMap(compare)
    for _ in range(367282):
        # el = randint(1, 100)
        put(s, _, chr(_ + 97))

    # h = values(s, 23, 30)
    # q = valueSet(s)
    t1 = time.perf_counter()
    # t = pairsRange(s, 175662, 345555)
    # # # e = keySet(s)
    # y = gen2(t)
    y = operationRange(s, 175662, 345555, gen)
    # y = iteration(s, gen)
    t2 = time.perf_counter()
    print(t2 - t1)
