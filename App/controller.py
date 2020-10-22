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
import config as cf
from DISClib.Algorithms.Sorting.insertionsort import insertionSort
from App import model as md
from datetime import datetime, time
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""


# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init(in_t):
    Type = 'BST' if in_t == '1' else 'RBT'
    analyzer = md.newAnalyzer(Type)
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, list_files):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    count_t = 0
    for file in list_files:
        accident_file = cf.data_dir + file
        input_file = csv.DictReader(open(accident_file, encoding="utf-8"), delimiter=",")
        count = 0
        print(file, 'cargando')
        for accident in input_file:
            md.addAccident(analyzer, accident)
            count += 1
            if not count % 10000:
                print(count, 'cargados')
            del accident
        del input_file
        count_t += count
        print(file, 'cargado', count, 'datos cargados')
    print('se han cargado en total', count_t, 'datos')
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def getDateInfo(dateOmap, date):
    date = strToDatetime(date)
    dateEntry = md.getDateValue(dateOmap, date)
    if dateEntry is None:
        return None
    severityList = md.operationSetMp(dateEntry['SeverityIndex'], md.makeListMp, md.newList('ARRAY_LIST'))
    insertionSort(severityList, md.orderByKey)
    severityListAndTotal = {'list': severityList, 'total': dateEntry['numAccidents']}
    return severityListAndTotal


def mstFreqDateBfADate(dateOmap, before_date):
    before_date = strToDatetime(before_date)
    mstFreqDate = md.operationBeforeOmp(dateOmap, before_date, md.TotalAndFrequentOmp, md.MakeMaxFormat(True))
    return mstFreqDate


def mstFreqSeverityInRgDates(dateOmap, date1, date2):
    date1, date2 = strToDatetime(date1), strToDatetime(date2)
    frequency_fun = md.frequencyInMapForOmp('SeverityIndex')
    severityFrequency = md.operationRangeOmp(dateOmap, date1, date2, frequency_fun, md.MakeMapFormat(3))
    mstFreqSeverity = md.operationSetMp(severityFrequency, md.TotalAndFrequentMp, md.MakeMaxFormat(True))
    return mstFreqSeverity


def MstFreqDateAndMstFreqStateInRgDates(dateOmap, date1, date2):
    date1, date2 = strToDatetime(date1), strToDatetime(date2)
    freqAndFrequencyForm = {'KeyFrequent': md.MakeMaxFormat(False), 'map': md.MakeMapFormat(40)}
    frequency_fun = md.FrequencyInMapAndFrequentKey('StateIndex')
    stateFrequencyAndMfDate = md.operationRangeOmp(dateOmap, date1, date2, frequency_fun, freqAndFrequencyForm)
    mostFrequentState = md.operationSetMp(stateFrequencyAndMfDate['map'], md.FrequentMp, md.MakeMaxFormat(False))
    mostFreqDateAndMostFreqState = {'mstDate': stateFrequencyAndMfDate['KeyFrequent'], 'mstState': mostFrequentState}
    return mostFreqDateAndMostFreqState


def severityFrequencyListInRgHours(timeOmap, time1, time2):
    frequency_fun = md.frequencyInMapForOmp('SeverityIndex')
    severityFrequency = md.operationRangeOmp(timeOmap, time1, time2, frequency_fun, md.MakeMapFormat(3))
    severityListAndTotal = md.operationSetMp(severityFrequency, md.makeListAndTotalMp, md.MakeListFormat())
    insertionSort(severityListAndTotal['list'], md.orderByKey)
    md.AddPercents(severityListAndTotal)
    return severityListAndTotal


def weekdayFrequencyListInArea(zoneOmap, Lat, Lng, dist):
    Lat, Lng, dist = float(Lat), float(Lng), float(dist)
    cir_fun = md.sndCircleRangeDobOmap(Lat, Lng, dist, md.frequencyInMapForOmp('weekdayIndex'))
    weekdayFrequency = md.operationRangeOmp(zoneOmap, Lat - dist, Lat + dist, cir_fun, md.MakeMapFormat(7))
    weekdayListAndTotal = md.operationSetMp(weekdayFrequency, md.makeListAndTotalMp, md.MakeListFormat())
    insertionSort(weekdayListAndTotal['list'], md.orderByKey)
    md.weekdayFromIntToStr(weekdayListAndTotal['list'])
    return weekdayListAndTotal


def heightOmap(omap):
    return md.heightOmap(omap)


def sizeOmap(omap):
    return md.sizeOmap(omap)


def proxyTime(time_string):
    r_time = time.fromisoformat(time_string)
    return md.proxyTime(r_time)


def strToDatetime(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()
