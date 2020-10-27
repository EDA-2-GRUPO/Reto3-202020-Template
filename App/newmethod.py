from DISClib.ADT import list as lt
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m

def rango_de_fechas(cont, min, max):
    lst = values(cont['dateIndex'], min, max,cont)
    return lst
def values(map, keylo, keyhi,cont):
    """
    Retorna todas los valores del arbol que se encuentren entre
    [keylo, keyhi]

    Args:
        map: La tabla de simbolos
        keylo: limite inferior
        keylohi: limite superiorr
    Returns:
        Las llaves en el rago especificado
    Raises:
        Exception
    """
    return keys(map, keylo, keyhi,cont)
def keys(map, keylo, keyhi,cont):
    """
    Retorna todas las llaves del arbol que se encuentren entre
    [keylo, keyhi]

    Args:
        map: La tabla de simbolos
        keylo: limite inferior
        keylohi: limite superiorr
    Returns:
        Las llaves en el rago especificado
    Raises:
        Exception
    """
    if (map['type'] == 'BST'):
        return keysb(map, keylo, keyhi,cont)
    else:
        return keysr(map, keylo, keyhi,cont)

def keysb(bst, keylo, keyhi,cont):
    """
    Retorna todas las llaves del arbol que se encuentren entre
    [keylo, keyhi]

    Args:
        bst: La tabla de simbolos
        keylo: limite inferior
        keylohi: limite superiorr
    Returns:
        Las llaves en el rago especificado
    Raises:
        Exception
    """
    try:
        lstkeys = lt.newList('SINGLELINKED', bst['cmpfunction'])
        lstkeys = keysRange(bst['root'], keylo, keyhi, lstkeys,
                            bst['cmpfunction'],cont)
        return lstkeys
    except Exception as exp:
        error.reraise(exp, 'BST:keys')
def keysr(rbt, keylo, keyhi,cont,num,quequiero):
    """
    Retorna todas las llaves del arbol que se encuentren entre
    [keylo, keyhi]
    Args:
        bst: La tabla de simbolos
        keylo: limite inferior
        keylohi: limite superiorr
    Returns:
        Las llaves en el rago especificado
    Raises:
        Exception
    """
    try:
        lstkeys = lt.newList('SINGLELINKED', rbt['cmpfunction'])
        lstkeys = keysRange(rbt['root'], keylo, keyhi, lstkeys,
                            rbt['cmpfunction'],cont,num,None,quequiero)
        return lstkeys
    except Exception as exp:
        error.reraise(exp, 'RBT:keys')
def keysRange(root , keylo, keyhi, lstkeys, cmpfunction, cont, num , mapau=None, quequiero):
    """
    Retorna todas las llaves del arbol en un rango dado
    Args:
        quequiero:quiero ya sea Severity
        bst: La tabla de simbolos
        keylo: limite inferior
        keylohi: limite superiorr
    Returns:
        Las llaves en el rago especificado
    Raises:
        Excep
    """
    ntotal= 0
    if (mapau != None) and (quequiero=="SeverityIndex"):
       mapau = m.newMap(numelements=11,maptype='PROBING',comparefunction=compareOffenses)
       for a in range(1,5):
          m.put(mapau, a,0)
       m.put(mapau,"ntotal",0)
       listafinal = lt.newList("ARRAY_LIST")
       listakeys = lt.newList("ARRAY_LIST",compareIds)
    try:
        if (root is not None):
            complo = cmpfunction(keylo, root['key'])
            comphi = cmpfunction(keyhi, root['key'])
            if (complo < 0):
                keysRange(root['left'], keylo, keyhi, lstkeys, cmpfunction,cont,num,mapau,quequiero)
            if ((complo <= 0) and (comphi >= 0)):
                listaa=om.get(cont['dateIndex'], root['key'])["value"]["lstaccidentes"]
                m.get(mapau,"ntotal")["value"]+=listaa
                g = om.get(cont['dateIndex'], root['key'])["value"]["SeverityIndex"]
                for a in range(1,5):
                    if om.contains(cont, a) and m.contains(mapau, a):
                        valor2=m.get(mapau,a)["value"]
                        valor=m.get(g, a)["value"]["size"]
                        m.put(mapau,a,valor+valor2)
                    elif om.contains(cont, a):
                        valor=m.get(g, a)["value"]["size"]
                        m.put(mapau,a,valor)
                        lt.addLast(listakeys,a)
            if (comphi > 0):

                keysRange(root['right'], keylo, keyhi, lstkeys, cmpfunction,cont,num,mapau,quequiero)
        return lstkeys
    except Exception as exp:
        error.reraise(exp, 'BST:keysRange')
def compareOffenses(offense1, offense2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

