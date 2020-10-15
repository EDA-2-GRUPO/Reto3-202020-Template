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
                'ZoneIndexLatLng': om.newMap(omaptype=tipo, comparefunction=compareOmpLst)
                }

    return analyzer


def addAccident(analyzer, accident):
    analyzer['numAccidents'] += 1
    SevKey = int(accident['Severity'])
    stateKey = accident['State']
    """Latitude = float(accident['Start_Lat'])
    Longitude = float(accident['Start_Lng'])"""
    occurredTf = datetime.datetime.strptime(accident['Start_Time'], '%Y-%m-%d %H:%M:%S')
    occurredDate = occurredTf.date()
    """weekday = occurredDate.weekday()
    occurredTime = HoursAndMinutes(occurredTf.time())"""
    updateDateIndex(analyzer['dateIndex'], occurredDate, SevKey, stateKey)
    """updateTimeIndex(analyzer['timeIndex'], occurredTime, SevKey)
    updateLatitudeIndex(analyzer['ZoneIndexLatLng'], Latitude, Longitude, weekday)"""
    return analyzer


def updateDateIndex(omap, occurredDate, SevKey, stateKey):
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
        dateEntry = me.getValue(entry)
    else:
        dateEntry = newDateEntry()
        om.put(omap, occurredDate, dateEntry)

    addDateIndex(dateEntry, SevKey, stateKey)
    return omap


def updateTimeIndex(omap, occurredTime, SevKey):
    """

    Args:
        omap:
        occurredTime: datetime con el la Hora con minutos en que sucedio, en formato HH:MM
        SevKey: str con el nivel de severidad

    Returns:

    """

    entry = om.get(omap, occurredTime)
    if entry:
        timeEntry = me.getValue(entry)
    else:
        timeEntry = newTimeEntry()
        om.put(omap, occurredTime, timeEntry)

    addTimeIndex(timeEntry, SevKey)
    return omap


def updateLatitudeIndex(DoubleOmp, Latitude, Longitude, weekday):
    """

    Args:
        DoubleOmp:
        Latitude: cordenada Latitud
        Longitude: cordenada Longitud
        weekday: dia del la semana representado del 1 al 7

    Returns:

    """
    entry = om.get(DoubleOmp, Latitude)

    if entry:
        LtEntry = me.getValue(entry)
    else:
        LtEntry = om.newMap(DoubleOmp['type'], compareOmpLst)
        om.put(DoubleOmp, Latitude, LtEntry)

    updateLongitudeIndex(LtEntry, Longitude, weekday)
    return DoubleOmp


def updateLongitudeIndex(LtEntry, Longitude, weekday):
    """

    Args:
        LtEntry:
        Longitude: cordenada Longitud
        weekday: dia del la semana representado del 1 al 7

    Returns:

    """
    entry = om.get(LtEntry, Longitude)

    if entry:
        LngEntry = me.getValue(entry)

    else:
        LngEntry = newZoneEntry()
        om.put(LtEntry, Longitude, LngEntry)

    addZoneIndex(LngEntry, weekday)
    return LtEntry


def addZoneIndex(zoneEntry, weekday):
    """
        Actualiza los sub Index del zoneEntry

    Args:
        zoneEntry:
        weekday: dia del la semana representado del 1 al 7

    Returns:

    """
    zoneEntry['numAccidents'] += 1
    weekdayIndex = zoneEntry['weekdayIndex']
    updateIndex(weekdayIndex, weekday)


def addDateIndex(dateEntry, SevKey, stateKey):
    """
    Actualiza los sub Index del dateEntry
    Args:
        dateEntry:
        SevKey: str con el nivel de severidad
        stateKey: str con el estado de ocurrencia

    Returns:

    """
    dateEntry['numAccidents'] += 1
    SeverityIndex = dateEntry['SeverityIndex']
    updateIndex(SeverityIndex, SevKey)
    StateIndex = dateEntry['StateIndex']
    updateIndex(StateIndex, stateKey)

    return dateEntry


def addTimeIndex(timeEntry, SevKey):
    """
    Actualiza los sub Index del TimeEntry

    Args:
        timeEntry:
        SevKey: str con el nivel de severidad

    Returns:

    """
    timeEntry['numAccidents'] += 1
    SeverityIndex = timeEntry['SeverityIndex']
    updateIndex(SeverityIndex, SevKey)

    return timeEntry


def updateIndex(Index, indexKey):
    """
    Actualiza el conteo del mapa Index con su indexkey
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
    entry = {'SeverityIndex': mp.newMap(numelements=3,
                                        maptype='PROBING',
                                        comparefunction=compareMp),

             'StateIndex': mp.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareMp),

             'numAccidents': 0}

    return entry


def newTimeEntry():
    """
    Crea una entrada en el indice por horas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': mp.newMap(numelements=3,
                                        maptype='PROBING',
                                        comparefunction=compareMp),
             'numAccidents': 0}

    return entry


def newZoneEntry():
    """
    Crea una entrada en el indice por Latitud Longitud, es decir en el doble arbol
    binario.

    """
    entry = {'weekdayIndex': mp.newMap(numelements=7, comparefunction=compareMp),
             'numAccidents': 0}

    return entry


# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================

def requirement1(cont, date):
    dateEntry = me.getValue(om.get(cont['dateIndex'], date))
    severityMap = dateEntry['SeverityIndex']
    totalAccident = dateEntry['numAccidents']
    ListEntry = Nmp.operationSet(severityMap, makeListMp, lt.newList('ARRAY_LIST'))
    insertionSort(ListEntry, orderByKey)
    return {'list': ListEntry, 'total': totalAccident}


def requirement2(cont, date):
    mostFrequent = Nom.operationBefore(cont['dateIndex'], date, TotalAndFrequentOmp,
                                       {'maxKey': None, 'maxValue': -1, 'total': 0})
    return mostFrequent


def requirement3(cont, date1, date2):
    severityFrequency = Nom.operationRange(cont['dateIndex'], date1, date2, frequencyInMapForOmp('SeverityIndex'),
                                           mp.newMap(3, maptype='PROBING', comparefunction=compareMp))
    mostFrequent = Nmp.operationSet(severityFrequency, TotalAndFrequentMp, {'maxKey': None, 'maxValue': -1, 'total': 0})

    return mostFrequent


def requirement4(cont, date1, date2):
    stateFrequency = Nom.operationRange(cont['dateIndex'], date1, date2, frequencyInMapForOmp('StateIndex'),
                                        mp.newMap(40, maptype='PROBING', comparefunction=compareMp))
    mostFrequent = Nmp.operationSet(stateFrequency, TotalAndFrequentMp, {'maxKey': None, 'maxValue': -1, 'total': 0})
    return mostFrequent


def requirement5(cont, date1, date2):
    severityFrequency = Nom.operationRange(cont['timeIndex'], date1, date2,
                                           frequencyInMapForOmp('SeverityIndex'),
                                           mp.newMap(3, maptype='PROBING', comparefunction=compareMp))
    SeverityListAndTotal = Nmp.operationSet(severityFrequency, makeListAndTotalMp,
                                            {'list': lt.newList('ARRAY_LIST'), 'total': 0})
    insertionSort(SeverityListAndTotal['list'], orderByKey)
    AddPercents(SeverityListAndTotal)
    return SeverityListAndTotal


def requirement6(cont, Lat, Lng, dist):
    weekdayFrequency = Nom.operationRange(cont['ZoneIndexLatLng'], Lat - dist, Lat + dist,
                                          sndCircleRangeDobOmap(Lat, Lng, dist, frequencyInMapForOmp('weekdayIndex')),
                                          mp.newMap(7, maptype='CHAINING', comparefunction=compareMp))

    weekdayListAndTotal = Nmp.operationSet(weekdayFrequency, makeListAndTotalMp,
                                           {'list': lt.newList('ARRAY_LIST'), 'total': 0})
    insertionSort(weekdayListAndTotal['list'], orderByKey)
    weekdayFromIntToStr(weekdayListAndTotal['list'])
    return weekdayListAndTotal


# ==============================
# Funciones auxiliares
# ==============================


def HoursAndMinutes(time):
    return datetime.time(hour=time.hour, minute=time.minute)


def AddPercents(ListAndTotal):
    sList = ListAndTotal['list']
    iterator = it.newIterator(sList)
    total = ListAndTotal['total']
    for _ in range(lt.size(sList)):
        el = it.next(iterator)
        el['percent'] = round(el['value'] / total * 100, 2)


def proxyTime(o_time):
    hour = o_time.hour
    minute = o_time.minute

    if hour < 24:
        if minute < 15:
            minute = 0
        elif minute <= 30:
            minute = 30
        elif hour == 23:
            minute = 59
        else:
            minute = 0
            hour += 1

    new_time = datetime.time(hour, minute)
    return new_time


def weekdayFromIntToStr(weekdayList):
    weekday_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    iterator = it.newIterator(weekdayList)
    for _ in range(lt.size(weekdayList)):
        el = it.next(iterator)
        el['key'] = weekday_list[el['key']]
    return weekdayList


# ===================================
# Funciones auxiliares para Order Map
# ===================================


def frequencyInMapForOmp(mapIndex):
    def resultFunc(dateRoot, returnEntry):
        dateEntry = dateRoot['value']
        acMap = dateEntry[mapIndex]
        Nmp.operationSet(acMap, frequencyInMap, returnEntry)
        return returnEntry

    return resultFunc


def TotalAndFrequentOmp(root, returnEntry):
    num_accidents = root['value']['numAccidents']

    if num_accidents > returnEntry['maxValue']:
        returnEntry['maxKey'] = root['key']
        returnEntry['maxValue'] = num_accidents

    returnEntry['total'] += num_accidents
    return returnEntry


def sndCircleRangeDobOmap(x, y, distance, secondOperation):
    def resultFunction(root, entry):
        move = mt.sqrt(distance**2 - (root['key']-x)**2)
        Nom.operationRange(root['value'], y - move, y + move, secondOperation, entry)

    return resultFunction


# ===================================
# Funciones auxiliares para Map
# ===================================
def makeListMp(entry, ListEntry):
    lt.addLast(ListEntry, entry)
    return ListEntry


def makeListAndTotalMp(entry, returnEntry):
    lt.addLast(returnEntry['list'], entry)
    returnEntry['total'] += entry['value']
    return returnEntry


def frequencyInMap(entry, returnEntry):
    key = entry['key']
    num_acc = entry['value']
    Ek = mp.get(returnEntry, key)
    if Ek:
        Ek['value'] += num_acc
    else:
        mp.put(returnEntry, key, num_acc)

    return returnEntry


def TotalAndFrequentMp(entry, returnEntry):
    acn = entry['value']
    if acn > returnEntry['maxValue']:
        returnEntry['maxValue'] = acn
        returnEntry['maxKey'] = entry['key']
    returnEntry['total'] += acn

    return returnEntry


# ==============================
# Funciones de Comparacion
# ==============================
def orderByKey(el1, el2):
    if el1['key'] > el2['key']:
        return 0
    else:
        return 1


def compareOmpLst(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1


def compareMp(offense1, offense2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(offense2)
    if offense1 == offense:
        return 0
    elif offense1 > offense:
        return 1
    else:
        return -1
