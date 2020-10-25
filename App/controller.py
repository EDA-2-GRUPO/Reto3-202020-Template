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
        print(file, 'cargando...')
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
    return md.getDateInfo(dateOmap, date)


def mstFreqDateBfADate(dateOmap, before_date):
    before_date = strToDatetime(before_date)
    return md.mstFreqDateBfADate(dateOmap, before_date)


def mstFreqSeverityInRgDates(dateOmap, date1, date2):
    date1, date2 = strToDatetime(date1), strToDatetime(date2)
    return md.mstFreqSeverityInRgDates(dateOmap, date1, date2)


def MstFreqDateAndMstFreqStateInRgDates(dateOmap, date1, date2):
    date1, date2 = strToDatetime(date1), strToDatetime(date2)
    return md.MstFreqDateAndMstFreqStateInRgDates(dateOmap, date1, date2)


def severityFrequencyListInRgHours(timeOmap, time1, time2):
    time1, time2 = proxyTime(time1), proxyTime(time2)
    return {'result': md.severityFrequencyListInRgHours(timeOmap, time1, time2), 'horas': (time1, time2)}


def weekdayFrequencyListInArea(zoneOmap, Lat, Lng, dist):
    Lat, Lng, dist = float(Lat), float(Lng), float(dist)
    return md.weekdayFrequencyListInArea(zoneOmap, (Lat, Lng), dist)


def heightOmap(omap):
    return md.heightOmap(omap)


def sizeOmap(omap):
    return md.sizeOmap(omap)


def proxyTime(time_string):
    r_time = time.fromisoformat(time_string)
    return md.proxyTime(r_time)


def strToDatetime(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()
