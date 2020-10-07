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
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from App import newOrderMetod as nom

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
    analyzer = {'Accidente': None, 'dateIndex': om.newMap(omaptype='BST',
                                                          comparefunction=compareDates)}

    return analyzer


def addAccident(analyzer, accident):
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer


def updateDateIndex(omap, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurredDate = accident['Start_Time']
    accidentDate = datetime.datetime.strptime(occurredDate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(omap, accidentDate.date())
    if entry is None:
        datentry = newDataEntry()
        om.put(omap, accidentDate.date(), datentry)
    else:
        datentry = me.getValue(entry)

    SevKey = int(accident['Severity'])
    stateKey = accident['State']

    addDateIndex(datentry, SevKey, stateKey)
    return omap


def addDateIndex(datentry, SevKey, stateKey):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    datentry['numAccidents'] += 1
    # lst = datentry['lstaccidentes']
    # lt.addLast(lst, accident)
    SeverityIndex = datentry['SeverityIndex']
    # SevKey = int(accident['Severity'])
    updateIndex(SeverityIndex, SevKey)
    StateIndex = datentry['StateIndex']
    # stateKey = accident['State']
    updateIndex(StateIndex, stateKey)

    return datentry


def updateIndex(Index, indexKey):
    indexEntry = mp.get(Index, indexKey)
    if not indexEntry:
        # indexEntry = lt.newList('SINGLELINKED', compareOffenses)
        mp.put(Index, indexKey, 1)
    else:
        indexEntry['value'] += 1

    return Index


def newDataEntry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': mp.newMap(numelements=10,
                                        maptype='PROBING',
                                        comparefunction=compareOffenses),

             'StateIndex': mp.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses),

             'numAccidents': 0}

    return entry


# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================

def requirement1(cont, date):
    dataEntry = om.get(cont['dateIndex'], date)
    return Severity_list(dataEntry)


def getDate(cont, fecha):
    return om.get(cont['dateIndex'], fecha)["value"]


def Severity_list(dateEntry):
    severityMap = dateEntry['SeverityIndex']
    sevKeys = mp.keySet(severityMap)
    iterKeys = it.newIterator(sevKeys)
    listP = lt.newList()
    for _ in range(lt.size(sevKeys)):
        Key = it.next(iterKeys)
        value = me.getValue(mp.get(severityMap, Key))
        el = {"key": Key, "value": value}
        lt.addLast(listP, el)
    return listP


def requirement2(cont, date):
    return nom.operationBefore(cont['dateIndex'], date, TotalAndFrequent)


def TotalAndFrequent(dateRoot, returnEntry):
    dateEntry = dateRoot['value']
    num_accidents = dateEntry['numAccidents']

    try:
        current_n = returnEntry['mayor']
        if num_accidents > current_n:
            returnEntry['maxDate'] = dateRoot['key']
            returnEntry['mayor'] = num_accidents

    except KeyError:
        returnEntry['maxDate'] = dateRoot['key']
        returnEntry['mayor'] = num_accidents
        returnEntry['totalAccidents'] = 0

    returnEntry['totalAccidents'] += num_accidents


def requirement3(cont, date1, date2):
    severityFrequency = nom.operationRange(cont['dateIndex'], date1, date2,
                                           frequentSeverity)
    severityFrequency['total'] = 0
    for v in severityFrequency.values():
        severityFrequency['total'] += v

    return severityFrequency


def frequentSeverity(dateRoot, returnEntry):
    frequentInMap(dateRoot, returnEntry, 'SeverityIndex')


def requirement4(cont, date1, date2):
    stateFrequency = nom.operationRange(cont['dateIndex'], date1, date2, frequentState)
    return stateFrequency


def frequentState(dateRoot, returnEntry):
    frequentInMap(dateRoot, returnEntry, 'StateIndex')


def frequentInMap(dateRoot, returnEntry, mapIndex):
    dateEntry = dateRoot['value']
    acMap = dateEntry[mapIndex]
    Keys = mp.keySet(acMap)
    iterKeys = it.newIterator(Keys)
    for _ in range(lt.size(Keys)):
        key = it.next(iterKeys)
        num_acc = me.getValue(mp.get(acMap, key))
        try:
            returnEntry[key] += num_acc
        except KeyError:
            returnEntry[key] = num_acc


# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if id1 == id2:
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
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
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
