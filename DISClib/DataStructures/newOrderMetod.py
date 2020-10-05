import config
from DISClib.DataStructures import rbtnode as node
from DISClib.Utils import error as error
from DISClib.ADT import list as lt
from DISClib.DataStructures.rbt import keySetTree, newMap, put, keySet, values, valueSet
from DISClib.DataStructures import listiterator as it

assert config


# ordermap funccion

def pairSet(omap):
    """
    Retorna una lista con todas las parejas llave-valor de la tabla
    Args:
        omap: La tabla de simbolos
    Returns:
        Una lista con todas las llaves de la tabla
    Raises:
        Exception
    """
    try:
        klist = lt.newList()
        klist = pairSetTree(omap['root'], klist)
        return klist
    except Exception as exp:
        error.reraise(exp, 'RBT:pairSet')


def keysBefore(omap, key):
    """
    Retorna todas las llaves del arbol que se encuentren antes de key
    Args:
        key: key a comparar
        omap: La tabla de simbolos

    Returns:
        Las llaves en el rago especificado
    Raises:
        Exception
    """
    try:
        lstkeys = lt.newList('SINGLELINKED', omap['cmpfunction'])
        lstkeys = keysBefore_Tree(omap['root'], key, omap['cmpfunction'], lstkeys)
        return lstkeys
    except Exception as exp:
        error.reraise(exp, 'RBT:KeysBefore')


def pairsBefore(omap, key):
    """
    Retorna todas las llaves del arbol que se encuentren entre
    [keylo, keyhi]
    Args:
        omap:
        key:
    Returns:
        Las llaves en el rago especificado
    Raises:
        Exception
    """
    try:
        lstkeys = lt.newList('SINGLELINKED', omap['cmpfunction'])
        lstkeys = PairBefore_tree(omap['root'], key, omap['cmpfunction'], lstkeys)
        return lstkeys
    except Exception as exp:
        error.reraise(exp, 'RBT:keys')


def iterationRange(omap, keylo, keyhi, operation):
    try:
        root = omap['root']
        cmpfunction = omap['cmpfunction']
        entry = {}
        return iterationRangeTree(root, keylo, keyhi, operation, entry, cmpfunction)
    except Exception as exp:
        error.reraise(exp, 'Nom: iterationRange')


def iteration(omap, operation):
    try:
        root = omap['root']
        return iterationTree(root, operation, {})
    except Exception as exp:
        error.reraise(exp, 'Nom: iteration')


# tree function

def iterationTree(root, operation, entry):
    try:
        if root is not None:
            iterationTree(root['left'], operation, entry)
            operation(root, entry)
            iterationTree(root['right'], operation, entry)
        return entry
    except Exception as exp:
        error.reraise(exp, 'BST:pairSetTree')


def iterationBeforeTree(root, key, operation, entry, comparefunction):
    try:
        if root is None:
            return entry
        cmp = comparefunction(key, root['key'])
        if cmp < 0:
            return iterationBeforeTree(root['left'], key, operation, entry, comparefunction)
        elif cmp > 0:
            iteration(root['left'], operation)
            operation(root, entry)
            iterationBeforeTree(root['right'], key, operation, entry, comparefunction)
            return entry
        else:
            return iteration(root['left'], operation)

    except Exception as exp:
        error.reraise(exp, 'RBT:BeforeKeys')


def iterationRangeTree(root, keylo, keyhi, operation, entry, cmpfunction):
    """
    Retorna todas las llaves del arbol en un rango dado
    Args:
        root: El arbol binario
        keylo: limite inferior
        keyhi: limite superiorr
        cmpfunction:
        entry:
        operation:
        keyhi:

    Returns:
        Las llaves en el rago especificado
    Raises:
        Exception
    """
    try:
        if root is not None:
            complo = cmpfunction(keylo, root['key'])
            comphi = cmpfunction(keyhi, root['key'])

            if complo < 0:
                iterationRangeTree(root['left'], keylo, keyhi, operation, cmpfunction)
            if (complo <= 0) and (comphi >= 0):
                iterationTree(root, operation, entry)
            if comphi > 0:
                iterationRangeTree(root['right'], keylo, keyhi, operation, cmpfunction)
        return entry
    except Exception as exp:
        error.reraise(exp, 'RBT:keysRange')


def pairSetTree(root, klist):
    """
    Construye una lista con las llaves de la tabla
    Args:
        root: El arbol con los elementos
        klist: La lista de respuesta
    Returns:
        Una lista con todos las llaves
    Raises:
        Exception
    """
    try:
        if root is not None:
            pairSetTree(root['left'], klist)
            lt.addLast(klist, {'key': root['key'], 'value': root['value']})
            pairSetTree(root['right'], klist)
        return klist
    except Exception as exp:
        error.reraise(exp, 'BST:pairSetTree')


def keysBefore_Tree(root, key, comparefunction, list_):
    """
    Retorna el número de llaves en la tabla estrictamente menores que key
    Args:
        root:
        key: La llave de busqueda
        comparefunction:
        list_:

    Returns:
       El numero de llaves
    Raises:
        Exception
    """
    try:
        if root is None:
            return list_
        cmp = comparefunction(key, root['key'])
        if cmp < 0:
            return keysBefore_Tree(root['left'], key, comparefunction, list_)
        elif cmp > 0:
            keySetTree(root['left'], list_)
            lt.addLast(list_, root['key'])
            keysBefore_Tree(root['right'], key, comparefunction, list_)
            return list_
        else:
            return keySetTree(root['left'], list_)

    except Exception as exp:
        error.reraise(exp, 'RBT:BeforeKeys')


def PairBefore_tree(root, key, comparefunction, list_):
    """
    Retorna el número de llaves en la tabla estrictamente menores que key
    Args:
        root: Arbo binario
        key: La llave de busqueda
        comparefunction:
        list_:
    Returns:
       El numero de llaves
    Raises:
        Exception
    """
    try:
        if root is None:
            return list_
        cmp = comparefunction(key, root['key'])
        if cmp < 0:
            return PairBefore_tree(root['left'], key, comparefunction, list_)
        elif cmp > 0:
            pairSetTree(root['left'], list_)
            lt.addLast(list_, {'key': root['key'], 'value': root['value']})
            PairBefore_tree(root['right'], key, comparefunction, list_)
            return list_
        else:
            return pairSetTree(root['left'], list_)

    except Exception as exp:
        error.reraise(exp, 'RBT:BeforeValues')


if __name__ == '__main__':
    def compare(el1, el2):
        if el1 == el2:
            return 0
        elif el1 < el2:
            return -1


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


    from random import randint
    import time

    s = newMap(compare)
    for _ in range(367282):
        # el = randint(1, 100)
        put(s, _, chr(_ + 97))

    # t = pairsBefore(s, 23)
    # h = values(s, 23, 30)
    # q = valueSet(s)
    t1 = time.perf_counter()
    g = pairSet(s)
    iterador = it.newIterator(g)
    m = {}
    for _ in range(lt.size(g)):
        el = it.next(iterador)
        gen(el, m)

    # y = iteration(s, gen)
    t2 = time.perf_counter()
    print(t2 - t1)
