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
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import newOrderMetod as nom

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


def addAccident(analyzer, date):
    updateDateIndex(analyzer['dateIndex'], date)
    return analyzer


def updateDateIndex(map, date):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurredDate = date['Start_Time']
    accidentDate = datetime.datetime.strptime(occurredDate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentDate.date())
    if entry is None:
        datentry = newDataEntry()
        om.put(map, accidentDate.date(), datentry)
    else:
        datentry = me.getValue(entry)

    addDateIndex(datentry, date)
    return map


def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidentes']
    lt.addLast(lst, accident)

    SeverityIndex = datentry['SeverityIndex']
    SevKey = int(accident['Severity'])
    SeverityEntry = m.get(SeverityIndex, SevKey)
    if not SeverityEntry:
        entry = lt.newList('SINGLELINKED', compareOffenses)
        m.put(SeverityIndex, SevKey, entry)
    else:
        entry = me.getValue(SeverityEntry)

    lt.addLast(entry, accident)
    return datentry


def newDataEntry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': m.newMap(numelements=10,
                                       maptype='PROBING',
                                       comparefunction=compareOffenses),

             'lstaccidentes': lt.newList('SINGLE_LINKED', compareDates)}

    return entry


# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================

def requirement1(cont, date):
    dataEntry = om.get(cont['dateIndex'], date)["value"]
    return Severity_list(dataEntry)


def Severity_list(dataEntry):
    Severity = dataEntry['SeverityIndex']
    listK = m.keySet(Severity)
    listP = lt.newList()
    iterator = it.newIterator(listK)
    for _ in range(lt.size(listK)):
        Key = it.next(iterator)
        value = lt.size(me.getValue(m.get(Severity, Key)))
        el = {"key": Key, "value": value}
        lt.addLast(listP, el)
    return listP


def requirement2(cont, date):
    return nom.iterationBefore(cont['dateIndex'], date, TotalAndFrequent)


def TotalAndFrequent(dateRoot, returnEntry):
    dateEntry = dateRoot['value']
    num_accidents = lt.size(dateEntry['lstaccidentes'])
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
    severityFrequency = nom.iterationRange(cont['dateIndex'], date1, date2, frequentSeverity, {1: 0, 2: 0, 3: 0, 4: 0})
    return severityFrequency


def frequentSeverity(dateRoot, returnEntry):
    dateEntry = dateRoot['value']
    severityMap = dateEntry['SeverityIndex']
    sevKeys = m.keySet(severityMap)
    iterKeys = it.newIterator(sevKeys)
    for _ in range(lt.size(sevKeys)):
        s_key = it.next(iterKeys)
        num_acc = lt.size(me.getValue(m.get(severityMap, s_key)))
        returnEntry[s_key] += num_acc


def getDate(cont, fecha):
    return om.get(cont['dateIndex'], fecha)["value"]


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
    if offense1 == offense:
        return 0
    elif offense1 > offense:
        return 1
    else:
        return -1
