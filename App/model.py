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
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import listiterator as it
from App import newOrderMetod as Nom
from App import newMpMetod as Nmp

import datetime

assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""


# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'numAccidents': 0,
                'dateIndex': om.newMap(omaptype='BST', comparefunction=compareDates),
                'timeIndex': om.newMap(omaptype='BST', comparefunction=compareDates),
                'ZoneIndexLatLng': om.newMap(omaptype='BST', comparefunction=compareDates)
                }

    return analyzer


def addAccident(analyzer, accident):
    analyzer['numAccidents'] += 1
    SevKey = int(accident['Severity'])
    stateKey = accident['State']
    Latitude = float(accident['Start_Lat'])
    Longitude = float(accident['Start_Lng'])
    occurredTf = datetime.datetime.strptime(accident['Start_Time'], '%Y-%m-%d %H:%M:%S')
    occurredDate = occurredTf.date()
    weekday = occurredDate.weekday()
    occurredTime = HoursAndMinutes(occurredTf.time())
    updateDateIndex(analyzer['dateIndex'], occurredDate, SevKey, stateKey)
    updateTimeIndex(analyzer['timeIndex'], occurredTime, SevKey)
    updateLatitudeIndex(analyzer['ZoneIndexLatLng'], Latitude, Longitude, weekday)
    return analyzer


def updateDateIndex(omap, occurredDate, SevKey, stateKey):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    entry = om.get(omap, occurredDate)

    if entry is None:
        datentry = newDataEntry()
        om.put(omap, occurredDate, datentry)
    else:
        datentry = me.getValue(entry)

    addDateIndex(datentry, SevKey, stateKey)
    return omap


def updateTimeIndex(omap, occurredTime, SevKey):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """

    entry = om.get(omap, occurredTime)
    if entry is None:
        datentry = newTimeEntry()
        om.put(omap, occurredTime, datentry)
    else:
        datentry = me.getValue(entry)

    addTimeIndex(datentry, SevKey)
    return omap


def updateLatitudeIndex(omap, Latitude, Longitude, weekday):
    entry = om.get(omap, Latitude)

    if entry is None:
        LtEntry = om.newMap('RBT', compareDates)
        om.put(omap, Latitude, LtEntry)
    else:
        LtEntry = me.getValue(entry)

    updateLongitudeIndex(LtEntry, Longitude, weekday)
    return omap


def updateLongitudeIndex(LtEntry, Longitude, weekday):
    entry = om.get(LtEntry, Longitude)

    if entry is None:
        LngEntry = newZoneEntry()
        om.put(LtEntry, Longitude, LngEntry)
    else:
        LngEntry = me.getValue(entry)

    addZoneIndex(LngEntry, weekday)
    return LtEntry


def addZoneIndex(LngEntry, weekday):
    LngEntry['numAccidents'] += 1
    weekdayIndex = LngEntry['weekdayIndex']
    updateIndex(weekdayIndex, weekday)


def addDateIndex(datentry, SevKey, stateKey):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    datentry['numAccidents'] += 1
    SeverityIndex = datentry['SeverityIndex']
    updateIndex(SeverityIndex, SevKey)
    StateIndex = datentry['StateIndex']
    updateIndex(StateIndex, stateKey)

    return datentry


def addTimeIndex(datentry, SevKey):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    datentry['numAccidents'] += 1
    SeverityIndex = datentry['SeverityIndex']
    updateIndex(SeverityIndex, SevKey)

    return datentry


def updateIndex(Index, indexKey):
    indexEntry = mp.get(Index, indexKey)
    if not indexEntry:
        mp.put(Index, indexKey, 1)
    else:
        indexEntry['value'] += 1

    return Index


def newDataEntry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': mp.newMap(numelements=3,
                                        maptype='PROBING',
                                        comparefunction=compareOffenses),

             'StateIndex': mp.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses),

             'numAccidents': 0}

    return entry


def newTimeEntry():
    entry = {'SeverityIndex': mp.newMap(numelements=3,
                                        maptype='PROBING',
                                        comparefunction=compareOffenses),
             'numAccidents': 0}

    return entry


def newZoneEntry():
    entry = {'weekdayIndex': mp.newMap(numelements=5,
                                       maptype='PROBING',
                                       comparefunction=compareOffenses),
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
    ListEntry = Nmp.operationSet(severityMap, makeListMp, lt.newList())
    return {'list': ListEntry, 'total': totalAccident}


def requirement2(cont, date):
    mostFrequent = Nom.operationBefore(cont['dateIndex'], date, TotalAndFrequentOmp,
                                       {'maxKey': None, 'maxValue': -1, 'total': 0})
    return mostFrequent


def requirement3(cont, date1, date2):
    severityFrequency = Nom.operationRange(cont['dateIndex'], date1, date2, frequencyInMapForOmp('SeverityIndex'),
                                           mp.newMap(3, maptype='PROBING', comparefunction=compareOffenses))
    mostFrequent = Nmp.operationSet(severityFrequency, TotalAndFrequentMp, {'maxKey': None, 'maxValue': -1, 'total': 0})

    return mostFrequent


def requirement4(cont, date1, date2):
    stateFrequency = Nom.operationRange(cont['dateIndex'], date1, date2, frequencyInMapForOmp('StateIndex'),
                                        mp.newMap(40, maptype='PROBING', comparefunction=compareOffenses))
    mostFrequent = Nmp.operationSet(stateFrequency, TotalAndFrequentMp, {'maxKey': None, 'maxValue': -1, 'total': 0})
    return mostFrequent


def requirement5(cont, date1, date2):
    severityFrequency = Nom.operationRange(cont['timeIndex'], date1, date2,
                                           frequencyInMapForOmp('SeverityIndex'),
                                           mp.newMap(3, maptype='PROBING', comparefunction=compareOffenses))
    SeverityListAndTotal = Nmp.operationSet(severityFrequency, makeListAndTotalMp,
                                            {'list': lt.newList(), 'total': 0})
    AddPercents(SeverityListAndTotal)
    return SeverityListAndTotal


def requirement6(cont, Lat, Lng, dist):
    weekdayFrequency = Nom.operationRange(cont['ZoneIndexLatLng'], Lat - dist, Lat + dist,
                                          sndCircleRangeDobOmap(Lat, Lng, dist, frequencyInMapForOmp('weekdayIndex')),
                                          mp.newMap(7, maptype='PROBING', comparefunction=compareOffenses))
    weekdayListAndTotal = Nmp.operationSet(weekdayFrequency, makeListAndTotalMp, {'list': lt.newList(), 'total': 0})

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
        else:
            minute = 0
            hour += 1
    else:
        hour = 23
        minute = 59

    new_time = datetime.time(hour, minute)
    return new_time


# ===================================
# Funciones auxiliares para Order Map
# ===================================


def frequencyInMapForOmp(mapIndex):
    def resultFunc(dateRoot, returnEntry, ):
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
        move = ((distance ** 2) - (root['key'] - x) ** 2) ** (1 / 2)
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
def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


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
