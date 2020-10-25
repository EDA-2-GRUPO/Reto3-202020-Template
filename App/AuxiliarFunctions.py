"""Hay codigo repetido, de a 3 a 5 lineas  que se podrian contraer, especialmente en las funciones con frequente en
su nombre, sin embargo las lineas de codigo que aorraban era pocas mas o menos 20, pero podian tener un
rendimientO alrededor de 20% menor por su llamado (estamos hablando de numeros muy pequños igual, fue por gusto),
aclarar que las funciones son llamadas cada vez que se itera dentro del arbol o del map """
import config
from DISClib.DataStructures.liststructure import addLast
from DISClib.DataStructures import mapstructure as mp
from App.Operations import operationSetMap
assert config
# ===================================
# Funciones auxiliares para Order Map
# ===================================**


def TotalAndFrequentOmp(root, totalAndMaxEntry):
    """
    Funcion auxiliar para buscar en un orderMap visto como histograma la key
    con mayor numero de accidentes, y el valor total del conteo
    Args:
        root: rama de un omap
        totalAndMaxEntry:
    """
    num_acc = root['value']['numAccidents']
    if num_acc > totalAndMaxEntry['value']:
        totalAndMaxEntry['value'] = num_acc
        totalAndMaxEntry['key'] = root['key']
    totalAndMaxEntry['total'] += num_acc
    return totalAndMaxEntry


def frequencyInMapForOmp(mapIndex):
    """
    Funcion axuliar para realizar la frecuencia acumulada de los maps, vistos como histogramas, dentro
    de cada rama del Omap
    Args:
        mapIndex: el indice del mapa buscado
    """

    def resultFunc(root, frequencyEntry):
        """
        root: rama de un omap
        frequencyEntry: map
        """
        operationSetMap(root['value'][mapIndex], frequencyInMap, frequencyEntry)
        return frequencyEntry

    return resultFunc


def FrequencyInMapAndFrequentKeyForOmp(mapIndex):
    """
    Funcion axuliar que es la union de frequencyInMapForOmp y TotalAndFrequentOmap, sin realizar
    el conteo total
    Args:
        mapIndex: el indice del mapa
    """

    def resultFunc(root, mapAndMaxEntry):
        """
        root: rama de un omap
        mapAndMaxEntry: tiene un formato {'map': mewmap, 'KeyFrequent': maxEntry}
        """
        rValue = root['value']
        num_acc = rValue['numAccidents']
        key_freq = mapAndMaxEntry['KeyFrequent']
        if num_acc > key_freq['value']:
            key_freq['value'] = num_acc
            key_freq['key'] = root['key']
        operationSetMap(rValue[mapIndex], frequencyInMap, mapAndMaxEntry['map'])
        return mapAndMaxEntry

    return resultFunc


def frequencyInMapForOmpInCircle(point, distance, mapIndex):
    """
    Crea una funcion auxiliar para hallar la frecuencia acumulada de los maps,
    vistos como histogramas, dentro de en un Order map ordenado por tuplas cordenadas,
    para una Area representa un
    por un 'circulo', definido por un punto (point), y una distncia
    Args:
        point: tupla con cordenada x, y
        distance: radio en el que se busca
        mapIndex:
    """

    def resultFunction(root, frequencyEntry):
        """
        root: rama de un omap
        frequencyEntry: map ADT
        """
        tkey = root['key']
        if (tkey[0] - point[0]) ** 2 + (tkey[1] - point[1]) ** 2 <= distance ** 2:
            operationSetMap(root['value'][mapIndex], frequencyInMap, frequencyEntry)
        return frequencyEntry

    return resultFunction


# ===================================
# Funciones auxiliares para Map
# ===================================

def makeListMp(entry, listEntry):
    """
    Funcion Auxiliar para crear un dict con una lista con las entradas
    de un map.
    Args:
        listEntry: un entry con una lista
        entry: una entrada de un map
    Returns:

    """
    addLast(listEntry, entry)
    return listEntry


def makeListAndTotalMp(entry, listAndTotalEntry):
    """
    Funcion Auxiliar para crear un dict con una lista con las entradas
    de un map, y el valor total que almacenan las llaves
    Args:
        entry: una entrada de un map
        listAndTotalEntry: un entry con una lista, y un valor de total

    Returns:

    """
    addLast(listAndTotalEntry['list'], entry)
    listAndTotalEntry['total'] += entry['value']
    return listAndTotalEntry


def frequencyInMap(entry, frequencyEntry):
    """
    Funcion Auxiliar para sacar la frecuencia de las llaves
    en un mapa visto como histagrama
    Args:
        entry: una entrada de un map
        frequencyEntry: map ADT
    """
    key = entry['key']
    num_acc = entry['value']
    try:
        mp.get(frequencyEntry, key)['value'] += num_acc
    except TypeError:
        mp.put(frequencyEntry, key, num_acc)

    return frequencyEntry


def FrequentMp(entry, maxEntry):
    """
    Funcion Auxiliar para obtener la llave mas frecuente de un map
    visto como histograma
    Args:
        entry: una entrada de un map
        maxEntry: un entry con una Lista, y un valor de total
    """
    num_acc = entry['value']
    if num_acc > maxEntry['value']:
        maxEntry['value'] = num_acc
        maxEntry['key'] = entry['key']
    return maxEntry


def TotalAndFrequentMp(entry, maxEntry):
    """
    Funcion Auxiliar para obtener la llave mas frecuente de un map
    visto como histograma,  y obtener el total del conteo
    Args:
        entry: una entrada de un map
        maxEntry: un entry con un maxKey, un maxValue y un valor de total
    """
    num_acc = entry['value']
    if num_acc > maxEntry['value']:
        maxEntry['value'] = num_acc
        maxEntry['key'] = entry['key']
    maxEntry['total'] += num_acc
    return maxEntry