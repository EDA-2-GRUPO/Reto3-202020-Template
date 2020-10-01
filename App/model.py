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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as lstit
from DISClib.DataStructures import mapstructure as mp
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
        datentry = newDataEntry(date)
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
    SevKey = accident['Severity']
    SeverityEntry = m.get(SeverityIndex, SevKey)
    if SeverityEntry is None:
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
def rango_de_fechas(cont, min, max):
    lst = om.values(cont['dateIndex'], min, max)
    return lst


def fecha(cont, fecha):
    return om.get(cont['dateIndex'], fecha)


def recorrido(cont, lista):
    # funcion que saca la fecha con la mayor catidad de accidentes
    # la cantidad de accidentes en las lista de fechas
    mayor = 0
    contar = 0
    nombre = "None"
    w = lstit.newIterator(lista)
    listafinal = lt.newList("ARRAY_LIST")
    while lstit.hasNext(w):
        x = lstit.next(w)
        g = lt.size(om.get(cont['dateIndex'], x)["value"]["lstaccidentes"])
        contar += g
        if g > mayor:
            mayor = g
            nombre = x
    lt.addLast(listafinal, nombre)
    lt.addLast(listafinal, contar)
    lt.addLast(listafinal, mayor)
    return listafinal
def requerimient3(cont,lista):
    mayor = 0
    contar = 0
    nombre = "None"
    w = lstit.newIterator(lista)
    mapa = mp.newMap()
    listafinal = lt.newList("ARRAY_LIST")
    while lstit.hasNext(w):
        x = lstit.next(w)
        g = om.get(cont['dateIndex'], x)["value"]["SeverityIndex"]
        g= om.keySet(g)
        iteseg= lstit.newIterator(g)
        while lstit.hasNext(iteseg):
            key = lstit.next(iteseg)
            if mp.contains(mapa, key):
               valor=om.get(g, key)["size"]
               valor+=mp.get(mapa, x)
    return 0
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
