"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config

import math as mt
from DISClib.DataStructures import liststructure as lt
from DISClib.DataStructures import listiterator as it

from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import mapstructure as mp
from DISClib.DataStructures import orderedmapstructure as om

from App import newOrderMetod as Nom
from App import newMpMetod as Nmp
from DISClib.Algorithms.Sorting.insertionsort import insertionSort
import datetime

assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""


# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer(tipo):
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'numAccidents': 0,
                'dateIndex': om.newMap(omaptype=tipo, comparefunction=compareOmpLst),
                'timeIndex': om.newMap(omaptype=tipo, comparefunction=compareOmpLst),
                'ZoneIndexLatLng': {'DoubleMap': om.newMap(omaptype=tipo, comparefunction=compareOmpLst),
                                    'num_zones': 0}
                }

    return analyzer


def addAccident(analyzer, accident):
    SevKey = int(accident['Severity'])
    occurredTf = datetime.datetime.strptime(accident['Start_Time'], '%Y-%m-%d %H:%M:%S')
    analyzer['numAccidents'] += 1
    updateDateOmap(analyzer['dateIndex'], occurredTf.date(), SevKey, accident['State'])
    updateTimeOmap(analyzer['timeIndex'], HoursAndMinutes(occurredTf.time()), SevKey)
    updateZoneDoubleOmap(analyzer['ZoneIndexLatLng'], float(accident['Start_Lat']), float(accident['Start_Lng']),
                         occurredTf.weekday())
    return analyzer


def updateDateOmap(omap, occurredDate, SevKey, stateKey):
    """

    Args:
        omap:
        occurredDate: datetime con el dia en que sucedio, en formato YY-MM-dd
        SevKey: str con el nivel de severidad
        stateKey: str con el estado de ocurrencia

    Returns:

    """
    entry = om.get(omap, occurredDate)

    if entry:
        dateEntry = entry['value']  # lo correcto es me.get(entry), se usa para optimizar de aqui en adelante
    else:
        dateEntry = newDateEntry()
        om.put(omap, occurredDate, dateEntry)

    dateEntry['numAccidents'] += 1
    updateIndex(dateEntry['SeverityIndex'], SevKey)
    updateIndex(dateEntry['StateIndex'], stateKey)

    return omap


def updateTimeOmap(omap, occurredTime, SevKey):
    """

    Args:
        omap:
        occurredTime: datetime con el la Hora con minutos en que sucedio, en formato HH:MM
        SevKey: str con el nivel de severidad

    Returns:

    """

    entry = om.get(omap, occurredTime)
    if entry:
        timeEntry = entry['value']
    else:
        timeEntry = newTimeEntry()
        om.put(omap, occurredTime, timeEntry)

    timeEntry['numAccidents'] += 1
    updateIndex(timeEntry['SeverityIndex'], SevKey)

    return omap


def updateZoneDoubleOmap(LatLng, Latitude, Longitude, weekday):
    """

    Args:
        LatLng: entry con un map y un conyteo de cordenadas
        Latitude: cordenada Latitud
        Longitude: cordenada Longitud
        weekday: dia del la semana representado del 0 al 6

    Returns:

    """
    DoubleOmp = LatLng['DoubleMap']
    entryLt = om.get(DoubleOmp, Latitude)

    if entryLt:
        LtEntry = entryLt['value']
    else:
        LtEntry = om.newMap(DoubleOmp['type'], compareOmpLst)
        om.put(DoubleOmp, Latitude, LtEntry)

    entryLng = om.get(LtEntry, Longitude)

    if entryLng:
        LngEntry = entryLng['value']

    else:
        LngEntry = newZoneEntry()
        om.put(LtEntry, Longitude, LngEntry)
        LatLng['num_zones'] += 1

    LngEntry['numAccidents'] += 1
    updateIndex(LngEntry['weekdayIndex'], weekday)

    return DoubleOmp


def updateIndex(Index, indexKey):
    """
    Actualiza el conteo del mapa Index con su indexKey
    Args:
        Index: El map
        indexKey: la llave que se quiere actualizar

    Returns:

    """
    indexEntry = mp.get(Index, indexKey)
    if indexEntry:
        indexEntry['value'] += 1
    else:
        mp.put(Index, indexKey, 1)

    return Index


def newDateEntry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': MakeMapFormat(4),

             'StateIndex': MakeMapFormat(40, 'CHAINING'),

             'numAccidents': 0}

    return entry


def newTimeEntry():
    """
    Crea una entrada en el indice por horas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': MakeMapFormat(4),
             'numAccidents': 0}

    return entry


def newZoneEntry():
    """
    Crea una entrada en el indice por Latitud Longitud, es decir en el doble arbol
    binario.

    """
    entry = {'weekdayIndex': MakeMapFormat(7),
             'numAccidents': 0}

    return entry


def MakeMaxFormat(Total=False):
    if Total:
        return {'maxKey': None, 'maxValue': -1, 'total': 0}
    else:
        return {'maxKey': None, 'maxValue': -1}


def MakeMapFormat(els, Type='PROBING'):
    return mp.newMap(els, maptype=Type, comparefunction=compareMp)


# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================

def requirement1(dateOmap, date):
    dateRoot = om.get(dateOmap, date)
    if not dateRoot:
        return None
    dateEntry = dateRoot['value']
    ListEntry = Nmp.operationSet(dateEntry['SeverityIndex'], makeListMp, lt.newList('ARRAY_LIST'))
    insertionSort(ListEntry, orderByKey)
    return {'list': ListEntry, 'total': dateEntry['numAccidents']}


def requirement2(dateOmap, date):
    mostFrequentDate = Nom.operationBefore(dateOmap, date, TotalAndFrequentOmp, MakeMaxFormat(True))
    return mostFrequentDate


def requirement3(dateOmap, date1, date2):
    severityFrequency = Nom.operationRange(dateOmap, date1, date2, frequencyInMapForOmp('SeverityIndex'),
                                           MakeMapFormat(3))
    mostFrequentSeverity = Nmp.operationSet(severityFrequency, TotalAndFrequentMp, MakeMaxFormat(True))

    return mostFrequentSeverity


def requirement4(dateOmap, date1, date2):
    stateFrequencyAndMfDate = Nom.operationRange(dateOmap, date1, date2, FrequencyInMapAndFrequentKey('StateIndex'),
                                                 {'KeyFrequent': MakeMaxFormat(), 'map': MakeMapFormat(40)})

    mostFrequentState = Nmp.operationSet(stateFrequencyAndMfDate['map'], FrequentMp, MakeMaxFormat(False))

    mfState_mfKey = {'mKey': stateFrequencyAndMfDate['KeyFrequent'], 'mState': mostFrequentState}

    return mfState_mfKey


def requirement5(timeOmap, time1, time2):
    severityFrequency = Nom.operationRange(timeOmap, time1, time2,
                                           frequencyInMapForOmp('SeverityIndex'), MakeMapFormat(3))

    SeverityListAndTotal = Nmp.operationSet(severityFrequency, makeListAndTotalMp,
                                            {'list': lt.newList('ARRAY_LIST'), 'total': 0})

    insertionSort(SeverityListAndTotal['list'], orderByKey)
    AddPercents(SeverityListAndTotal)
    return SeverityListAndTotal


def requirement6(zoneOmap, Lat, Lng, dist):
    weekdayFrequency = Nom.operationRange(zoneOmap, Lat - dist, Lat + dist,
                                          sndCircleRangeDobOmap(Lat, Lng, dist, frequencyInMapForOmp('weekdayIndex')),
                                          MakeMapFormat(7))

    weekdayListAndTotal = Nmp.operationSet(weekdayFrequency, makeListAndTotalMp,
                                           {'list': lt.newList('ARRAY_LIST'), 'total': 0})

    insertionSort(weekdayListAndTotal['list'], orderByKey)
    weekdayFromIntToStr(weekdayListAndTotal['list'])
    return weekdayListAndTotal


# ==============================
# Funciones auxiliares
# ==============================


def sizeOmap(omap):
    try:
        return om.size(omap)
    except TypeError:
        return 0


def heightOmap(omap):
    try:
        return om.height(omap)
    except TypeError:
        return 0


def HoursAndMinutes(time):
    """
    solo tiene en cuenta las horas y los minutos de time
    Args:
        time: datetime.time

    Returns:

    """
    return datetime.time(hour=time.hour, minute=time.minute)


def AddPercents(ListAndTotal):
    """
    Añade los porcentajes a una lista contenida en un dict que ademas tiene
    el valor total del conteo
    Args:
        ListAndTotal:

    Returns:

    """
    sList = ListAndTotal['list']
    iterator = it.newIterator(sList)
    for _ in range(lt.size(sList)):
        el = it.next(iterator)
        el['percent'] = round(el['value'] / ListAndTotal['total'] * 100, 2)


def proxyTime(o_time):
    """
    Aproxima las horas con minutos
    Args:
        o_time: datetime.time

    Returns:

    """

    hour = o_time.hour
    minute = o_time.minute

    if minute <= 30:
        minute = round(minute / 30) * 30
    elif hour == 23:
        minute = 59
    else:
        minute = 0
        hour += 1

    new_time = datetime.time(hour, minute)
    return new_time


def weekdayFromIntToStr(weekdayList):
    """
    Para los entry de una lista Transforma el numero de dia de la semana
    al nombre de este dia
    Args:
        weekdayList:

    Returns:

    """
    weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    iterator = it.newIterator(weekdayList)
    for _ in range(lt.size(weekdayList)):
        el = it.next(iterator)
        el['key'] = weekday_list[el['key']]
    return weekdayList


"""
Hay codigo repetido de a 3 a 5 lineas  que se podrian contraer, sobre todo en las funciones que tienen Frequent en su 
nombre, sin embargo las lineas de codigo que aorraban era pocas mas o menos 20, pero podian tener un rendimientO 
alrededor de 20% menor por su llamado (estamos hablando de numeros muy pequños igual, fue por gusto), aclarar que las 
funciones son llamadas cada vez que se itera dentro del arbol o del map
"""


# ===================================
# Funciones auxiliares para Order Map
# ===================================**


def TotalAndFrequentOmp(root, returnEntry):
    """Funcion auxiliar para buscar en un orderMap visto como histograma la key
    con mayor numero de accidentes, y el valor total del conteo
    """
    num_acc = root['value']['numAccidents']
    if num_acc > returnEntry['maxValue']:
        returnEntry['maxValue'] = num_acc
        returnEntry['maxKey'] = root['key']
    returnEntry['total'] += num_acc
    return returnEntry


def frequencyInMapForOmp(mapIndex):
    """
    Funcion axuliar para realizar la frecuencia acumulada de los maps, vistos como histogramas, dentro
    de cada rama del Omap
    Args:
        mapIndex: el indice del mapa buscado
    """

    def resultFunc(root, returnEntry):
        acMap = root['value'][mapIndex]
        Nmp.operationSet(acMap, frequencyInMap, returnEntry)
        return returnEntry

    return resultFunc


def FrequencyInMapAndFrequentKey(mapIndex):
    """
    Funcion axuliar que es la union de frequencyInMapForOmp y TotalAndFrequentOmap, sin realizar
    el conteo total
    returnEntry: tiene un formato {'map': mewmap, 'KeyFrequent': maxEntry}
    Args:
        mapIndex: el indice del mapa
    """
    def resultFunc(root, returnEntry):
        rValue = root['value']
        num_acc = rValue['numAccidents']
        key_freq = returnEntry['KeyFrequent']
        if num_acc > key_freq['maxValue']:
            key_freq['maxValue'] = num_acc
            key_freq['maxKey'] = root['key']
        Nmp.operationSet(rValue[mapIndex], frequencyInMap, returnEntry['map'])
        return returnEntry

    return resultFunc


def sndCircleRangeDobOmap(x, y, distance, secondOperation):
    """
    Funcion axuliar para crear una operacion en un DobleOmap (order map dentro de order map)
    para un rango dado que representa un 'circulo', definido por un punto en el primer order map,
    un punto en el segundo, y un radio
    Args:
        x: cordenada x (primer order map)
        y: cordenada y (segundo order map)
        distance: radio en el que se busca
        secondOperation: operacion que se quiere realizar en el segundo Omap

    Returns:
        una
    """

    def resultFunction(root, entry):
        move = mt.sqrt(distance ** 2 - (root['key'] - x) ** 2)
        Nom.operationRange(root['value'], y - move, y + move, secondOperation, entry)
        return entry

    return resultFunction


# ===================================
# Funciones auxiliares para Map
# ===================================

def makeListMp(entry, ListEntry):
    """
    Funcion Auxiliar para crear un dict con una lista con las entradas
    de un map.
    Args:
        entry: una entrada de un map
        returnEntry: un entry con una Lista, y un valor de total

    Returns:

    """
    lt.addLast(ListEntry, entry)
    return ListEntry


def makeListAndTotalMp(entry, returnEntry):
    """
    Funcion Auxiliar para crear un dict con una lista con las entradas
    de un map, y el valor total que almacenan las llaves
    Args:
        entry: una entrada de un map
        returnEntry: un entry con una Lista, y un valor de total

    Returns:

    """
    lt.addLast(returnEntry['list'], entry)
    returnEntry['total'] += entry['value']
    return returnEntry


def frequencyInMap(entry, returnEntry):
    """
    Funcion Auxiliar para sacar la frecuencia de las llaves
    en un mapa visto como histagrama
    Args:
        entry: una entrada de un map
        returnEntry: un Map

    Returns:

    """
    key = entry['key']
    num_acc = entry['value']
    try:
        mp.get(returnEntry, key)['value'] += num_acc
    except TypeError:
        mp.put(returnEntry, key, num_acc)

    return returnEntry


def FrequentMp(entry, returnEntry):
    """
    Funcion Auxiliar para obtener la llave mas frecuente de un map
    visto como histograma
    Args:
        entry: una entrada de un map
        returnEntry: un entry con una Lista, y un valor de total

    Returns:

    """
    num_acc = entry['value']
    if num_acc > returnEntry['maxValue']:
        returnEntry['maxValue'] = num_acc
        returnEntry['maxKey'] = entry['key']
    return returnEntry


def TotalAndFrequentMp(entry, returnEntry):
    """
    Funcion Auxiliar para obtener la llave mas frecuente de un map
    visto como histograma,  y obtener el total del conteo
    Args:
        entry: una entrada de un map
        returnEntry: un entry con un maxKey, un maxValue y un valor de total

    Returns:

    """
    num_acc = entry['value']
    if num_acc > returnEntry['maxValue']:
        returnEntry['maxValue'] = num_acc
        returnEntry['maxKey'] = entry['key']
    returnEntry['total'] += num_acc
    return returnEntry


# ==============================
# Funciones de Comparacion
# ==============================

def orderByKey(el1, el2):
    """
    funcion de comparacion mayor de dos entrys
    apartir de sus llaves

    """
    if el1['key'] > el2['key']:
        return 0
    else:
        return 1


def compareOmpLst(date1, date2):
    """
    Compara dos elementos
    """
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1


def compareMp(key1, el2):
    """
    Comparacion para Map
    """
    key2 = el2['key']
    if key1 == key2:
        return 0
    elif key1 > key2:
        return 1
    else:
        return -1
