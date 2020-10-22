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
    def updatemap(mapa, llave):
        esta=m.get(mapa, llave)
        if esta is None:
            entry = lt.newList('SINGLELINKED', compareOffenses)
            lt.addLast(entry,0)
            m.put(mapa, llave, entry)
        else:
            entry = me.getValue(esta)
        ele_ante=lt.getElement(entry, 0)
        lt.deleteElement(entry, 0)
        lt.addLast(entry, ele_ante+1)
    lst = int(datentry['lstaccidentes'])
    datentry['lstaccidentes']=lst+1
   
    SeverityIndex = datentry['SeverityIndex']
    SevKey = accident['Severity']
    updatemap(SeverityIndex,SevKey)

    Contry=datentry['Country']
    contKey = accident['Country']
    updatemap(Contry,contKey)
    
    return datentry

def newDataEntry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': m.newMap(numelements=2,
                                       maptype='PROBING',
                                       comparefunction=compareOffenses),
             'lstaccidentes': 0,
             'Country': m.newMap(numelements=10,
                                       maptype='CHAINING',
                                       comparefunction=compareOffenses)}
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
        g = om.get(cont['dateIndex'], x)["value"]["lstaccidentes"]
        contar += g
        if g > mayor:
            mayor = g
            nombre = x
    lt.addLast(listafinal, nombre)
    lt.addLast(listafinal, mayor)
    lt.addLast(listafinal, contar)
    return listafinal

def requerimeint04(cont,lista):
    ntotal=0
    w = lstit.newIterator(lista)
    mapau = m.newMap(numelements=11,maptype='PROBING',comparefunction=compareOffenses)
    listafinal = lt.newList("ARRAY_LIST")
    listakeys = lt.newList("ARRAY_LIST",compareIds)
    while lstit.hasNext(w):
        x = lstit.next(w)
        listaa= om.get(cont['dateIndex'], x)["value"]["lstaccidentes"]
        ntotal+=listaa
        g = om.get(cont['dateIndex'], x)["value"]["Contry"]

def requerimient3(cont,lista):
    ntotal=0
    w = lstit.newIterator(lista)
    mapau = m.newMap(numelements=11,maptype='PROBING',comparefunction=compareOffenses)
    listafinal = lt.newList("ARRAY_LIST")
    listakeys = lt.newList("ARRAY_LIST",compareIds)
    while lstit.hasNext(w):
        x = lstit.next(w)
        listaa= om.get(cont['dateIndex'], x)["value"]["lstaccidentes"]
        ntotal+=listaa
        g = om.get(cont['dateIndex'], x)["value"]["SeverityIndex"]

        listallaves= mp.keySet(g)
        iteseg= lstit.newIterator(listallaves)
        while lstit.hasNext(iteseg):
            key = lstit.next(iteseg)
            if lt.isPresent(listakeys,key)!=0:
               valor2=m.get(mapau,key)["value"]
               valor=m.get(g, key)["value"]["size"]
               m.put(mapau,key,valor+valor2)
            else:
                valor=m.get(g, key)["value"]["size"]
                m.put(mapau,key,valor)
                lt.addLast(listakeys,key)
    sap=m.keySet(mapau)
    mayor= 0
    nombre = "None"
    iteseg= lstit.newIterator(sap)
    while lstit.hasNext(iteseg):
        key = lstit.next(iteseg)
        prueba=mp.get(mapau,key)["value"]
        if prueba>mayor:
            mayor=prueba
            nombre=key   
    lt.addLast(listafinal, nombre)
    lt.addLast(listafinal, mayor)
    lt.addLast(listafinal, ntotal)
    return listafinal
"""def rq4(cont,lista):

def repaction():"""
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
