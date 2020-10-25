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
from datetime import datetime, time
# Modulos Curso complementarios de lista, iteradores, y sorting
from DISClib.DataStructures.liststructure import newList
from DISClib.DataStructures import listiterator as it
# Modulos Curso de mapas Omap y map
from DISClib.DataStructures import mapstructure as mp, orderedmapstructure as om
# Modulos propios de operaciones en Omap y map, para implementacion del curso
from App import Operations as Op,  AuxiliarFunctions as Aux

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


# ===================================
# Funciones para agregar informacion al catalogo
# ===================================**


def addAccident(analyzer, accident):
    SevKey = int(accident['Severity'])
    occurredTf = datetime.strptime(accident['Start_Time'], '%Y-%m-%d %H:%M:%S')
    analyzer['numAccidents'] += 1
    updateDateOmap(analyzer['dateIndex'], occurredTf.date(), SevKey, accident['State'])
    updateTimeOmap(analyzer['timeIndex'], HoursAndMinutes(occurredTf.time()), SevKey)
    updateZoneOmap(analyzer['ZoneIndexLatLng'], (float(accident['Start_Lat']), float(accident['Start_Lng'])),
                   occurredTf.weekday() + 1)
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
    dateRoot = om.get(omap, occurredDate)

    if dateRoot:
        dateValue = dateRoot['value']  # lo correcto es me.getValue(entry), se usa para optimizar de aqui en adelante
    else:
        dateValue = {'SeverityIndex': MakeMapFormat(2, ints=True), 'StateIndex': MakeMapFormat(23, 'CHAINING'),
                     'numAccidents': 0}
        om.put(omap, occurredDate, dateValue)

    dateValue['numAccidents'] += 1
    updateIndex(dateValue['SeverityIndex'], SevKey)
    updateIndex(dateValue['StateIndex'], stateKey)

    return omap


def updateTimeOmap(omap, occurredTime, SevKey):
    """

    Args:
        omap: omap de time
        occurredTime: datetime con el la Hora con minutos en que sucedio, en formato HH:MM
        SevKey: str con el nivel de severidad

    Returns:

    """

    timeRoot = om.get(omap, occurredTime)
    if timeRoot:
        timeValue = timeRoot['value']
    else:
        timeValue = {'SeverityIndex': MakeMapFormat(2, ints=True), 'numAccidents': 0}
        om.put(omap, occurredTime, timeValue)

    timeValue['numAccidents'] += 1
    updateIndex(timeValue['SeverityIndex'], SevKey)

    return omap


def updateZoneOmap(ZoneOmap, zoneTuple, weekday):
    """
    Args:
        zoneTuple: tupla con cordenada Latitud, cordenada Longitud
        ZoneOmap: entry con un omap y un conteo de cordenadas
        weekday: dia del la semana representado del 1 al 7
    Returns:

    """
    zoneRoot = om.get(ZoneOmap, zoneTuple)

    if zoneRoot:
        zoneValue = zoneRoot['value']
    else:
        zoneValue = {'weekdayIndex': MakeMapFormat(1, 'CHAINING', True), 'numAccidents': 0}
        om.put(ZoneOmap, zoneTuple, zoneValue)

    zoneValue['numAccidents'] += 1
    updateIndex(zoneValue['weekdayIndex'], weekday)
    return zoneRoot


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

def getDateInfo(dateOmap, date):
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
    severityList = Op.operationSetMap(dateEntry['SeverityIndex'], Aux.makeListMp, newList('ARRAY_LIST'))
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
    mstFreqDate = Op.operationBeforeOmp(dateOmap, before_date, Aux.TotalAndFrequentOmp, MakeMaxFormat(True))
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
    frequency_fun = Aux.frequencyInMapForOmp('SeverityIndex')
    severityFrequency = Op.operationRangeOmp(dateOmap, date1, date2, frequency_fun, MakeMapFormat(2, ints=True))
    mstFreqSeverity = Op.operationSetMap(severityFrequency, Aux.TotalAndFrequentMp, MakeMaxFormat(True))
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
    frequency_fun = Aux.FrequencyInMapAndFrequentKeyForOmp('StateIndex')
    freqAndFrequencyForm = {'KeyFrequent': MakeMaxFormat(False), 'map': MakeMapFormat(40)}
    stateFrequencyAndMfDate = Op.operationRangeOmp(dateOmap, date1, date2, frequency_fun, freqAndFrequencyForm)
    mostFrequentState = Op.operationSetMap(stateFrequencyAndMfDate['map'], Aux.FrequentMp, MakeMaxFormat(False))
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
    frequency_fun = Aux.frequencyInMapForOmp('SeverityIndex')
    severityFrequency = Op.operationRangeOmp(timeOmap, time1, time2, frequency_fun, MakeMapFormat(2, ints=True))
    severityListAndTotal = Op.operationSetMap(severityFrequency, Aux.makeListAndTotalMp, MakeListFormat())
    AddPercents(severityListAndTotal)
    return severityListAndTotal


def weekdayFrequencyListInArea(zoneOmap, cPoint, dist):
    """
    Para un area definida por una latitud una longitud y una distancia devuelve una
    lista de la cantidad de accidentes por severidad y el total de accidentes
    Args:
    Returns:
        Entry con la lista y el total
    """
    cir_fun = Aux.frequencyInMapForOmpInCircle(cPoint, dist, 'weekdayIndex')
    point1, point2 = (cPoint[0] - dist, cPoint[1]), (cPoint[0] + dist, cPoint[1])
    weekdayFrequency = Op.operationRangeOmp(zoneOmap, point1, point2, cir_fun, MakeMapFormat(3, ints=True))
    weekdayListAndTotal = Op.operationSetMap(weekdayFrequency, Aux.makeListAndTotalMp, MakeListFormat())
    weekdayFromIntToStr(weekdayListAndTotal['list'])
    return weekdayListAndTotal


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
    if minute < 45:
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
        el['key'] = weekday_list[el['key'] - 1]
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
