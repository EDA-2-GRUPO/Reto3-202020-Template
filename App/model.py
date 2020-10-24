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
# Modulos externos nativos
from math import sqrt
from datetime import datetime, time
# Modulos Curso complementarios de lista, iteradores, y sorting
from DISClib.DataStructures.liststructure import addLast, newList
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Sorting.insertionsort import insertionSort
# Modulos Curso de mapas Omap y map
from DISClib.DataStructures import mapstructure as mp
from DISClib.DataStructures import orderedmapstructure as om
# Modulos propios de operaciones en Omap y map, para implementacion del curso
from App import operationInOrderMap as Op_om
from App import operationInMap as Op_mp

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


# ===================================
# Funciones para agregar informacion al catalogo
# ===================================**


def addAccident(analyzer, accident):
    SevKey = int(accident['Severity'])
    occurredTf = datetime.strptime(accident['Start_Time'], '%Y-%m-%d %H:%M:%S')
    analyzer['numAccidents'] += 1
    updateDateOmap(analyzer['dateIndex'], occurredTf.date(), SevKey, accident['State'])
    updateTimeOmap(analyzer['timeIndex'], HoursAndMinutes(occurredTf.time()), SevKey)
    # updateZoneDoubleOmap(analyzer['ZoneIndexLatLng'], float(accident['Start_Lat']), float(accident['Start_Lng']),
    #                      occurredTf.weekday())
    return analyzer


def updateDateOmap(omap, occurredDate, SevKey, stateKey):
    """

    Args:
        omap: omap de date
        occurredDate: datetime con el dia en que sucedio, en formato YY-MM-dd
        SevKey: str con el nivel de severidad
        stateKey: str con el estado de ocurrencia

    Returns:

    """
    entry = om.get(omap, occurredDate)

    if entry:
        dateEntry = entry['value']  # lo correcto es me.getValue(entry), se usa para optimizar de aqui en adelante
    else:
        dateEntry = {'SeverityIndex': MakeMapFormat(2, ints=True), 'StateIndex': MakeMapFormat(23, 'CHAINING'),
                     'numAccidents': 0}
        om.put(omap, occurredDate, dateEntry)

    dateEntry['numAccidents'] += 1
    updateIndex(dateEntry['SeverityIndex'], SevKey)
    updateIndex(dateEntry['StateIndex'], stateKey)

    return omap


def updateTimeOmap(omap, occurredTime, SevKey):
    """

    Args:
        omap: omap de time
        occurredTime: datetime con el la Hora con minutos en que sucedio, en formato HH:MM
        SevKey: str con el nivel de severidad

    Returns:

    """

    entry = om.get(omap, occurredTime)
    if entry:
        timeEntry = entry['value']
    else:
        timeEntry = {'SeverityIndex': MakeMapFormat(2, ints=True), 'numAccidents': 0}
        om.put(omap, occurredTime, timeEntry)

    timeEntry['numAccidents'] += 1
    updateIndex(timeEntry['SeverityIndex'], SevKey)

    return omap


def updateZoneDoubleOmap(LatLng, Latitude, Longitude, weekday):
    """
    Args:
        LatLng: entry con un omap y un conteo de cordenadas
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
        LngEntry = {'weekdayIndex': MakeMapFormat(2, 'CHAINING'), 'numAccidents': 0}
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


# ==============================
# Funciones de consulta
# ==============================

def getDateInfo(dateOmap: mp.newMap, date: datetime):
    """
    Para una fecha devuelve una lista de la cantidad de
    accidentes por severidad y el total de accidentes
    Args:
        dateOmap: Order map organizado por fechas
        date: datetime de la fecha

    Returns:
        Entry con la lista y el total
    """
    dateRoot = om.get(dateOmap, date)
    if dateRoot is None:
        return None
    dateEntry = dateRoot['value']
    severityList = Op_mp.operationSet(dateEntry['SeverityIndex'], makeListMp, newList('ARRAY_LIST'))
    severityListAndTotal = {'list': severityList, 'total': dateEntry['numAccidents']}
    return severityListAndTotal


def mstFreqDateBfADate(dateOmap, before_date):
    """
    Para una serie de fechas antes de la fecha indicada, se calcula la
    que tiene mayor cantidad de accidentes y el total de accidentes en la
    serie de fechas
    Args:
        dateOmap: Order map organizado por fechas
        before_date: datetime de la fecha
    Returns:
        entry con la fecha el numero de accidentes en esa fecha, y total
    """
    mstFreqDate = Op_om.operationBefore(dateOmap, before_date, TotalAndFrequentOmp, MakeMaxFormat(True))
    return mstFreqDate


def mstFreqSeverityInRgDates(dateOmap, date1, date2):
    """
    Para un rango de fechas calcula la severidad mas frecuente y el
    total de accidentes
    Args:
        dateOmap: Order map organizado por fechas
        date1:  datetime de la fecha de la primera fecha
        date2:  datetime de la fecha de la segunda fecha
    Returns:
        entry con la fecha el numero de accidentes en esa fecha, y total


    """
    frequency_fun = frequencyInMapForOmp('SeverityIndex')
    severityFrequency = Op_om.operationRange(dateOmap, date1, date2, frequency_fun, MakeMapFormat(2, ints=True))
    mstFreqSeverity = Op_mp.operationSet(severityFrequency, TotalAndFrequentMp, MakeMaxFormat(True))
    return mstFreqSeverity


def MstFreqDateAndMstFreqStateInRgDates(dateOmap, date1, date2):
    """
    Para un rango de fechas retorna la fecha con mas accidentes y el
    estado con mas accidentes
    Args:
        dateOmap: Order map organizado por fechas
        date1:  datetime de la fecha de la primera fecha
        date2:  datetime de la fecha de la segunda fecha
    Returns:
        dobleentry con un entry con la fecha el numero de accidentes en esa fecha
        y un entry con el estado el numero de accidentes en ese estado
    """
    frequency_fun = FrequencyInMapAndFrequentKey('StateIndex')
    freqAndFrequencyForm = {'KeyFrequent': MakeMaxFormat(False), 'map': MakeMapFormat(40)}
    stateFrequencyAndMfDate = Op_om.operationRange(dateOmap, date1, date2, frequency_fun, freqAndFrequencyForm)
    mostFrequentState = Op_mp.operationSet(stateFrequencyAndMfDate['map'], FrequentMp, MakeMaxFormat(False))
    mostFreqDateAndMostFreqState = {'mstDate': stateFrequencyAndMfDate['KeyFrequent'], 'mstState': mostFrequentState}
    return mostFreqDateAndMostFreqState


def severityFrequencyListInRgHours(timeOmap, time1, time2):
    """
    Para un rango de horas devuelve una lista de la cantidad de
    accidentes por severidad y el total de accidentes
    Args:
        timeOmap: Order map organizado por horas
        time1: time de la hora 1
        time2: time de la hora 2
    Returns:
        Entry con la lista y el total
    """
    frequency_fun = frequencyInMapForOmp('SeverityIndex')
    severityFrequency = Op_om.operationRange(timeOmap, time1, time2, frequency_fun, MakeMapFormat(2, ints=True))
    severityListAndTotal = Op_mp.operationSet(severityFrequency, makeListAndTotalMp, MakeListFormat())
    AddPercents(severityListAndTotal)
    return severityListAndTotal


def weekdayFrequencyListInArea(zoneOmap, Lat, Lng, dist):
    """
    Para un area definida por una latitud una longitud y una distancia devuelve una
    lista de la cantidad de accidentes por severidad y el total de accidentes
    Args:
    Returns:
        Entry con la lista y el total
    """
    cir_fun = sndCircleRangeDobOmap(Lat, Lng, dist, frequencyInMapForOmp('weekdayIndex'))
    weekdayFrequency = Op_om.operationRange(zoneOmap, Lat - dist, Lat + dist, cir_fun, MakeMapFormat(3, ints=True))
    weekdayListAndTotal = Op_mp.operationSet(weekdayFrequency, makeListAndTotalMp, MakeListFormat())
    insertionSort(weekdayListAndTotal['list'], orderByKey)
    weekdayFromIntToStr(weekdayListAndTotal['list'])
    return weekdayListAndTotal


# ==============================
# Funciones auxiliares
# ==============================

"""
Hay codigo repetido, de a 3 a 5 lineas  que se podrian contraer, sobre todo en las funciones que tienen Frequent en su 
nombre, sin embargo las lineas de codigo que aorraban era pocas mas o menos 20, pero podian tener un rendimientO 
alrededor de 20% menor por su llamado (estamos hablando de numeros muy pequños igual, fue por gusto), aclarar que las 
funciones son llamadas cada vez que se itera dentro del arbol o del map
"""


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
        Op_mp.operationSet(root['value'][mapIndex], frequencyInMap, frequencyEntry)
        return frequencyEntry

    return resultFunc


def FrequencyInMapAndFrequentKey(mapIndex):
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
        Op_mp.operationSet(rValue[mapIndex], frequencyInMap, mapAndMaxEntry['map'])
        return mapAndMaxEntry

    return resultFunc


def sndCircleRangeDobOmap(x, y, distance, secondOperation):
    """
    Funcion axuliar para crear una operacion en un DobleOmap (order map dentro de order map)
    para un rango dado que representa un 'circulo', definido por una key en el primer order map (x),
    una key en el segundo (y), y un radio
    Args:
        x: cordenada x (primer order map)
        y: cordenada y (segundo order map)
        distance: radio en el que se busca
        secondOperation: operacion que se quiere realizar en el segundo Omap

    """

    def resultFunction(root, frequencyEntry):
        """
        root: rama de un omap
        frequencyEntry: map ADT
        """
        move = sqrt(distance ** 2 - (root['key'] - x) ** 2)
        Op_om.operationRange(root['value'], y - move, y + move, secondOperation, frequencyEntry)
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


# ==============================
# Funciones de Formatos
# ==============================

def MakeMaxFormat(Total=False):
    if Total:
        return {'key': None, 'value': -1, 'total': 0}
    else:
        return {'key': None, 'value': -1}


def MakeMapFormat(els, Type='PROBING', ints=False):
    return mp.newMap(els, maptype=Type, comparefunction=compareMp, ints=ints)


def MakeListFormat(Type='ARRAY_LIST'):
    return {'list': newList(Type), 'total': 0}


# =========================================
# Funciones ajustes de dato e info
# =========================================

def HoursAndMinutes(o_time):
    return time(o_time.hour, o_time.minute)


def proxyTime(o_time):
    """
    Aproxima las horas con minutos
    Args:
        o_time: datetime.time
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
    new_time = time(hour, minute)
    return new_time


def AddPercents(ListAndTotal):
    """
    Añade los porcentajes a una lista contenida en un dict que ademas tiene
    el valor total del conteo
    Args:
        ListAndTotal: {'list': list ADT, 'total': 0}
    """
    sList = ListAndTotal['list']
    iterator = it.newIterator(sList)
    for _ in range(sList['size']):
        el = it.next(iterator)
        el['percent'] = round(el['value'] / ListAndTotal['total'] * 100, 2)
    return ListAndTotal


def weekdayFromIntToStr(weekdayList):
    """
    Para los entry de una lista Transforma el numero de dia de la semana
    al nombre de este dia
    Args:
        weekdayList: list ADT
    """
    weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    iterator = it.newIterator(weekdayList)
    for _ in range(weekdayList['size']):
        el = it.next(iterator)
        el['key'] = weekday_list[el['key']]
    return weekdayList


# ==============================
# Funciones de Comparacion e Info
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
